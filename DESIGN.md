# SoundSiren Design Draft (Updated Vision)

Goal: expose the complex speech‑to‑singing pipeline behind a minimal interface so creators get “input‑to‑output” simplicity.

> 中文版本见 `DESIGN_CN.md`

---

## 1. Product Definition
- One‑liner: SoundSiren is a zero‑shot speech‑to‑singing system that generates singing with the user’s vocal identity from short speech samples.
- Target users:
  - Creators: quick demos with their own vocal identity
  - AIGC tool builders: need high‑level, composable voice conversion
  - Researchers: voice identity transfer, melody control, expressiveness

## 2. Core Promises
- Zero‑shot identity extraction from short speech
- End‑to‑end pipeline: retrieval, separation, pitch control, synthesis, rendering
- LLM orchestration (planned)
- Minimal API/CLI surface

## 3. Current Implementation (MVP)
### 3.1 What’s implemented
- Local or retrieved song input (`song_query` can be a local path)
- Source separation (Demucs)
- Singing voice conversion (Seed‑VC via external command)
- Mixdown (FFmpeg)
- Demo mode: default 30‑second generation
- Light denoise: vocals, accompaniment, converted vocals

### 3.2 Known constraints
- YouTube downloads may require cookies
- Local inference can be slow for full songs
- Seed‑VC may produce “electronic vibrato” artifacts, needs tuning

## 4. UX Flow
1. Upload 3–30s speech
2. Provide song name/link (or local file) + optional style/emotion
3. System runs retrieval → separation → conversion → mix
4. Output demo/full song audio

Surfaces:
- API (primary)
- CLI (primary)
- Web console (demo)

## 5. System Architecture (Current)
```
Input Speech + Song Query
        |
   [Song Retrieval] -> (optional cookies)
        |
   [Source Separation (Demucs)]
        |
   [Seed‑VC Conversion]
        |
   [Denoise + Mixdown]
        |
   Output Audio
```

## 6. API (Current)
`POST /v1/sing`
- input:
  - `voice_samples[]` (audio)
  - `song_query` (string or local path)
  - `demo_seconds` (optional, default=30)
  - `output_format` (optional)
- output:
  - `job_id`
  - `preview_url`
  - `output_path`

`GET /v1/jobs/{id}`
- output:
  - `status`
  - `result_urls[]`
  - `metadata`

## 7. MVP Quality Targets
- Voice similarity: acceptable subjective match
- Melody preservation: keep original singing contour
- Naturalness: reduce electronic vibrato/whine
- Demo latency: 2–8 min on local machine

## 8. Risks & Mitigations
- Copyright: support local input and cookie‑based downloads
- Sample quality: recommend clean, close‑mic speech
- Latency: demo‑first, full songs require more compute

## 9. Milestones
- M0: MVP demo pipeline complete
- M1: voice similarity improvements (F0 smoothing / denoise / tuning)
- M2: LLM orchestration, multi‑version outputs
- M3: Web console + multilingual UI

---
Next: decide long‑term roadmap (true zero‑shot SVS vs SVC‑based conversion).
