from rundfunk.event_bus import Event


class Previous(Event):
    name: str = "radio::previous"
