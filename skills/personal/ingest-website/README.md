# ingest-website Skill

## Overview

The `ingest-website` skill handles the full lifecycle for a single generic website task: fetch content via Jina Reader API → generate a summary in the configured output language → write a Markdown report → append an AI analysis suggestion → mark the Google Task as completed.

It is designed to run as a standalone one-shot skill or be invoked per-task by `daily-workflow` for all tasks in the Delegate list that contain a valid HTTP/HTTPS URL that is not a Threads or YouTube link.

## Problem Statement

The daily content pipeline successfully processes newsletters, Threads posts, and YouTube videos. However, users frequently delegate generic articles, documentation pages, and technical blogs via Google Tasks. These URLs were previously skipped with `"Skipping '<title>': no supported URL"`, leaving valuable content unprocessed.

## Solution

A dedicated `ingest-website` skill that uses the `web-to-markdown` approach (Jina Reader API at `r.jina.ai`) for fast, clean Markdown extraction. Falls back to `content-cleaner` for sites where Jina fails. Raw content is omitted from reports to keep token consumption low during daily distillation.

### Key Features

1. **Jina Reader Fetch**: Prepends `https://r.jina.ai/` to the target URL — typically resolves in seconds with no JS execution required.
2. **Soft-Failure Fallback**: If Jina fails, falls back to `content-cleaner` (direct HTTP + AI extraction). If both fail, logs and skips without halting the pipeline.
3. **Shared Summarisation Rules**: Reads `content-summary/references/summarise.md` — Zero Hallucination, 7-Layer Analysis, configured output language.
4. **Structured Output**: Markdown report with domain metadata, 7-layer analysis, and no raw content section (see `../content-summary/references/output_template.md`).
5. **Separate AI Analysis Backlog**: AI suggestion appended to `data/suggestions_pending.md` with `{SourceType}` = `Website`.
6. **Full Lifecycle**: Marks the Google Task as completed after confirming the report and suggestion are written.

## File Structure

```
ingest-website/
├── SKILL.md                    # Skill definition and workflow steps
└── README.md                   # This file
```

## Dependencies

- `web-to-markdown` / Jina Reader (`r.jina.ai`) — primary content fetch mechanism.
- `content-cleaner` — fallback for sites that don't render well in Jina.
- `content-summary` — shared summarisation rules, AI analysis definitions, suggestion log format, filename rules.
- `gws-tasks` — marking the Google Task as completed via `gws tasks tasks patch`.

## Triggering

This skill triggers when the user says:
- "ingest this article"
- "summarize this page"
- "process this website"
- Provides any `http://` or `https://` URL that is not Threads or YouTube

Or when invoked per-task by `daily-workflow` (Step 4W).

## Output Location

```
reports/
└── Website_YYYY_MM_DD/
    └── {domain}_{slugified_title}.md
```

## Changelog

| Version | Date | Change Summary |
|---|---|---|
| v1.0.0 | 2026-05-25 | Initial skill: Jina Reader fetch with content-cleaner fallback, Traditional Chinese 7-layer summary, no raw content section. Integrated into daily-workflow Step 4W. |
| v1.1.0 | 2026-06-16 | Made output language globally configurable, defaulting to English and preferring Traditional Chinese. |
