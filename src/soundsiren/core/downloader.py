from __future__ import annotations

import os
import time
from pathlib import Path
import subprocess


def download_song(query: str, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    if Path(query).expanduser().exists():
        return Path(query).expanduser().resolve()
    is_url = query.startswith("http://") or query.startswith("https://")
    target = query if is_url else f"ytsearch1:{query}"

    output_template = out_dir / "song.%(ext)s"
    cmd = [
        "yt-dlp",
        "-x",
        "--audio-format",
        "wav",
        "-o",
        str(output_template),
    ]
    cookies_from_browser = os.getenv("SOUNDSIREN_YTDLP_COOKIES_FROM_BROWSER")
    if cookies_from_browser:
        cmd.extend(["--cookies-from-browser", cookies_from_browser])
    cookies_file = os.getenv("SOUNDSIREN_YTDLP_COOKIES")
    if cookies_file:
        cmd.extend(["--cookies", cookies_file])
    cmd.append(target)
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as exc:
        message = exc.stderr.strip() if exc.stderr else "yt-dlp failed"
        raise RuntimeError(message) from exc

    candidates = list(out_dir.glob("song.*"))
    if not candidates:
        raise FileNotFoundError("yt-dlp completed but no output file was found")
    latest = max(candidates, key=lambda p: p.stat().st_mtime)
    time.sleep(0.1)
    return latest
