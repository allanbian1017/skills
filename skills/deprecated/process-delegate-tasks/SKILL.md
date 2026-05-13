---
name: process-delegate-tasks
description: "Automatically process URL-based tasks from the Google Tasks 'Delegate' list. Supports Threads posts (threads.net / threads.com) and YouTube videos (youtube.com / youtu.be). Fetches content, generates a Traditional Chinese summary with verbatim raw content appended, saves a Markdown report, and marks the task as completed. Use this skill whenever the user says 'process my Delegate tasks', 'run my delegate workflow', 'summarize my task list', 'check my task list', or any request involving clearing the Delegate list — even if Threads or YouTube are not explicitly mentioned."
allowed-tools: Bash(gws:*, agent-browser:*, docker:*)
---

# process-delegate-tasks

Automate the full lifecycle of every URL-based task in the "Delegate" list:

1. Pick up the task from Google Tasks
2. Detect the URL type (Threads post or YouTube video)
3. Fetch or transcribe the content
4. Summarize in Traditional Chinese with the raw content appended verbatim
5. Save a report
6. Mark the task done

**Two URL types are handled:**
| URL Type | Trigger | Processing |
|---|---|---|
| Threads post | `threads.net` or `threads.com` | `fetch-threads-post` skill → synchronous |
| YouTube video | `youtube.com` or `youtu.be` | `yt2doc` Docker → background (async) |

**DO NOT STOP after processing a single task.** This skill clears the entire backlog. The workflow is idempotent — skipping tasks already completed or lacking a supported URL ensures safe re-runs.

## Prerequisites

- `gws` CLI installed and authenticated (`gws auth login` if needed)
- `agent-browser` installed (for Threads tasks)
- Docker running (for YouTube tasks) — verify with `docker info`
- For all Google Tasks API calls, refer to `../gws-tasks/SKILL.md`

---

## Procedure

### Step 1 — Discover the "Delegate" task list

The list ID can change, so always resolve it by name:

```bash
gws tasks tasklists list
```

Parse the JSON and find the item where `title == "Delegate"`. Extract its `id`. If the list doesn't exist, stop and tell the user.

### Step 2 — Fetch incomplete tasks

```bash
gws tasks tasks list \
  --params '{"tasklist": "<DELEGATE_LIST_ID>", "showCompleted": false, "maxResults": 100}'
```

This returns only tasks with `status == "needsAction"`. If `items` is empty or missing, the list is clear — tell the user.

### Step 3 — Classify each task

For each task, scan these fields for a URL: `title`, `links[].link`, `links[].description`, `notes`.

| URL contains | Task type | Action |
|---|---|---|
| `threads.net` or `threads.com` | **Threads task** | Queue for Threads flow |
| `youtube.com` or `youtu.be` | **YouTube task** | Queue for YouTube flow |
| Neither | **Unrecognised** | Skip — log: `"Skipping '<title>': no supported URL"` |

Extract the first matching URL from each task. Build two separate queues: `threads_queue` and `youtube_queue`.

---

## Async Strategy

Because YouTube transcription takes 5–80 minutes, use a **fire-and-poll** approach:

1. **Fire** — launch all YouTube background jobs first (Step 4Y)
2. **Process** — immediately handle all Threads tasks synchronously (Steps 4T–7T)
3. **Poll** — once Threads tasks are done, poll each YouTube job until complete (Steps 5Y–7Y)

This means a 45-minute video never blocks five Threads tasks from finishing.

---

## Threads Flow (Steps 4T–7T)

### Step 4T — Fetch the Threads post content

For each task in `threads_queue`, follow the full procedure defined in `fetch-threads-post`:

> 📄 Read and follow `.agents/skills/fetch-threads-post/SKILL.md`

Use a unique session name per task to avoid state collisions:

```bash
agent-browser --session delegate-task-<task-id> open "<THREADS_URL>"
# ... follow fetch-threads-post procedure to expand and extract content ...
agent-browser --session delegate-task-<task-id> close
```

**CRITICAL**: Ensure the post is fully expanded (click "Read more") and captured entirely. Truncated raw content is unacceptable.
1. **Scroll first**: Run `agent-browser --session delegate-task-<task-id> scroll down 1000` to trigger lazy-loading and move past overlays.
2. **Extract body**: Use `agent-browser --session delegate-task-<task-id> get text body` as the primary extraction method for the `📄 原始內容` section.

### Step 5T — Verify and generate a Traditional Chinese summary

**Verification first**: Compare extracted text length against the visible post. If the raw content appears cut off mid-sentence, repeat extraction with `get text body`.

Produce a summary in **Traditional Chinese (繁體中文)**:
- **零幻覺（Zero Hallucination）**: Only summarize what is in the post. No inference or extrapolation.
- **全面性（Comprehensiveness）**: Include all key points — don't drop information for brevity.
- **客觀性（Objectivity）**: Neutral tone, no personal commentary.

### Step 6T — Save the Threads report

Output directory: `reports/Threads_YYYY_MM_DD/` (today's date).

**Filename**: Derived from author handle + topic. Strip invalid path characters (`/`, `?`, `=`, `&`, spaces → `_`).

```
@cooljerrett + topic "AI productivity" → cooljerrett_AI_productivity.md
```

Write the report using the **Threads 報告格式** defined in `assets/output_template.md`.

> 🎯 **產生「AI 分析」區塊前，必須遵照 `assets/output_template.md` 中的指示**讀取 `data/goals.md` 與 `data/user_preferences.md`（若存在）。

Confirm the file is written before proceeding.

### Step 6Tb — Append suggestion to pending backlog

Append the AI analysis suggestion from this report to `data/suggestions_pending.md`:

```markdown
---

### YYYY-MM-DD | Threads | [@{handle} — {topic}]({threads_url})
- 🏷️ {分類} | 💎 {價值評分} | ⚡ {可行動性} | 🎯 {決策建議}
- 📋 建議：{建議下一步}
- 📄 [報告](file:///absolute/path/to/report.md)
```

If `data/suggestions_pending.md` doesn't exist, create it with the `# 📋 Pending Suggestions` heading first.

### Step 7T — Mark the Threads task as completed

```bash
gws tasks tasks patch \
  --params '{"tasklist": "<DELEGATE_LIST_ID>", "task": "<TASK_ID>"}' \
  --json '{"status": "completed"}'
```

Log: `"✅ Task '<title>' marked as completed. Report saved to reports/Threads_YYYY_MM_DD/<filename>.md"`

---

## YouTube Flow (Steps 4Y–7Y)

### Step 4Y — Launch YouTube background job

For each task in `youtube_queue`, apply the **Video Strategist** from `yt2doc`:

> 📄 Read the Video Strategist table in `.agents/skills/yt2doc/SKILL.md` (Step 2)

| Video Duration | Whisper Model | Est. Time | Min Docker RAM |
|---|---|---|---|
| < 30 min | `medium` | 5–10 min | 4 GB |
| 30–60 min | `small` | 10–20 min | 6 GB |
| 1–2 hours | `small` | 35–55 min | 8 GB |
| > 2 hours | `base` | 50–80 min | 10 GB |

If duration is unknown, look it up via web search or `yt-dlp --print duration_string`. Default to the conservative path when uncertain.

Create the output directory and launch in the background (use `run_command` with `WaitMsBeforeAsync=5000`, then poll with `command_status`):

```bash
mkdir -p reports/YouTube_YYYY_MM_DD

docker run --rm \
  -v "$(pwd)/reports/YouTube_YYYY_MM_DD:/output" \
  ghcr.io/shun-liang/yt2doc \
  --video "<YouTube URL>" \
  --output /output/<video_id>.md \
  --whisper-model <model> \
  --add-table-of-contents
```

Tell the user what's happening:
> "Launching yt2doc for `<url>` using the `<model>` model (~X–Y minutes). Running in the background while I process Threads tasks."

Store the job metadata in-memory: `{ task_id, youtube_url, command_id, output_path, model }`.

**Docker not running?** Skip this task with a warning: `"⚠️ Skipping YouTube task '<title>': Docker is not running."` Continue with remaining tasks.

### Step 5Y — Poll for YouTube job completion

After all Threads tasks are done, poll each YouTube `command_id`:

```
command_status(command_id, WaitDurationSeconds=60)  # repeat until DONE
```

While polling, periodically report elapsed time to the user:
> "Still transcribing `<title>`… (N minutes elapsed)."

On completion, check the exit code:
- **Exit code 0** → proceed to Step 6Y
- **Exit code 137 (OOM)** → report: `"⚠️ Task '<title>' FAILED: Docker ran out of memory. Increase Docker RAM: Docker Desktop → Settings → Resources → Advanced → Memory (8 GB minimum, 12 GB recommended)."` Do **not** mark the task as done.
- **Other non-zero** → show last 20 lines of stderr. Do **not** mark the task as done.

### Step 6Y — Generate the YouTube report

Once the yt2doc output file is confirmed non-empty:

1. Read the full transcript file content
2. Extract: video title (first `#` heading), chapter count, approximate character count
3. Generate a Traditional Chinese summary from the transcript content following the same quality rules as the Threads flow (Zero Hallucination, Comprehensiveness, Objectivity)
4. Write the report using the **YouTube 影片報告格式** defined in `assets/output_template.md`.

> 🎯 **產生「AI 分析」區塊前，必須遵照 `assets/output_template.md` 中的指示**讀取 `data/goals.md` 與 `data/user_preferences.md`（若存在）。

Confirm the file is written before proceeding.

### Step 6Yb — Append suggestion to pending backlog

Append the AI analysis suggestion from this report to `data/suggestions_pending.md`:

```markdown
---

### YYYY-MM-DD | YouTube | [{Video Title}]({youtube_url})
- 🏷️ {分類} | 💎 {價值評分} | ⚡ {可行動性} | 🎯 {決策建議}
- 📋 建議：{建議下一步}
- 📄 [報告](file:///absolute/path/to/report.md)
```

If `data/suggestions_pending.md` doesn't exist, create it with the `# 📋 Pending Suggestions` heading first.

### Step 7Y — Mark the YouTube task as completed and cleanup

```bash
# Mark as completed
gws tasks tasks patch \
  --params '{"tasklist": "<DELEGATE_LIST_ID>", "task": "<TASK_ID>"}' \
  --json '{"status": "completed"}'

# Remove the intermediate raw transcription file (already included in the final report)
rm "/Users/allanbian/my-ai-workflow/reports/YouTube_YYYY_MM_DD/<video_id>.md"
```

Log: `"✅ Task '<title>' marked as completed. Report saved to reports/YouTube_YYYY_MM_DD/<filename>.md. Intermediate file removed."`

---

## Step 8 — Final Summary

After all queues are processed, output a unified summary:

```
Processed X Threads task(s):
  ✅ @handle1 — topic → reports/Threads_2026_04_29/filename1.md
  ✅ @handle2 — topic → reports/Threads_2026_04_29/filename2.md

Processed Y YouTube task(s):
  ✅ Video Title → reports/YouTube_2026_04_29/video_id.md
  ⚠️ Another Video → FAILED (OOM — increase Docker RAM to 8 GB)

Skipped Z task(s) (no supported URL):
  — "Buy groceries"
  — "Call dentist"
```

## Step 9 — Ephemeral Cleanup

Once the entire backlog is cleared, delete all temporary diagnostic files created during the session:
- Screenshots (`*.png`)
- Temporary scratch files or ID lists (`*.txt`, `*.json` generated for the task)
- Any debug logs outside `reports/`

Log: `"🧹 Session cleanup complete: removed temporary diagnostic files."`

---

## Troubleshooting

**Task list not found**: Run `gws tasks tasklists list` and confirm "Delegate" exists.

**Threads URL behind login wall**: Follow the authenticated access section in `fetch-threads-post/SKILL.md`.

**`gws tasks tasks patch` fails**: Double-check `tasklist` and `task` are IDs (not titles). The task ID comes from the `id` field in the `tasks list` response.

**YouTube — Exit code 137 (OOM)**: Increase Docker RAM: *Docker Desktop → Settings → Resources → Advanced → Memory* (8 GB minimum, 12 GB recommended). Retry with `--whisper-model base` if RAM is still constrained.

**YouTube — `LLMModelNotSpecified` error**: Do NOT use `--segment-unchaptered` unless you also have a local Ollama running. Remove that flag.

**YouTube — `ChunkedEncodingError`**: Network interruption during model download — retry the same command; it resumes from cache.

**URL contains `&` in shell**: Always wrap URLs in quotes.

---

## Anti-Truncation Standard (Threads)

1. **Click "Read more"** if visible.
2. **Scroll down mandatory**: Always run `scroll down 1000` before extraction to trigger lazy-loading of long posts and masked content.
3. **Use `get text body`**: Always use `get text body` as the primary extraction method to capture content behind modals or overlays.
4. **Manual check**: A complete post usually ends with a footer, signature, or engagement metrics. If the text ends abruptly, it is likely truncated.
5. **No summarization of Raw Content**: The `📄 原始內容` section **MUST** contain verbatim extraction — never summarize or omit parts.
