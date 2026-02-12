#!/usr/bin/env bash
set -euo pipefail

if [[ -z "${SOUNDSIREN_SEED_VC_DIR:-}" ]]; then
  echo "SOUNDSIREN_SEED_VC_DIR is required (path to seed-vc repo)." >&2
  exit 1
fi
SEED_VC_DIR="$(cd "$SOUNDSIREN_SEED_VC_DIR" && pwd)"

INPUT=""
OUTPUT=""
REFERENCE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --input)
      INPUT="$2"
      shift 2
      ;;
    --output)
      OUTPUT="$2"
      shift 2
      ;;
    --reference)
      REFERENCE="$2"
      shift 2
      ;;
    *)
      echo "Unknown arg: $1" >&2
      exit 1
      ;;
  esac
done

if [[ -z "$INPUT" || -z "$OUTPUT" || -z "$REFERENCE" ]]; then
  echo "Usage: $0 --input in.wav --output out.wav --reference ref.wav" >&2
  exit 1
fi

TMP_DIR="$(mktemp -d)"
LOG_FILE="$TMP_DIR/seed_vc.log"

set +e
cd "$SEED_VC_DIR"
python "$SEED_VC_DIR/inference.py" \
  --source "$INPUT" \
  --target "$REFERENCE" \
  --output "$TMP_DIR" \
  --diffusion-steps 30 \
  --inference-cfg-rate 0.7 \
  --length-adjust 0.97 \
  --f0-condition True \
  --auto-f0-adjust False \
  --semi-tone-shift 0 >"$LOG_FILE" 2>&1
STATUS=$?
set -e

if [[ "$STATUS" -ne 0 ]]; then
  echo "Seed-VC failed (exit $STATUS). Log:" >&2
  tail -n 80 "$LOG_FILE" >&2
  exit "$STATUS"
fi

OUT_FILE="$(ls -t "$TMP_DIR"/*.wav | head -n 1)"
if [[ -z "$OUT_FILE" ]]; then
  echo "Seed-VC did not produce output wav." >&2
  exit 1
fi

mkdir -p "$(dirname "$OUTPUT")"
mv "$OUT_FILE" "$OUTPUT"
rm -rf "$TMP_DIR"
