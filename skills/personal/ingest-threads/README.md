# ingest-threads Skill

## Overview

The `ingest-threads` skill handles the full lifecycle for a single Threads post task: fetch content → generate a summary in the configured output language → write a Markdown report → append an AI analysis suggestion → mark the Google Task as completed.

It is designed to run as a standalone one-shot skill or be invoked per-task by `daily-workflow` for all tasks in the Delegate list that contain a `threads.net` or `threads.com` URL.

## Problem Statement

Processing a Threads post involves multiple steps across two tools (`agent-browser` and `gws`) with strict content extraction requirements to prevent truncation. Previously this logic was embedded inside `process-delegate-tasks` alongside YouTube transcription, mixing fast synchronous tasks with slow async ones and making the skill harder to invoke independently.

## Solution

Extracted the Threads processing path into its own focused skill. Uses `fetch-threads-post` as a sub-skill for content extraction and `content-summary` references for all shared summarisation and analysis logic.

### Key Features

1. **Anti-Truncation Standard:** Mandatory scroll-before-extract, `get text body` as primary method, and a verbatim raw content section that must never be summarised.
2. **Shared Summarisation Rules:** Reads `content-summary/references/summarise.md` — Zero Hallucination, Comprehensiveness, Objectivity.
3. **Structured Output:** Markdown report with source metadata, executive summary, key highlights, action items, disclaimers, and verbatim raw content (see `../content-summary/references/output_template.md`).
4. **Separate AI Analysis Backlog:** AI analysis is appended to `data/suggestions_pending.md`, not written to the report.
5. **Full Lifecycle:** Marks the Google Task as completed after confirming the report and suggestion are written.

## File Structure

```
ingest-threads/
├── SKILL.md                    # Skill definition and workflow steps
├── README.md                   # This file
└── assets/
    └── output_template.md      # Threads-specific Markdown report template
```

## Dependencies

- `fetch-threads-post` — browser-based extraction of Threads post content.
- `content-summary` — shared summarisation rules, AI analysis definitions, suggestion log format, filename rules.
- `gws-tasks` — marking the Google Task as completed via `gws tasks tasks patch`.

## Triggering

This skill triggers when the user says:
- "process this Threads post"
- "fetch this Threads URL"
- Provides a `threads.net` or `threads.com` URL to process

Or when invoked per-task by `daily-workflow` (Step 4).

## Output Location

```
reports/
└── Threads_YYYY_MM_DD/
    └── {handle}_{topic}.md
```

## Changelog

| Version | Date | Change Summary |
|---|---|---|
| v1.0.0 | 2026-05-13 | Initial skill: extracted from `process-delegate-tasks` Steps 4T–7T. Uses `content-summary` references for summarise/analysis/suggestion. |
| v1.1.0 | 2026-05-14 | Unified output template moved to `content-summary/references/output_template.md`. |
| v1.2.0 | 2026-06-16 | Made output language globally configurable, defaulting to English and preferring Traditional Chinese. |
