import gi

from radio import Radio, Channel, AudioPlayer
from gui import AppMenuFactory, MenuBuilder

gi.require_version('Gtk', '3.0')
gi.require_version('Gst', '1.0')
gi.require_version('AppIndicator3', '0.1')

from gi.repository import Gtk as GimpToolkit
from gi.repository import AppIndicator3 as AppIndicator
from gi.repository import Gst as GStreamer


def main():
    audio_player = AudioPlayer.create(GStreamer)
    radio = Radio.create(audio_player, Channel.DEUTSCHLANDFUNK)
    menu_builder = MenuBuilder.create(GimpToolkit)
    app_menu_factory = AppMenuFactory(menu_builder, radio, Channel, GimpToolkit.main_quit)
    indicator = AppIndicator.Indicator.new(
        'rundfunk_app_indicator_id',
        'gtk-media-play',
        AppIndicator.IndicatorCategory.APPLICATION_STATUS
    )

    indicator.set_status(AppIndicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(app_menu_factory.create())
    GimpToolkit.main()


if __name__ == "__main__":
    main()
