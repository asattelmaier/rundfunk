import gi

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')

from gi.repository import Gtk as GimpToolkit
from gi.repository import AppIndicator3 as AppIndicator
from gi.overrides.Gtk import Menu
from gi.repository.Gtk import CheckMenuItem
from gi.repository.GLib import Variant
