from typing import Callable

from rundfunk.event_bus import Subscription

from ..events import Previous


class OnPrevious(Subscription):
    event_name: str = Previous.name

    def __init__(self, handler: Callable[[Previous], None]):
        super().__init__(handler)
