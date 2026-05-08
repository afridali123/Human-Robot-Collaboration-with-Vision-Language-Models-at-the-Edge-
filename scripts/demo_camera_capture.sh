#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "${SCRIPT_DIR}/common.sh"
load_env

cd "${PROJECT_ROOT}"

python3 app/camera_capture.py \
  --camera "${CAMERA_INDEX:-0}" \
  --output "${CAPTURE_IMAGE:-images/capture.jpg}" \
  --width "${CAMERA_WIDTH:-1280}" \
  --height "${CAMERA_HEIGHT:-720}" \
  "${@}"
