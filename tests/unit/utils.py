"""Define fixtures for these tests."""

from typing import Iterator, NewType

from .fixtures import fixture


TypeA = NewType("TypeA", str)
TypeB = NewType("TypeB", str)


@fixture
def fixture_a() -> Iterator[TypeA]:
    """A simple fixture that yields a string."""
    yield TypeA("Value A")


@fixture
def fixture_b(val_b: TypeB) -> Iterator[TypeB]:
    """A fixture that takes injected value from the test function decoration."""
    yield TypeB(f"Injectd {val_b}")
