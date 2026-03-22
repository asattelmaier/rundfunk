from rundfunk.event_bus import Event

from ..channel import Channel


class Play(Event):
    name: str = "radio::play"

    def __init__(self, channel: Channel):
        self.channel = channel
