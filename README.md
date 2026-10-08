# Rundfunk

[![rundfunk](https://snapcraft.io/rundfunk/badge.svg)](https://snapcraft.io/rundfunk)

Listen to Deutschlandfunk, Deutschlandfunk Kultur and Deutschlandfunk Nova live from your Linux system tray.

Rundfunk is an unofficial client and not affiliated with Deutschlandradio.

<p align="center">
  <img src="https://drive.google.com/uc?export=view&id=15w5cfdpoHcn0kl6izspzTgR-6ywPxkbO" alt="Rundfunk App">
</p>

## Install

[![Get it from the Snap Store](https://snapcraft.io/static/images/badges/en/snap-store-black.svg)](https://snapcraft.io/rundfunk)

```bash
sudo snap install rundfunk
```

On GNOME outside Ubuntu, add the
[AppIndicator extension](https://extensions.gnome.org/extension/615/appindicator-support/) for the tray icon.

## Usage

- Open a channel in the tray menu to listen. Its submenu shows what's on air.
- Close the menu to keep listening, collapse the submenu to stop.
- Play, pause and switch channels with your media keys or your desktop's media controls, in GNOME under the clock.

## Development

```bash
tooling/scripts/run.sh     # start the tray app, extra args go to rundfunk, e.g. --log-level debug
tooling/scripts/test.sh    # run pytest, extra args go to pytest
tooling/scripts/lint.sh    # run ruff and ShellCheck
tooling/scripts/format.sh  # apply ruff fixes and formatting
tooling/scripts/shell.sh   # open a shell in the dev container
```

## Test a Local Snap Build

Requires [snapcraft](https://snapcraft.io/snapcraft) 9 and [LXD](https://snapcraft.io/lxd).

```bash
rm -f rundfunk_*.snap
snapcraft clean rundfunk
snapcraft pack
sudo snap install --dangerous ./rundfunk_*.snap
```

Go back to the store version with `sudo snap refresh rundfunk --amend`. If the build times out waiting for networking
and ufw is active, let LXD through:

```bash
sudo ufw allow in on lxdbr0
sudo ufw route allow in on lxdbr0
sudo ufw route allow out on lxdbr0
```

## Release

Every push to `main` makes the [snapcraft.io build service](https://snapcraft.io/rundfunk/builds) build all
architectures and upload them to `edge`. Test there with `sudo snap refresh rundfunk --edge`, then promote the new
revisions step by step:

```bash
snapcraft login
snapcraft status rundfunk                            # revisions per channel and architecture
snapcraft release rundfunk <revision> beta,candidate
snapcraft release rundfunk <revision> stable
```

Each architecture has its own revision. To roll back, release the previous revision to the channel again.
