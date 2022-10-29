"""Test the compute end-point."""

import json
import requests

import pytest


@pytest.mark.usefixtures("operation")
def test_compute_identity(base_url: str, uuid: int) -> None:
    """Test the /compute end-point for a user with identity operation."""
    # GIVEN
    input_value = 9
    url = f"{base_url}/compute"
    payload = {"uuid": uuid, "input": input_value}

    # WHEN
    response = requests.post(url, json=payload, timeout=5)

    # THEN
    assert response.status_code == 200

    output = json.loads(response.text)
    assert output["result"] == input_value  # Identity operation
