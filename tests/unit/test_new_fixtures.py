"""Test the new fixtures."""

from .utils import fixture_a, TypeA


@fixture_a
def test_a(val_a: TypeA) -> None:
    """Test fixture_A in isolation."""
    assert val_a == "Value A"
