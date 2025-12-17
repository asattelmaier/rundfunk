import os

from src.event_bus import EventBus
from src.radio import Channel
from .g_object import GimpToolkit, AppIndicator
from .menu import AppMenuFactory, MenuHandler, MenuBuilder
from .mpris import MprisMediaPlayer


def create(event_bus: EventBus) -> None:
    name = 'rundfunk'
    icon = os.path.dirname(os.path.realpath(__file__)) + "/assets/rundfunk-app-icon.svg"
    category = AppIndicator.IndicatorCategory.APPLICATION_STATUS
    handler = MenuHandler.create(event_bus, GimpToolkit.main_quit)
    builder = MenuBuilder.create(GimpToolkit, handler)
    factory = AppMenuFactory(builder, Channel)
    indicator = AppIndicator.Indicator.new(name, icon, category)
    mpris_media_player = MprisMediaPlayer(name, event_bus, desktop_entry_name='rundfunk_rundfunk')

    mpris_media_player.publish()
    indicator.set_status(AppIndicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(factory.create())
    GimpToolkit.main()
