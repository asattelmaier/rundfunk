import gi

gi.require_version('Gst', '1.0')

from gi.repository import Gst as GStreamer
from gi.repository.Gst import State, TagList
from gi.repository.Gst import Bus as GstBus
