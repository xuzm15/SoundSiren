from __future__ import annotations

from pathlib import Path
import subprocess

from soundsiren.core.tasks import StemAssets


def separate_stems(audio_path: Path, out_dir: Path) -> StemAssets:
    out_dir.mkdir(parents=True, exist_ok=True)
    cmd = [
        "python",
        "-m",
        "demucs",
        "--two-stems",
        "vocals",
        "-o",
        str(out_dir),
        str(audio_path),
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as exc:
        message = exc.stderr.strip() if exc.stderr else "demucs failed"
        raise RuntimeError(message) from exc

    candidates = list(out_dir.glob(f"*/{audio_path.stem}"))
    if not candidates:
        raise FileNotFoundError("Demucs output directory not found")
    model_dir = candidates[0]
    vocals = model_dir / "vocals.wav"
    accompaniment = model_dir / "no_vocals.wav"
    if not vocals.exists() or not accompaniment.exists():
        raise FileNotFoundError("Demucs output missing expected stems")
    return StemAssets(vocal=str(vocals), accompaniment=str(accompaniment))
