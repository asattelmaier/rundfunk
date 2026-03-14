from enum import Enum


class PlaybackStatus(Enum):
    """
    Source: https://specifications.freedesktop.org/mpris-spec/2.2/Player_Interface.html#Enum:Playback_Status
    """

    PLAYING = "Playing"
    PAUSED = "Paused"
    STOPPED = "Stopped"
