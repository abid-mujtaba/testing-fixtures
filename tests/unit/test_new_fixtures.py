"""Test the new fixtures."""

from .utils import fixture_a, TypeA
from .utils import fixture_b, TypeB1, TypeB2, TypeB3
from .utils import fixture_c, TypeC


@fixture_a()
def test_a(val_a: TypeA) -> None:
    """Test fixture_a in isolation."""
    assert val_a == "Value A"


@fixture_b(TypeB1(42), TypeB2(3.14))
def test_b(val_b: TypeB3) -> None:
    """Test parametrized fixture_b in isolation."""
    assert val_b == "Injected into fixture b 42 and 3.14"


@fixture_c()  # pylint: disable=E1120
def test_c(val_c: TypeC) -> None:
    """Test fixture_c which receives values from fixture_b."""
    assert val_c == "Injected into fixture_C: Injected into fixture b 13 and 1.44"


# @fixture_b(TypeB("Value B"), inject=False)
# def test_b_no_injection() -> None:
#     """The value yielded by fixture_b is NOT injected into the test."""
