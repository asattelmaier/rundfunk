#!/bin/bash
#
# Applies ruff fixes and formatting in the dev container.

set -euo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/_compose.sh"

readonly COMMANDS='
ruff check --fix src/ tests/
ruff format src/ tests/
'

run_in_container tools bash -ec "${COMMANDS}"
