# Rundfunk

[![rundfunk](https://snapcraft.io/rundfunk/badge.svg)](https://snapcraft.io/rundfunk)

Unofficial Deutschlandradio GNU/Linux client for the Deutschlandradio channels Deutschlandfunk, Deutschlandfunk Kultur,
and Deutschlandfunk Nova.

<p align="center">
  <img src="https://drive.google.com/uc?export=view&id=15w5cfdpoHcn0kl6izspzTgR-6ywPxkbO" alt="Rundfunk App">
</p>

## Development

```bash
tooling/scripts/run.sh               # start the tray app; extra args go to rundfunk, e.g. --log-level debug
tooling/scripts/test.sh              # run pytest; extra args go to pytest
tooling/scripts/lint.sh              # run ruff and ShellCheck
tooling/scripts/format.sh            # apply ruff fixes and formatting
tooling/scripts/shell.sh             # open a shell in the dev container
tooling/scripts/resolve_apt_pins.sh  # print the Dockerfile's apt pins for today's Ubuntu snapshot
```

## Build Snap

Requires [snapcraft](https://snapcraft.io/snapcraft).

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
