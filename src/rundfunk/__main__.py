import argparse
from rundfunk import __version__
from rundfunk.logger import Logger


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
    main()


if __name__ == "__main__":
    cli()
