---
name: ingest-threads
description: "Fetch a Threads post and produce a summary report in the configured output language (defaulting to English), then mark the Google Task as completed. Use when the user provides a Threads URL to process, says 'process this Threads post', or when invoked by daily-workflow for tasks in the Delegate list."
allowed-tools: Bash(gws:*, agent-browser:*)
---

# ingest-threads

Full lifecycle for a single Threads task: fetch → summarise → write report → append suggestion → mark done.

> **Prerequisites**: `agent-browser` installed. For Google Tasks API calls, refer to `../gws-tasks/SKILL.md`.

---

## Procedure

### Step 1 — Fetch the Threads post content

Follow the full procedure defined in `fetch-threads-post`:

> 📄 Read and follow `../fetch-threads-post/SKILL.md`

Use a unique session name per task to avoid state collisions:

```bash
agent-browser --session ingest-threads-<task-id> open "<THREADS_URL>"
# ... follow fetch-threads-post procedure to expand and extract content ...
agent-browser --session ingest-threads-<task-id> close
```

**Anti-Truncation Standard**:
1. Click "Read more" if visible.
2. Run `agent-browser --session ... scroll down 1000` to trigger lazy-loading.
3. Use `agent-browser --session ... get text body` as the primary extraction method.
4. A complete post ends with a footer, signature, or engagement metrics. Truncated = retry.
5. The `📄 原始內容` section MUST contain verbatim extraction — never summarize.

### Step 2 — Verify and generate a summary in the configured output language

**Verification**: Compare extracted text length against the visible post. If cut off, repeat extraction.

> 📄 Read `../content-summary/references/summarise.md`

### Step 3 — Write the report

> 📄 Read `../content-summary/references/filename_rules.md`

> 📄 Read `../content-summary/references/output_template.md`

Confirm the file is written before proceeding.

### Step 4 — Append suggestion to pending backlog

> 📄 Read `../content-summary/references/ai_analysis.md`

> 📄 Follow `../content-summary/references/suggestion_log.md`

`{SourceType}` = `Threads`

### Step 5 — Mark the task as completed

```bash
gws tasks tasks patch \
  --params '{"tasklist": "<DELEGATE_LIST_ID>", "task": "<TASK_ID>"}' \
  --json '{"status": "completed"}'
```

Log: `"✅ Task '<title>' marked as completed. Report saved to reports/Threads_YYYY_MM_DD/<filename>.md"`

---

## Troubleshooting

**Threads URL behind login wall**: Follow the authenticated access section in `fetch-threads-post/SKILL.md`.

**`gws tasks tasks patch` fails**: Double-check `tasklist` and `task` are IDs (not titles).
