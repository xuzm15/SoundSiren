from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from soundsiren.config import load_settings
from soundsiren.core.pipeline import run_pipeline
from soundsiren.storage import save_uploads

app = FastAPI(title="SoundSiren API", version="0.1.0")
settings = load_settings()
settings.work_dir.mkdir(parents=True, exist_ok=True)
app.mount("/runs", StaticFiles(directory=str(settings.work_dir)), name="runs")


class SingRequest(BaseModel):
    song_query: str = Field(..., description="Song name or link")
    emotion: str | None = Field(default=None, description="Optional emotion prompt")
    style: str | None = Field(default=None, description="Optional style prompt")
    output_format: str | None = Field(default="wav", description="Output audio format")
    demo_seconds: int | None = Field(default=None, description="Trim song to N seconds")


class SingResponse(BaseModel):
    job_id: str
    preview_url: str | None = None
    output_path: str | None = None


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/v1/sing", response_model=SingResponse)
def sing(
    song_query: str = Form(...),
    emotion: str | None = Form(default=None),
    style: str | None = Form(default=None),
    output_format: str | None = Form(default="wav"),
    demo_seconds: int | None = Form(default=None),
    voice_samples: list[UploadFile] | None = File(default=None),
) -> SingResponse:
    job_dir = settings.work_dir / "uploads"
    saved = save_uploads(voice_samples or [], job_dir)
    try:
        result = run_pipeline(
            song_query=song_query,
            voice_samples=[str(p) for p in saved],
            emotion=emotion,
            style=style,
            output_format=output_format or "wav",
            demo_seconds=demo_seconds,
            settings=settings,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    output_path = Path(result["output_path"])
    preview_url = None
    if settings.work_dir in output_path.parents:
        preview_url = f"/runs/{output_path.relative_to(settings.work_dir)}"
    return SingResponse(job_id=result["job_id"], preview_url=preview_url, output_path=result["output_path"])


@app.get("/v1/jobs/{job_id}")
def job_status(job_id: str) -> dict:
    # Placeholder: implement job tracking and result URLs.
    return {
        "job_id": job_id,
        "status": "queued",
        "result_urls": [],
        "metadata": {},
    }
