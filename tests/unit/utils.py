"""Define fixtures for these tests."""

from typing import Iterator, NewType

from .fixtures import fixture


TypeA = NewType("TypeA", str)


@fixture
def fixture_a() -> Iterator[TypeA]:
    """A simple fixture that yields a string."""
    yield TypeA("Value A")
