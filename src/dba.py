"""DB (Postgres) Accessor."""

from contextlib import contextmanager
import os
from typing import Any, cast, Iterator, Optional

import psycopg


DB_USER = "postgres"
DB_PASSWORD = os.environ["POSTGRES_PASSWORD"]
DB_HOST = "db-host"


Record = dict[str, Any]  # Object returned by cursor SELECT (using dict row)


@contextmanager
def get_cursor() -> Iterator[psycopg.Cursor[Optional[Record]]]:
    """Create cursor to postgres DB."""
    conn = psycopg.connect(user=DB_USER, password=DB_PASSWORD, host=DB_HOST)

    # Yield a cursor that uses a dict row factory
    with conn.cursor(row_factory=psycopg.rows.dict_row) as cursor:
        yield cursor


def get_operation(uuid: int) -> Optional[str]:
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
        return cast(str, record["operation"])

    return None  # indicates that uuid is not in table
