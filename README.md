# Rundfunk

[![rundfunk](https://snapcraft.io/rundfunk/badge.svg)](https://snapcraft.io/rundfunk)

Unofficial Deutschlandradio GNU/Linux client for the Deutschlandradio channels, Deutschlandfunk, Deutschlandfunk Kultur,
Deutschlandfunk Nova and Dokumente und Debatten.

<p align="center">
  <img src="https://drive.google.com/uc?export=view&id=1RpcYPeN7rZ04PpSK2FSs4HpuGf3cp_kR" alt="Rundfunk App">
</p>

## Prerequirement

* python >= 3.8
* [snapcraft](https://snapcraft.io/snapcraft)
* [gir1.2-appindicator3-0.1](https://packages.ubuntu.com/impish/gir1.2-appindicator3-0.1)
* [python3-gst-1.0](https://packages.ubuntu.com/bionic/python3-gst-1.0)

## Build

```bash
snapcraft
```

## Install

```bash
snap install --devmode *.snap
```

## Run

```bash
rundfunk
```

## Publish

```bash
# Login
snapcraft login
# push
snapcraft push rundfunk_<version>_<arch>.snap
```
