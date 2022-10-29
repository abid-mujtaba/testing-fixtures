"""Fixtures for integration tests."""

from typing import Iterator
import pytest

import dba


@pytest.fixture
def base_url() -> Iterator[str]:
    """URL to flask server in composable environment."""
    yield "http://server"


@pytest.fixture(name="uuid")
def uuid_fixture() -> Iterator[int]:
    """Yield the uuid used for testing."""
    yield 1234


@pytest.fixture(name="operation")
def operation_fixture(uuid: int) -> Iterator[str]:
    """Bind uuid to operation string in DB."""
    with dba.get_cursor(autocommit=True) as cursor:
        operation = "identity"
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
        cursor.execute(query, {"uuid": uuid, "operation": operation})

    yield operation

    with dba.get_cursor(autocommit=True) as cursor:
        query = """
            DELETE
                FROM operations
            WHERE
                uuid=%(uuid)s
        """
        cursor.execute(query, {"uuid": uuid})
