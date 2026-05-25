# daily-workflow Skill

## Overview

The `daily-workflow` skill orchestrates the full content intelligence pipeline in optimal order. It maximises throughput by firing slow async YouTube transcription jobs first, then processing fast synchronous tasks (newsletters and Threads), then collecting the YouTube results once ready.

## Problem Statement

Running newsletters, Threads posts, and YouTube videos one-by-one is inefficient — a 45-minute video would block five Threads tasks from finishing. Previously, `process-delegate-tasks` mixed all three content types in one skill, and `daily-distiller` / `review-suggestions` had to be run manually as separate steps. There was no single entrypoint to chain the full pipeline.

## Solution

A dedicated orchestrator skill that:
1. Discovers and classifies all Delegate tasks by URL type.
2. Fires all YouTube jobs to the background immediately.
3. Processes newsletters and Threads tasks synchronously while `yt2doc` runs.
4. Collects YouTube results and completes their post-processing.
5. Chains `daily-distiller` and `review-suggestions` as final steps.

## File Structure

```
daily-workflow/
├── SKILL.md                    # Skill definition and workflow steps
└── README.md                   # This file
```

## Pipeline Sequence

```
t=0     Fire `yt2doc` for all YouTube tasks (background)
t=0     Process newsletters → ingest-newsletter (full lifecycle)
t=Ns    Process Threads tasks → ingest-threads (per task, full lifecycle)
t=Mw    Process Website tasks → ingest-website (per task, full lifecycle)
t=Mw+   Poll YouTube jobs → summarise → suggest → mark done (self-handled)
t=end   daily-distiller → review-suggestions
```

## Who Marks What as Done

| Scenario | Who marks done |
|---|---|
| Newsletter processing | `ingest-newsletter` (full lifecycle delegation) |
| Threads task processing | `ingest-threads` (full lifecycle delegation) |
| Website task processing | `ingest-website` (full lifecycle delegation) |
| YouTube task processing | `daily-workflow` itself (post-processing after polling) |
| Distillation | `daily-distiller` |

YouTube is the exception because the orchestrator must manage the async polling loop and interleave it with other work — it cannot delegate a complete `ingest-youtube` invocation to the background.

## Dependencies

- `ingest-newsletter` — newsletter processing.
- `ingest-threads` — Threads post processing.
- `ingest-website` — generic website/article processing.
- `ingest-youtube` — YouTube Video Strategist table (model selection).
- `content-summary` — shared summarisation, AI analysis, suggestion log, filename rules (used directly by orchestrator for YouTube post-processing).
- `daily-distiller` — synthesis of today's reports.
- `review-suggestions` — review of pending AI suggestions.
- `gws-tasks` — Delegate list discovery and task completion.

## Triggering

This skill triggers when the user says:
- "run my daily workflow"
- "run daily"
- "start my daily routine"
- Any request to run all content processing tasks in sequence

## Output

```
reports/
├── Newsletter_YYYY_MM_DD/      # From ingest-newsletter
├── Threads_YYYY_MM_DD/         # From ingest-threads
├── Website_YYYY_MM_DD/         # From ingest-website
├── YouTube_YYYY_MM_DD/         # From daily-workflow (YouTube post-processing)
└── distillations/
    └── Knowledge_Distillation_YYYY_MM_DD.md
data/
└── suggestions_pending.md      # Appended by all ingest steps
```

## Changelog

| Version | Date | Change Summary |
|---|---|---|
| v1.0.0 | 2026-05-13 | Initial skill: absorbs router logic from `process-delegate-tasks`. Chains fire-YouTube → ingest-newsletter → ingest-threads → poll-YouTube → daily-distiller → review-suggestions. YouTube post-processing done directly by orchestrator using `content-summary` references. |
| v1.1.0 | 2026-05-18 | Replaced Docker dependencies with local `yt2doc` CLI usage for YouTube transcription jobs. |
| v1.2.0 | 2026-05-25 | Added `website_queue` routing and Step 4W: delegates generic URL tasks to `ingest-website` synchronously after Threads processing. Skips tasks with no URL (previously "no supported URL"). |
