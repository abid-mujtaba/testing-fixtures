"""Test the /test end-point in the server."""

import json
import requests


def test_test_endpoint() -> None:
    """Test the /test end-point in the server."""
    # GIVEN
    url = "http://server/test"

    # WHEN
    response = requests.get(url, timeout=5)

    # THEN
    assert response.status_code == 200
    payload = json.loads(response.text)

    assert payload["test"]["success"] is True
