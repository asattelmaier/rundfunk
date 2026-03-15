from .menu_handler import MenuHandler
from .menu_item import MenuItemLabelChannelMap
from rundfunk.radio import Channel
from ..g_object import CheckMenuItem, GimpToolkit, GtkLabel, GtkMenuItem, Menu, Pango


class MenuBuilder:
    _TITLE_WIDTH_CHARS = 28

    def __init__(self, gimp_toolkit: GimpToolkit, menu: Menu, menu_handler: MenuHandler):
        self._gimp_toolkit = gimp_toolkit
        self._menu = menu
        self._menu_handler = menu_handler

    @staticmethod
    def create(gimp_toolkit: GimpToolkit, menu_handler: MenuHandler) -> 'MenuBuilder':
        menu = gimp_toolkit.Menu()

        return MenuBuilder(gimp_toolkit, menu, menu_handler)

    def add_channel(self, channel: Channel):
        item: CheckMenuItem = self._gimp_toolkit.CheckMenuItem(label=MenuItemLabelChannelMap.get_label(channel))
        submenu: Menu = self._gimp_toolkit.Menu()
        title_item: GtkMenuItem = self._gimp_toolkit.MenuItem()
        title_label: GtkLabel = self._create_title_label()

        item.set_draw_as_radio(True)
        title_item.set_sensitive(False)
        title_item.add(title_label)
        submenu.append(title_item)
        item.set_submenu(submenu)
        self._menu_handler.add_channel_item(item, title_label, submenu, channel)
        self._add_to_menu(item)

        return self

    def add_quit_item(self, label: str):
        item: GtkMenuItem = self._gimp_toolkit.MenuItem(label=label)

        item.connect('activate', self._menu_handler.quit_item_handler)
        self._add_to_menu(item)

        return self

    def add_separator(self):
        item = self._gimp_toolkit.SeparatorMenuItem()

        self._add_to_menu(item)

        return self

    def build(self):
        self._menu.show_all()

        return self._menu

    def _create_title_label(self) -> GtkLabel:
        label = self._gimp_toolkit.Label(label='...')

        label.set_xalign(0.0)
        label.set_line_wrap(True)
        label.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR)
        label.set_width_chars(self._TITLE_WIDTH_CHARS)
        label.set_max_width_chars(self._TITLE_WIDTH_CHARS)

        return label

    def _add_to_menu(self, item):
        self._menu.append(item)
