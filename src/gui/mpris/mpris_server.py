from typing import Optional

from pydbus import SessionBus
from pydbus.publication import Publication

from src.event_bus import EventBus
from .player import MprisPlayer


class MprisMediaPlayer:
    _INTERFACE: str = 'org.mpris.MediaPlayer2'
    _DBUS_PATH: str = '/org/mpris/MediaPlayer2'
    _publication_token: Optional[Publication] = None

    def __init__(self, app_name: str, event_bus: EventBus, desktop_entry_name: str) -> None:
        self._media_player_name = f'{self._INTERFACE}.{app_name}'
        self._player = MprisPlayer(self._INTERFACE, event_bus, desktop_entry_name)

    def __del__(self) -> None:
        self._unpublish()

    def publish(self) -> None:
        bus = SessionBus()

        self._publication_token = bus.publish(self._media_player_name, (self._DBUS_PATH, self._player))

    def _unpublish(self) -> None:
        if self._publication_token:
            self._publication_token.unpublish()
            self._publication_token = None
