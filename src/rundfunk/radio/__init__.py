from __future__ import annotations

from typing import TYPE_CHECKING

from .radio import (
    Channel as Channel,
)
from .radio import (
    Next as Next,
)
from .radio import (
    OnMetaDataUpdate as OnMetaDataUpdate,
)
from .radio import (
    OnPause as OnPause,
)
from .radio import (
    OnPlay as OnPlay,
)
from .radio import (
    Pause as Pause,
)
from .radio import (
    Play as Play,
)
from .radio import (
    Previous as Previous,
)
from .radio import (
    Toggle as Toggle,
)
from .radio import (
    UpdateMetaData as UpdateMetaData,
)

if TYPE_CHECKING:
    from rundfunk.event_bus import EventBus


def create(event_bus: EventBus, current_channel: Channel) -> None:
    from .audio_player import AudioPlayer
    from .g_object import GStreamer
    from .radio.radio import Radio

    player = AudioPlayer.create(event_bus, GStreamer)
    Radio.create(player, event_bus, current_channel)
