from typing import Callable
from .event import Event


class Subscription:
    event_name: str = ''

    def __init__(self, handler: Callable) -> None:
        self._handler = handler

    def notify(self, event: Event) -> None:
        self._handler(event)
