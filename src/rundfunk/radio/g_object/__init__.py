from rundfunk.runtime import require_namespace

gi = require_namespace('Gst', '1.0', 'python3-gst-1.0')

from gi.repository import Gst as GStreamer
from gi.repository.Gst import State, TagList
from gi.repository.Gst import Bus as GstBus
