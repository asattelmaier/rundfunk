from rundfunk.event_bus import Event


class Next(Event):
    name: str = 'radio::next'
