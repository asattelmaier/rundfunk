import argparse
import sys

from rundfunk import __version__
from rundfunk.logger import Logger
from rundfunk.runtime import MissingSystemDependencyError, ensure_host_runtime_environment


def main() -> None:
    from rundfunk import gui, radio
    from rundfunk.event_bus import EventBus

    current_channel = radio.Channel.DEUTSCHLANDFUNK
    event_bus = EventBus()

    radio.create(event_bus, current_channel)
    gui.create(event_bus)


def cli() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument("--log-level", help="Set the log level (DEBUG)")
    parser.add_argument("--version", action="version", version=f"rundfunk version {__version__}")
    args = parser.parse_args()
    Logger.setup(args.log_level)
    ensure_host_runtime_environment()
    try:
        main()
    except MissingSystemDependencyError as exc:
        print(exc, file=sys.stderr)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    cli()
