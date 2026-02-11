"""Test the new fixtures."""

import inspect
import sys

import pytest

from testing.fixtures import noinject

from .utils import (
    Ao,
    Bi1,
    Bi2,
    Bo,
    Co,
    Di,
    Do,
    Eo,
    Fi,
    Fo,
    Gi,
    Go,
    Hi,
    Ho,
    fixture_a,
    fixture_b,
    fixture_c,
    fixture_d,
    fixture_e,
    fixture_f,
    fixture_g,
    fixture_h,
)


@fixture_a
def test_a(a: Ao) -> None:
    """Test fixture_a in isolation."""
    assert a == "a"


def test_a_as_contextmanager() -> None:
    """Test fixture_a as a context_manager rather than as a decorator."""
    with fixture_a as a:  # pylint: disable=E1129
        assert a == "a"


@fixture_b.set(Bi1(42), Bi2(3.14))
def test_b(b: Bo) -> None:
    """Test parametrized fixture_b in isolation."""
    assert b == {"b1": 42, "b2": 3.14}


@fixture_b.set(Bi1(88), Bi2(12.3))
@fixture_a
def test_a_and_b(a: Ao, b: Bo) -> None:
    """Test application of two fixtures to one test."""
    print("Entering test a_and_b")

    assert a == "a"
    assert b == {"b1": 88, "b2": 12.3}

    print("Leaving test a_and_b")


@fixture_c
def test_c(c: Co) -> None:
    """Test fixture_c which receives values from fixture_b."""
    assert c == {"c": {"b1": 13, "b2": 1.44}}


# NOTE: The rule is that the state set at the first entry into the context manager(s)
#       wrapping the test takes precedence.
#       Since the state of fixture_b is being set at composition time we will require
#       fixture_c to be the outermost decorator here to ensure that, that is the state
#       that takes precedence from the start.
#       Reversing the order will result in an error.
@fixture_c
@fixture_b
def test_b_and_c(b: Bo, c: Co) -> None:
    """Use fixture_b both in test & composed via c with its state set at composition."""
    assert b == {"b1": 13, "b2": 1.44}
    assert c == {"c": {"b1": 13, "b2": 1.44}}


@pytest.mark.xfail(reason="Invalid fixture application order")
@fixture_b
@fixture_c
def test_invalid_b_and_c(c: Co, b: Bo) -> None:
    """Use fixture_b both in test & composed via c with its state set at composition."""
    assert b == {"b1": 13, "b2": 1.44}
    assert c == {"c": {"b1": 13, "b2": 1.44}}


@fixture_d.set(Di(True))
def test_d(d: Do) -> None:
    """Test fixture_d which receives values from both fixture_b and the test site."""
    assert d == {"b": {"b1": 123, "b2": 1.23}, "d": True}


@fixture_e
def test_e(e: Eo) -> None:
    """Test mutation of injected state by fixture_e."""
    assert e == 1


@fixture_f.set(Fi(42))
@fixture_e
def test_f(e: Eo, f: Fo) -> None:
    """Test fixture_f and double injection of fixture_e."""
    print("Entering test f")

    assert e == 1
    assert f == {"e": 1, "f": 42}

    print("Leaving test f")


# NOTE: Since fixture_g requires injection from fixture_b AND we are setting the
#       state for fixture_b at the test site the fixture_b decorator here MUST
#       wrap the fixture_b decorator here.
#       This ensures that the state for fixture_b set here (at the test site) is the
#       outer-most state when the context managers around the test are created and so
#       takes precedence.
#       Reversing the order will result in an error.
@fixture_b.set(Bi1(56), Bi2(9.7))
@fixture_g.set(Gi(41))
def test_g(g: Go, b: Bo) -> None:
    """Inject args into fixture from test site and trickle down to pulled in fixture."""
    assert b == {"b1": 56, "b2": 9.7}
    assert g == {"b": b, "g": 41}


@pytest.mark.xfail(reason="Invalid fixture application order")
@fixture_g.set(Gi(41))
@fixture_b.set(Bi1(56), Bi2(9.7))
def test_invalid_g(b: Bo, g: Go) -> None:
    """Inject args into fixture from test site and trickle down to pulled in fixture."""
    assert b == {"b1": 56, "b2": 9.7}
    assert g == {"b": b, "g": 41}


@noinject(fixture_b.set(Bi1(75), Bi2(2.71)))
def test_b_no_injection() -> None:
    """The value yielded by fixture_b is NOT injected into the test."""


@fixture_h.set(Hi(49))
def test_fixture_h(h: Ho) -> None:
    """Test fixture_h which uses a noinject composed fixture_b."""
    assert h == {"h": 49}


@fixture_b.set(Bi1(23), Bi2(4.7))
@fixture_h.set(Hi(26))
def test_fixture_b_and_h(h: Ho, b: Bo) -> None:
    """Test fixtures b and h where the latter uses b but ignored yielded value."""
    assert h == {"h": 26}
    assert b == {"b1": 23, "b2": 4.7}


def test_line_number_preservation() -> None:
    """Test that decorated functions preserve the def line number."""
    # GIVEN
    # Store the line number of the def statement before decoration
    # This test verifies that the fix correctly identifies and preserves this line
    def_line_single = 0  # Will be set below

    # WHEN
    @fixture_a  # Decorator line (should NOT be the reported line)
    def test_single_decorator(  # This is the def line we want preserved
        a: Ao,
    ) -> None:
        """Test with single decorator."""

    # THEN
    # Capture what line the def was on by finding it in our own source
    current_frame = sys._getframe()
    test_source, test_start = inspect.getsourcelines(current_frame.f_code)

    # Find where test_single_decorator def is in our test source
    for i, line in enumerate(test_source):
        if "def test_single_decorator" in line and line.lstrip().startswith("def "):
            def_line_single = test_start + i
            break

    # The decorated function should have co_firstlineno pointing to the def line
    # Verify:
    # 1. The wrapper has a _def_lineno attribute
    # 2. The co_firstlineno matches _def_lineno
    # 3. It points to the actual def line (not decorator line)
    assert hasattr(test_single_decorator, "_def_lineno")
    assert (
        test_single_decorator.__code__.co_firstlineno
        == test_single_decorator._def_lineno
    )
    assert test_single_decorator._def_lineno == def_line_single


def test_line_number_preservation_stacked() -> None:
    """Test that functions preserve the def line number with stacked decorators."""
    # GIVEN
    # Test with stacked decorators to verify caching works
    def_line_stacked = 0  # Will be set below

    # WHEN
    @fixture_b.set(Bi1(1), Bi2(2.0))  # Outer decorator
    @fixture_a  # Inner decorator
    def test_stacked_decorators(  # This is the def line
        a: Ao,
        b: Bo,
    ) -> None:
        """Test with stacked decorators."""

    # THEN
    # Capture what line the def was on by finding it in our own source
    current_frame = sys._getframe()
    test_source, test_start = inspect.getsourcelines(current_frame.f_code)

    # Find where test_stacked_decorators def is
    for i, line in enumerate(test_source):
        if "def test_stacked_decorators" in line and line.lstrip().startswith("def "):
            def_line_stacked = test_start + i
            break

    # Both decorators should share the same cached _def_lineno
    assert hasattr(test_stacked_decorators, "_def_lineno")
    assert (
        test_stacked_decorators.__code__.co_firstlineno
        == test_stacked_decorators._def_lineno
    )
    # Verify the line number points to def, not the first decorator
    assert test_stacked_decorators._def_lineno == def_line_stacked
