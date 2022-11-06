"""Implementation of new fixtures module."""

from contextlib import contextmanager
from functools import partial, wraps

from typing import Callable, Concatenate, Iterator, ParamSpec, TypeVar

D = ParamSpec("D")  # Parameters injected into fixture definition
T = ParamSpec("T")  # Test function parameters
Y = TypeVar("Y")  # Type of value yielded by fixture generator to be injected into test
R = TypeVar("R")  # Return value of the function decorated by the fixture.
#                 # Will be None for tests.


def fixture(
    fixture_generator: Callable[D, Iterator[Y]],
) -> Callable[D, Callable[[Callable[Concatenate[Y, T], R]], Callable[T, R]]]:
    """
    Convert a one-shot generator into a test fixture.

    Return a decorator that is applied to test functions.
    This decorator will inject the value yielded by the one-shot generator into the
    test function.
    It will essentially behave as a context manager wrapping the test function.

    The decorator will be able to take values which will be passed in as arguments
    to the fixture definition (one-shot generator).
    """

    # Convert the fixture generator (fixture definition) into a context
    # manager to convert it into a fixture
    fixture_context_manager = contextmanager(fixture_generator)

    @wraps(fixture_context_manager)
    def _parametrized_test_decorator(
        *d_args: D.args, **d_kwargs: D.kwargs
    ) -> Callable[[Callable[Concatenate[Y, T], R]], Callable[T, R]]:
        """
        A fixture definition that expected arguments.

        Passed in arguments are passed into the fixture definition (context manager).
        """

        def _test_decorator(
            test_function: Callable[Concatenate[Y, T], R]
        ) -> Callable[T, R]:
            """The returned decorator that will be applied to test functions."""

            # Create throwaway partial function which removes the injected variable
            # for wrapping the inner function (below)
            # Without this pytest will see the injected parameter and complain of
            # a missing value for it
            temp_test_function_for_signature = partial(test_function, None)

            @wraps(temp_test_function_for_signature)
            def _wrapped_test_function(*t_args: T.args, **t_kwargs: T.kwargs) -> R:
                """The function that will replace the test function (by wrapping it)."""
                # fg_value: The value yielded by the fixture_generator as defined by
                #           the user
                with fixture_context_manager(*d_args, **d_kwargs) as fg_value:
                    return test_function(fg_value, *t_args, **t_kwargs)

            return _wrapped_test_function

        return _test_decorator

    return _parametrized_test_decorator
