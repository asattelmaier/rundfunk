from rundfunk.event_bus import EventBus

from ..g_object import GStreamer, State
from .events import Tags
from .playbin import Playbin


class AudioPlayer:
    def __init__(self, player: any, player_state: State):
        self._player = player
        self._player_state = player_state

    @staticmethod
    def create(event_bus: EventBus, g_streamer: GStreamer) -> "AudioPlayer":
        g_streamer.init(None)
        player: Playbin = g_streamer.ElementFactory.make("playbin", "player")
        player_bus = player.get_bus()

        player_bus.add_signal_watch()

        # GstMessageTypes:
        # https://gstreamer.freedesktop.org/documentation/gstreamer/gstmessage.html?gi-language=c#GstMessageType
        # Python message bindings:
        # https://github.com/GStreamer/gstreamer/blob/2db3ddaa9d8e9e0a1659d7e48623c512dbda691b/subprojects/gst-plugins-base/tests/examples/seek/jsseek.c#L2537
        player_bus.connect("message::tag", lambda _, message: event_bus.publish(Tags(message.parse_tag())))

        return AudioPlayer(player, g_streamer.State)

    @property
    def is_playing(self) -> bool:
        is_playing = self._player.current_state is self._player_state.PLAYING
        is_ready = self._player.current_state is self._player_state.READY

        return is_playing or is_ready

    def set_uri(self, uri) -> None:
        self._player.set_property("uri", uri)

    def play(self) -> None:
        self._player.set_state(self._player_state.PLAYING)

    def pause(self) -> None:
        self._player.set_state(self._player_state.NULL)
