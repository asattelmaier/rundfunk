#!/bin/bash
#
# Prints the Dockerfile's apt pins as resolved in an Ubuntu archive snapshot.
# Usage: resolve_apt_pins.sh [SNAPSHOT_ID], defaults to today 00:00 UTC.

set -euo pipefail

DOCKERFILE="$(dirname "${BASH_SOURCE[0]}")/../docker/Dockerfile"
readonly DOCKERFILE
readonly PACKAGE_REGEX='^ +([a-z0-9][a-z0-9.+-]*)(=[^ ]+)? \\$'

read -r -d '' RESOLVE_SCRIPT << 'EOF' || true
set -euo pipefail
snapshot="$1"
shift

cat > /tmp/bootstrap-ca.crt
rm /etc/apt/sources.list.d/ubuntu.sources
cat > /etc/apt/sources.list.d/ubuntu-snapshot.sources << SOURCES
Types: deb
URIs: https://snapshot.ubuntu.com/ubuntu/${snapshot}/
Suites: noble noble-updates noble-security
Components: main universe
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
SOURCES
apt-get -o Acquire::https::CAInfo=/tmp/bootstrap-ca.crt update > /dev/null

pins=()
for package in "$@"; do
  version="$(apt-cache policy "${package}" | sed -n 's/^ *Candidate: //p')"
  if [[ -z "${version}" || "${version}" == '(none)' ]]; then
    echo "No candidate for ${package} in snapshot ${snapshot}." >&2
    exit 1
  fi
  pins+=("${package}=${version}")
done
if ! output="$(apt-get install --simulate --no-install-recommends \
  "${pins[@]}" 2>&1)"; then
  echo "${output}" >&2
  exit 1
fi

echo "ARG UBUNTU_SNAPSHOT=${snapshot}"
printf '      %s \\\n' "${pins[@]}"
EOF
readonly RESOLVE_SCRIPT

die() {
  echo "$*" >&2
  exit 1
}

main() {
  local snapshot="${1:-}"
  if [[ -z "${snapshot}" ]]; then
    snapshot="$(date -u +%Y%m%dT000000Z)"
  fi
  if [[ ! "${snapshot}" =~ ^[0-9]{8}T[0-9]{6}Z$ ]]; then
    die "Invalid snapshot ID ${snapshot}, expected e.g. 20261008T000000Z."
  fi
  if (( ${snapshot//[TZ]/} > $(date -u +%Y%m%d%H%M%S) )); then
    die "Snapshot ${snapshot} lies in the future, its content still changes."
  fi

  local line ubuntu_image='' ca_image=''
  local -a packages=()
  while IFS= read -r line; do
    if [[ "${line}" == 'ARG UBUNTU_IMAGE='* ]]; then
      ubuntu_image="${line#*=}"
    elif [[ "${line}" == 'ARG CA_BOOTSTRAP_IMAGE='* ]]; then
      ca_image="${line#*=}"
    elif [[ "${line}" =~ ${PACKAGE_REGEX} ]]; then
      packages+=("${BASH_REMATCH[1]}")
    fi
  done < "${DOCKERFILE}"
  if [[ -z "${ubuntu_image}" || -z "${ca_image}" ]] \
    || (( ${#packages[@]} == 0 )); then
    die "Found no images or apt packages in ${DOCKERFILE}."
  fi

  docker run --rm "${ca_image}" cat /etc/ssl/certs/ca-certificates.crt \
    | docker run --rm --interactive "${ubuntu_image}" \
      bash -c "${RESOLVE_SCRIPT}" bash "${snapshot}" "${packages[@]}"
}

main "$@"
