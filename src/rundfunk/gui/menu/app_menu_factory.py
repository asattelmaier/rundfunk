from rundfunk.gui.menu.menu_item import MenuItemLabel
from rundfunk.radio import Channel


class AppMenuFactory:
    def __init__(self, menu_builder):
        self._menu_builder = menu_builder

    def create(self) -> None:
        return self._build_menu()

    def _build_menu(self) -> None:
        return self._menu_builder \
            .add_channel(Channel.DEUTSCHLANDFUNK) \
            .add_channel(Channel.DEUTSCHLANDFUNK_KULTUR) \
            .add_channel(Channel.DEUTSCHLANDFUNK_NOVA) \
            .add_separator() \
            .add_quit_item(MenuItemLabel.QUIT.value) \
            .build()
