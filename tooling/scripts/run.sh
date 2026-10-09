#!/bin/bash
#
# Runs rundfunk in the dev container, attached to the host desktop session.
# Arguments are passed to rundfunk, e.g. --log-level debug.

set -euo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/_compose.sh"

readonly MPRIS_NAME='org.mpris.MediaPlayer2.rundfunk'

require_socket() {
  if [[ ! -S "$1" ]]; then
    echo "Missing $2 socket at $1. Run this from a desktop session." >&2
    exit 1
  fi
}

is_rundfunk_running() {
  command -v busctl > /dev/null \
    && busctl --address="unix:path=${RUNDFUNK_RUNTIME_DIR}/bus" \
      status "${MPRIS_NAME}" &> /dev/null
}

main() {
  require_socket "${RUNDFUNK_RUNTIME_DIR}/bus" 'D-Bus session bus'
  require_socket "${RUNDFUNK_RUNTIME_DIR}/pulse/native" 'PulseAudio'
  if [[ -z "${WAYLAND_DISPLAY:-}" && -z "${DISPLAY:-}" ]]; then
    echo 'No WAYLAND_DISPLAY or DISPLAY. Run this from a desktop session.' >&2
    exit 1
  fi
  if is_rundfunk_running; then
    echo 'Another rundfunk instance (e.g. the snap) is running.' \
      'Quit it from its tray menu first.' >&2
    exit 1
  fi

  run_in_container app "$@"
}

main "$@"
