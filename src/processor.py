"""Request processor of flask server."""

import logging

from flask import Flask, jsonify, Response, request


logger = logging.getLogger(__name__)
app = Flask(__name__)


@app.route("/test")
def process_test() -> Response:
    """Implement /test end-point."""
    response = {"test": {"success": True}}
    return jsonify(response)


@app.route("/compute", methods=["POST"])
def process_compute() -> Response:
    """The /compute end-point fetches operation corresponding to uuid and applies it."""
    payload = request.json
    logger.info("Request to /compute: %s", payload)

    return jsonify({})
