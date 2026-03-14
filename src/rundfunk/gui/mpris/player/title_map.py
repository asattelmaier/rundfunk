from rundfunk.radio import Channel
from .title import Title


class TitleMap:
    _map = {
        Title.DEUTSCHLANDFUNK.value: Channel.DEUTSCHLANDFUNK,
        Title.DEUTSCHLANDFUNK_KULTUR.value: Channel.DEUTSCHLANDFUNK_KULTUR,
        Title.DEUTSCHLANDFUNK_NOVA.value: Channel.DEUTSCHLANDFUNK_NOVA,
        Title.DOKUMENTE_UND_DEBATTEN.value: Channel.DOKUMENTE_UND_DEBATTEN,
    }

    @staticmethod
    def get_label(channel: Channel) -> str:
        for label, current_channel in TitleMap._map.items():
            if channel.value == current_channel.value:
                return label
