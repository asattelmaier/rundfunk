# syntax=docker/dockerfile:1.27.1@sha256:4edf897a3ffa55b89f906fc8cc78afdb3f1834cc9c7083565e611a8a7d5fe99e

ARG UBUNTU_IMAGE=ubuntu:24.04@sha256:534baea6a22c03a63003dbc8dbe78fe34bc0d7e595d9a9dc9834884ff530eb55
ARG UV_IMAGE=ghcr.io/astral-sh/uv:0.12.23@sha256:61d393e44e249f2e4b526b6c7ddcecce245946826e608e11c93ad4f5bba55b21
ARG CA_BOOTSTRAP_IMAGE=alpine:3.24.2@sha256:294b683cb724975bec92580e1e685676bd4b50bda910ddb8c51d4cabeaec77e6

FROM ${UV_IMAGE} AS uv
FROM ${CA_BOOTSTRAP_IMAGE} AS ca-bootstrap

FROM ${UBUNTU_IMAGE}

ARG UBUNTU_SNAPSHOT=20261008T000000Z

ENV DEBIAN_FRONTEND=noninteractive \
    LANG=C.UTF-8

RUN <<EOF
set -eu
rm /etc/apt/sources.list.d/ubuntu.sources
cat > /etc/apt/sources.list.d/ubuntu-snapshot.sources <<SOURCES
Types: deb
URIs: https://snapshot.ubuntu.com/ubuntu/${UBUNTU_SNAPSHOT}/
Suites: noble noble-updates noble-security
Components: main universe
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
SOURCES
EOF

# The snapshot service is HTTPS-only and the base image has no CA bundle yet.
RUN --mount=type=bind,from=ca-bootstrap,source=/etc/ssl/certs/ca-certificates.crt,target=/tmp/bootstrap-ca.crt \
    apt-get -o Acquire::https::CAInfo=/tmp/bootstrap-ca.crt update \
 && apt-get -o Acquire::https::CAInfo=/tmp/bootstrap-ca.crt install --yes --no-install-recommends \
      ca-certificates=20260601~24.04.1 \
      gir1.2-ayatanaappindicator3-0.1=0.5.93-1build3 \
      gir1.2-gstreamer-1.0=1.24.2-1ubuntu0.1 \
      gir1.2-gtk-3.0=3.24.41-4ubuntu1.3 \
      glib-networking=2.80.0-1build1 \
      gstreamer1.0-plugins-base=1.24.2-1ubuntu0.5 \
      gstreamer1.0-plugins-good=1.24.2-1ubuntu1.8 \
      gstreamer1.0-pulseaudio=1.24.2-1ubuntu1.8 \
      python3=3.12.3-0ubuntu2.1 \
      python3-gi=3.48.2-1 \
      python3-gst-1.0=1.24.1-1 \
      python3.12=3.12.3-1ubuntu0.17 \
      shellcheck=0.9.0-1 \
 && rm -rf /var/lib/apt/lists/*

COPY --from=uv /uv /usr/local/bin/uv

ENV UV_PYTHON_DOWNLOADS=never \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    VIRTUAL_ENV=/opt/venv \
    UV_NO_SYNC=1 \
    UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    PATH=/opt/venv/bin:$PATH \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# PyGObject comes from apt, so uv has to use the system Python it was built for.
WORKDIR /tmp/rundfunk-lock
RUN --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    UV_PYTHON=/usr/bin/python3.12 \
    uv sync --frozen --no-build --no-install-project --extra dev --no-cache
WORKDIR /
