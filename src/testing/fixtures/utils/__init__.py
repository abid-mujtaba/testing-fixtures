"""Sub-package containing commonly used utility fixtures."""

import os
from pathlib import Path
from tempfile import TemporaryDirectory

from testing.fixtures import FixtureDefinition, fixture


@fixture
def create_temp_dir() -> FixtureDefinition[Path]:
    """Create and inject a temporary directory."""
    with TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@fixture
def create_temp_cwd() -> FixtureDefinition[Path]:
    """Create a temporrary directory and switch the cwd to it."""
    original_cwd = Path.cwd().absolute()

    with TemporaryDirectory() as temp_dir:
        try:
            os.chdir(temp_dir)

            yield Path(temp_dir)

        finally:
            os.chdir(original_cwd)
