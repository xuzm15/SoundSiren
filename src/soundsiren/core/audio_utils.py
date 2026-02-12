from __future__ import annotations

import subprocess
from pathlib import Path


def trim_audio(input_path: Path, output_path: Path, seconds: int) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(input_path),
        "-t",
        str(seconds),
        str(output_path),
    ]
    subprocess.run(cmd, check=True, capture_output=True, text=True)
    if not output_path.exists():
        raise FileNotFoundError("Trim did not produce output")
    return output_path


def denoise_audio(input_path: Path, output_path: Path, *, noise_floor_db: str) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(input_path),
        "-af",
        f"afftdn=nf={noise_floor_db},highpass=f=80,lowpass=f=12000",
        str(output_path),
    ]
    subprocess.run(cmd, check=True, capture_output=True, text=True)
    if not output_path.exists():
        raise FileNotFoundError("Denoise did not produce output")
    return output_path
