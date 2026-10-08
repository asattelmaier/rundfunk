#!/bin/bash
#
# Runs ruff and ShellCheck in the dev container.

set -euo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/_compose.sh"

readonly CHECKS='
ruff check src/ tests/
ruff format --check src/ tests/
shellcheck tooling/scripts/*.sh snap/local/run-rundfunk
'

run_in_container tools bash -ec "${CHECKS}"
