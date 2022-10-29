FROM python:latest AS server

RUN --mount=type=cache,target=/root/.cache \
        python3.11 -m pip install \
            flask

RUN apt-get update \
 && apt-get install -y \
        netcat

WORKDIR /work
ENV PYTHONDONTWRITEBYTECODE=1


FROM python:latest AS test

RUN --mount=type=cache,target=/root/.cache \
        python3.11 -m pip install \
            pytest \
            requests

WORKDIR /work
ENV PYTHONDONTWRITEBYTECODE=1
