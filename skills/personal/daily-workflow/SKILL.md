---
name: daily-workflow
description: "Chains the full content intelligence pipeline in optimal order: discover Delegate tasks, dispatch all content items as parallel full-lifecycle subagents, collect results, merge suggestions, run daily distillation, review suggestions. Use when the user says 'run my daily workflow', 'run daily', 'start my daily routine', or any request to run all content processing tasks in sequence."
allowed-tools: Bash(gws:*, yt2doc, agent-browser:*)
---

# daily-workflow

Orchestrates the full content intelligence pipeline. Dispatches each content item as an independent full-lifecycle subagent, then waits for all to complete before distillation.

> **Prerequisites**: `gws` CLI, `agent-browser`, `yt2doc`. Refer to `../gws-shared/SKILL.md` for auth.

---

## Procedure

### Step 1 — Discover and classify Delegate tasks

```bash
gws tasks tasklists list
```

Find the item where `title == "Delegate"`. Extract its `id` as `DELEGATE_LIST_ID`. If not found, skip Steps 2–7.

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

Also fetch the count of unread newsletters:

```bash
gws gmail users messages list \
  --params '{"userId": "me", "q": "label:newsletter is:unread", "maxResults": 1}'
```

Use `resultSizeEstimate` to determine whether any newsletters exist.

**Early exit**: If all queues are empty and no unread newsletters exist, skip Steps 2–7 and report: `"No content to process today."` Exit.

---

### Step 2 — Pre-create report directories

Create date-stamped report directories **only for content types that have items**, plus the suggestion staging area:

```bash
mkdir -p data/suggestions_pending

# Create only directories for non-empty queues:
# mkdir -p reports/Newsletter_YYYY_MM_DD   ← if unread newsletters exist
# mkdir -p reports/Threads_YYYY_MM_DD      ← if threads_queue is non-empty
# mkdir -p reports/Website_YYYY_MM_DD      ← if website_queue is non-empty
# mkdir -p reports/YouTube_YYYY_MM_DD      ← if youtube_queue is non-empty
```

Pre-creating directories prevents race conditions when multiple subagents write to the same directory simultaneously.

---

### Step 3 — Dispatch all content items in parallel

Spawn all subagents immediately (fire-and-forget). Do **not** wait for any individual subagent to finish before dispatching the next.

#### 3a — Newsletter subagents

Fetch unread newsletter email IDs in batches of 10:

```bash
gws gmail users messages list \
  --params '{"userId": "me", "q": "label:newsletter is:unread", "maxResults": 10}'
```

For each `MESSAGE_ID` in the batch, spawn a **focused subagent** scoped to `ingest-newsletter`:

**Subagent prompt template:**
```
Follow the ingest-newsletter skill at .agents/skills/ingest-newsletter/SKILL.md.

MESSAGE_ID: <MESSAGE_ID>
SuggestionOutputPath: data/suggestions_pending/suggestion_newsletter_<MESSAGE_ID>.json
Report directory: reports/Newsletter_YYYY_MM_DD/

Skip Step 1 (batch discovery) — process only this single email.
Pass SuggestionOutputPath through to suggestion_log.md.
```

If `nextPageToken` is present in the response, fetch the next batch and dispatch those as well. Repeat until all unread newsletters are dispatched.

Track each spawned subagent: `{ message_id, subagent_id, suggestion_path }`.

#### 3b — Threads subagents

For each task in `threads_queue`, spawn a **focused subagent** scoped to `ingest-threads`:

**Subagent prompt template:**
```
Follow the ingest-threads skill at .agents/skills/ingest-threads/SKILL.md.

THREADS_URL: <URL>
TASK_ID: <TASK_ID>
DELEGATE_LIST_ID: <DELEGATE_LIST_ID>
SuggestionOutputPath: data/suggestions_pending/suggestion_threads_<TASK_ID>.json
Report directory: reports/Threads_YYYY_MM_DD/

Pass SuggestionOutputPath through to suggestion_log.md.
```

Track each spawned subagent: `{ task_id, url, subagent_id, suggestion_path }`.

#### 3c — Website subagents

For each task in `website_queue`, spawn a **focused subagent** scoped to `ingest-website`:

**Subagent prompt template:**
```
Follow the ingest-website skill at .agents/skills/ingest-website/SKILL.md.

WEBSITE_URL: <URL>
TASK_ID: <TASK_ID>
DELEGATE_LIST_ID: <DELEGATE_LIST_ID>
SuggestionOutputPath: data/suggestions_pending/suggestion_website_<TASK_ID>.json
Report directory: reports/Website_YYYY_MM_DD/

Pass SuggestionOutputPath through to suggestion_log.md.
```

Track each spawned subagent: `{ task_id, url, subagent_id, suggestion_path }`.

#### 3d — YouTube subagents

For each task in `youtube_queue`, spawn a **focused subagent** scoped to `ingest-youtube`:

**Subagent prompt template:**
```
Follow the ingest-youtube skill at .agents/skills/ingest-youtube/SKILL.md.

YOUTUBE_URL: <URL>
TASK_ID: <TASK_ID>
DELEGATE_LIST_ID: <DELEGATE_LIST_ID>
SuggestionOutputPath: data/suggestions_pending/suggestion_youtube_<TASK_ID>.json
Report directory: reports/YouTube_YYYY_MM_DD/

Pass SuggestionOutputPath through to suggestion_log.md.
```

Track each spawned subagent: `{ task_id, url, subagent_id, suggestion_path }`.

---

### Step 4 — Collect all results

Wait for all spawned subagents to complete. The system automatically notifies the orchestrator when each subagent finishes — **no polling loop needed**.

Set a **30-minute global timeout** via the `schedule` tool after all subagents are dispatched:

```
schedule(DurationSeconds=1800, Prompt="30-minute timeout reached. Proceed with completed subagent results. Report any still-running subagents as timed out.", TimerCondition="never")
```

If the timeout fires before all subagents finish:
- Proceed with results from completed subagents.
- Report timed-out subagents as failures in the Final Summary.

For each completed subagent, record: `success/failure`, `report path`, `error message if any`.

---

### Step 4M — Merge suggestions

Read all files matching `data/suggestions_pending/suggestion_*.json`.

For each file:
1. Read the suggestion entry.
2. Append it to `data/suggestions_pending.md` (following `suggestion_log.md` format).
3. Delete the pending file after successful append.

If `data/suggestions_pending/` is empty, skip this step.

---

### Step 5 — (Removed — replaced by parallel dispatch in Step 3)

Steps 2–5 of the old sequential model have been replaced by Steps 2–4M above.

---

### Step 6 — Distill

> 📄 Follow `../daily-distiller/SKILL.md`

### Step 7 — Review suggestions

> 📄 Follow `../review-suggestions/SKILL.md`

### Final Summary

```
Dispatched N items total (N newsletter(s), T Threads, W website(s), Y YouTube).
Completed: <success_count> | Failed: <failed_count> | Timed out: <timeout_count>

Newsletter(s): reports/Newsletter_YYYY_MM_DD/
Threads:
  ✅ @handle — topic → reports/Threads_YYYY_MM_DD/filename.md
  ⚠️ @handle — FAILED (reason)
Website(s):
  ✅ example.com — Article Title → reports/Website_YYYY_MM_DD/filename.md
  ⚠️ another.com — FAILED (Jina + content-cleaner both failed)
YouTube:
  ✅ Video Title → reports/YouTube_YYYY_MM_DD/filename.md
  ⚠️ Another Video — FAILED (OOM)
Skipped Z task(s) (no URL found).
Suggestions merged: <count> pending → data/suggestions_pending.md
Distillation complete. Suggestions reviewed.
```
