from typing import Callable, Optional

from rundfunk.event_bus import EventBus
from rundfunk.gui.menu.menu_item import MenuItem
from rundfunk.logger import Logger
from rundfunk.radio import Channel, OnMetaDataUpdate, OnPause, OnPlay, Pause, Play, UpdateMetaData
from .shell_menu_state import ShellMenuState
from ..g_object import CheckMenuItem, GLib, GtkLabel, GtkMenuItem, Menu


class MenuHandler:
    _logger: Logger = Logger('MenuHandler')

    def __init__(self, event_bus: EventBus, quit_handler: Callable):
        self._items: [MenuItem] = []
        self._event_bus: EventBus = event_bus
        self._quit_handler: Callable = quit_handler
        self._menu: Optional[Menu] = None
        self._is_ready: bool = False
        self._active_channel: Optional[Channel] = None
        self._session_channel: Optional[Channel] = None

    @staticmethod
    def create(event_bus: EventBus, quit_handler: Callable) -> 'MenuHandler':
        menu_handler = MenuHandler(event_bus, quit_handler)

        event_bus.subscribe(OnPlay(menu_handler._activate_item))
        event_bus.subscribe(OnPause(menu_handler._disable_item))
        event_bus.subscribe(OnMetaDataUpdate(menu_handler._update_title))

        return menu_handler

    def ready(self, menu: Menu) -> None:
        self._menu = menu
        menu.connect('hide', self._schedule_menu_session_reset)
        menu.connect('unmap', self._schedule_menu_session_reset)
        menu.connect('deactivate', self._schedule_menu_session_reset)
        menu.connect('selection-done', self._schedule_menu_session_reset)
        menu.connect('cancel', self._schedule_menu_session_reset)
        self._is_ready = True

    def add_channel_item(
        self,
        item: CheckMenuItem,
        title_label: GtkLabel,
        submenu: Menu,
        channel: Channel,
    ) -> None:
        menu_item = MenuItem(item, title_label, submenu, channel)

        item.connect('toggled', self._toggle_channel, menu_item)
        submenu.connect('hide', self._close_preview, menu_item)
        submenu.connect('unmap', self._close_preview, menu_item)
        submenu.connect('deactivate', self._close_preview, menu_item)
        submenu.connect('selection-done', self._close_preview, menu_item)
        self._items.append(menu_item)

    def _get_item_by_channel(self, channel: Channel) -> Optional[MenuItem]:
        for item in self._items:
            if item.channel.value == channel.value:
                return item

    def quit_item_handler(self, _: GtkMenuItem) -> None:
        self._quit_handler()

    def _schedule_menu_session_reset(self, *_: object) -> None:
        GLib.idle_add(self._reset_menu_session_if_closed)

    def _reset_menu_session_if_closed(self) -> bool:
        if self._menu and self._menu.get_mapped():
            return False

        self._session_channel = None
        return False

    def _toggle_channel(self, _: CheckMenuItem, item: MenuItem) -> None:
        if not self._is_ready:
            return

        if not item.is_updated_by_click:
            item.update_done()
            return

        self._logger.debug("ToggleChannel - " + item.channel.name)
        item.show_title()

        is_active_channel = self._active_channel and self._active_channel.value == item.channel.value
        self._session_channel = item.channel

        if item.is_active:
            if not is_active_channel:
                self._event_bus.publish(Play(item.channel))
            return

        if not is_active_channel:
            return

        item.activate()

    def _close_preview(self, _: Menu, item: MenuItem) -> None:
        if not self._is_ready:
            return

        GLib.timeout_add(150, self._pause_if_submenu_collapsed, item)

    def _pause_if_submenu_collapsed(self, item: MenuItem) -> bool:
        if item.submenu.get_mapped():
            return False

        if not ShellMenuState.is_channel_menu_open():
            return False

        if not self._active_channel or self._active_channel.value != item.channel.value:
            return False

        if not self._session_channel or self._session_channel.value != item.channel.value:
            return False

        self._logger.debug("ClosePreview - " + item.channel.name)
        self._session_channel = None
        self._event_bus.publish(Pause(item.channel))

        return False

    def _update_title(self, event: UpdateMetaData) -> None:
        item = self._get_item_by_channel(event.channel)

        if not item:
            return

        self._logger.debug("OnMetaDataUpdate - " + item.channel.name)
        item.update_title(event.title)

    def _activate_item(self, event: Play) -> None:
        item = self._get_item_by_channel(event.channel)

        if not item:
            return

        self._logger.debug("OnPlay - " + item.channel.name)
        self._active_channel = item.channel

        if not item.is_active:
            item.activate()

        for current_item in self._items:
            if current_item.channel.value == item.channel.value:
                continue

            if current_item.is_active:
                current_item.disable()

    def _disable_item(self, event: Pause) -> None:
        item = self._get_item_by_channel(event.channel)

        if not item:
            return

        self._logger.debug("OnPause - " + item.channel.name)

        if item.is_active:
            item.disable()

        if self._active_channel and self._active_channel.value == item.channel.value:
            self._active_channel = None
