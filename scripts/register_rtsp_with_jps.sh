#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "${SCRIPT_DIR}/common.sh"
load_env

cd "${PROJECT_ROOT}"

python3 scripts/jps_vlm_demo.py add-stream \
  --api "${JPS_API:-http://127.0.0.1:5010}" \
  --rtsp "${RTSP_PUBLIC_URL:-rtsp://127.0.0.1:8554/camera}"
