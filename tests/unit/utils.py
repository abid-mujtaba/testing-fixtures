"""Define fixtures for these tests."""

from typing import Iterator, NewType, TypedDict

from .fixtures import fixture


A = NewType("A", str)


@fixture
def fixture_a() -> Iterator[A]:
    """A simple fixture that yields a string."""
    yield A("a")


Bi1 = NewType("Bi1", int)
Bi2 = NewType("Bi2", float)


class Bo(TypedDict):
    """Output type for fixture_b encapsulating the two inputs."""

    b1: Bi1
    b2: Bi2


@fixture
def fixture_b(b1: Bi1, b2: Bi2) -> Iterator[Bo]:
    """A fixture that takes injected value from the test function decoration."""
    yield Bo(b1=b1, b2=b2)


# TypeC = NewType("TypeC", str)


# @fixture
# @fixture_b(TypeB1(13), TypeB2(1.44))
# def fixture_c(val_b: TypeB3) -> Iterator[TypeC]:
#     """A fixture that takes an injected value from ANOTHER fixture."""
#     yield TypeC(f"Injected into fixture_c: {val_b}")


# TypeD1 = NewType("TypeD1", bool)
# TypeD2 = NewType("TypeD2", str)


# @fixture
# @fixture_b(TypeB1(123), TypeB2(1.23))
# def fixture_d(val_b: TypeB3, val_d: TypeD1) -> Iterator[TypeD2]:
#     """
#     A fixture that takes injected value from two places.

#     From both the test function site AND from ANOTHER fixture.
#     """
#     yield TypeD2(f"Injected into fixture_d from both b: {val_b} and test site: {val_d}")


# TypeE = NewType("TypeE", int)
# VALUE_E = {"value": 0}


# @fixture
# def fixture_e() -> Iterator[TypeE]:
#     """A fixture that mutates the inject value before yielding it."""
#     VALUE_E["value"] += 1

#     yield TypeE(VALUE_E["value"])


# TypeF1 = NewType("TypeF1", int)
# TypeF2 = NewType("TypeF2", str)


# @fixture
# @fixture_e()
# def fixture_f(val_e: TypeE, val_f: TypeF1) -> Iterator[TypeF2]:
#     """A fixture that gets state from both test site and fixture_e (mutating)."""
#     yield TypeF2(
#         f"Injected into fixture_f values from fixture_e {val_e} and "
#         f"from test site {val_f}"
#     )
