#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: $0 <song_query> <voice_sample_path>" >&2
  exit 1
fi

SONG_QUERY="$1"
VOICE_SAMPLE="$2"

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DEFAULT_VC_COMMAND="bash scripts/seed_vc_convert.sh --input \$input --output \$output --reference \$reference"

export SOUNDSIREN_WORKDIR="${SOUNDSIREN_WORKDIR:-$ROOT_DIR/runs}"
export SOUNDSIREN_SEED_VC_DIR="${SOUNDSIREN_SEED_VC_DIR:-$ROOT_DIR/third_party/seed-vc}"
export SOUNDSIREN_VC_BACKEND="${SOUNDSIREN_VC_BACKEND:-external}"
export SOUNDSIREN_YTDLP_COOKIES_FROM_BROWSER="${SOUNDSIREN_YTDLP_COOKIES_FROM_BROWSER:-edge}"

if [[ -z "${SOUNDSIREN_VC_COMMAND:-}" || "$SOUNDSIREN_VC_COMMAND" == *"{"* ]]; then
  export SOUNDSIREN_VC_COMMAND="$DEFAULT_VC_COMMAND"
fi

ensure_server() {
  if lsof -ti :8000 >/dev/null 2>&1; then
    echo "[SoundSiren] API already running."
    return 1
  fi

  echo "[SoundSiren] Starting API in background..."
  source "$ROOT_DIR/.venv/bin/activate"
  nohup uvicorn soundsiren.api.app:app --host 127.0.0.1 --port 8000 > "$ROOT_DIR/runs/api.log" 2>&1 &
  echo $! > "$ROOT_DIR/runs/api.pid"

  for _ in {1..30}; do
    if curl -s http://127.0.0.1:8000/health >/dev/null 2>&1; then
      echo "[SoundSiren] API is ready."
      return 0
    fi
    sleep 1
  done

  echo "[SoundSiren] API failed to start. Check runs/api.log"
  return 2
}

shutdown_server() {
  if [[ -f "$ROOT_DIR/runs/api.pid" ]]; then
    PID="$(cat "$ROOT_DIR/runs/api.pid")"
    if kill -0 "$PID" >/dev/null 2>&1; then
      kill "$PID"
      rm -f "$ROOT_DIR/runs/api.pid"
      echo "[SoundSiren] API stopped."
      return 0
    fi
  fi
  return 0
}

STARTED=0
ensure_server || STARTED=$?

curl -X POST "http://127.0.0.1:8000/v1/sing" \
  -F "song_query=${SONG_QUERY}" \
  -F "demo_seconds=30" \
  -F "voice_samples=@${VOICE_SAMPLE}"

if [[ "$STARTED" -eq 0 ]]; then
  shutdown_server
fi
