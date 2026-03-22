import time
from typing import Callable, Optional

from rundfunk.event_bus import EventBus
from rundfunk.gui.menu.menu_item import MenuItem
from rundfunk.logger import Logger
from rundfunk.radio import Channel, OnMetaDataUpdate, OnPause, OnPlay, Pause, Play, UpdateMetaData
from rundfunk.runtime import MissingSystemDependencyError, require_namespace
from ..g_object import CheckMenuItem, GLib, GtkLabel, GtkMenuItem, Menu

try:
    gi = require_namespace('Gio', '2.0', 'python3-gi')
    from gi.repository import Gio
except MissingSystemDependencyError:
    Gio = None


class MenuHandler:
    _DBUS_MENU_INTERFACE = 'com.canonical.dbusmenu'
    _DBUS_MENU_EVENT = 'Event'
    _DBUS_MENU_ROOT_ID = 0
    _DBUS_MENU_OPENED = 'opened'
    _DBUS_MENU_CLOSED = 'closed'
    _ROOT_CLOSE_WINDOW_SECONDS = 0.5
    _logger: Logger = Logger('MenuHandler')

    def __init__(self, event_bus: EventBus, quit_handler: Callable):
        self._items: [MenuItem] = []
        self._event_bus: EventBus = event_bus
        self._quit_handler: Callable = quit_handler
        self._menu: Optional[Menu] = None
        self._is_ready: bool = False
        self._active_channel: Optional[Channel] = None
        self._session_channel: Optional[Channel] = None
        self._root_menu_closed_at: Optional[float] = None
        self._dbus_connection = None
        self._dbus_filter_id: Optional[int] = None

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
        self._attach_dbus_menu_filter()
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
        was_submenu_open = item.submenu.get_mapped()
        was_channel_opened_in_current_session = (
            self._session_channel is not None and self._session_channel.value == item.channel.value
        )

        is_active_channel = self._active_channel and self._active_channel.value == item.channel.value
        self._session_channel = item.channel

        if item.is_active:
            if not is_active_channel:
                self._event_bus.publish(Play(item.channel))
            return

        if not is_active_channel:
            return

        if was_submenu_open or was_channel_opened_in_current_session:
            self._logger.debug("ClosePreviewByToggle - " + item.channel.name)
            self._session_channel = None
            self._event_bus.publish(Pause(item.channel))
            return

        item.activate()

    def _close_preview(self, _: Menu, item: MenuItem) -> None:
        if not self._is_ready:
            return

        GLib.timeout_add(150, self._pause_if_submenu_collapsed, item)

    def _pause_if_submenu_collapsed(self, item: MenuItem) -> bool:
        if item.submenu.get_mapped():
            return False

        if not self._active_channel or self._active_channel.value != item.channel.value:
            return False

        if not self._session_channel or self._session_channel.value != item.channel.value:
            return False

        if self._was_root_menu_closed_recently():
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

    def _attach_dbus_menu_filter(self) -> None:
        if Gio is None or self._dbus_filter_id is not None:
            return

        self._dbus_connection = Gio.bus_get_sync(Gio.BusType.SESSION, None)
        self._dbus_filter_id = self._dbus_connection.add_filter(self._on_dbus_menu_message)

    def _on_dbus_menu_message(self, _connection, message, incoming: bool):
        if Gio is None or not incoming:
            return message

        if message.get_message_type() != Gio.DBusMessageType.METHOD_CALL:
            return message

        if message.get_interface() != self._DBUS_MENU_INTERFACE:
            return message

        if message.get_member() != self._DBUS_MENU_EVENT:
            return message

        body = message.get_body()

        if body is None:
            return message

        item_id, event_name, *_ = body.unpack()

        if item_id != self._DBUS_MENU_ROOT_ID:
            return message

        if event_name == self._DBUS_MENU_OPENED:
            self._root_menu_closed_at = None
            self._session_channel = None
            return message

        if event_name == self._DBUS_MENU_CLOSED:
            self._root_menu_closed_at = time.monotonic()
            self._session_channel = None

        return message

    def _was_root_menu_closed_recently(self) -> bool:
        return bool(
            self._root_menu_closed_at is not None
            and (time.monotonic() - self._root_menu_closed_at) <= self._ROOT_CLOSE_WINDOW_SECONDS
        )
