from typing import Callable

from rundfunk.event_bus import Subscription
from ..events import Tags


class OnTags(Subscription):
    event_name: str = Tags.name

    def __init__(self, handler: Callable[[Tags], None]):
        super().__init__(handler)
