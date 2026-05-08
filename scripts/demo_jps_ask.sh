#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "${SCRIPT_DIR}/common.sh"
load_env

cd "${PROJECT_ROOT}"

PROMPT="${1:-What do you see?}"

if [[ -z "${JPS_STREAM_ID:-}" ]]; then
  echo "Set JPS_STREAM_ID in .env before running this script." >&2
  exit 1
fi

python3 scripts/jps_vlm_demo.py ask \
  --api "${JPS_API:-http://127.0.0.1:5010}" \
  --stream-id "${JPS_STREAM_ID}" \
  --prompt "${PROMPT}" \
  --action-rules actions/example_rules.json \
  --dry-run-action
