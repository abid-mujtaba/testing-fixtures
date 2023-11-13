"""Request processor of flask server."""

import logging

from flask import Flask, Response, jsonify, request

from . import dba

logger = logging.getLogger(__name__)
app = Flask(__name__)


@app.route("/test")
def process_test() -> Response:
    """Implement /test end-point."""
    response = {"test": {"success": True}}
    return jsonify(response)


@app.route("/compute", methods=["POST"])
def process_compute() -> Response:
    """Fetch operation corresponding to uuid and apply it."""
    payload = request.json
    logger.info("Request to /compute: %s", payload)

    uuid = payload["uuid"]
    value = payload["input"]

    operation = dba.get_operation(uuid)
    logger.info("operation for uuid %s from db: %s", uuid, operation)

    match operation:
        case "identity":
            response = {"result": value}

        case "square":
            response = {"result": value * value}

        case "cube":
            response = {"result": value * value * value}

        case _:
            response = {
                "error": {"message": f"Unable to find operation for uuid: {uuid}"}
            }

    logger.info("Response from /computer: %s", response)

    return jsonify(response)
