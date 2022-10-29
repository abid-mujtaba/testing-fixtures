"""Request processor of flask server."""

import logging

from flask import Flask, jsonify, Response


logger = logging.getLogger(__name__)
app = Flask(__name__)


@app.route("/test")
def process_test() -> Response:
    """Implement /test end-point."""
    response = {"test": {"success": True}}
    return jsonify(response)
