from rundfunk.runtime import require_namespace

gi = require_namespace('Gtk', '3.0', 'python3-gi')
require_namespace('AppIndicator3', '0.1', 'gir1.2-appindicator3-0.1')

from gi.repository import Gtk as GimpToolkit
from gi.repository import AppIndicator3 as AppIndicator
from gi.repository import Pango
from gi.overrides.Gtk import Menu
from gi.repository import GLib
from gi.repository.Gtk import CheckMenuItem
from gi.repository.Gtk import Label as GtkLabel
from gi.repository.Gtk import MenuItem as GtkMenuItem
from gi.repository.GLib import Variant
