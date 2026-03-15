# Rundfunk

[![rundfunk](https://snapcraft.io/rundfunk/badge.svg)](https://snapcraft.io/rundfunk)

Unofficial Deutschlandradio GNU/Linux client for the Deutschlandradio channels Deutschlandfunk, Deutschlandfunk Kultur,
and Deutschlandfunk Nova.

<p align="center">
  <img src="https://drive.google.com/uc?export=view&id=15w5cfdpoHcn0kl6izspzTgR-6ywPxkbO" alt="Rundfunk App">
</p>

## Prerequisites

* Python `3.12.3` for local development via [uv](https://docs.astral.sh/uv/)
* [snapcraft](https://snapcraft.io/snapcraft)
* system packages:
  * `python3-gi`
  * [gir1.2-appindicator3-0.1](https://packages.ubuntu.com/impish/gir1.2-appindicator3-0.1)
  * [python3-gst-1.0](https://packages.ubuntu.com/bionic/python3-gst-1.0)

`uv` manages the Python package dependency (`pydbus`); the GTK/GStreamer bindings stay system-managed.
The packaged app remains compatible with Python `3.8+`, because the current Snap targets `core20`.

## Setup

```bash
sudo apt install python3-gi gir1.2-appindicator3-0.1 python3-gst-1.0
uv sync
```

## Run

```bash
uv run rundfunk
```

## Build Snap

```bash
rm -f rundfunk_*.snap
snapcraft clean rundfunk cleanup
snapcraft pack
```

## Install / Update Snap

```bash
sudo snap install --devmode ./rundfunk_*.snap
```

## Publish

```bash
# Login
snapcraft login
# upload
snapcraft upload --release <channel> rundfunk_<version>_<arch>.snap
```
