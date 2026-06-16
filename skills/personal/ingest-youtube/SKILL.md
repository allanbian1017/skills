---
name: ingest-youtube
description: "Transcribe a YouTube video using yt2doc CLI and produce a summary report in the configured output language (defaulting to English), then mark the Google Task as completed. Use when the user provides a YouTube URL to transcribe, says 'transcribe this YouTube video', 'get the content of this YouTube video', or any request involving a youtube.com or youtu.be URL where the goal is readable content. Always prefer this skill over manual browser-based approaches."
allowed-tools: Bash(gws:*)
---

# ingest-youtube

Full lifecycle for a single YouTube task: launch transcription → poll → summarise → write report → append suggestion → mark done.

> **Prerequisites**: `yt2doc` must be installed locally. For Google Tasks API calls, refer to `../gws-tasks/SKILL.md`.

---

## Procedure

### Step 1 — Determine Whisper model (Video Strategist)

| Video Duration | Whisper Model | Est. Time | Min Local RAM |
|---|---|---|---|
| < 30 min | `medium` | 5–10 min | 4 GB |
| 30–60 min | `small` | 10–20 min | 6 GB |
| 1–2 hours | `small` | 35–55 min | 8 GB |
| > 2 hours | `base` | 50–80 min | 10 GB |

If duration is unknown, look it up via web search or `yt-dlp --print duration_string`. Default to the conservative path when uncertain.

### Step 2 — Launch transcription

```bash
mkdir -p reports/YouTube_YYYY_MM_DD

yt2doc \
  --video "<YouTube URL>" \
  --output ./reports/YouTube_YYYY_MM_DD/<video_id>.md \
  --whisper-model <model> \
  --add-table-of-contents
```

Use `run_command` with `WaitMsBeforeAsync=5000`, then poll with `command_status`.

Tell the user: `"Launching yt2doc for <url> using the <model> model (~X–Y minutes)."`

**yt2doc not found?** Tell the user to install it via `uv tool install yt2doc`.

### Step 3 — Poll for completion

```
command_status(command_id, WaitDurationSeconds=60)  # repeat until DONE
```

Periodically report elapsed time: `"Still transcribing <title>… (N minutes elapsed)."`

On completion, check exit code:
- **Exit 0** → proceed to Step 4
- **Exit 137 / 9 (Killed/OOM)** → report: `"⚠️ FAILED: Process was killed, likely ran out of memory. Ensure you have enough free memory (8 GB minimum, 12 GB recommended)."` Do **not** mark task done.
- **Other non-zero** → show last 20 lines of stderr. Do **not** mark task done.

### Step 4 — Generate summary

Once the output file is confirmed non-empty:

> 📄 Read `../content-summary/references/summarise.md`

Extract: video title (first `#` heading), chapter count, approximate character count. Generate summary in the configured output language.

### Step 5 — Write the report

> 📄 Read `../content-summary/references/filename_rules.md`

> 📄 Read `../content-summary/references/output_template.md`

Confirm the file is written before proceeding.

### Step 6 — Append suggestion to pending backlog

> 📄 Read `../content-summary/references/ai_analysis.md`

> 📄 Follow `../content-summary/references/suggestion_log.md`

`{SourceType}` = `YouTube`

### Step 7 — Mark the task as completed and cleanup

```bash
# Mark as completed
gws tasks tasks patch \
  --params '{"tasklist": "<DELEGATE_LIST_ID>", "task": "<TASK_ID>"}' \
  --json '{"status": "completed"}'

# Remove intermediate raw transcription file
rm "reports/YouTube_YYYY_MM_DD/<video_id>.md"
```

Log: `"✅ Task '<title>' marked as completed. Report saved to reports/YouTube_YYYY_MM_DD/<filename>.md. Intermediate file removed."`

---

## Troubleshooting

**Exit code 137 / 9 (Killed/OOM)**: Ensure you have enough free memory. Retry with `--whisper-model base` if RAM is constrained.

**`LLMModelNotSpecified` error**: Do NOT use `--segment-unchaptered` without a local Ollama running. Remove that flag.

**`ChunkedEncodingError`**: Network interruption during model download — retry; it resumes from cache.

**URL contains `&` in shell**: Always wrap URLs in quotes.
