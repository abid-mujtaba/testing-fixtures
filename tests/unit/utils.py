"""Define fixtures for these tests."""

from typing import Iterator, NewType

from .fixtures import fixture


TypeA = NewType("TypeA", str)

TypeB1 = NewType("TypeB1", int)
TypeB2 = NewType("TypeB2", float)
TypeB3 = NewType("TypeB3", str)

TypeC = NewType("TypeC", str)

TypeD1 = NewType("TypeD1", bool)
TypeD2 = NewType("TypeD2", str)


@fixture
def fixture_a() -> Iterator[TypeA]:
    """A simple fixture that yields a string."""
    yield TypeA("Value A")


@fixture
def fixture_b(val_b1: TypeB1, val_b2: TypeB2) -> Iterator[TypeB3]:
    """A fixture that takes injected value from the test function decoration."""
    yield TypeB3(f"Injected into fixture_b {val_b1} and {val_b2}")


@fixture
@fixture_b(TypeB1(13), TypeB2(1.44))
def fixture_c(val_b: TypeB3) -> Iterator[TypeC]:
    """A fixture that takes an injected value from ANOTHER fixture."""
    yield TypeC(f"Injected into fixture_c: {val_b}")


@fixture
@fixture_b(TypeB1(123), TypeB2(1.23))
def fixture_d(val_b: TypeB3, val_d: TypeD1) -> Iterator[TypeD2]:
    """
    A fixture that takes injected value from two places.

    From both the test function site AND from ANOTHER fixture.
    """
    yield TypeD2(f"Injected into fixture_d from both b: {val_b} and test site: {val_d}")
