"""Define fixtures for these tests."""

from typing import Iterator, NewType, TypedDict

from .fixtures import fixture


Ao = NewType("Ao", str)


@fixture
def fixture_a() -> Iterator[Ao]:
    """A simple fixture that yields a string."""
    yield Ao("a")


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


class Co(TypedDict):
    """Output type for fixture_c encapsulating the injected value from fixture_b."""

    c: Bo


@fixture
@fixture_b(Bi1(13), Bi2(1.44))
def fixture_c(b: Bo) -> Iterator[Co]:
    """A fixture that takes an injected value from ANOTHER fixture."""
    yield Co(c=b)


Di = NewType("Di", bool)


class Do(TypedDict):
    """
    Output type for fixture_d which contains injection from two locations.

    Both fixture_b and test definition site.
    """

    b: Bo
    d: Di


@fixture
@fixture_b(Bi1(123), Bi2(1.23))
def fixture_d(b: Bo, d: Di) -> Iterator[Do]:
    """
    A fixture that takes injected value from two places.

    From both the test function site AND from ANOTHER fixture.
    """
    yield Do(b=b, d=d)


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
