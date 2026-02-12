from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    work_dir: Path
    vc_backend: str
    vc_command: str | None
    vc_model: str | None
    denoise_enabled: bool
    denoise_nf: str


def load_settings() -> Settings:
    work_dir = Path(os.getenv("SOUNDSIREN_WORKDIR", "runs")).resolve()
    vc_backend = os.getenv("SOUNDSIREN_VC_BACKEND", "none")
    vc_command = os.getenv("SOUNDSIREN_VC_COMMAND")
    vc_model = os.getenv("SOUNDSIREN_VC_MODEL")
    denoise_enabled = os.getenv("SOUNDSIREN_DENOISE", "1") == "1"
    denoise_nf = os.getenv("SOUNDSIREN_DENOISE_NF", "-25")
    return Settings(
        work_dir=work_dir,
        vc_backend=vc_backend,
        vc_command=vc_command,
        vc_model=vc_model,
        denoise_enabled=denoise_enabled,
        denoise_nf=denoise_nf,
    )
