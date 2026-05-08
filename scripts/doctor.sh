#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "${SCRIPT_DIR}/common.sh"
load_env

cd "${PROJECT_ROOT}"

print_step "Project"
echo "Root: ${PROJECT_ROOT}"
test -f README.md
test -f requirements.txt

print_step "Jetson"
if is_jetson; then
  cat /etc/nv_tegra_release || true
  apt show nvidia-jetpack 2>/dev/null | sed -n '1,12p' || true
else
  echo "Not running on Jetson Linux."
fi

print_step "Power and telemetry"
if command -v nvpmodel >/dev/null 2>&1; then
  sudo nvpmodel -q || true
fi
if command -v tegrastats >/dev/null 2>&1; then
  timeout 3 tegrastats || true
else
  echo "tegrastats not found."
fi

print_step "Docker"
if command -v docker >/dev/null 2>&1; then
  docker --version
  docker info >/dev/null 2>&1 && echo "Docker daemon reachable." || echo "Docker daemon not reachable for this user."
else
  echo "Docker not found."
fi

print_step "jetson-containers"
if command -v jetson-containers >/dev/null 2>&1; then
  jetson-containers --help | sed -n '1,8p'
else
  echo "jetson-containers not found on PATH."
fi

print_step "Python"
python3 --version
python3 -m py_compile app/agent_logic.py app/camera_capture.py app/vlm_image_demo.py scripts/jps_vlm_demo.py
python3 app/agent_logic.py --text "The image contains a person near a box."

print_step "Camera"
if command -v v4l2-ctl >/dev/null 2>&1; then
  v4l2-ctl --list-devices || true
else
  echo "v4l2-ctl not found."
fi
ls /dev/video* 2>/dev/null || true

print_step "JPS VLM health"
if [[ -n "${JPS_HEALTH_URL:-}" ]]; then
  python3 scripts/jps_vlm_demo.py health --health-url "${JPS_HEALTH_URL}" || true
fi

print_step "Doctor complete"
