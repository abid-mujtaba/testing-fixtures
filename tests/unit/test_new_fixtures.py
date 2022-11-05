"""Test the new fixtures."""

from .utils import fixture_a, TypeA
from .utils import fixture_b, TypeB


@fixture_a
def test_a(val_a: TypeA) -> None:
    """Test fixture_a in isolation."""
    assert val_a == "Value A"


@fixture_b(TypeB("Value B"))
def test_b(val_b: TypeB) -> None:
    """Test parametrized fixture_b in isolation."""
    assert val_b == "Injected Value B"
