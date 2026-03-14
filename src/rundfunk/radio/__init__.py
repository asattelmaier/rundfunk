from __future__ import annotations

from typing import TYPE_CHECKING

from .radio import Channel, Next, OnMetaDataUpdate, OnPause, OnPlay, Pause, Play, Previous, Toggle, UpdateMetaData

if TYPE_CHECKING:
    from rundfunk.event_bus import EventBus


def create(event_bus: EventBus, current_channel: Channel) -> None:
    from .audio_player import AudioPlayer
    from .g_object import GStreamer
    from .radio.radio import Radio

    player = AudioPlayer.create(event_bus, GStreamer)
    Radio.create(player, event_bus, current_channel)
