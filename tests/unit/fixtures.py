"""Implementation of new fixtures module."""

from functools import partial, wraps

from types import TracebackType
from typing import (
    Any,
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


class Fixture(Generic[Y, D]):
    """
    Instances of this class function both as a context manager and a decorator.

    As a decorator they can be applied to test functions to act as a fixture which
    runs the setup, injects its yielded value into the test, and then runs the
    teardown.
    Instances are created from a generator function passed in which is the fixture
    definition generator.
    The fixture definition generator MUST be single-shot (single yield) otherwise a
    RuntimeError will be raised.

    The __enter__ and __exit__ have been copied from contextlib._GeneratorContextManager
    (the underlying class of contextlib.contextmanager) and then altered to make the
    context manager BOTH reentrant and reusable.

    The Fixture behaves similarly to contextlib.contextmanager with the
    important difference that the decorator does an injection of the yielded value
    rather than ignoring it completely.

    The fixture definition generator can expect args and kwargs.
    These are specified AFTER the Fixture object has been instantiated by calling the
    .set() method.

    Since a Fixture instance can be used by multiple tests AND composed with multiple
    other fixture definitions the definition args and kwargs are cached at
    various levels by mostly being closed over.
    """

    def __init__(self, generator_func: Callable[D, FixtureDefinition[Y]]):
        """
        Create a Fixture object.

        Pass in the generator_func which is the fixture definition, a function with a
        SINGLE yield.
        """
        self._func = generator_func
        self._generator: FixtureDefinition[Y]  # Declare here for pylint. Assigned later
        self._value: Y

        # Default values for fixture definition args and kwargs
        self.args: tuple[Any, ...] = tuple()
        self.kwargs: dict[str, Any] = {}

        self._entries = 0  # Keep track of rentrance

    def set(self, *d_args: D.args, **d_kwargs: D.kwargs) -> "Fixture[Y, D]":
        """Method for setting the args and kwargs passed down to the fixture defn."""
        self.args = d_args
        self.kwargs = d_kwargs

        return self

    def reset(self) -> None:
        """Reset the fixture definition args and kwargs."""
        print(f"Resetting  {self._func.__name__}")
        self.args = tuple()
        self.kwargs = {}

    def __enter__(self) -> Y:
        self._entries += 1

        if self._entries == 1:  # First entry
            self._generator = self._func(*self.args, **self.kwargs)

            try:
                self._value = next(self._generator)
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

                    # Now that we are at the last exit we reset the args and kwargs
                    # to avoid collisions with later usage
                    self.reset()

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

        # Store the fixture definition args and kwargs in the closure
        fixture_args = self.args
        fixture_kwargs = self.kwargs

        @wraps(reduced_func)
        def _inner(*t_args: T.args, **t_kwargs: T.kwargs) -> None:
            """Decorated test function which has the fixture yielded value injected."""
            # Use the closed over values to set the fixture definition args and kwargs
            self.set(*fixture_args, **fixture_kwargs)

            # Since the class defines __enter__ and __exit__, we can use `self` as a
            # context manager
            # fg_value: The value yielded by the fixture definition (generator function,
            #           now context manager) as defined by the user
            with self as fg_value:
                return test_function(fg_value, *t_args, **t_kwargs)

        return _inner


# We declare 'fixture' to be an alias for the Fixture class
# When applied as a decorator to a fixture definition it creates the corresponding
# instance of the Fixture class
fixture = Fixture


Q = ParamSpec("Q")
Z = TypeVar("Z")


def compose(
    fixture_: Fixture[Y, D]
) -> Callable[
    [Callable[Concatenate[Y, Q], FixtureDefinition[Z]]],
    Callable[Q, FixtureDefinition[Z]],
]:
    """
    Take a fixture and return a decorator for fixture definitions.

    Injects a first argument into the fixture definition returning a simplified
    definition (generator function).
    """

    # Store the fixture (being composed) definition args and kwargs here allowing
    # it to be closed over
    fixture_args = fixture_.args
    fixture_kwargs = fixture_.kwargs

    def _decorator(
        fixture_definition: Callable[Concatenate[Y, Q], FixtureDefinition[Z]]
    ) -> Callable[Q, FixtureDefinition[Z]]:
        """Decorator for fixture defns that injects value from composed fixture."""

        @wraps(fixture_definition)
        def _inner(*d_args: Q.args, **d_kwargs: Q.kwargs) -> FixtureDefinition[Z]:
            """
            Replacement for fixture defintion.

            The first value is injected from the composed fixture resulting in a
            simpler fixture definition (generator function).
            """

            # Set definition args and kwargs for the fixture being compsed using
            # the values closed over earlier.
            # This allows for the definition args and kwargs to be injected from the
            # test site if desired.
            fixture_.set(*fixture_args, **fixture_kwargs)

            with fixture_ as yielded_value:
                yield from fixture_definition(yielded_value, *d_args, **d_kwargs)

        return _inner

    return _decorator
