---
name: daily-workflow
description: "Chains the full content intelligence pipeline in optimal order: discover Delegate tasks, dispatch all content items as parallel full-lifecycle subagents, collect results, merge suggestions, run daily distillation, review suggestions. Use when the user says 'run my daily workflow', 'run daily', 'start my daily routine', or any request to run all content processing tasks in sequence."
allowed-tools: Bash(gws:*, yt2doc, agent-browser:*)
---

# daily-workflow

Orchestrates the full content intelligence pipeline by discovering pending items, dispatching parallel worker subagents, merging AI suggestions, and triggering daily distillation and review.

> **Prerequisites**: `gws` CLI, `agent-browser`, `yt2doc`. Refer to `../gws-shared/SKILL.md` for auth.
> **Dispatch Spec & Schemas**: See [dispatch_spec.md](references/dispatch_spec.md) for classification rules, prompt templates, and output formats.

---

## Orchestration Pipeline

```
[1. Discover & Classify] ──> [2. Pre-create Directories] ──> [3. Parallel Dispatch]
                                                                     │
[6. Review Suggestions] <── [5. Distill Knowledge] <── [4. Collect & Merge]
```

---

### Step 1 — Discover and Classify Items

1. Discover Google Task `Delegate` list:
   ```bash
   gws tasks tasklists list
   ```
   Extract `DELEGATE_LIST_ID` for list matching `title == "Delegate"`. List pending tasks:
   ```bash
   gws tasks tasks list --params '{"tasklist": "<DELEGATE_LIST_ID>", "showCompleted": false, "maxResults": 100}'
   ```
   Classify each task into `threads_queue`, `youtube_queue`, or `website_queue` based on URL matching rules in [dispatch_spec.md](references/dispatch_spec.md).

2. Discover unread newsletters via Gmail API:
   ```bash
   gws gmail users messages list --params '{"userId": "me", "q": "label:newsletter is:unread", "maxResults": 1}'
   ```
   Check `resultSizeEstimate` for unread newsletter count.

3. **Early exit**: If all queues are empty and no unread newsletters exist, log `"No content to process today."` and exit.

---

### Step 2 — Pre-create Directories

Create date-stamped output directories for non-empty queues and the suggestion staging area:
```bash
mkdir -p data/suggestions_pending
# Pre-create reports/<Type>_YYYY_MM_DD/ for active queues only (Newsletter, Threads, Website, YouTube)
```

---

### Step 3 — Dispatch Parallel Subagents

Dispatch all content items concurrently in fire-and-forget mode. Do not block on individual completions.

- **Newsletters**: Fetch email IDs in batches of 10 (`q: "label:newsletter is:unread"`). Spawn subagent for each `MESSAGE_ID` scoped to `ingest-newsletter`.
- **Threads / Website / YouTube**: For each item in `threads_queue`, `website_queue`, and `youtube_queue`, spawn a subagent scoped to `ingest-threads`, `ingest-website`, or `ingest-youtube`.

Refer to [dispatch_spec.md](references/dispatch_spec.md) for prompt parameter templates and tracking specs.

---

### Step 4 — Collect Results & Merge Suggestions

1. **Synchronization Barrier**:
   Set a 30-minute global timeout timer via `schedule`:
   ```
   schedule(DurationSeconds=1800, Prompt="30-minute timeout reached. Proceed with completed subagent results.", TimerCondition="never")
   ```
   Wait for subagents to complete (reactive notification — no polling loop needed). Proceed when all complete or timeout fires.

2. **Merge Suggestions**:
   For each file matching `data/suggestions_pending/suggestion_*.json`:
   - Read suggestion entry and append to `data/suggestions_pending.md`.
   - Remove processed pending JSON file.

---

### Step 5 — Distill Knowledge

Follow `../daily-distiller/SKILL.md` to synthesize today's reports in `reports/distillations/`.

---

### Step 6 — Review Suggestions

Follow `../review-suggestions/SKILL.md` to review pending AI suggestions.

---

### Step 7 — Final Summary

Print final summary adhering to the output format in [dispatch_spec.md](references/dispatch_spec.md).
