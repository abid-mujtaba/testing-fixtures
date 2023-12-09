"""Unit tests for utility fixtures."""

from pathlib import Path

import testing.fixtures.utils as sut


@sut.create_temp_dir
def test_create_temp_dir(temp_dir: Path) -> None:
    """Test the create_temp_dir utility fixture."""
    # THEN
    assert temp_dir != Path.cwd()
    assert "tmp" in str(temp_dir)


@sut.create_temp_cwd
def test_create_temp_cwd(cwd: Path) -> None:
    """Test the create_temp_cwd utility fixture."""
    # THEN
    assert cwd.samefile(Path.cwd())
    assert "tmp" in str(cwd)
