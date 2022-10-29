FROM python:latest AS server

RUN apt-get update \
 && apt-get install -y \
        netcat

RUN --mount=type=cache,target=/root/.cache \
        python3.11 -m pip install \
            flask \
            psycopg[binary]

WORKDIR /work
ENV PYTHONDONTWRITEBYTECODE=1


FROM python:latest AS test

RUN --mount=type=cache,target=/root/.cache \
        python3.11 -m pip install \
            psycopg[binary] \
            pytest \
            requests

WORKDIR /work
ENV PYTHONDONTWRITEBYTECODE=1
