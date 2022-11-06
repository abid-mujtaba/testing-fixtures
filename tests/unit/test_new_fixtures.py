"""Test the new fixtures."""

import pytest

from .utils import fixture_a, Ao
from .utils import fixture_b, Bi1, Bi2, Bo
from .utils import fixture_c, Co
from .utils import fixture_d, Di, Do

# from .utils import fixture_e, TypeE
# from .utils import fixture_f, TypeF1, TypeF2


@fixture_a()
def test_a(a: Ao) -> None:
    """Test fixture_a in isolation."""
    assert a == "a"


@fixture_b(Bi1(42), Bi2(3.14))
def test_b(b: Bo) -> None:
    """Test parametrized fixture_b in isolation."""
    assert b == {"b1": 42, "b2": 3.14}


@fixture_b(Bi1(88), Bi2(12.3))
@fixture_a()
def test_a_and_b(a: Ao, b: Bo) -> None:
    """Test application of two fixtures to one test."""
    assert a == "a"
    assert b == {"b1": 88, "b2": 12.3}


@fixture_c()  # pylint: disable=E1120
def test_c(c: Co) -> None:
    """Test fixture_c which receives values from fixture_b."""
    assert c == {"c": {"b1": 13, "b2": 1.44}}


@fixture_d(Di(True))  # pylint: disable=E1120
def test_d(d: Do) -> None:
    """Test fixture_d which receives values from both fixture_b and the test site."""
    assert d == {"b": {"b1": 123, "b2": 1.23}, "d": True}


# @fixture_e()
# def test_e(val_e: TypeE) -> None:
#     """Test mutation of injected state by fixture_e."""
#     assert val_e == 1


# @pytest.mark.skip
# @fixture_f(TypeF1(42))  # pylint: disable=E1120
# @fixture_e()
# def test_fixture_f(val_e: TypeE, val_f: TypeF2) -> None:
#     """Test fixture_f and double injecion of fixture_e."""
#     assert val_e == 1
#     assert val_f == (
#         "Injected into fixture_f values from fixture_e 1 and from test site 42"
#     )


# # @fixture_b(TypeB("Value B"), inject=False)
# # def test_b_no_injection() -> None:
# #     """The value yielded by fixture_b is NOT injected into the test."""
