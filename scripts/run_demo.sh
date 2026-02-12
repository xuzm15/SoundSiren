#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

if [[ -z "${SOUNDSIREN_SEED_VC_DIR:-}" ]]; then
  export SOUNDSIREN_SEED_VC_DIR="$ROOT_DIR/third_party/seed-vc"
fi

export SOUNDSIREN_WORKDIR="${SOUNDSIREN_WORKDIR:-$ROOT_DIR/runs}"
export SOUNDSIREN_VC_BACKEND="${SOUNDSIREN_VC_BACKEND:-external}"
export SOUNDSIREN_VC_COMMAND="${SOUNDSIREN_VC_COMMAND:-bash scripts/seed_vc_convert.sh --input $input --output $output --reference $reference}"

source "$ROOT_DIR/.venv/bin/activate"

uvicorn soundsiren.api.app:app --reload
