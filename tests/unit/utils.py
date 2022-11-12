"""Define fixtures for these tests."""

from typing import NewType, TypedDict

from .fixtures import compose, fixture, FixtureDefinition


Ao = NewType("Ao", str)


@fixture
def fixture_a() -> FixtureDefinition[Ao]:
    """A simple fixture that yields a string."""
    print("Entering a")

    yield Ao("a")

    print("Leaving a")


fixture_a.set()


Bi1 = NewType("Bi1", int)
Bi2 = NewType("Bi2", float)


class Bo(TypedDict):
    """Output type for fixture_b encapsulating the two inputs."""

    b1: Bi1
    b2: Bi2


@fixture
def fixture_b(b1: Bi1, b2: Bi2) -> FixtureDefinition[Bo]:
    """A fixture that takes injected value from the test function decoration."""
    print("Entering b")

    yield Bo(b1=b1, b2=b2)

    print("Leaving b")


class Co(TypedDict):
    """Output type for fixture_c encapsulating the injected value from fixture_b."""

    c: Bo


@fixture
@compose(fixture_b.set(Bi1(13), Bi2(1.44)))
def fixture_c(b: Bo) -> FixtureDefinition[Co]:
    """A fixture that takes an injected value from ANOTHER fixture."""
    print("Entering c")

    yield Co(c=b)

    print("Leaving c")


Di = NewType("Di", bool)


class Do(TypedDict):
    """
    Output type for fixture_d which contains injection from two locations.

    Both fixture_b and test definition site.
    """

    b: Bo
    d: Di


@fixture
@compose(fixture_b.set(Bi1(123), Bi2(1.23)))
def fixture_d(b: Bo, d: Di) -> FixtureDefinition[Do]:
    """
    A fixture that takes injected value from two places.

    From both the test function site AND from ANOTHER fixture.
    """
    print("Entering d")

    yield Do(b=b, d=d)

    print("Leaving d")


Eo = NewType("Eo", int)
VALUE_E = {"value": 0}


@fixture
def fixture_e() -> FixtureDefinition[Eo]:
    """A fixture that mutates the inject value before yielding it, then unmutates it."""
    print("Entering e")
    VALUE_E["value"] += 1

    yield Eo(VALUE_E["value"])

    VALUE_E["value"] -= 1
    print("Leaving e")


Fi = NewType("Fi", int)


class Fo(TypedDict):
    """Output type for fixture_f encapsulating injection from fixture_e and test site"""

    e: Eo
    f: Fi


@fixture
@compose(fixture_e)
def fixture_f(e: Eo, f: Fi) -> FixtureDefinition[Fo]:
    """A fixture that gets state from both test site and fixture_e (mutating)."""
    print("Entering f")
    try:
        yield Fo(e=e, f=f)
    finally:
        print("Leaving f")


Gi = NewType("Gi", int)


class Go(TypedDict):
    """Output type for fixture_g encapsulating injection from fixture_b and test site."""

    b: Bo
    g: Gi


@fixture
@compose(fixture_b)
def fixture_g(b: Bo, g: Gi) -> FixtureDefinition[Go]:
    """Fixture that uses a late-injected fixture_b and a value from the test sit."""
    print("Entering g")

    yield {"b": b, "g": g}

    print("Leaving g")
