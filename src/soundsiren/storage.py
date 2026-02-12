from __future__ import annotations

from pathlib import Path
from typing import Iterable

from fastapi import UploadFile


def save_uploads(files: Iterable[UploadFile], out_dir: Path) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    saved: list[Path] = []
    for idx, file in enumerate(files):
        suffix = Path(file.filename or f"sample_{idx}").suffix or ".wav"
        path = out_dir / f"sample_{idx}{suffix}"
        with path.open("wb") as f:
            f.write(file.file.read())
        saved.append(path)
    return saved
