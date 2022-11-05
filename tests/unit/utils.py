"""Define fixtures for these tests."""

from typing import Iterator, NewType

from .fixtures import fixture


TypeA = NewType("TypeA", str)
TypeB1 = NewType("TypeB1", int)
TypeB2 = NewType("TypeB2", float)
TypeB3 = NewType("TypeB3", str)


@fixture
def fixture_a() -> Iterator[TypeA]:
    """A simple fixture that yields a string."""
    yield TypeA("Value A")


@fixture
def fixture_b(val_b1: TypeB1, val_b2: TypeB2) -> Iterator[TypeB3]:
    """A fixture that takes injected value from the test function decoration."""
    yield TypeB3(f"Injected into fixture b {val_b1} and {val_b2}")


# @fixture
# @fixture_b(TypeB("Value B"))
# def fixture_c(val_b: TypeB) -> Iterator[TypeC]:
#     """A fixture that takes an injected value from ANOTHER fixture."""
#     yield TypeC(f"Injected into C: {val_b}")
