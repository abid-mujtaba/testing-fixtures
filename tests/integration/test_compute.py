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


@operation("square")
def test_compute_square(base_url: str, uuid: int) -> None:
    """Test the /compute end-point for a user with square operation."""
    # GIVEN
    payload = {"uuid": uuid, "input": 9}

    # WHEN
    response = requests.post(f"{base_url}/compute", json=payload, timeout=5)

    # THEN
    assert response.status_code == 200

    output = json.loads(response.text)
    assert output["result"] == 81  # square operation


@operation("cube")
def test_compute_cube(base_url: str, uuid: int) -> None:
    """Test the /compute end-point for a user with cube operation."""
    # GIVEN
    payload = {"uuid": uuid, "input": 9}

    # WHEN
    response = requests.post(f"{base_url}/compute", json=payload, timeout=5)

    # THEN
    assert response.status_code == 200

    output = json.loads(response.text)
    assert output["result"] == 729  # cube operation


# Note: No operation record in the DB
def test_compute_no_operation(base_url: str) -> None:
    """Test the /compute end-point for a user with no operation in the DB."""
    # GIVEN
    uuid = 7890
    payload = {"uuid": uuid, "input": 9}

    # WHEN
    response = requests.post(f"{base_url}/compute", json=payload, timeout=5)

    # THEN
    assert response.status_code == 200

    output = json.loads(response.text)
    assert "error" in output
    assert str(uuid) in output["error"]["message"]
