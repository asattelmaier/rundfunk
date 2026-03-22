from rundfunk.event_bus import Event

from ..channel import Channel


class Pause(Event):
    name: str = "radio::pause"

    def __init__(self, channel: Channel):
        self.channel = channel
