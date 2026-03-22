"""Tests for the MPRIS player logic.

Requires system GTK/GLib packages (python3-gi, gir1.2-gtk-3.0).
Tests are skipped automatically when these are unavailable.
"""

import pytest

try:
    from rundfunk.gui.mpris.player.mpris_player import MprisPlayer
    from rundfunk.gui.mpris.player.playback_status import PlaybackStatus
    from rundfunk.gui.mpris.player.title_map import TitleMap

    HAS_GTK = True
except Exception:
    HAS_GTK = False

pytestmark = pytest.mark.skipif(not HAS_GTK, reason="GTK system packages not available")

from rundfunk.event_bus import EventBus
from rundfunk.radio.radio.channel import Channel
from rundfunk.radio.radio.events import Play, Pause, Toggle, Next, Previous, UpdateMetaData

from conftest import EventCollector


@pytest.fixture
def mpris(event_bus):
    return MprisPlayer('org.mpris.MediaPlayer2', event_bus, 'rundfunk')


# ---------------------------------------------------------------------------
# Playback status
# ---------------------------------------------------------------------------

class TestPlaybackStatus:
    def test_initial_status_is_stopped(self, event_bus, mpris):
        assert mpris.PlaybackStatus == "Stopped"

    def test_status_after_play_event(self, event_bus, mpris):
        event_bus.publish(Play(Channel.DEUTSCHLANDFUNK))

        assert mpris.PlaybackStatus == "Playing"

    def test_status_after_pause_event(self, event_bus, mpris):
        event_bus.publish(Play(Channel.DEUTSCHLANDFUNK))
        event_bus.publish(Pause(Channel.DEUTSCHLANDFUNK))

        assert mpris.PlaybackStatus == "Paused"


# ---------------------------------------------------------------------------
# MPRIS commands publish correct events
# ---------------------------------------------------------------------------

class TestMprisCommands:
    def test_play_pause_publishes_toggle(self, event_bus, mpris):
        toggle_events = EventCollector(event_bus, Toggle)

        mpris.PlayPause()

        assert len(toggle_events) == 1

    def test_next_publishes_next_event(self, event_bus, mpris):
        next_events = EventCollector(event_bus, Next)

        mpris.Next()

        assert len(next_events) == 1

    def test_previous_publishes_previous_event(self, event_bus, mpris):
        prev_events = EventCollector(event_bus, Previous)

        mpris.Previous()

        assert len(prev_events) == 1


# ---------------------------------------------------------------------------
# Metadata
# ---------------------------------------------------------------------------

class TestMprisMetadata:
    def test_play_updates_artist_to_channel_label(self, event_bus, mpris):
        event_bus.publish(Play(Channel.DEUTSCHLANDFUNK))

        metadata = mpris.Metadata
        artist = metadata['xesam:artist'].unpack()
        assert artist == [TitleMap.get_label(Channel.DEUTSCHLANDFUNK)]

    def test_metadata_update_sets_title(self, event_bus, mpris):
        event_bus.publish(UpdateMetaData(Channel.DEUTSCHLANDFUNK, "Nachrichten"))

        metadata = mpris.Metadata
        title = metadata['xesam:title'].unpack()
        assert title == "Nachrichten"

    def test_next_clears_title(self, event_bus, mpris):
        event_bus.publish(UpdateMetaData(Channel.DEUTSCHLANDFUNK, "Old Title"))

        mpris.Next()

        metadata = mpris.Metadata
        title = metadata['xesam:title'].unpack()
        assert title == ""
