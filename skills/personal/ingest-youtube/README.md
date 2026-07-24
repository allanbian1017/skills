# ingest-youtube Skill

## Overview

The `ingest-youtube` skill handles the full lifecycle for a single YouTube video task: launch `yt2doc` CLI transcription → poll until complete → generate a summary in the configured output language → write a Markdown report → append an AI analysis suggestion → mark the Google Task as completed.

It is designed to run as a standalone one-shot skill or be dispatched by `daily-workflow` as a **focused parallel subagent** that owns its full lifecycle independently.

## Problem Statement

YouTube transcription takes 5–80 minutes depending on video length. Previously this was embedded inside `process-delegate-tasks` alongside fast Threads tasks, requiring the orchestrator to manage async polling while also running synchronous work — all in one monolithic skill. Standalone invocation was awkward.

## Solution

Extracted the YouTube processing path into its own focused skill with a clear Video Strategist table for model selection. When used standalone or dispatched as a parallel subagent, the skill runs fully synchronously — it launches `yt2doc`, polls for completion, and handles all post-processing itself.

### Key Features

1. **Video Strategist:** Selects the optimal Whisper model based on video duration, balancing accuracy and RAM requirements.
2. **Full-Lifecycle Subagent:** Runs entirely independently when dispatched by `daily-workflow`. Owns transcription, polling, summarisation, suggestion, and mark-done — no orchestrator post-processing needed.
3. **Error Handling:** Exit code 137 (OOM) produces a clear remediation message. Non-zero exits surface the last 20 lines of stderr. Neither marks the task as done.
4. **Shared Summarisation Rules:** Reads `content-summary/references/summarise.md` — Zero Hallucination, Comprehensiveness, Objectivity.
5. **Structured Output:** Markdown report with source metadata, executive summary, key highlights, and full verbatim transcript (see `../content-summary/references/output_template.md`).
6. **Separate AI Analysis Backlog:** AI analysis is appended to `data/suggestions_pending.md`, not written to the report.
7. **Full Lifecycle:** Marks the Google Task as completed and removes the intermediate raw transcription file after confirming the report is written.

## File Structure

```
ingest-youtube/
├── SKILL.md                    # Skill definition and workflow steps
├── README.md                   # This file
└── assets/
    └── output_template.md      # YouTube-specific Markdown report template
```

## Video Strategist (Model Selection)

| Video Duration | Whisper Model | Est. Time | Min Local RAM |
|---|---|---|---|
| < 30 min | `medium` | 5–10 min | 4 GB |
| 30–60 min | `small` | 10–20 min | 6 GB |
| 1–2 hours | `small` | 35–55 min | 8 GB |
| > 2 hours | `base` | 50–80 min | 10 GB |

## Dependencies

- `yt2doc` CLI tool (installed locally) — transcription engine.
- `content-summary` — shared summarisation rules, AI analysis definitions, suggestion log format, filename rules.
- `gws-tasks` — marking the Google Task as completed via `gws tasks tasks patch`.

## Triggering

This skill triggers when the user says:
- "transcribe this YouTube video"
- "get the content of this YouTube video"
- Provides a `youtube.com` or `youtu.be` URL

Or when invoked by `daily-workflow` as a **focused parallel subagent** (Step 3d). The orchestrator passes `YOUTUBE_URL`, `TASK_ID`, `DELEGATE_LIST_ID`, and an optional `SuggestionOutputPath` for per-subagent file isolation.

## Output Location

```
reports/
└── YouTube_YYYY_MM_DD/
    └── {video_title}.md
```

## Changelog

| Version | Date | Change Summary |
|---|---|---|
| v1.0.0 | 2026-05-13 | Initial skill: extracted from `process-delegate-tasks` Steps 4Y–7Y. Includes Video Strategist table, OOM/non-zero error handling, and full lifecycle (launch → poll → summarise → suggest → mark done). Uses `content-summary` references for shared logic. |
| v1.1.0 | 2026-05-14 | Unified output template moved to `content-summary/references/output_template.md`. |
| v1.2.0 | 2026-06-16 | Made output language globally configurable, defaulting to English and preferring Traditional Chinese. |
| v1.3.0 | 2026-07-24 | Skill now runs as a full-lifecycle parallel subagent when dispatched by `daily-workflow` (owns transcription → poll → summarise → suggest → mark-done). Added optional `SuggestionOutputPath` parameter passed through to `suggestion_log.md` for per-subagent file isolation (RFC: parallel-content-processing). |
