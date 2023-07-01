FROM python:latest AS server

RUN apt-get update \
 && apt-get install -y \
        netcat-traditional

WORKDIR /work

COPY example/pyproject.toml /work/
COPY example/src /work/src

RUN --mount=type=cache,target=/root/.cache \
        python3.11 -m pip install -e .

ENV PYTHONDONTWRITEBYTECODE=1


FROM python:latest AS builder

WORKDIR /work

COPY pyproject.toml README.md /work/
COPY src /work/src

RUN --mount=type=cache,target=/root/.cache \
        python3.11 -m pip install build \
 &&     python3.11 -m build


FROM server AS test

COPY --from=builder /work/dist/*.whl /tmp/
RUN python3.11 -m pip install /tmp/*.whl

RUN --mount=type=cache,target=/root/.cache \
        python3.11 -m pip install \
                pytest \
                requests
