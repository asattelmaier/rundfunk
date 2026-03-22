from typing import Callable

from rundfunk.event_bus import Subscription

from ..events import UpdateMetaData


class OnMetaDataUpdate(Subscription):
    event_name: str = UpdateMetaData.name

    def __init__(self, handler: Callable[[UpdateMetaData], None]):
        super().__init__(handler)
