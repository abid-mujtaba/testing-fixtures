"""Utilities for testing such as shared constants and fixtures."""

from typing import NewType, ParamSpec
from example.server import dba

from testing.fixtures import fixture, FixtureDefinition

P = ParamSpec("P")
Uuid = NewType("Uuid", int)

UUID: Uuid = Uuid(1234)
base_url = "http://server"


def inject_operation(uuid: Uuid, operation_name: str) -> None:
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


def uninject_operation(uuid: Uuid) -> None:
    """Remove injected operation from DB."""
    with dba.get_cursor(autocommit=True) as cursor:
        query = """
            DELETE
                FROM operations
            WHERE
                uuid=%(uuid)s
        """
        cursor.execute(query, {"uuid": uuid})


@fixture
def operation(operation_name: str) -> FixtureDefinition[Uuid]:
    """Tunable fixture that injects specified operation_name into DB and yield uuid."""
    try:
        inject_operation(UUID, operation_name)

        yield UUID

    finally:
        uninject_operation(UUID)
