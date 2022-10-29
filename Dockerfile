FROM python:latest AS server

RUN apt-get update \
 && apt-get install -y \
        netcat

WORKDIR /work

COPY pyproject.toml /work/
COPY src /work/src

RUN --mount=type=cache,target=/root/.cache \
        python3.11 -m pip install -e .

ENV PYTHONDONTWRITEBYTECODE=1


FROM server AS test

RUN --mount=type=cache,target=/root/.cache \
        python3.11 -m pip install -e .[dev]
