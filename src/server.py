"""Entrypoint of flask server."""

import logging

from processor import app


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s %(name)s %(filename)s:%(lineno)d - %(message)s",
        level=logging.INFO,
    )
    app.run(host="0.0.0.0", port=80)
