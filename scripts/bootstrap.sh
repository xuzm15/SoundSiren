#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SEED_VC_DIR="${SOUNDSIREN_SEED_VC_DIR:-$ROOT_DIR/third_party/seed-vc}"

mkdir -p "$ROOT_DIR/third_party"

if [[ ! -d "$SEED_VC_DIR" ]]; then
  echo "[SoundSiren] Cloning Seed-VC into $SEED_VC_DIR"
  git clone https://github.com/Plachtaa/seed-vc.git "$SEED_VC_DIR"
else
  echo "[SoundSiren] Seed-VC already exists at $SEED_VC_DIR"
fi

PYTHON_BIN="${SOUNDSIREN_PYTHON:-}"
if [[ -z "$PYTHON_BIN" ]]; then
  if command -v python3.11 >/dev/null 2>&1; then
    PYTHON_BIN="python3.11"
  else
    PYTHON_BIN="python3"
  fi
fi

echo "[SoundSiren] Using Python: $PYTHON_BIN"
"$PYTHON_BIN" -m venv "$ROOT_DIR/.venv"
source "$ROOT_DIR/.venv/bin/activate"

pip install -U pip
pip install -e "$ROOT_DIR"
pip install yt-dlp demucs

# Seed-VC dependencies (best effort; see Seed-VC README for GPU-specific extras)
REQ_IN="$SEED_VC_DIR/requirements.txt"
REQ_TMP="$ROOT_DIR/.seed_vc_requirements.filtered.txt"

if [[ "$(uname -s)" == "Darwin" ]]; then
  echo "[SoundSiren] Detected macOS: installing torch stack separately and filtering Seed-VC requirements."
  pip install torch torchvision torchaudio
  pip install torchcodec
  # Remove CUDA nightly and torch pin lines that conflict on macOS.
  grep -v -E '^(torch|torchvision|torchaudio)(==| --pre)|^torch==|^torchvision==|^torchaudio==|^torch --pre|^torchvision --pre|^torchaudio --pre|download\.pytorch\.org/whl/nightly' "$REQ_IN" > "$REQ_TMP"
  pip install -r "$REQ_TMP"
else
  pip install -r "$REQ_IN"
fi

cat <<'EOM'

[SoundSiren] Bootstrap complete.
Next:
1) export SOUNDSIREN_SEED_VC_DIR=<path to seed-vc>
2) export SOUNDSIREN_VC_BACKEND=external
3) export SOUNDSIREN_VC_COMMAND="bash scripts/seed_vc_convert.sh --input {input} --output {output} --reference {reference}"
4) uvicorn soundsiren.api.app:app --reload
EOM
