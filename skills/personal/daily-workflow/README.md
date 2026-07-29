# daily-workflow Skill

## Overview

The `daily-workflow` skill orchestrates the full content intelligence pipeline. It acts as a **pure metadata dispatcher** — it discovers item IDs and URLs, fires each content item as an independent full-lifecycle subagent, waits for all to complete, merges suggestions, and chains distillation + review.

## Problem Statement

The previous sequential pipeline processed content types one-by-one. With 5 newsletters + 3 Threads posts + 2 website articles (each taking 3–8 minutes), the total wall-clock time was 30–80 minutes. Additionally, processing earlier items filled the main agent's context with full article content, degrading summary quality for later items.

## Solution

A parallel dispatch-and-collect orchestrator that:
1. Discovers and classifies all Delegate tasks and unread newsletters (metadata only).
2. Pre-creates report directories to prevent race conditions.
3. Spawns each content item as an independent **focused full-lifecycle subagent** (fire-and-forget).
4. Waits for all subagents with a 30-minute global timeout.
5. Merges per-subagent suggestion files into the main log.
6. Chains `daily-distiller` and `review-suggestions`.

Wall-clock time drops from 30–80 minutes to the duration of the single slowest item (~8–15 minutes).

## File Structure

```
daily-workflow/
├── SKILL.md                    # Lean Spine workflow definition (<100 lines)
├── README.md                   # Skill architecture and technical reference
└── references/
    └── dispatch_spec.md        # Classification schemas, subagent prompt specs, and output templates
```

## Architecture

### Main Agent (Pure Metadata Dispatcher)

The main agent **never sees article content**. Its context contains only: task list metadata, message IDs, subagent IDs, and completion status.

```
Step 1 → Discover + classify (email IDs, task URLs)
Step 2 → Pre-create report directories + data/suggestions_pending/
Step 3 → Dispatch all subagents in parallel (fire-and-forget using dispatch_spec.md)
Step 4 → Sync barrier (30-min global timeout) & merge suggestion files → main log
Step 5 → daily-distiller
Step 6 → review-suggestions
Step 7 → Final summary output
```

### Subagents (Focused Full-Lifecycle Workers)

Each content item gets its own subagent scoped to only the relevant skill:

| Content Type | Subagent skill | Parameters passed |
|---|---|---|
| Newsletter | `ingest-newsletter` | `MESSAGE_ID`, `SuggestionOutputPath` |
| Threads | `ingest-threads` | `THREADS_URL`, `TASK_ID`, `DELEGATE_LIST_ID`, `SuggestionOutputPath` |
| Website | `ingest-website` | `WEBSITE_URL`, `TASK_ID`, `DELEGATE_LIST_ID`, `SuggestionOutputPath` |
| YouTube | `ingest-youtube` | `YOUTUBE_URL`, `TASK_ID`, `DELEGATE_LIST_ID`, `SuggestionOutputPath` |

Each subagent independently: fetches → summarises → writes report → writes suggestion → marks source done.

### Suggestion Isolation

Each subagent writes to a unique staging file:
```
data/suggestions_pending/suggestion_<type>_<item_id>.json
```

After the sync barrier (Step 4), the orchestrator merges all pending files into `data/suggestions_pending.md` in a single-threaded pass, eliminating concurrent write contention.

### Crash Safety

Operation ordering within each subagent: **write report → write suggestion → mark done**. No window exists where a source is marked done without a report.

### Timeout Handling

A 30-minute global timeout is set after all subagents are dispatched. If reached, the orchestrator proceeds with completed results and reports timed-out items as failures. Orphaned suggestion files from timed-out subagents merge into the next run (no cleanup at startup).

## Dependencies

- `ingest-newsletter` — newsletter processing (single-email mode).
- `ingest-threads` — Threads post processing (focused parallel subagent).
- `ingest-website` — generic website/article processing (focused parallel subagent).
- `ingest-youtube` — YouTube transcription + post-processing (focused parallel subagent).
- `content-summary` — shared summarisation, AI analysis, suggestion log, filename rules.
- `daily-distiller` — synthesis of today's reports.
- `review-suggestions` — review of pending AI suggestions.
- `gws-tasks` — Delegate list discovery.
- `gws-gmail` — unread newsletter discovery.

## Triggering

This skill triggers when the user says:
- "run my daily workflow"
- "run daily"
- "start my daily routine"
- Any request to run all content processing tasks in sequence

## Output

```
reports/
├── Newsletter_YYYY_MM_DD/      # From ingest-newsletter subagents
├── Threads_YYYY_MM_DD/         # From ingest-threads subagents
├── Website_YYYY_MM_DD/         # From ingest-website subagents
├── YouTube_YYYY_MM_DD/         # From ingest-youtube subagents
└── distillations/
    └── Knowledge_Distillation_YYYY_MM_DD.md
data/
├── suggestions_pending/        # Per-subagent staging (deleted after Step 4)
└── suggestions_pending.md      # Merged suggestion log
```

## Changelog

| Version | Date | Change Summary |
|---|---|---|
| v1.0.0 | 2026-05-13 | Initial skill: absorbs router logic from `process-delegate-tasks`. Chains fire-YouTube → ingest-newsletter → ingest-threads → poll-YouTube → daily-distiller → review-suggestions. YouTube post-processing done directly by orchestrator using `content-summary` references. |
| v1.1.0 | 2026-05-18 | Replaced Docker dependencies with local `yt2doc` CLI usage for YouTube transcription jobs. |
| v1.2.0 | 2026-05-25 | Added `website_queue` routing and Step 4W: delegates generic URL tasks to `ingest-website` synchronously after Threads processing. Skips tasks with no URL (previously "no supported URL"). |
| v2.0.0 | 2026-07-24 | **Parallel dispatch rewrite (RFC: parallel-content-processing)**. Main agent rewritten as pure metadata dispatcher. Steps 2–5 replaced with: pre-create directories (Step 2), fire-and-forget parallel subagent dispatch for all content types (Step 3a–3d), 30-minute global timeout barrier (Step 4), and suggestion merge (Step 4M). Each content item now gets a focused full-lifecycle subagent scoped to only its relevant skill. Wall-clock time reduced from ~30–80 min sequential to ~8–15 min (slowest item). |
| v2.1.0 | 2026-07-29 | **Context Engineering Refactor (`skill-context-refactor`)**. Restructured `SKILL.md` into a 100-line Lean Spine (55.5% line reduction). Extracted prompt parameter templates, classification rules, and summary schemas into `references/dispatch_spec.md`. Removed obsolete step markers and unhobbled restrictive directives. |
