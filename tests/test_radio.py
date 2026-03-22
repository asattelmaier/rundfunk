"""Tests for the Radio state machine.

Uses a FakeAudioPlayer (no GStreamer) with the real EventBus
to verify actual application behavior.
"""

from conftest import EventCollector, FakeTagList

from rundfunk.radio.audio_player.events import Tags
from rundfunk.radio.radio.channel import Channel
from rundfunk.radio.radio.events import Next, Pause, Play, Previous, Toggle, UpdateMetaData

# ---------------------------------------------------------------------------
# Toggle behaviour
# ---------------------------------------------------------------------------


class TestToggle:
    def test_toggle_when_stopped_starts_playback(self, event_bus, audio_player, radio):
        play_events = EventCollector(event_bus, Play)

        event_bus.publish(Toggle())

        assert audio_player.is_playing
        assert len(play_events) == 1
        assert play_events.last.channel == Channel.DEUTSCHLANDFUNK

    def test_toggle_when_playing_pauses(self, event_bus, audio_player, radio):
        event_bus.publish(Toggle())  # start
        pause_events = EventCollector(event_bus, Pause)

        event_bus.publish(Toggle())  # stop

        assert not audio_player.is_playing
        assert len(pause_events) == 1
        assert pause_events.last.channel == Channel.DEUTSCHLANDFUNK

    def test_double_toggle_restores_playback(self, event_bus, audio_player, radio):
        event_bus.publish(Toggle())
        event_bus.publish(Toggle())
        event_bus.publish(Toggle())

        assert audio_player.is_playing


# ---------------------------------------------------------------------------
# Channel navigation
# ---------------------------------------------------------------------------


class TestChannelNavigation:
    def test_next_from_dlf_plays_kultur(self, event_bus, audio_player, radio):
        play_events = EventCollector(event_bus, Play)

        event_bus.publish(Next())

        assert len(play_events) == 1
        assert play_events.last.channel == Channel.DEUTSCHLANDFUNK_KULTUR

    def test_previous_from_dlf_plays_nova(self, event_bus, audio_player, radio):
        play_events = EventCollector(event_bus, Play)

        event_bus.publish(Previous())

        assert len(play_events) == 1
        assert play_events.last.channel == Channel.DEUTSCHLANDFUNK_NOVA

    def test_next_cycles_through_all_channels(self, event_bus, audio_player, radio):
        play_events = EventCollector(event_bus, Play)

        event_bus.publish(Next())  # DLF -> Kultur
        event_bus.publish(Next())  # Kultur -> Nova
        event_bus.publish(Next())  # Nova -> DLF

        channels = [e.channel for e in play_events.events]
        assert channels == [
            Channel.DEUTSCHLANDFUNK_KULTUR,
            Channel.DEUTSCHLANDFUNK_NOVA,
            Channel.DEUTSCHLANDFUNK,
        ]

    def test_previous_cycles_backwards(self, event_bus, audio_player, radio):
        play_events = EventCollector(event_bus, Play)

        event_bus.publish(Previous())  # DLF -> Nova
        event_bus.publish(Previous())  # Nova -> Kultur
        event_bus.publish(Previous())  # Kultur -> DLF

        channels = [e.channel for e in play_events.events]
        assert channels == [
            Channel.DEUTSCHLANDFUNK_NOVA,
            Channel.DEUTSCHLANDFUNK_KULTUR,
            Channel.DEUTSCHLANDFUNK,
        ]


# ---------------------------------------------------------------------------
# Play / Pause with explicit channel
# ---------------------------------------------------------------------------


class TestPlayPause:
    def test_play_same_channel_does_not_change_uri(self, event_bus, audio_player, radio):
        original_uri = audio_player.uri

        event_bus.publish(Play(Channel.DEUTSCHLANDFUNK))

        assert audio_player.is_playing
        assert audio_player.uri == original_uri

    def test_play_different_channel_switches(self, event_bus, audio_player, radio):
        event_bus.publish(Play(Channel.DEUTSCHLANDFUNK_KULTUR))

        assert audio_player.is_playing
        assert audio_player.uri == Channel.DEUTSCHLANDFUNK_KULTUR.value

    def test_pause_same_channel_stops(self, event_bus, audio_player, radio):
        event_bus.publish(Play(Channel.DEUTSCHLANDFUNK))
        event_bus.publish(Pause(Channel.DEUTSCHLANDFUNK))

        assert not audio_player.is_playing

    def test_pause_different_channel_is_ignored(self, event_bus, audio_player, radio):
        event_bus.publish(Play(Channel.DEUTSCHLANDFUNK))
        event_bus.publish(Pause(Channel.DEUTSCHLANDFUNK_KULTUR))

        assert audio_player.is_playing


# ---------------------------------------------------------------------------
# Metadata / Tag handling
# ---------------------------------------------------------------------------


class TestMetadata:
    def test_title_tag_publishes_update(self, event_bus, audio_player, radio):
        meta_events = EventCollector(event_bus, UpdateMetaData)

        event_bus.publish(Tags(FakeTagList({"title": "Nachrichten"})))

        assert len(meta_events) == 1
        assert meta_events.last.title == "Nachrichten"
        assert meta_events.last.channel == Channel.DEUTSCHLANDFUNK

    def test_title_trailing_comma_is_stripped(self, event_bus, audio_player, radio):
        meta_events = EventCollector(event_bus, UpdateMetaData)

        event_bus.publish(Tags(FakeTagList({"title": "Nachrichten,"})))

        assert meta_events.last.title == "Nachrichten"

    def test_non_title_tag_is_ignored(self, event_bus, audio_player, radio):
        meta_events = EventCollector(event_bus, UpdateMetaData)

        event_bus.publish(Tags(FakeTagList({"artist": "DLF"})))

        assert len(meta_events) == 0

    def test_non_string_title_is_ignored(self, event_bus, audio_player, radio):
        meta_events = EventCollector(event_bus, UpdateMetaData)

        class BrokenTagList:
            def n_tags(self):
                return 1

            def nth_tag_name(self, i):
                return "title"

            def get_string(self, tag):
                return (False, None)

        event_bus.publish(Tags(BrokenTagList()))

        assert len(meta_events) == 0

    def test_metadata_reflects_current_channel_after_switch(self, event_bus, audio_player, radio):
        meta_events = EventCollector(event_bus, UpdateMetaData)

        event_bus.publish(Play(Channel.DEUTSCHLANDFUNK_NOVA))
        event_bus.publish(Tags(FakeTagList({"title": "Nova Song"})))

        assert meta_events.last.channel == Channel.DEUTSCHLANDFUNK_NOVA
