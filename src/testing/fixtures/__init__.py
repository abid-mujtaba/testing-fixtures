# pylint: disable=no-else-return
"""Implementation of new fixtures module."""

# pylint: disable=no-member

from __future__ import annotations

from functools import partial, wraps
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Generator,
    Generic,
    TypeVar,
)

from typing_extensions import Concatenate, ParamSpec, Self

if TYPE_CHECKING:
    from types import TracebackType

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

    def __init__(self, generator_func: Callable[D, FixtureDefinition[Y]]) -> None:
        """
        Create a Fixture object.

        Pass in the generator_func which is the fixture definition, a function with a
        SINGLE yield.
        """
        self._func = generator_func
        self._generator: FixtureDefinition[Y]  # Declare here for pylint. Assigned later
        self._value: Y

        # Default values for fixture definition args and kwargs
        self.args: tuple[Any, ...] = ()
        self.kwargs: dict[str, Any] = {}

        self._entries = 0  # Keep track of rentrance

    def set(self, *d_args: D.args, **d_kwargs: D.kwargs) -> Self:  # noqa: A003
        """Set the args and kwargs passed down to the fixture definition."""
        self.args = d_args
        self.kwargs = d_kwargs

        return self

    def reset(self) -> None:
        """Reset the fixture definition args and kwargs."""
        self.args = ()
        self.kwargs = {}

    def __enter__(self) -> Y:
        """Deal with re-entrance in this context manager."""
        self._entries += 1

        if self._entries == 1:  # First entry
            try:
                self._generator = self._func(*self.args, **self.kwargs)
            except TypeError:
                # This indicates that the order of re-entry is invalid causing incorrect
                # (kw)args to be passed in (usually the default/reset empty values)
                # Reset the (kw)args to be sure
                # Reset the entry count so that the next usage of the fixture (in a
                # test) works properly
                self.reset()
                self._entries = 0

                raise

            try:
                self._value = next(self._generator)

            except StopIteration:
                err_msg = "generator didn't yield"
                raise RuntimeError(err_msg) from None

            else:
                return self._value

        else:
            return self._value

    def _exit_no_exception(self) -> bool:
        """Handle exit when no exception was raised."""
        if self._entries == 0:  # Last exit (in rentrance) so finish up generator
            try:
                next(self._generator)
            except StopIteration:
                # Now that we are done with the fixture context manager we reset it
                self.reset()
                return False
            else:
                err_msg = "generator did not stop"
                raise RuntimeError(err_msg)
        else:
            return False

    def __exit__(  # pylint: disable=R0912
        self,
        typ: type[BaseException] | None,
        value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool:
        """Handle exception raised within context manager."""
        self._entries -= 1

        if typ is None:
            return self._exit_no_exception()

        # An excception has been raised
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
        except BaseException as exc:  # noqa: BLE001 pylint: disable=W0703
            # only re-raise if it's *not* the exception that was
            # passed to throw(), because __exit__() must not raise
            # an exception unless __exit__() itself failed.  But throw()
            # has to raise the exception to signal propagation, so this
            # fixes the impedance mismatch between the throw() protocol
            # and the __exit__() protocol.
            if exc is not value:
                raise
            return False

        err_msg = "generator did not stop after throw()"
        raise RuntimeError(err_msg)

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

        # Now that the values have been closed over we can delete from the object
        self.reset()

        @wraps(reduced_func)
        def _inner(*t_args: T.args, **t_kwargs: T.kwargs) -> None:
            """Compose fixture and inject yielded value into wrapped test function."""
            # Use the closed over values to set the fixture definition args and kwargs
            self.set(*fixture_args, **fixture_kwargs)

            # Since the class defines __enter__ and __exit__, we can use `self` as a
            # context manager
            # fg_value: The value yielded by the fixture definition (generator function,
            #           now context manager) as defined by the user
            with self as fg_value:
                return test_function(fg_value, *t_args, **t_kwargs)

        return _inner

    def __del__(self) -> None:
        """Validate usage on garbage collection."""
        if self._entries != 0:
            err_msg = (
                f"Fixture {self._func.__name__} destroyed while "
                "all rentries were not exited"
            )
            raise RuntimeError(err_msg)


# We declare 'fixture' to be an alias for the Fixture class
# When applied as a decorator to a fixture definition it creates the corresponding
# instance of the Fixture class
fixture = Fixture


Q = ParamSpec("Q")
Z = TypeVar("Z")


def compose(
    fixture_: Fixture[Y, D],
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

    # Now that the (kw)args have been closed over we can delete from the object
    fixture_.reset()

    def _decorator(
        fixture_definition: Callable[Concatenate[Y, Q], FixtureDefinition[Z]],
        /,
    ) -> Callable[Q, FixtureDefinition[Z]]:
        """Decorate fixture definition and inject value from composed fixture."""

        @wraps(fixture_definition)
        def _inner(*d_args: Q.args, **d_kwargs: Q.kwargs) -> FixtureDefinition[Z]:
            """
            Compose fixture and inject its yielded value into decorated fixture.

            The first value is injected from the composed fixture resulting in a
            simpler fixture definition (generator function).
            """
            # Set definition args and kwargs for the fixture being composed using
            # the values closed over earlier.
            # This allows for the definition args and kwargs to be injected from the
            # test site if desired.
            fixture_.set(*fixture_args, **fixture_kwargs)

            with fixture_ as yielded_value:
                yield from fixture_definition(yielded_value, *d_args, **d_kwargs)

        return _inner

    return _decorator


def compose_noinject(
    fixture_: Fixture[Y, D],
) -> Callable[
    [Callable[Q, FixtureDefinition[Z]]],
    Callable[Q, FixtureDefinition[Z]],
]:
    """
    Take a fixture and return a decorator for fixture definitions.

    Does NOT inject value yielded from fixture into wrapped definition.
    """
    # Store the fixture (being composed) definition args and kwargs here allowing
    # it to be closed over
    fixture_args = fixture_.args
    fixture_kwargs = fixture_.kwargs

    # Now that the (kw)args have been closed over we can delete from the object
    fixture_.reset()

    def _decorator(
        fixture_definition: Callable[Q, FixtureDefinition[Z]],
    ) -> Callable[Q, FixtureDefinition[Z]]:
        """Decorate fixture definition such that it does NOT inject yielded value."""

        @wraps(fixture_definition)
        def _inner(*d_args: Q.args, **d_kwargs: Q.kwargs) -> FixtureDefinition[Z]:
            """
            Use fixture but ignore its yielded value (no injection).

            The first value is injected from the composed fixture resulting in a
            simpler fixture definition (generator function).
            """
            # Set definition args and kwargs for the fixture being composed using
            # the values closed over earlier.
            # This allows for the definition args and kwargs to be injected from the
            # test site if desired.
            fixture_.set(*fixture_args, **fixture_kwargs)

            with fixture_:  # Ignore yielded value
                yield from fixture_definition(*d_args, **d_kwargs)

        return _inner

    return _decorator


def noinject(
    fixture_: Fixture[Y, D],
) -> Callable[[Callable[T, None]], Callable[T, None]]:
    """Transform a Fixture to make it non-injecting (absorb yielded value)."""

    def _decorator(test_function: Callable[T, None]) -> Callable[T, None]:
        """Non-injecting decorator for test functions."""
        fixture_args = fixture_.args
        fixture_kwargs = fixture_.kwargs

        def _inner(*args: T.args, **kwargs: T.kwargs) -> None:
            """Run test function while ignoring the value yielded by the fixture."""
            fixture_.set(*fixture_args, **fixture_kwargs)

            with fixture_:  # Yielded value is being ignored
                return test_function(*args, **kwargs)

        return _inner

    return _decorator
