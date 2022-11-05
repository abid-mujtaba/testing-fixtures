"""Implementation of new fixtures module."""

from contextlib import contextmanager
from functools import partial, wraps


def fixture(fixture_generator):
    """
    Convert a one-shot generator into a test fixture.

    Return a decorator that is applied to test functions.
    This decorator will inject the value yielded by the one-shot generator into the
    test function.
    It will essentially behave as a context manager wrapping the test function.
    """

    # Convert the fixture generator (fixture definition) into a context
    # manager to convert it into a fixture
    fixture_context_manager = contextmanager(fixture_generator)

    def _test_decorator(test_function):
        """The returned decorator that will be applied to test functions."""

        # Create throwaway partial function which removes the injected variable
        # for wrapping the inner function (below)
        # Without this pytest will see the injected parameter and complain of
        # a missing value for it
        temp_test_function_for_signature = partial(test_function, None)

        @wraps(temp_test_function_for_signature)
        def _wrapped_test_function(*tf_args, **tf_kwargs):
            """The function that will replace the test function (by wrapping it)."""
            # fg_value: The value yielded by the fixture_generator as defined by
            #           the user
            with fixture_context_manager() as fg_value:
                return test_function(fg_value, *tf_args, **tf_kwargs)

        return _wrapped_test_function

    return _test_decorator
