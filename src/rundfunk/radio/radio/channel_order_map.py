from .channel import Channel


class ChannelOrderMap:
    _map = {
        Channel.DEUTSCHLANDFUNK.value: {
            "previous": Channel.DEUTSCHLANDFUNK_NOVA,
            "next": Channel.DEUTSCHLANDFUNK_KULTUR,
        },
        Channel.DEUTSCHLANDFUNK_KULTUR.value: {
            "previous": Channel.DEUTSCHLANDFUNK,
            "next": Channel.DEUTSCHLANDFUNK_NOVA,
        },
        Channel.DEUTSCHLANDFUNK_NOVA.value: {
            "previous": Channel.DEUTSCHLANDFUNK_KULTUR,
            "next": Channel.DEUTSCHLANDFUNK,
        },
    }

    @staticmethod
    def next(channel: Channel) -> Channel:
        return ChannelOrderMap._map[channel.value]["next"]

    @staticmethod
    def previous(channel: Channel) -> Channel:
        return ChannelOrderMap._map[channel.value]["previous"]
