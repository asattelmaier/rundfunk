from typing import Callable

from rundfunk.event_bus import EventBus
from rundfunk.gui.menu.menu_item import MenuItemLabel, MenuItem, MenuItemLabelChannelMap
from rundfunk.logger import Logger
from rundfunk.radio import Channel, OnPlay, Play, OnPause, Pause
from ..g_object import CheckMenuItem


class MenuHandler:
    _logger: Logger = Logger('MenuHandler')

    def __init__(self, event_bus: EventBus, quit_handler: Callable):
        self._items: [MenuItem] = []
        self._event_bus: EventBus = event_bus
        self._quit_handler: Callable = quit_handler

    @staticmethod
    def create(event_bus: EventBus, quit_handler: Callable) -> 'MenuHandler':
        menu_handler = MenuHandler(event_bus, quit_handler)

        event_bus.subscribe(OnPlay(menu_handler._activate_item))
        event_bus.subscribe(OnPause(menu_handler._disable_item))

        return menu_handler

    def add_item(self, item: CheckMenuItem) -> None:
        channel = MenuItemLabelChannelMap.get_channel(item.get_label())

        return self._items.append(MenuItem(item, channel))

    def item_handler(self, item: CheckMenuItem) -> None:
        label = item.get_label()

        self._logger.debug("ItemHandler - " + label)

        if label == MenuItemLabel.QUIT.value:
            return self._quit_handler()

        self._item_handler(self._get_item_by_label(label))

    @staticmethod
    def _disable_items(items: [MenuItem]) -> None:
        for item in items:
            if item.is_active:
                item.disable()

    def _get_item_by_channel(self, channel: Channel) -> MenuItem:
        for item in self._items:
            if item.channel.value == channel.value:
                return item

    def _get_item_by_label(self, label: str) -> MenuItem:
        for item in self._items:
            if item.label == label:
                return item

    def _item_handler(self, item: MenuItem) -> None:
        if not item.is_updated_by_click:
            return item.update_done()

        if not item.is_active:
            self._logger.debug("Pause - " + item.channel.name)
            return self._event_bus.publish(Pause(item.channel))

        self._logger.debug("Play - " + item.channel.name)
        return self._event_bus.publish(Play(item.channel))

    def _filter_item(self, item_to_filter: MenuItem) -> [MenuItem]:
        return filter(lambda item: item is not item_to_filter, self._items)

    def _activate_item(self, event: Play) -> None:
        item = self._get_item_by_channel(event.channel)

        self._logger.debug("OnPlay - " + item.channel.name)

        if not item.is_active:
            item.activate()

        items = self._filter_item(item)
        MenuHandler._disable_items(items)

    def _disable_item(self, event: Pause) -> None:
        item = self._get_item_by_channel(event.channel)

        self._logger.debug("OnPause - " + item.channel.name)

        if item.is_active:
            item.disable()
