from __future__ import annotations

import os

from rundfunk.runtime import MissingSystemDependencyError, require_namespace

from .menu_item import MenuItemLabel

Gio = None


def _populate_atspi_bus_address() -> None:
    if Gio is None or "AT_SPI_BUS_ADDRESS" in os.environ:
        return

    proxy = _safe_call(
        lambda: Gio.DBusProxy.new_for_bus_sync(
            Gio.BusType.SESSION,
            Gio.DBusProxyFlags.DO_NOT_AUTO_START,
            None,
            "org.a11y.Bus",
            "/org/a11y/bus",
            "org.a11y.Bus",
            None,
        )
    )

    if proxy is None:
        return

    result = _safe_call(
        lambda: proxy.call_sync(
            "GetAddress",
            None,
            Gio.DBusCallFlags.NONE,
            -1,
            None,
        )
    )

    if result is None:
        return

    address = _safe_call(lambda: result.unpack()[0])

    if address:
        os.environ["AT_SPI_BUS_ADDRESS"] = address


def _safe_call(callback, default=None):
    try:
        return callback()
    except Exception:
        return default


try:
    gi = require_namespace("Gio", "2.0", "python3-gi")
    from gi.repository import Gio

    _populate_atspi_bus_address()
    gi = require_namespace("Atspi", "2.0", "gir1.2-atspi-2.0")
    from gi.repository import Atspi
except MissingSystemDependencyError:
    Atspi = None
    Gio = None


class ShellMenuState:
    _GNOME_SHELL = "gnome-shell"
    _CHANNEL_LABELS = {
        MenuItemLabel.DEUTSCHLANDFUNK.value,
        MenuItemLabel.DEUTSCHLANDFUNK_KULTUR.value,
        MenuItemLabel.DEUTSCHLANDFUNK_NOVA.value,
    }
    _MENU_SENTINEL_LABEL = MenuItemLabel.QUIT.value

    @staticmethod
    def is_channel_menu_open() -> bool:
        if Atspi is None:
            return False

        ShellMenuState._init_atspi()
        shell = ShellMenuState._get_gnome_shell()

        if shell is None:
            return False

        is_channel_label_visible = False
        is_menu_sentinel_visible = False

        for label in ShellMenuState._visible_label_names(shell):
            if label in ShellMenuState._CHANNEL_LABELS:
                is_channel_label_visible = True

            if label == ShellMenuState._MENU_SENTINEL_LABEL:
                is_menu_sentinel_visible = True

            if is_channel_label_visible and is_menu_sentinel_visible:
                return True

        return False

    @staticmethod
    def _visible_label_names(root):
        for accessible in ShellMenuState._walk_accessibles(root):
            label = ShellMenuState._visible_label_name(accessible)

            if label is not None:
                yield label

    @staticmethod
    def _walk_accessibles(root):
        stack = [root]

        while stack:
            accessible = stack.pop()
            yield accessible

            if ShellMenuState._role_name(accessible) == "label":
                continue

            stack.extend(ShellMenuState._children(accessible))

    @staticmethod
    def _visible_label_name(accessible):
        if ShellMenuState._role_name(accessible) != "label":
            return None

        if not ShellMenuState._is_showing(accessible):
            return None

        return ShellMenuState._safe_call(accessible.get_name, "") or None

    @staticmethod
    def _role_name(accessible) -> str:
        return ShellMenuState._safe_call(accessible.get_role_name, "")

    @staticmethod
    def _get_gnome_shell():
        desktop = ShellMenuState._safe_call(lambda: Atspi.get_desktop(0))

        if desktop is None:
            return None

        for index in range(ShellMenuState._safe_call(desktop.get_child_count, 0) or 0):
            application = ShellMenuState._safe_call(
                lambda current_index=index: desktop.get_child_at_index(current_index)
            )

            if application is None:
                continue

            if ShellMenuState._safe_call(application.get_name, "") == ShellMenuState._GNOME_SHELL:
                return application

        return None

    @staticmethod
    def _children(accessible) -> list:
        children = []
        child_count = ShellMenuState._safe_call(accessible.get_child_count, 0) or 0

        for index in range(child_count):
            child = ShellMenuState._safe_call(lambda current_index=index: accessible.get_child_at_index(current_index))

            if child is not None:
                children.append(child)

        return children

    @staticmethod
    def _is_showing(accessible) -> bool:
        state_set = ShellMenuState._safe_call(accessible.get_state_set)

        return bool(state_set and state_set.contains(Atspi.StateType.SHOWING))

    @staticmethod
    def _init_atspi() -> None:
        if Atspi is None:
            return

        if not Atspi.is_initialized():
            ShellMenuState._safe_call(Atspi.init)

    @staticmethod
    def _safe_call(callback, default=None):
        return _safe_call(callback, default)
