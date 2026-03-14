from rundfunk.radio import Channel
from .menu_item_label import MenuItemLabel


class MenuItemLabelChannelMap:
    _map = {
        MenuItemLabel.DEUTSCHLANDFUNK.value: Channel.DEUTSCHLANDFUNK,
        MenuItemLabel.DEUTSCHLANDFUNK_KULTUR.value: Channel.DEUTSCHLANDFUNK_KULTUR,
        MenuItemLabel.DEUTSCHLANDFUNK_NOVA.value: Channel.DEUTSCHLANDFUNK_NOVA,
        MenuItemLabel.DOKUMENTE_UND_DEBATTEN.value: Channel.DOKUMENTE_UND_DEBATTEN,
        MenuItemLabel.QUIT.value: Channel.EMPTY,
    }

    @staticmethod
    def get_channel(label: str) -> Channel:
        return MenuItemLabelChannelMap._map[label]

    @staticmethod
    def get_label(channel: Channel) -> str:
        for label, current_channel in MenuItemLabelChannelMap._map.items():
            if channel.value == current_channel.value:
                return label
