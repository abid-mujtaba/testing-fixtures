"""Implementation of new fixtures module."""

import inspect
from collections.abc import Callable, Generator
from functools import partial, wraps
from types import FunctionType, TracebackType
from typing import (
    Any,
    Concatenate,
    Generic,
    TypeVar,
)

from typing_extensions import ParamSpec, Self

D = ParamSpec("D")  # Parameters injected into fixture definition
T = ParamSpec("T")  # Test function parameters
Y = TypeVar("Y")  # Type of value yielded by fixture generator to be injected into test

# Fixture definitions are Generators (not just Iterators) since they need to support
# throwing exceptions to the yield statement
FixtureDefinition = Generator[Y, None, None]


def preserve_metadata(
    original: Callable[..., Any], noinject: bool = False
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Apply @wraps and preserve the def line number.

    This ensures VS Code's Python test explorer places the run/status icon at the
    correct line (the def keyword) rather than at decorators or end of function.

    Args:
        original: The original test function to extract def line number from
        noinject: Whether the fixture being decorated is non-injecting
                  (absorbs yielded value).

    Returns:
        A decorator function

    """

    def decorator(inner: Callable[..., Any]) -> Callable[..., Any]:

        # Preserve the test function's def line number for proper IDE integration
        # Check if already cached by inner decorators to avoid redundant inspect calls
        _def_lineno = getattr(original, "_def_lineno", None)

        if _def_lineno is None:
            try:
                lines, start = inspect.getsourcelines(original)
                # Scan for the actual def line (skipping decorators)
                for i, line in enumerate(lines):
                    if line.lstrip().startswith(("def ", "async def ")):
                        _def_lineno = start + i
                        break
                else:
                    # Fallback if no def line found (shouldn't happen)
                    _def_lineno = original.__code__.co_firstlineno
            except (OSError, TypeError):
                # Fallback if source unavailable or unexpected function type
                _def_lineno = original.__code__.co_firstlineno

        # Create a corrected copy of original with proper line number for __wrapped__
        # We will need to pass this to functools.wraps because VS Code can in certain
        # cases drill down to the .__wrapped__ attributed of a test function and
        # use it to determine the line number for the test run/status icon.
        corrected_original = FunctionType(
            original.__code__.replace(co_firstlineno=_def_lineno),
            original.__globals__,
            original.__name__,
            original.__defaults__,
            original.__closure__,
        )

        # Use functools.wraps to copy metadata from the function being decorated to
        # the output function
        if not noinject:
            # Create a temporary reduced function for wrapping.
            # It removes the injected variable since after decoration that variable
            # is no longer visible
            reduced_func = partial(corrected_original, None)
            inner = wraps(reduced_func)(inner)
        else:
            inner = wraps(corrected_original)(inner)

        # Cache for outer decorators and update code object
        inner._def_lineno = _def_lineno  # type: ignore[attr-defined]  # noqa: SLF001
        inner.__code__ = inner.__code__.replace(  # type: ignore[attr-defined]
            co_firstlineno=_def_lineno
        )

        return inner

    return decorator


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

        self._entries = 0  # Keep track of reentrance

    def set(self, *d_args: D.args, **d_kwargs: D.kwargs) -> Self:
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
                err_msg = "generator did not yield"
                raise RuntimeError(err_msg) from None

            else:
                return self._value

        else:
            return self._value

    def _exit_no_exception(self) -> bool:
        """Handle exit when no exception was raised."""
        if self._entries == 0:  # Last exit (in reentrance) so finish up generator
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

        # An exception has been raised
        if value is None:
            # Need to force instantiation so we can reliably
            # tell if we get the same exception back
            value = typ()
        try:
            self._generator.throw(value)
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
        except BaseException as exc:
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
        # Store the fixture definition args and kwargs in the closure
        fixture_args = self.args
        fixture_kwargs = self.kwargs

        # Now that the values have been closed over we can delete from the object
        self.reset()

        @preserve_metadata(test_function)
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
                "all reentries were not exited"
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

        @preserve_metadata(test_function, noinject=True)
        def _inner(*args: T.args, **kwargs: T.kwargs) -> None:
            """Run test function while ignoring the value yielded by the fixture."""
            fixture_.set(*fixture_args, **fixture_kwargs)

            with fixture_:  # Yielded value is being ignored
                return test_function(*args, **kwargs)

        return _inner

    return _decorator
