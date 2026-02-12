from __future__ import annotations

from pathlib import Path
import uuid

from soundsiren.config import Settings
from soundsiren.core.audio_utils import trim_audio, denoise_audio
from soundsiren.core.downloader import download_song
from soundsiren.core.separation import separate_stems
from soundsiren.core.voice_conversion import convert_vocals
from soundsiren.core.mix import mixdown
from soundsiren.core.tasks import IdentityEmbedding


def run_pipeline(
    *,
    song_query: str,
    voice_samples: list[str],
    emotion: str | None,
    style: str | None,
    output_format: str,
    demo_seconds: int | None,
    settings: Settings,
) -> dict:
    job_id = uuid.uuid4().hex
    job_dir = settings.work_dir / job_id
    input_dir = job_dir / "inputs"
    output_dir = job_dir / "outputs"

    song_audio = download_song(song_query, input_dir / "song")
    if demo_seconds:
        song_audio = trim_audio(
            Path(song_audio),
            input_dir / f"song_{demo_seconds}s.wav",
            seconds=demo_seconds,
        )

    # Placeholder: future identity embedding from voice samples.
    identity = IdentityEmbedding(vector_id="identity_placeholder")

    stems = separate_stems(song_audio, job_dir / "stems")
    reference_path = None
    if voice_samples:
        reference_path = trim_audio(
            Path(voice_samples[0]),
            job_dir / "inputs" / "reference_30s.wav",
            seconds=30,
        )
    vocals_path = Path(stems.vocal)
    accompaniment_path = Path(stems.accompaniment)
    if settings.denoise_enabled:
        vocals_path = denoise_audio(
            vocals_path,
            job_dir / "stems" / "vocals_denoised.wav",
            noise_floor_db=settings.denoise_nf,
        )
        accompaniment_path = denoise_audio(
            accompaniment_path,
            job_dir / "stems" / "accomp_denoised.wav",
            noise_floor_db=settings.denoise_nf,
        )
    converted_vocals = convert_vocals(
        vocals_path,
        reference_path,
        job_dir / "vc",
        settings,
    )
    if settings.denoise_enabled:
        converted_vocals = denoise_audio(
            converted_vocals,
            job_dir / "vc" / "vocals_converted_denoised.wav",
            noise_floor_db=settings.denoise_nf,
        )
    mixed = mixdown(
        vocals=converted_vocals,
        accompaniment=accompaniment_path,
        out_path=output_dir / f"mixdown.{output_format}",
    )

    return {
        "job_id": job_id,
        "status": "completed",
        "identity": identity.vector_id,
        "output_path": str(mixed),
        "emotion": emotion,
        "style": style,
    }
