from rundfunk.event_bus import Event
from ...g_object import TagList


class Tags(Event):
    name: str = 'audio_player::tags'

    def __init__(self, tag_list: TagList):
        self.tagList = tag_list
