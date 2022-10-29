"""Fixtures for integration tests."""

from typing import Iterator
import pytest


@pytest.fixture
def base_url() -> Iterator[str]:
    """URL to flask server in composable environment."""
    yield "http://server"
