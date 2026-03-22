import textwrap

from rundfunk.radio import Channel

from ...g_object import CheckMenuItem, GtkLabel, Menu


class MenuItem:
    _PLACEHOLDER = "..."
    _TITLE_WRAP_WIDTH = 28

    def __init__(
        self,
        item: CheckMenuItem,
        title_label: GtkLabel,
        submenu: Menu,
        channel: Channel,
    ):
        self._item = item
        self._title_label = title_label
        self._submenu = submenu
        self._channel = channel
        self._title = ""
        self._is_updated_by_click = True

    @property
    def channel(self) -> Channel:
        return self._channel

    @property
    def submenu(self) -> Menu:
        return self._submenu

    @property
    def is_active(self) -> bool:
        return self._item.get_active()

    @property
    def is_updated_by_click(self) -> bool:
        return self._is_updated_by_click

    def show_title(self) -> None:
        self._title_label.set_label(self._format_title(self._title))

    def update_title(self, title: str) -> None:
        self._title = title
        self.show_title()

    def activate(self) -> None:
        self._is_updated_by_click = False
        self._item.set_active(True)

    def disable(self) -> None:
        self._is_updated_by_click = False
        self._item.set_active(False)

    def update_done(self) -> None:
        self._is_updated_by_click = True

    def _format_title(self, title: str) -> str:
        if not title:
            return self._PLACEHOLDER

        return textwrap.fill(
            title,
            width=self._TITLE_WRAP_WIDTH,
            break_long_words=True,
            break_on_hyphens=True,
        )
