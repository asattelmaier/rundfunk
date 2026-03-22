from rundfunk.event_bus import Event


class Toggle(Event):
    name: str = "radio::toggle"
