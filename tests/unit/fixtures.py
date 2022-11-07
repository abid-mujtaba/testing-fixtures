"""Implementation of new fixtures module."""

# from contextlib import contextmanager
from functools import partial, wraps

from types import TracebackType
from typing import (
    Callable,
    Concatenate,
    Generic,
    Iterator,
    Optional,
    ParamSpec,
    Type,
    TypeVar,
)

D = ParamSpec("D")  # Parameters injected into fixture definition
T = ParamSpec("T")  # Test function parameters
Y = TypeVar("Y")  # Type of value yielded by fixture generator to be injected into test


class Fixture(Generic[Y]):
    """
    Instances of this class function both as a context manager and a decorator.

    As a decorator they can be applied to test functions to act as a fixture which
    runs the setup, injects its yielded value into the test, and then runs the
    teardown.
    Instances are created from a single generator passed in. No other arguments.
    The instantiating generator MUST be single-shot (single yield) otherwise a
    RuntimeError will be raised.
    """

    def __init__(
        self,
        generator_func: Callable[D, Iterator[Y]],
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
        self._generator = self._func(*d_args, **d_kwargs)

    def __enter__(self) -> Y:
        """Execute up to the first yield in the generator and return that value."""
        try:
            return next(self._generator)

        except StopIteration as err:
            raise RuntimeError("Generator failed to yield first value") from err

    def __exit__(
        self, typ: Optional[Type[Exception]], value: Exception, traceback: TracebackType
    ) -> bool:
        """Execute to the end of the ideally one-shot generator."""
        try:
            next(self._generator)

        except StopIteration:
            pass

        else:
            raise RuntimeError("Generator failed to stop, yielded more than value.")

        return not bool(typ)  # return True if no exception is passed in

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
    generator_func: Callable[D, Iterator[Y]],
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
