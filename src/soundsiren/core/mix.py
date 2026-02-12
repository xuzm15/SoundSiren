from __future__ import annotations

import subprocess
from pathlib import Path


def mixdown(
    vocals: Path,
    accompaniment: Path,
    out_path: Path,
    *,
    vocal_gain_db: float = 6.0,
    accompaniment_gain_db: float = -3.0,
) -> Path:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    filter_complex = (
        f"[0:a]volume={vocal_gain_db}dB[a0];"
        f"[1:a]volume={accompaniment_gain_db}dB[a1];"
        "[a0][a1]amix=inputs=2:duration=longest:dropout_transition=2,"
        "loudnorm=I=-14:TP=-2:LRA=11"
    )
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(vocals),
        "-i",
        str(accompaniment),
        "-filter_complex",
        filter_complex,
        str(out_path),
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as exc:
        message = exc.stderr.strip() if exc.stderr else "ffmpeg mixdown failed"
        raise RuntimeError(message) from exc
    if not out_path.exists():
        raise FileNotFoundError("Mixdown failed to produce output")
    return out_path
