#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "${SCRIPT_DIR}/common.sh"
load_env

DEVICE="${1:-${USB_CAMERA_DEVICE:-/dev/video0}}"
RTSP_URL="${2:-${RTSP_SERVER_URL:-rtsp://127.0.0.1:8554/camera}}"
WIDTH="${WIDTH:-${CAMERA_WIDTH:-1280}}"
HEIGHT="${HEIGHT:-${CAMERA_HEIGHT:-720}}"
FPS="${FPS:-${CAMERA_FPS:-15}}"
BITRATE="${BITRATE:-2500}"

gst-launch-1.0 -e \
  v4l2src device="${DEVICE}" ! \
  "video/x-raw,width=${WIDTH},height=${HEIGHT},framerate=${FPS}/1" ! \
  videoconvert ! \
  x264enc tune=zerolatency bitrate="${BITRATE}" speed-preset=ultrafast key-int-max="${FPS}" ! \
  rtspclientsink location="${RTSP_URL}"
