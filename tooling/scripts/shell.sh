#!/bin/bash
#
# Opens a shell in the dev container. Arguments are passed to bash.

set -euo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/_compose.sh"

run_in_container tools bash "$@"
