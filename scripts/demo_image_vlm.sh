#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "${SCRIPT_DIR}/common.sh"
load_env

cd "${PROJECT_ROOT}"

IMAGE="${1:-${SAMPLE_IMAGE:-images/sample.jpg}}"
PROMPT="${2:-${VLM_PROMPT:-Describe this scene for a robot assistant.}}"

python3 app/vlm_image_demo.py \
  --image "${IMAGE}" \
  --prompt "${PROMPT}" \
  --model "${HF_VLM_MODEL:-llava-hf/llava-1.5-7b-hf}" \
  --max-new-tokens "${MAX_NEW_TOKENS:-120}" \
  --show-action
