"""Test the compute end-point."""

import json

import requests

from .utils import Uuid, base_url, operation

HTTP_OK = 200


@operation.set("identity")
def test_compute_identity(uuid: Uuid) -> None:
    """Test the /compute end-point for a user with identity operation."""
    # GIVEN
    payload = {"uuid": uuid, "input": 9}

    # WHEN
    response = requests.post(f"{base_url}/compute", json=payload, timeout=5)

    # THEN
    assert response.status_code == HTTP_OK

    output = json.loads(response.text)
    assert output["result"] == payload["input"]  # Identity operation


@operation.set("square")
def test_compute_square(uuid: Uuid) -> None:
    """Test the /compute end-point for a user with square operation."""
    # GIVEN
    payload = {"uuid": uuid, "input": 9}
    expected_result = 9 * 9  # square operation

    # WHEN
    response = requests.post(f"{base_url}/compute", json=payload, timeout=5)

    # THEN
    assert response.status_code == HTTP_OK

    output = json.loads(response.text)
    assert output["result"] == expected_result


@operation.set("cube")
def test_compute_cube(uuid: Uuid) -> None:
    """Test the /compute end-point for a user with cube operation."""
    # GIVEN
    payload = {"uuid": uuid, "input": 9}
    expected_result = 9 * 9 * 9  # cube operation

    # WHEN
    response = requests.post(f"{base_url}/compute", json=payload, timeout=5)

    # THEN
    assert response.status_code == HTTP_OK

    output = json.loads(response.text)
    assert output["result"] == expected_result


# Note: No operation record in the DB
def test_compute_no_operation() -> None:
    """Test the /compute end-point for a user with no operation in the DB."""
    # GIVEN
    uuid = 7890
    payload = {"uuid": uuid, "input": 9}

    # WHEN
    response = requests.post(f"{base_url}/compute", json=payload, timeout=5)

    # THEN
    assert response.status_code == HTTP_OK

    output = json.loads(response.text)
    assert "error" in output
    assert str(uuid) in output["error"]["message"]
