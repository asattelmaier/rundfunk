from rundfunk.gui.menu.menu_item import MenuItemLabel


class AppMenuFactory:
    def __init__(self, menu_builder, channel):
        self._menu_builder = menu_builder
        self._channel = channel

    def create(self) -> None:
        return self._build_menu()

    def _build_menu(self) -> None:
        return self._menu_builder \
            .add_item(MenuItemLabel.DEUTSCHLANDFUNK.value) \
            .add_item(MenuItemLabel.DEUTSCHLANDFUNK_KULTUR.value) \
            .add_item(MenuItemLabel.DEUTSCHLANDFUNK_NOVA.value) \
            .add_item(MenuItemLabel.DOKUMENTE_UND_DEBATTEN.value) \
            .add_separator() \
            .add_item(MenuItemLabel.QUIT.value) \
            .build()
