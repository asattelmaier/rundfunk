from rundfunk.radio import Channel
from ...g_object import CheckMenuItem


class MenuItem:
    def __init__(self, item: CheckMenuItem, channel: Channel):
        self._item = item
        self._is_updated_by_click = True
        self._channel = channel

    @property
    def channel(self) -> Channel:
        return self._channel

    @property
    def is_active(self) -> bool:
        return self._item.get_active()

    @property
    def label(self) -> str:
        return self._item.get_label()

    @property
    def is_updated_by_click(self) -> bool:
        return self._is_updated_by_click

    def disable(self) -> None:
        self._is_updated_by_click = False
        self._item.set_active(False)

    def activate(self) -> None:
        self._is_updated_by_click = False
        self._item.set_active(True)

    def update_done(self):
        self._is_updated_by_click = True
