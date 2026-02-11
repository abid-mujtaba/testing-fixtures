"""
Test the logic for incorporating the correct def line number.

VS Code should detect the correct line number for the test function definition even
if it has one or more fixture decorators applied to it.
"""

import inspect
import sys

from testing.fixtures import noinject

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


def test_line_number_preservation_noinject() -> None:
    """Test that noinject also preserves the def line number."""
    # GIVEN
    def_line_noinject = 0  # Will be set below

    # WHEN
    @noinject(fixture_a)  # Decorator line (should NOT be the reported line)
    def test_noinject_decorator() -> None:  # This is the def line we want preserved
        """Test with noinject decorator."""

    # THEN
    # Capture what line the def was on by finding it in our own source
    current_frame = sys._getframe()
    test_source, test_start = inspect.getsourcelines(current_frame.f_code)

    # Find where test_noinject_decorator def is in our test source
    for i, line in enumerate(test_source):
        if "def test_noinject_decorator" in line and line.lstrip().startswith("def "):
            def_line_noinject = test_start + i
            break

    # The decorated function should have co_firstlineno pointing to the def line
    assert hasattr(test_noinject_decorator, "_def_lineno")
    assert (
        test_noinject_decorator.__code__.co_firstlineno
        == test_noinject_decorator._def_lineno
    )
    assert test_noinject_decorator._def_lineno == def_line_noinject


def test_wrapped_chain_has_correct_line_number() -> None:
    """Test that __wrapped__ chain also has correct line number for IDE tools."""
    # GIVEN
    def_line_wrapped = 0  # Will be set below

    # WHEN
    @fixture_a  # Decorator line (should NOT be the reported line)
    def test_wrapped_chain(  # This is the def line we want preserved
        a: Ao,
    ) -> None:
        """Test __wrapped__ chain preservation."""

    # THEN
    # Capture what line the def was on by finding it in our own source
    current_frame = sys._getframe()
    test_source, test_start = inspect.getsourcelines(current_frame.f_code)

    # Find where test_wrapped_chain def is in our test source
    # Use a more specific search to avoid matching the outer function name
    for i, line in enumerate(test_source):
        if "def test_wrapped_chain(" in line and line.lstrip().startswith("def "):
            def_line_wrapped = test_start + i
            break

    # The wrapper should have the correct line number
    assert test_wrapped_chain.__code__.co_firstlineno == def_line_wrapped

    # VS Code/pytest may follow the __wrapped__ chain, so verify it's also correct
    assert hasattr(test_wrapped_chain, "__wrapped__")
    wrapped = test_wrapped_chain.__wrapped__

    # For injecting fixtures, __wrapped__ is a partial object
    if hasattr(wrapped, "func"):
        # The underlying function should also have the correct line number
        assert wrapped.func.__code__.co_firstlineno == def_line_wrapped
    elif hasattr(wrapped, "__code__"):
        # For regular functions, check the code object directly
        assert wrapped.__code__.co_firstlineno == def_line_wrapped
