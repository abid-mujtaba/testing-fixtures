"""Test the /test end-point in the server."""

import json
import requests

from .utils import base_url


def test_test_endpoint() -> None:
    """Test the /test end-point in the server."""
    # GIVEN
    url = f"{base_url}/test"

    # WHEN
    response = requests.get(url, timeout=5)

    # THEN
    assert response.status_code == 200
    payload = json.loads(response.text)

    assert payload["test"]["success"] is True
