from __future__ import annotations

import shlex
import subprocess
from pathlib import Path
from string import Template

from soundsiren.config import Settings


def convert_vocals(
    vocal_path: Path,
    reference_path: Path | None,
    out_dir: Path,
    settings: Settings,
) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    if settings.vc_backend == "none":
        return vocal_path

    if settings.vc_backend != "external":
        raise ValueError(f"Unsupported vc backend: {settings.vc_backend}")

    if not settings.vc_command:
        raise ValueError("SOUNDSIREN_VC_COMMAND is required for external backend")
    if not reference_path:
        raise ValueError("Voice conversion requires a reference sample")

    output_path = out_dir / "vocals_converted.wav"
    template = Template(settings.vc_command)
    command = template.safe_substitute(
        input=str(vocal_path),
        output=str(output_path),
        model=settings.vc_model or "",
        reference=str(reference_path),
    )
    if command.strip() == settings.vc_command.strip():
        command = (
            f"{settings.vc_command} --input {vocal_path} "
            f"--output {output_path} --reference {reference_path}"
        )
    cmd = shlex.split(command)
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as exc:
        detail = (exc.stderr or exc.stdout or "voice conversion failed").strip()
        raise RuntimeError(detail) from exc
    if not output_path.exists():
        raise FileNotFoundError("Voice conversion command did not produce output")
    return output_path
