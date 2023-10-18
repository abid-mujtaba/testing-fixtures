FROM python:3.12.0-slim-bookworm AS base

FROM base AS server

RUN apt-get update \
 && apt-get install -y \
        netcat-traditional

WORKDIR /work

COPY example/pyproject.toml /work/
COPY example/src /work/src

RUN --mount=type=cache,target=/root/.cache \
        python3.12 -m pip install -e .

ENV PYTHONDONTWRITEBYTECODE=1


FROM base AS builder

WORKDIR /work

COPY pyproject.toml README.md /work/
COPY src /work/src

RUN --mount=type=cache,target=/root/.cache \
        python3.12 -m pip install build \
 &&     python3.12 -m build


FROM server AS test

COPY --from=builder /work/dist/*.whl /tmp/
RUN --mount=type=cache,target=/root/.cache \
        python3.12 -m pip install \
                /tmp/*.whl \
                pytest \
                requests
