"""DB (Postgres) Accessor."""

from __future__ import annotations

import os
from contextlib import contextmanager
from typing import TYPE_CHECKING, Any, cast

import psycopg

if TYPE_CHECKING:
    from collections.abc import Iterator

DB_USER = "postgres"
DB_PASSWORD = os.environ["POSTGRES_PASSWORD"]
DB_HOST = "db-host"


Record = dict[str, Any]  # Object returned by cursor SELECT (using dict row)


@contextmanager
def get_cursor(autocommit: bool = False) -> Iterator[psycopg.Cursor[Record | None]]:
    """Create cursor to postgres DB."""
    conn = psycopg.connect(
        autocommit=autocommit, user=DB_USER, password=DB_PASSWORD, host=DB_HOST
    )

    # Yield a cursor that uses a dict row factory
    with conn.cursor(row_factory=psycopg.rows.dict_row) as cursor:
        yield cursor


def get_operation(uuid: int) -> str | None:
    """Get operation for given uuid from operations table."""
    with get_cursor() as cursor:
        query = """
            SELECT
                operation
            FROM operations
            WHERE
                uuid=%(uuid)s
        """
        cursor.execute(query, {"uuid": uuid})
        record = cursor.fetchone()

    if record:
        return cast("str", record["operation"])

    return None  # indicates that uuid is not in table
