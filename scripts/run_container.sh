#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "${SCRIPT_DIR}/common.sh"
load_env

CONTAINER="${1:-${JETSON_CONTAINER_PACKAGE:-llava}}"

if ! command -v jetson-containers >/dev/null 2>&1; then
  echo "jetson-containers is not installed or not on PATH." >&2
  echo "Install it from https://github.com/dusty-nv/jetson-containers" >&2
  exit 1
fi

cd "${PROJECT_ROOT}"
jetson-containers run \
  --volume "${PROJECT_ROOT}:${PROJECT_ROOT}" \
  --workdir "${PROJECT_ROOT}" \
  "$(autotag "${CONTAINER}")"
