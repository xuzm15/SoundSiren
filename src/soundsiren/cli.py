import json
import typer

from soundsiren.config import load_settings
from soundsiren.core.pipeline import run_pipeline

app = typer.Typer(add_completion=False, help="SoundSiren CLI")


@app.command()
def sing(
    song_query: str = typer.Argument(..., help="Song name or link"),
    voice_sample: list[str] = typer.Option(
        None, "--voice", "-v", help="Path(s) to voice sample audio"
    ),
    emotion: str = typer.Option(None, "--emotion", "-e"),
    style: str = typer.Option(None, "--style", "-s"),
    output_format: str = typer.Option("wav", "--format", "-f"),
    demo_seconds: int | None = typer.Option(None, "--demo-seconds"),
) -> None:
    settings = load_settings()
    result = run_pipeline(
        song_query=song_query,
        voice_samples=voice_sample or [],
        emotion=emotion,
        style=style,
        output_format=output_format,
        demo_seconds=demo_seconds,
        settings=settings,
    )
    typer.echo(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    app()
