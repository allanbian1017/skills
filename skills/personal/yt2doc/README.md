# yt2doc Skill

An Antigravity skill that transcribes and organizes YouTube videos into clean, structured Markdown documents — hands-free.

## Overview

`yt2doc` wraps the [`yt2doc`](https://github.com/shun-liang/yt2doc) CLI tool to give you a fully automated pipeline from YouTube URL → readable Markdown. It downloads the video audio, transcribes it with [Whisper](https://github.com/openai/whisper), segments the content into chapters or topics, and saves the result as a structured `.md` file.

Because transcription is CPU-bound, the process time scales with video length — a 30-minute talk takes ~10 minutes; a 2-hour lecture can take 40–55 minutes. The skill automatically selects the right Whisper model for the video length (see **Video Strategist** below) and runs the job in the background, polling every 60 seconds — you don't need to babysit it.

## Features

- **Zero setup beyond uv/Python** — no API keys or complex Whisper install required (just `uv tool install yt2doc`)
- **Automatic chapter segmentation** — uses chapters from YouTube metadata if present
- **Video Strategist** — automatically selects the optimal Whisper model (`base` / `small` / `medium`) based on video duration and local RAM constraints
- **Table of contents** — auto-generated TOC at the top of every document
- **Organized output** — files saved to `./reports/YouTube_YYYY_MM_DD/` with `snake_case` filenames
- **Long-run safe** — the agent polls every 60 seconds and reports progress; won't time out on lengthy videos
- **Playlist support** — can process an entire YouTube playlist with a single command

## Prerequisites

| Requirement | Notes |
|---|---|
| Local yt2doc CLI | Install with `uv tool install yt2doc` |
| Internet access | Required to download audio and AI models |
| Local RAM (≥ 4 GB for short, ≥ 8 GB for long videos) | Ensure enough free system memory |

The AI models are downloaded automatically on first use.

> **⚠️ OOM Risk:** For videos longer than 1 hour, your machine must have at least **8 GB of free RAM**. Without this, the process may be killed mid-transcription and no output is saved.

## Usage

Trigger the skill naturally in chat — just mention a YouTube URL alongside a transcription intent.

### Example Prompts

**Transcribe a single video:**
> "Transcribe this YouTube video for me: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`"

**Save organized notes from a talk:**
> "Turn this conference talk into a document I can read: `https://youtu.be/abc123`"

**Get a video's content without watching it:**
> "Extract the content from this YouTube video and save it to a Markdown file."

**With timestamps:**
> "Transcribe this video and include timestamps on each paragraph."

**Full playlist:**
> "Organize all videos in this YouTube playlist into documents: `https://www.youtube.com/playlist?list=PL...`"

## Output

The skill saves a Markdown file to `./reports/YouTube_YYYY_MM_DD/<filename>.md`. The agent will **not** paste the full transcript into chat — instead it reports a summary:

```
✅ Done! Saved to ./reports/YouTube_2026_04_28/building_better_agents.md
Title: Building Better Agents
Sections: 8 chapters
~3,200 words
```

### Document structure

```markdown
# [Video Title]

## Table of Contents
- [Introduction](#introduction)
- [Chapter 1: ...](#chapter-1)
- [Chapter 2: ...](#chapter-2)

## Introduction
<transcribed content...>

## Chapter 1: ...
<transcribed content...>
```

## Key Options

| Flag | Default | Description |
|---|---|---|
| `--add-table-of-contents` | off | Adds a TOC (always enabled by this skill) |
| `--whisper-model` | none | Model size — selected automatically by the Video Strategist |
| `--timestamp-paragraphs` | off | Prepends timestamps to each paragraph |
| `--segment-unchaptered` | off | ⚠️ Requires `--llm-model` + `--llm-server` (local Ollama). **Not used by default.** |
| `--playlist` | — | Use instead of `--video` for playlist URLs |

### Video Strategist — Automatic Model Selection

The skill picks the Whisper model and sets time expectations automatically:

| Video Duration | Whisper Model | Est. Transcription Time | Min Local RAM |
|---|---|---|---|
| < 30 min | `medium` | 5–10 min | 4 GB |
| 30–60 min | `small` | 10–20 min | 6 GB |
| 1–2 hours | `small` | 35–55 min | 8 GB |
| > 2 hours | `base` | 50–80 min | 10 GB |

## Troubleshooting

| Problem | Solution |
|---|---|
| `yt2doc` not found | Install via `uv tool install yt2doc` |
| Video is private or unavailable | Verify the URL is publicly accessible |
| `LLMModelNotSpecified` error | You ran `--segment-unchaptered` without an LLM. Remove that flag — it's not enabled by default |
| `ChunkedEncodingError` (HuggingFace) | Network interruption during model download. Retry — it will resume from cache |
| `DownloadError: downloaded file is empty` | YouTube rate-limiting or stale signature. Wait a few minutes and retry |
| Non-zero exit code (other) | The agent will show you the last 20 lines of stderr for diagnosis |

## How It Works Internally

```
YouTube URL
    │
    ▼
yt-dlp (audio download)
    │
    ▼
Whisper (speech-to-text via faster-whisper)
    │
    ▼
SAT model (sentence boundary detection / topic segmentation)
    │
    ▼
Structured Markdown → ./reports/YouTube_YYYY_MM_DD/<filename>.md
```

The local yt2doc CLI handles all of this end-to-end. The Antigravity agent runs the command and saves the output directly to your local `reports/` directory.

## Files

```
yt2doc/
├── SKILL.md   — Agent instructions (read by Antigravity at runtime)
└── README.md  — This file
```

---

## Changelog

### v3.0.0 — 2026-05-14

**Switch to Local CLI Execution**

Migrated from Docker-based execution to using the local `yt2doc` CLI tool. This resolves bot detection issues caused by the containerized `yt-dlp` lacking browser cookies, and bypasses missing package dependencies (`torchvision`) in the previous Docker image.

### v2.0.0 — 2026-04-29

**Video Strategist Integration**

Merged adaptive model selection directly into the skill, eliminating the need to manually specify `--whisper-model` for each run. The skill now auto-selects the Whisper model based on the video's estimated duration and communicates realistic time expectations upfront.

**Changes:**
- ➕ Added **Video Strategist** decision table: duration → model → time estimate → min RAM
- ➕ Added proactive Docker RAM warning for long videos (OOM prevention)
- ➕ Added `--whisper-model` as an explicit required flag in the run command (model chosen by Video Strategist)
- ⚠️ Removed `--segment-unchaptered` from the default command — this flag throws `LLMModelNotSpecified` unless a local LLM (Ollama) is running with `--llm-model` and `--llm-server` configured
- ➕ Expanded error handling with four new documented cases:
  - Exit Code 137 (OOM)
  - `LLMModelNotSpecified`
  - `ChunkedEncodingError` from HuggingFace
  - `DownloadError: downloaded file is empty`
- 📊 Updated time estimates with real-world benchmark data (1h50m Chinese lecture, `small` model, CPU-only, 8 GB Docker RAM → ~45 min)

### v1.0.0 — 2026-04-28

**Initial release.** Basic yt2doc wrapper with background polling, TOC generation, and chapter segmentation support.
