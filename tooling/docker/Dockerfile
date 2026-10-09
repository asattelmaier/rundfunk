# syntax=docker/dockerfile:1.27.1@sha256:4edf897a3ffa55b89f906fc8cc78afdb3f1834cc9c7083565e611a8a7d5fe99e

FROM ghcr.io/astral-sh/uv:0.12.24@sha256:3af4716e991d6956a41e573eab705d0ee08500cd829ed30293eb8472f372c65a AS uv
FROM alpine:3.24.2@sha256:294b683cb724975bec92580e1e685676bd4b50bda910ddb8c51d4cabeaec77e6 AS ca-bootstrap

FROM ubuntu:24.04@sha256:534baea6a22c03a63003dbc8dbe78fe34bc0d7e595d9a9dc9834884ff530eb55

# Fixes every apt package version. Bump it to update them.
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
      ca-certificates \
      gir1.2-ayatanaappindicator3-0.1 \
      gir1.2-gstreamer-1.0 \
      gir1.2-gtk-3.0 \
      glib-networking \
      gstreamer1.0-plugins-base \
      gstreamer1.0-plugins-good \
      gstreamer1.0-pulseaudio \
      python3 \
      python3-gi \
      python3-gst-1.0 \
      python3.12 \
      shellcheck \
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
