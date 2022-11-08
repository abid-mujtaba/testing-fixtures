"""Implementation of new fixtures module."""

from functools import partial, wraps

from types import TracebackType
from typing import (
    Callable,
    Concatenate,
    Generator,
    Generic,
    Optional,
    ParamSpec,
    Type,
    TypeVar,
)


D = ParamSpec("D")  # Parameters injected into fixture definition
T = ParamSpec("T")  # Test function parameters
Y = TypeVar("Y")  # Type of value yielded by fixture generator to be injected into test

# Fixture definitions are Generators (not just Iterators) since they need to support
# throwing exceptions to the yield statement
FixtureDefinition = Generator[Y, None, None]


class Fixture(Generic[Y]):
    """
    Instances of this class function both as a context manager and a decorator.

    As a decorator they can be applied to test functions to act as a fixture which
    runs the setup, injects its yielded value into the test, and then runs the
    teardown.
    Instances are created from a single generator passed in. No other arguments.
    The instantiating generator MUST be single-shot (single yield) otherwise a
    RuntimeError will be raised.

    The __enter__ and __exit__ have been copied from contextlib._GeneratorContextManager
    (the underlying class of contextlib.contextmanager) and then altered to both
    match the definition of __init__ AND
    to make the context manager BOTH reentrant and reusable.

    The Fixture behaves similarly to contextlib.contextmanager with the
    important difference that the decorator does an injection of the yielded value
    rather than ignoring it completely.
    """

    def __init__(
        self,
        generator_func: Callable[D, FixtureDefinition[Y]],
        *d_args: D.args,
        **d_kwargs: D.kwargs
    ):
        """
        Create a Fixture object.

        Pass in the generator_func which is the fixture definition, a function with a
        SINGLE yield.
        Additionally pass in args and kwargs accepted by the generator_func.
        """
        self._func = generator_func
        self._args = d_args
        self._kwargs = d_kwargs

        self._entries = 0  # Keep track of rentrance
        # self._generator = self._func(*d_args, **d_kwargs)

    def __enter__(self) -> Y:
        self._entries += 1

        if self._entries == 1:  # First entry
            self._generator = self._func(  # pylint: disable=W0201
                *self._args, **self._kwargs
            )

            try:
                self._value = next(self._generator)  # pylint: disable=W0201
                return self._value

            except StopIteration:
                raise RuntimeError("generator didn't yield") from None

        else:
            return self._value

    def __exit__(  # pylint: disable=R0912
        self, typ: Optional[Type[Exception]], value: Exception, traceback: TracebackType
    ) -> bool:
        self._entries -= 1

        if typ is None:
            if self._entries == 0:  # Last exit (in rentrance) so finish up generator
                try:
                    next(self._generator)
                except StopIteration:
                    return False
                else:
                    raise RuntimeError("generator didn't stop")
            else:
                return False
        else:
            if value is None:
                # Need to force instantiation so we can reliably
                # tell if we get the same exception back
                value = typ()
            try:
                self._generator.throw(typ, value, traceback)
            except StopIteration as exc:
                # Suppress StopIteration *unless* it's the same exception that
                # was passed to throw().  This prevents a StopIteration
                # raised inside the "with" statement from being suppressed.
                return exc is not value
            except RuntimeError as exc:
                # Don't re-raise the passed in exception. (issue27122)
                if exc is value:
                    return False
                # Avoid suppressing if a StopIteration exception
                # was passed to throw() and later wrapped into a RuntimeError
                # (see PEP 479 for sync generators; async generators also
                # have this behavior). But do this only if the exception wrapped
                # by the RuntimeError is actually Stop(Async)Iteration (see
                # issue29692).
                if isinstance(value, StopIteration) and exc.__cause__ is value:
                    return False
                raise
            except BaseException as exc:  # pylint: disable=W0703
                # only re-raise if it's *not* the exception that was
                # passed to throw(), because __exit__() must not raise
                # an exception unless __exit__() itself failed.  But throw()
                # has to raise the exception to signal propagation, so this
                # fixes the impedance mismatch between the throw() protocol
                # and the __exit__() protocol.
                if exc is not value:
                    raise
                return False
            raise RuntimeError("generator didn't stop after throw()")

    def __call__(
        self, test_function: Callable[Concatenate[Y, T], None]
    ) -> Callable[T, None]:
        """
        When used as a callable it behaves as a decorator for test functions.

        It injects the value yielded by the underlying fixture definition (generator
        func, now context manager) as the first argument of the test function.
        After decoration the test appears to have one less argument (the first one).
        """

        # Create a temporary reduced function to wrap the signature of the function
        # after it has been decorated
        reduced_func = partial(test_function, None)

        @wraps(reduced_func)
        def _inner(*t_args: T.args, **t_kwargs: T.kwargs) -> None:
            """Decorated test function which has the fixture yielded value injected."""
            # Since the class defines __enter__ and __exit__, we can use `self` as a
            # context manager
            # fg_value: The value yielded by the fixture definition (generator function,
            #           now context manager) as defined by the user
            with self as fg_value:
                return test_function(fg_value, *t_args, **t_kwargs)

        return _inner


def fixture(
    generator_func: Callable[D, FixtureDefinition[Y]],
) -> Callable[D, Fixture[Y]]:
    """
    Convert a one-shot generator func, which is the fixture defn, into a test fixture.

    Return a parameterized decorator that is applied to test functions.
    The decorator returned AFTER the parameters are applied will inject the value
    yielded by the fixture definition generator into the test function.
    It will essentially behave as a context manager wrapping the test function.

    The decorator will be able to take values which will be passed in as arguments
    to the fixture definition (one-shot generator).
    """

    @wraps(generator_func)
    def _parametrized_test_decorator(
        *d_args: D.args, **d_kwargs: D.kwargs
    ) -> Fixture[Y]:
        """
        Parameterized decorator that returns a Fixture object.

        The Fixture object takes the fixture definition (generator func) and the
        parameters to be passed to it.
        It is capable of behaving both as a decorator (of test functions) and
        a context manager (for fixture composition)
        """
        return Fixture(generator_func, *d_args, **d_kwargs)

    return _parametrized_test_decorator


Z = TypeVar("Z")


def compose(
    fixture_: Fixture[Y],
) -> Callable[
    [Callable[Concatenate[Y, D], FixtureDefinition[Z]]],
    Callable[D, FixtureDefinition[Z]],
]:
    """
    Take a fixture and return a decorator for fixture definitions.

    Injects a first argument into the fixture definition returning a simplified
    definition (generator function).
    """

    def _decorator(
        fixture_definition: Callable[Concatenate[Y, D], FixtureDefinition[Z]]
    ) -> Callable[D, FixtureDefinition[Z]]:
        """Decorator for fixture defns that injects value from composed fixture."""

        # with fixture as yielded_value:
        #     return partial(fixture_definition, yielded_value)

        def _inner(*d_args: D.args, **d_kwargs: D.kwargs) -> FixtureDefinition[Z]:
            """
            Replacement for fixture defintion.

            The first value is injected from the composed fixture resulting in a
            simpler definition (generator function).
            """

            with fixture_ as yielded_value:
                for value in fixture_definition(yielded_value, *d_args, **d_kwargs):
                    yield value

        return _inner

    return _decorator
