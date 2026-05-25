---
name: daily-workflow
description: "Chains the full content intelligence pipeline in optimal order: discover Delegate tasks, fire YouTube background jobs, process newsletters, process Threads tasks, complete YouTube tasks, run daily distillation, review suggestions. Use when the user says 'run my daily workflow', 'run daily', 'start my daily routine', or any request to run all content processing tasks in sequence."
allowed-tools: Bash(gws:*, yt2doc, agent-browser:*)
---

# daily-workflow

Orchestrates the full content intelligence pipeline. Maximises throughput by firing slow async jobs first, then handling fast sync tasks, then collecting async results.

> **Prerequisites**: `gws` CLI, `agent-browser`, `yt2doc`. Refer to `../gws-shared/SKILL.md` for auth.

---

## Procedure

### Step 1 — Discover and classify Delegate tasks

```bash
gws tasks tasklists list
```

Find the item where `title == "Delegate"`. Extract its `id`. If not found, skip Steps 2–5.

```bash
gws tasks tasks list \
  --params '{"tasklist": "<DELEGATE_LIST_ID>", "showCompleted": false, "maxResults": 100}'
```

For each task, scan `title`, `links[].link`, `links[].description`, `notes` for a URL:

| URL contains | Queue |
|---|---|
| `threads.net` or `threads.com` | `threads_queue` |
| `youtube.com` or `youtu.be` | `youtube_queue` |
| Any other `http`/`https` URL | `website_queue` |
| No URL found | Skip — log: `"Skipping '<title>': no URL found"` |

### Step 2 — Fire YouTube background jobs

For each task in `youtube_queue`:

> 📄 Read `../ingest-youtube/SKILL.md` §Step 1 (Video Strategist) to determine model

```bash
mkdir -p reports/YouTube_YYYY_MM_DD

yt2doc \
  --video "<YouTube URL>" \
  --output ./reports/YouTube_YYYY_MM_DD/<video_id>.md \
  --whisper-model <model> \
  --add-table-of-contents
```

Use `run_command` with `WaitMsBeforeAsync=5000`. Store: `{ task_id, youtube_url, command_id, output_path, model }`.

Tell the user what's happening: `"Launching yt2doc for <url> (~X–Y min). Running in background while I process other tasks."`

### Step 3 — Process newsletters

> 📄 Follow `../ingest-newsletter/SKILL.md`

(Full lifecycle: fetch → summarise → write report → append suggestion → mark read)

### Step 4 — Process Threads tasks

For each task in `threads_queue`:

> 📄 Follow `../ingest-threads/SKILL.md`

(Full lifecycle: fetch → summarise → write report → append suggestion → mark task done)

### Step 4W — Process Website tasks

For each task in `website_queue`:

> 📄 Follow `../ingest-website/SKILL.md`

(Full lifecycle: fetch via Jina Reader → summarise → write report → append suggestion → mark task done)

Log soft failures: `"⚠️ Skipping '<title>': fetch failed (Jina + content-cleaner both failed)."`

### Step 5 — Complete YouTube tasks

For each YouTube background job (from Step 2):

1. Poll: `command_status(command_id, WaitDurationSeconds=60)` — repeat until DONE. Report elapsed time periodically.
2. On exit code != 0, handle per `../ingest-youtube/SKILL.md` §Step 3 error handling. Do NOT mark task done.
3. Read transcript file.
4. Generate summary:
   > 📄 Read `../content-summary/references/summarise.md`
5. Write report:
   > 📄 Read `../content-summary/references/filename_rules.md`
   > 📄 Read `../content-summary/references/output_template.md`
6. Append suggestion:
   > 📄 Read `../content-summary/references/ai_analysis.md`
   > 📄 Follow `../content-summary/references/suggestion_log.md`
   (`{SourceType}` = `YouTube`)
7. Mark task done + cleanup:
   ```bash
   gws tasks tasks patch \
     --params '{"tasklist": "<DELEGATE_LIST_ID>", "task": "<TASK_ID>"}' \
     --json '{"status": "completed"}'
   rm "reports/YouTube_YYYY_MM_DD/<video_id>.md"
   ```

### Step 6 — Distill

> 📄 Follow `../daily-distiller/SKILL.md`

### Step 7 — Review suggestions

> 📄 Follow `../review-suggestions/SKILL.md`

### Final Summary

```
Processed N newsletter(s) → reports/Newsletter_YYYY_MM_DD/
Processed T Threads task(s):
  ✅ @handle — topic → reports/Threads_YYYY_MM_DD/filename.md
Processed W Website task(s):
  ✅ example.com — Article Title → reports/Website_YYYY_MM_DD/filename.md
  ⚠️ another.com — Article Title → FAILED (Jina + content-cleaner both failed)
Processed Y YouTube task(s):
  ✅ Video Title → reports/YouTube_YYYY_MM_DD/filename.md
  ⚠️ Another Video → FAILED (OOM — increase system RAM)
Skipped Z task(s) (no URL found).
Distillation complete. Suggestions reviewed.
```
