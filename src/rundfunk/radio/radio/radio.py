from rundfunk.event_bus import EventBus
from rundfunk.logger import Logger
from rundfunk.radio.audio_player import AudioPlayer, OnTags, Tags
from rundfunk.radio.radio.subscriptions import OnPlay, OnPause, OnToggle, OnNext, OnPrevious
from .channel import Channel
from .channel_order_map import ChannelOrderMap
from .events import Pause, Play, Toggle, Next, Previous, UpdateMetaData


class Radio:
    _logger: Logger = Logger('Radio')
    _current_channel: Channel

    def __init__(self, audio_player: AudioPlayer, event_bus: EventBus):
        self._audio_player = audio_player
        self._event_bus = event_bus

    @staticmethod
    def create(audio_player: AudioPlayer, event_bus: EventBus, current_channel: Channel) -> 'Radio':
        radio = Radio(audio_player, event_bus)

        radio._set_channel(current_channel)
        event_bus.subscribe(OnPlay(radio._on_play))
        event_bus.subscribe(OnPause(radio._on_pause))
        event_bus.subscribe(OnToggle(radio._on_toggle))
        event_bus.subscribe(OnNext(radio._on_next))
        event_bus.subscribe(OnPrevious(radio._on_previous))
        event_bus.subscribe(OnTags(radio._on_tags))

        return radio

    def _on_next(self, _: Next) -> None:
        self._logger.debug("OnNext")
        self._play(ChannelOrderMap.next(self._current_channel))

    def _on_previous(self, _: Previous) -> None:
        self._logger.debug("OnPrevious")
        self._play(ChannelOrderMap.previous(self._current_channel))

    def _on_toggle(self, _: Toggle) -> None:
        self._logger.debug("OnToggle")

        if self._audio_player.is_playing:
            return self._pause(self._current_channel)

        self._play(self._current_channel)

    def _on_play(self, event: Play) -> None:
        self._logger.debug("OnPlay - " + event.channel.name)

        if event.channel.value == self._current_channel.value:
            return self._audio_player.play()

        self._change_channel(event.channel)

    def _on_pause(self, event: Pause) -> None:
        self._logger.debug("OnPause - " + event.channel.name)

        if event.channel.value == self._current_channel.value:
            self._audio_player.pause()

    def _on_tags(self, event: Tags) -> None:
        for index in range(event.tagList.n_tags()):
            tag = event.tagList.nth_tag_name(index)

            # Tag Details:
            # https://gstreamer.freedesktop.org/documentation/gstreamer/gsttaglist.html?gi-language=c#GST_TAG_TITLE
            if tag == "title":
                title = event.tagList.get_string(tag)[1]
                self._publish_meta_data_update(title)

    def _publish_meta_data_update(self, title: str = None) -> None:
        if not isinstance(title, str):
            return

        # The title often ends with a comma, but we
        # do not want to show this to the user.
        if title.endswith(","):
            return self._event_bus.publish(UpdateMetaData(self._current_channel, title[:-1]))

        self._event_bus.publish(UpdateMetaData(self._current_channel, title))

    def _play(self, channel: Channel) -> None:
        self._logger.debug("Play - " + channel.name)
        self._event_bus.publish(Play(channel))

    def _pause(self, channel: Channel) -> None:
        self._logger.debug("Pause - " + channel.name)
        self._event_bus.publish(Pause(channel))

    def _set_channel(self, channel: Channel) -> None:
        self._current_channel = channel
        self._audio_player.set_uri(channel.value)

    def _change_channel(self, channel: Channel) -> None:
        self._audio_player.pause()
        self._set_channel(channel)
        self._audio_player.play()
