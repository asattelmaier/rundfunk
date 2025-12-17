from pydbus.generic import signal

from src.event_bus import EventBus
from src.logger import Logger
from src.radio import OnPlay, OnPause, Play, Pause, Toggle, Next, Previous, OnMetaDataUpdate, UpdateMetaData, Channel
from .playback_status import PlaybackStatus
from .title_map import TitleMap
from ...g_object import Variant


class MprisPlayer:
    _logger: Logger = Logger('MprisPlayer')

    """
    API Documentation:
    https://specifications.freedesktop.org/mpris-spec/2.2/Player_Interface.html
    """

    dbus = """
    <node>
      <interface name="org.mpris.MediaPlayer2">
        <property name="Identity" type="s" access="read"/>
        <property name="DesktopEntry" type="s" access="read"/>
        <property name="SupportedMimeTypes" type="as" access="read"/>
        <property name="SupportedUriSchemes" type="as" access="read"/>
        <property name="HasTrackList" type="b" access="read"/>
        <method name="Raise"/>
        <method name="Quit"/>
      </interface>
      <interface name="org.mpris.MediaPlayer2.Player">
        <property name="CanPlay" type="b" access="read"/>
        <property name="CanPause" type="b" access="read"/>
        <property name="CanGoNext" type="b" access="read"/>
        <property name="CanGoPrevious" type="b" access="read"/>
        <property name="PlaybackStatus" type="s" access="read"/>
        <property name="Metadata" type="a{sv}" access="read"/>
        <method name="Next"/>
        <method name="Previous"/>
        <method name="Pause"/>
        <method name="PlayPause"/>
        <method name="Stop"/>
        <method name="Play"/>
      </interface>
    </node>
    """
    CanPlay = True
    CanPause = True
    CanGoNext = True
    CanGoPrevious = True
    PlaybackStatus = PlaybackStatus.STOPPED.value
    Identity = 'Rundfunk'
    DesktopEntry = 'rundfunk'
    SupportedMimeTypes = []
    SupportedUriSchemes = []
    HasTrackList = False
    PropertiesChanged = signal()
    _metadata = {'title': '', 'artist': 'Rundfunk'}

    def __init__(self, main_interface: str, event_bus: EventBus, desktop_entry_name: str) -> None:
        self._interface: str = f'{main_interface}.Player'
        self.DesktopEntry = desktop_entry_name
        self._event_bus = event_bus

        event_bus.subscribe(OnPlay(self._on_play))
        event_bus.subscribe(OnPause(self._on_pause))
        event_bus.subscribe(OnMetaDataUpdate(self._on_meta_data_update))

    @property
    def Metadata(self) -> dict:
        """
        API Documentation:
        https://specifications.freedesktop.org/mpris-spec/2.2/Track_List_Interface.html#Mapping:Metadata_Map

        :return: Metadata Map
        """

        # Title Metadata information:
        # https://www.freedesktop.org/wiki/Specifications/mpris-spec/metadata/#xesam:title
        title = {'xesam:title': Variant('s', self._metadata['title'])}

        # Artist Metadata information:
        # https://www.freedesktop.org/wiki/Specifications/mpris-spec/metadata/#xesam:artist
        artist = {'xesam:artist': Variant('as', [self._metadata['artist']])}

        return {**title, **artist}

    def Next(self) -> None:
        self._logger.debug("Next")
        self._event_bus.publish(Next())
        self._update_title('')

    def Previous(self) -> None:
        self._logger.debug("Previous")
        self._event_bus.publish(Previous())
        self._update_title('')

    def PlayPause(self) -> None:
        self._logger.debug("PlayPause")
        self._event_bus.publish(Toggle())

    def _on_play(self, event: Play) -> None:
        self._logger.debug("OnPlay - " + event.channel.name)
        self._update_playback_status(PlaybackStatus.PLAYING)
        self._update_channel(event.channel)

    def _on_pause(self, event: Pause) -> None:
        self._logger.debug("OnPause - " + event.channel.name)
        self._update_playback_status(PlaybackStatus.PAUSED)

    def _on_meta_data_update(self, event: UpdateMetaData) -> None:
        # FIXME: The meta data is not displayed completely, only the last metadata received is displayed
        self._logger.debug("OnMetaDataUpdate - " + event.channel.name + ' - ' + event.title)
        self._update_channel(event.channel)
        self._update_title(event.title)

    def _update_playback_status(self, playback_status: PlaybackStatus) -> None:
        self._update({'PlaybackStatus': playback_status.value})

    def _update_channel(self, channel: Channel) -> None:
        self._metadata['artist'] = TitleMap.get_label(channel)
        self._update({'Metadata': self.Metadata})

    def _update_title(self, title: str) -> None:
        self._metadata['title'] = title
        self._update({'Metadata': self.Metadata})

    def Raise(self) -> None:
        pass

    def Quit(self) -> None:
        pass

    def _update(self, properties: dict) -> None:
        self.PropertiesChanged(self._interface, properties, [])
