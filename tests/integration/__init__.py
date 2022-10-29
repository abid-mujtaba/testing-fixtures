"""Shared package utilities for testing."""

from functools import partial, wraps
from typing import Callable, ParamSpec

from example.server import dba


P = ParamSpec("P")

UUID = 1234


def inject_operation(uuid: int, operation_name: str) -> None:
    """Inject specified uuid and operation into DB."""
    with dba.get_cursor(autocommit=True) as cursor:
        query = """
            INSERT
                INTO operations
                (
                    uuid,
                    operation
                )
            VALUES
                (
                    %(uuid)s,
                    %(operation)s
                )
        """
        cursor.execute(query, {"uuid": uuid, "operation": operation_name})


def uninject_operation(uuid: int) -> None:
    """Remove injected operation from DB."""
    with dba.get_cursor(autocommit=True) as cursor:
        query = """
            DELETE
                FROM operations
            WHERE
                uuid=%(uuid)s
        """
        cursor.execute(query, {"uuid": uuid})


def operation(operation_name: str) -> Callable[[Callable[P, None]], Callable[P, None]]:
    """Generate a decorator that injects specified operation into DB."""

    def decorator(func: Callable[P, None]) -> Callable[P, None]:
        """A decorator that injects operation into DB and associated uuid into test function."""

        new_func = partial(func, uuid=UUID)

        @wraps(new_func)
        def inner(*args: P.args, **kwargs: P.kwargs) -> None:
            """Inner function of decorator for wrapping."""
            try:
                inject_operation(UUID, operation_name)

                new_func(*args, **kwargs)

            finally:
                uninject_operation(UUID)

        return inner

    return decorator
