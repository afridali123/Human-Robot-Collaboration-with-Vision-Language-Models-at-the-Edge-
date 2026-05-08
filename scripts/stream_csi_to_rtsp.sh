#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "${SCRIPT_DIR}/common.sh"
load_env

RTSP_URL="${1:-${RTSP_SERVER_URL:-rtsp://127.0.0.1:8554/camera}}"
WIDTH="${WIDTH:-${CAMERA_WIDTH:-1280}}"
HEIGHT="${HEIGHT:-${CAMERA_HEIGHT:-720}}"
FPS="${FPS:-${CAMERA_FPS:-15}}"
BITRATE="${BITRATE:-2500000}"
SENSOR_ID="${SENSOR_ID:-${CSI_SENSOR_ID:-0}}"

gst-launch-1.0 -e \
  nvarguscamerasrc sensor-id="${SENSOR_ID}" ! \
  "video/x-raw(memory:NVMM),width=${WIDTH},height=${HEIGHT},framerate=${FPS}/1" ! \
  nvv4l2h264enc insert-sps-pps=true bitrate="${BITRATE}" iframeinterval="${FPS}" ! \
  h264parse ! \
  rtspclientsink location="${RTSP_URL}"
