import pytest

from rundfunk.event_bus import EventBus, Subscription
from rundfunk.radio.radio.channel import Channel


class FakeAudioPlayer:
    """Minimal in-memory replacement for GStreamer-backed AudioPlayer."""

    def __init__(self):
        self.state = "stopped"
        self.uri = None

    @property
    def is_playing(self) -> bool:
        return self.state == "playing"

    def play(self) -> None:
        self.state = "playing"

    def pause(self) -> None:
        self.state = "stopped"

    def set_uri(self, uri: str) -> None:
        self.uri = uri


class FakeTagList:
    """Mimics GStreamer TagList interface for testing tag parsing."""

    def __init__(self, tags: dict):
        self._tags = tags
        self._keys = list(tags.keys())

    def n_tags(self) -> int:
        return len(self._keys)

    def nth_tag_name(self, index: int) -> str:
        return self._keys[index]

    def get_string(self, tag: str):
        return (True, self._tags[tag])


class EventCollector:
    """Subscribes to an event type and collects all received events."""

    def __init__(self, event_bus: EventBus, event_class):
        self.events = []

        class _Sub(Subscription):
            event_name = event_class.name

            def __init__(inner_self, handler):
                super().__init__(handler)

        event_bus.subscribe(_Sub(self.events.append))

    @property
    def last(self):
        return self.events[-1] if self.events else None

    def __len__(self):
        return len(self.events)


@pytest.fixture
def event_bus():
    return EventBus()


@pytest.fixture
def audio_player():
    return FakeAudioPlayer()


@pytest.fixture
def radio(audio_player, event_bus):
    from rundfunk.radio.radio.radio import Radio

    return Radio.create(audio_player, event_bus, Channel.DEUTSCHLANDFUNK)
