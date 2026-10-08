#!/bin/bash
#
# Shared setup for the dev container scripts.

RUNDFUNK_REPO_ROOT="$(dirname "${BASH_SOURCE[0]}")/../.."
RUNDFUNK_REPO_ROOT="$(CDPATH='' cd -- "${RUNDFUNK_REPO_ROOT}" && pwd -P)"
RUNDFUNK_UID="$(id -u)"
RUNDFUNK_GID="$(id -g)"
RUNDFUNK_RUNTIME_DIR="${XDG_RUNTIME_DIR:-/run/user/${RUNDFUNK_UID}}"
readonly RUNDFUNK_REPO_ROOT RUNDFUNK_UID RUNDFUNK_GID RUNDFUNK_RUNTIME_DIR
export RUNDFUNK_REPO_ROOT RUNDFUNK_UID RUNDFUNK_GID RUNDFUNK_RUNTIME_DIR

readonly DEV_COMPOSE_FILE="${RUNDFUNK_REPO_ROOT}/tooling/docker/compose.yaml"
readonly DEV_IMAGE='rundfunk-dev:local'

#######################################
# Builds the dev image if needed and runs a one-off container.
# Globals:
#   DEV_COMPOSE_FILE
#   DEV_IMAGE
# Arguments:
#   Compose service, then the command and its arguments.
# Outputs:
#   Writes build progress of a first or failed image build to stderr.
#######################################
run_in_container() {
  local -ra compose=(docker compose --file "${DEV_COMPOSE_FILE}")
  local progress='quiet'
  local status=0

  if ! docker image inspect "${DEV_IMAGE}" &> /dev/null; then
    echo "Building ${DEV_IMAGE}, this takes a few minutes..." >&2
    progress='auto'
  fi
  "${compose[@]}" --progress "${progress}" build tools || status=$?
  if (( status == 130 )); then
    return "${status}"
  elif (( status != 0 )); then
    echo "Building ${DEV_IMAGE} failed, retrying with the full log..." >&2
    "${compose[@]}" --progress plain build tools || return
  fi
  "${compose[@]}" run --rm "$@"
}
