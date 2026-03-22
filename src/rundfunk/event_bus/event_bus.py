from rundfunk.logger import Logger

from .event import Event
from .subscription import Subscription


class EventBus:
    _logger: Logger = Logger("EventBus")

    def __init__(self) -> None:
        self._subscriptions: [Subscription] = []

    def subscribe(self, subscription: Subscription) -> None:
        self._logger.debug("Subscription - " + subscription.event_name)
        self._subscriptions.append(subscription)

    def publish(self, event: Event) -> None:
        self._logger.debug("Publish - " + event.name)

        for subscription in self._subscriptions:
            if subscription.event_name == event.name:
                subscription.notify(event)
