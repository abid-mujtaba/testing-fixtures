"""
Test the logic for adjusting the def line number when
a test is decorated with one or more fixtures.
"""

import inspect
import sys

from .utils import (
    Ao,
    Bi1,
    Bi2,
    Bo,
    fixture_a,
    fixture_b,
)


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
""