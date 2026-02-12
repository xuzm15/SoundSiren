# SoundSiren

SoundSiren: Zero-Shot Neural Vocal Morphing

English README. 中文说明请见 `README_CN.md`。

SoundSiren is an end-to-end system that turns everyday speech into high-fidelity singing. By disentangling vocal identity and melody, it enables zero-shot singing conversion from short speech samples.

## Key Features
- Zero-shot identity extraction from short speech samples
- End-to-end pipeline: search, separation, pitch conditioning, synthesis, rendering
- LLM-driven orchestration (planned)
- Minimal API interface

## Project Layout
- `src/soundsiren/` core logic
- `src/soundsiren/api/` API entrypoint
- `src/soundsiren/core/` pipeline modules
- `web/` prototype console UI
- `tests/` test placeholders

## Quick Start
```bash
# System dependencies
brew install ffmpeg

# Bootstrap (clone Seed-VC + install deps)
./scripts/bootstrap.sh

# If macOS + Python 3.13 fails SciPy, use Python 3.11:
# brew install python@3.11
# SOUNDSIREN_PYTHON=python3.11 ./scripts/bootstrap.sh

# Run API
./scripts/run_demo.sh

# Demo request (default 30s)
./scripts/request_demo.sh "Song Name or URL" /path/to/your_voice.wav

# Or use a local song file to bypass download limits
./scripts/request_demo.sh /path/to/song.wav /path/to/your_voice.wav
```

## Configuration
```bash
export SOUNDSIREN_WORKDIR=./runs
export SOUNDSIREN_SEED_VC_DIR=/path/to/seed-vc
export SOUNDSIREN_VC_BACKEND=external
export SOUNDSIREN_VC_COMMAND="bash scripts/seed_vc_convert.sh --input $input --output $output --reference $reference"

# Optional denoise (enabled by default)
export SOUNDSIREN_DENOISE=1
export SOUNDSIREN_DENOISE_NF=-25

# Optional yt-dlp cookies
export SOUNDSIREN_YTDLP_COOKIES=/path/to/youtube_cookies.txt
export SOUNDSIREN_YTDLP_COOKIES_FROM_BROWSER=edge
```

## Notes
- Current pipeline includes download, separation, and mixdown. Voice conversion is invoked externally.
- If VC is not configured, the system will mix original vocals (for pipeline smoke test only).
- `song_query` can be a local audio path to bypass download restrictions.
- Default request is a 30s demo. Use `demo_seconds` to override.

## Seed-VC
1. Clone Seed-VC and install its dependencies
2. Set `SOUNDSIREN_SEED_VC_DIR`
3. Enable `SOUNDSIREN_VC_COMMAND`

## Important
- First run downloads model weights from Hugging Face.
- Full-song conversion is compute-heavy.

## Roadmap
See `ROADMAP.md`.

## Docs
- Design draft: `DESIGN.md`
