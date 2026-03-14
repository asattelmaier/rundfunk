from typing import Callable

from rundfunk.event_bus import Subscription
from ..events import Toggle


class OnToggle(Subscription):
    event_name: str = Toggle.name

    def __init__(self, handler: Callable[[Toggle], None]):
        super().__init__(handler)
