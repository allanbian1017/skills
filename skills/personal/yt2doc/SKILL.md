---
name: yt2doc
description: Transcribe and organize a YouTube video into a structured Markdown document using the local yt2doc CLI tool. Use this skill whenever the user provides a YouTube URL and asks to transcribe, summarize, organize, extract content from, or document a video. Triggers include phrases like "transcribe this video", "get the content of this YouTube video", "convert YouTube to text", "organize this video", "extract transcript from YouTube", "turn this video into a document", or any request involving a youtube.com or youtu.be URL where the goal is to get readable content from the video. Always prefer this skill over manual browser-based approaches when a YouTube URL is provided.
---

# yt2doc Skill

This skill converts a YouTube video into a clean, structured Markdown document using the local `yt2doc` CLI tool. The process downloads audio, runs transcription via Whisper, and segments the content into chapters.

## Prerequisites

- `yt2doc` must be installed locally (e.g., via `uv tool install yt2doc`)
- Internet access for downloading video audio and AI models
- Sufficient local RAM for Whisper models

## Step-by-Step Instructions

### 1. Confirm the URL and set up output path

Extract the YouTube URL from the user's message. Derive a `snake_case` filename from the video URL (you can use the video ID or a short descriptive name). Decide the output directory:

- Default: `./reports/YouTube_YYYY_MM_DD/` (use today's date)
- If the user specifies a directory, use that instead

Create the output directory before running the command:
```bash
mkdir -p ./reports/YouTube_YYYY_MM_DD
```

### 2. Video Strategist — Select the Right Model

Before running, apply this decision table. If the duration is unknown, look it up (e.g., via web search or `yt-dlp --print duration_string`). Default to the conservative path when uncertain.

| Video Duration | Whisper Model | Est. Transcription Time | Min Local RAM |
|---|---|---|---|
| < 30 min | `medium` (default) | 5–10 min | 4 GB |
| 30–60 min | `small` | 10–20 min | 6 GB |
| 1–2 hours | `small` | 35–55 min | 8 GB |
| > 2 hours | `base` | 50–80 min | 10 GB |

> **⚠️ RAM Warning:** If the host machine does not have enough memory, the transcription process may be killed. Ensure you have enough free memory before running large models on long videos.

### 3. Tell the user what's happening

Before starting, let the user know the selected model and expected time:
> "Starting yt2doc on `<url>`. Using the `<model>` model — this should take approximately **X–Y minutes**. I'll run it in the background and report back."

### 4. Run yt2doc in the background

Use `run_command` with a generous `WaitMsBeforeAsync` (5000ms is fine), then poll with `command_status` until done.

```bash
yt2doc \
  --video "<YouTube URL>" \
  --output ./reports/YouTube_YYYY_MM_DD/<filename>.md \
  --whisper-model <model> \
  --add-table-of-contents
```

**Key flags:**
- `--whisper-model <model>` — set per the Video Strategist table above (e.g., `small`, `medium`, `base`)
- `--output ./reports/...` — saves result to the correct directory
- `--add-table-of-contents` — adds a TOC at the top of the document (recommended)
- `--timestamp-paragraphs` — optionally include timestamps per paragraph (add if user asks)

> **⚠️ Do NOT use `--segment-unchaptered`** unless you also have a local LLM running (e.g., Ollama) and pass `--llm-model` and `--llm-server`. This flag requires a connected LLM server and will throw `LLMModelNotSpecified` if omitted.

### 5. Poll for completion

The command can run for a long time. Use `command_status` with `WaitDurationSeconds: 60` in a loop — check every 60 seconds until the status is `DONE`.

While waiting, let the user know you're still monitoring:
> "Still running… (N minutes elapsed). I'll update you when it finishes."

```
command_status(id, WaitDurationSeconds=60)  # repeat until status == "DONE"
```

If the exit code is non-zero, report the error output to the user clearly.

### 6. Verify and report

Once done:
1. Check the output file exists and is non-empty
2. Read the first ~50 lines to confirm the document looks correct
3. Report to the user:
   - ✅ Path to the saved file
   - Title detected (usually the first `#` heading)
   - Number of sections/chapters found
   - Approximate word/character count (optional)

**Example report:**
> ✅ Done! Saved to `./reports/YouTube_2026_04_29/lVdajtNpaGI.md`
> **Title**: 【生成式人工智慧導論2025】第2講：上下文工程
> **Sections**: 2 chapters
> **~18,000 characters**

## Error Handling

| Situation | What to do |
|-----------|-----------|
| `yt2doc` not found | Tell the user to install it via `uv tool install yt2doc` |
| Video is private / unavailable | Report the yt-dlp error; suggest the user check the URL |
| `LLMModelNotSpecified` error | Remove `--segment-unchaptered`; it requires `--llm-model` and `--llm-server` to be set |
| `ChunkedEncodingError` from HuggingFace | Network interruption during model download — retry the same command, it will resume from cache |
| `DownloadError: downloaded file is empty` | YouTube rate-limiting or signature issue — wait a few minutes and retry |
| Exit code non-zero (other) | Show the last 20 lines of stderr to the user |

## Output Format

The generated Markdown file will look like:

```markdown
# [Video Title]

## Table of Contents
- [Chapter 1](#chapter-1)
- [Chapter 2](#chapter-2)

## Chapter 1
<transcribed content...>

## Chapter 2
<transcribed content...>
```

Do **not** paste the entire document into the chat. Just report the file path and key metadata.

## Notes

- The AI models are pulled on first run (can take extra time if not cached)
- `yt2doc` uses `faster-whisper` by default — no GPU needed, but CPU transcription is slow for long videos
- For a ~2 hour Chinese lecture, the `small` model takes ~40–50 minutes on CPU with 8 GB RAM
- `--segment-unchaptered` uses SAT (Segment Any Text) + LLM for topic detection; only works with a local Ollama setup
- For playlists, use `--playlist <url>` instead of `--video`
