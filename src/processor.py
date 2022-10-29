from flask import Flask, jsonify
import logging


logger = logging.getLogger(__name__)
app = Flask(__name__)


@app.route("/test")
def process_test():
    """Implement /test end-point."""
    response = {"test": {"success": True}}
    return jsonify(response)
