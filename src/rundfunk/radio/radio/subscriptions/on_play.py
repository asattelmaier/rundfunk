from typing import Callable

from rundfunk.event_bus import Subscription

from ..events import Play


class OnPlay(Subscription):
    event_name: str = Play.name

    def __init__(self, handler: Callable[[Play], None]):
        super().__init__(handler)
