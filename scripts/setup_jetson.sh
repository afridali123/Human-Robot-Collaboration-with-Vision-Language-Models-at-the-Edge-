#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "${SCRIPT_DIR}/common.sh"
load_env

cd "${PROJECT_ROOT}"

print_step "Preparing environment file"
if [[ ! -f .env ]]; then
  cp .env.example .env
  echo "Created .env from .env.example"
fi

print_step "Checking Jetson platform"
if is_jetson; then
  cat /etc/nv_tegra_release || true
else
  echo "Warning: /etc/nv_tegra_release not found. This script is intended for Jetson Linux."
fi

print_step "Installing host packages"
sudo apt update
sudo apt install -y \
  git curl wget ca-certificates gnupg lsb-release \
  python3-pip python3-venv python3-dev python3-opencv \
  htop nano v4l-utils ffmpeg gstreamer1.0-tools \
  gstreamer1.0-plugins-base gstreamer1.0-plugins-good \
  gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly

if ! command -v docker >/dev/null 2>&1; then
  sudo apt install -y docker.io
fi

if ! docker compose version >/dev/null 2>&1; then
  sudo apt install -y docker-compose-plugin || sudo apt install -y docker-compose
fi

print_step "Configuring user groups"
sudo usermod -aG docker,video "${USER}" || true

print_step "Setting max performance mode"
if [[ "${JETSON_SET_MAX_PERF:-true}" == "true" ]] && is_jetson; then
  sudo nvpmodel -m 0 || true
  sudo jetson_clocks || true
fi

print_step "Installing jetson-containers"
JETSON_CONTAINERS_DIR="${JETSON_CONTAINERS_DIR:-$HOME/jetson-containers}"
if [[ ! -d "${JETSON_CONTAINERS_DIR}/.git" ]]; then
  git clone https://github.com/dusty-nv/jetson-containers.git "${JETSON_CONTAINERS_DIR}"
else
  git -C "${JETSON_CONTAINERS_DIR}" pull --ff-only || true
fi
bash "${JETSON_CONTAINERS_DIR}/install.sh"

print_step "Creating local Python virtual environment"
python3 -m venv --system-site-packages .venv
# shellcheck disable=SC1091
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt

print_step "Making scripts executable"
chmod +x scripts/*.sh

print_step "Setup complete"
echo "Log out and back in if Docker access fails, because group membership changed."
echo "Next: ./scripts/doctor.sh"
