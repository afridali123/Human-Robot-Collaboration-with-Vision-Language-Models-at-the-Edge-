#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "${SCRIPT_DIR}/common.sh"
load_env

cd "${PROJECT_ROOT}/compose"
docker compose -f mediamtx.yml up -d
echo "RTSP server is starting. Default stream URL: ${RTSP_SERVER_URL:-rtsp://127.0.0.1:8554/camera}"
