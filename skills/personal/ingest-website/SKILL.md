---
name: ingest-website
description: "Fetch a generic website URL and produce a summary report in the configured output language (defaulting to English) using the Jina Reader API, then mark the Google Task as completed. Use when the user provides a website URL to process, says 'ingest this article', 'summarize this page', 'process this website', or when invoked by daily-workflow for tasks in the Delegate list that are not Threads or YouTube URLs. Triggers include any http/https URL that is not threads.net, threads.com, youtube.com, or youtu.be."
---

# ingest-website

Full lifecycle for a single website task: fetch via Jina Reader → summarise → write report → append suggestion → mark done.

> **Prerequisites**: Network access to `r.jina.ai`. For Google Tasks API calls, refer to `../gws-tasks/SKILL.md`.

---

## Procedure

### Step 1 — Fetch the website content

Prepend `https://r.jina.ai/` to the target URL and fetch using `read_url_content`:

```
https://r.jina.ai/<TARGET_URL>
```

**If Jina Reader fails** (empty response, HTTP error, or clearly broken content):

> 📄 Fall back to the `content-cleaner` skill to perform a direct HTTP fetch with AI text extraction.

If both fail, log the error and skip — do NOT mark the task as completed:

```
⚠️ Skipping '<title>': fetch failed (Jina + content-cleaner both failed).
```

### Step 2 — Generate a summary in the configured output language

> 📄 Read `../content-summary/references/summarise.md`

### Step 3 — Write the report

> 📄 Read `../content-summary/references/filename_rules.md`

Directory: `reports/Website_YYYY_MM_DD/`  
Filename: `[domain]_[slugified_title].md` (hostname without `www.`, then slugified page title)

> 📄 Read `../content-summary/references/output_template.md`

**Website-specific fields** under `## 🔖 來源 Metadata`:
- **Domain/Host**: the hostname of the URL (e.g. `martinfowler.com`)
- **原文連結**: the full original URL
- **抓取日期**: today's date (YYYY-MM-DD)

**Omit `## 📄 原始內容`** entirely — do not include the raw Jina Markdown in the report.

Confirm the file is written before proceeding.

### Step 4 — Append suggestion to pending backlog

> 📄 Read `../content-summary/references/ai_analysis.md`

> 📄 Follow `../content-summary/references/suggestion_log.md`

`{SourceType}` = `Website`

### Step 5 — Mark the task as completed

```bash
gws tasks tasks patch \
  --params '{"tasklist": "<DELEGATE_LIST_ID>", "task": "<TASK_ID>"}' \
  --json '{"status": "completed"}'
```

Log: `"✅ Task '<title>' marked as completed. Report saved to reports/Website_YYYY_MM_DD/<filename>.md"`

---

## Troubleshooting

**Jina returns empty or garbled content**: Dynamic React/SPA sites may not render well. Fall back to `content-cleaner` and proceed with whatever text is extracted.

**`gws tasks tasks patch` fails**: Double-check `tasklist` and `task` are IDs (not titles).
