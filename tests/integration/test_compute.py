"""Test the compute end-point."""

import json
import requests

from . import operation


@operation("identity")
def test_compute_identity(base_url: str, uuid: int) -> None:
    """Test the /compute end-point for a user with identity operation."""
    # GIVEN
    payload = {"uuid": uuid, "input": 9}

    # WHEN
    response = requests.post(f"{base_url}/compute", json=payload, timeout=5)

    # THEN
    assert response.status_code == 200

    output = json.loads(response.text)
    assert output["result"] == 9  # Identity operation
