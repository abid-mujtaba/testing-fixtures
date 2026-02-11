"""Fixtures for integration tests."""

from collections.abc import Iterator

import pytest


@pytest.fixture
def base_url() -> Iterator[str]:
    """URL to flask server in composable environment."""
    return "http://server"
