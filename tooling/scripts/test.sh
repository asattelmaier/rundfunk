#!/bin/bash
#
# Runs the test suite in the dev container. Arguments are passed to pytest.

set -euo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/_compose.sh"

run_in_container tools python -m pytest "$@"
