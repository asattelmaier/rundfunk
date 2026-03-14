from rundfunk.event_bus import Event
from ..channel import Channel


class UpdateMetaData(Event):
    name: str = 'radio::update_meta_data'

    def __init__(self, channel: Channel, title: str):
        self.channel = channel
        self.title = title
