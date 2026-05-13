# Delegate Task Processing Skill

## Overview

The `process-delegate-tasks` skill automates the full lifecycle of every URL-based task in the Google Tasks "Delegate" list. It picks up tasks, detects whether they are Threads posts or YouTube videos, fetches or transcribes the content, produces a structured Traditional Chinese summary, saves a report, and marks the task as completed — clearing the entire backlog in one run.

## Problem Statement

URL-based tasks (Threads posts, YouTube videos) shared for later reading or analysis often accumulate in task lists without a consistent processing method. Manually opening browsers, transcribing videos, reading content, and summarizing key points is tedious. Furthermore, without a centralized repository for these insights, the knowledge remains siloed, making it difficult to reference later alongside other information like newsletters.

## Solution

The `process-delegate-tasks` skill automates the extraction, transcription, summarization, and documentation of content stored in the Google Tasks "Delegate" list. It supports two content sources (Threads, YouTube) and provides an end-to-end processing pipeline with async handling for long-running transcription jobs.

### Key Features

1. **Dynamic Task Discovery:** Automatically identifies and fetches incomplete tasks from the "Delegate" task list using the `gws` CLI.
2. **Multi-Source Support:**
   - **Threads:** Filters for `threads.net` or `threads.com` URLs.
   - **YouTube:** Filters for `youtube.com` or `youtu.be` URLs.
3. **Automated Content Extraction:**
   - **Threads:** Uses `agent-browser` (via `fetch-threads-post`) to capture full post text and metadata.
   - **YouTube:** Uses the `yt2doc` Docker tool to transcribe and organize video content into Markdown.
4. **Async Parallel Processing:** Launches slow transcription jobs (YouTube) in the background while processing fast social media tasks (Threads) synchronously (fire-and-poll strategy).
5. **Structured Traditional Chinese Summary:** Each report contains an Executive Summary, Key Highlights, Action Items, and verbatim raw content or full transcript, plus an `🏷️ AI 分析` intelligence layer with five structured fields — 分類, 價值評分, 可行動性評估, 建議下一步, and 決策建議 — scored against the user's current goals in `data/goals.md` and calibrated by the user preference profile in `data/user_preferences.md` (if available). Placement differs by format: after Key Highlights in Threads reports; after Action Items in YouTube reports.
6. **Automatic State Completion:** Marks the Google Task as "completed" only after the report is successfully generated and stored.
7. **Intermediate File Cleanup:** Automatically removes temporary raw transcription files (`<video_id>.md`) after they have been successfully merged into the final summary report.
8. **Ephemeral Cleanup:** Deletes temporary diagnostic files (screenshots, scratch files) at the end of each session.

## File Structure

```
process-delegate-tasks/
├── SKILL.md                    # Skill definition and workflow steps
├── README.md                   # This file
└── assets/
    └── output_template.md      # Report templates for both Threads and YouTube output formats
```

> `assets/output_template.md` is the single source of truth for the output format. It contains both the **Threads report format** and the **YouTube report format**. Edit it to change section names, add metadata fields, or adjust the report structure — no need to touch `SKILL.md`.

## Output Location

```
reports/
├── Threads_YYYY_MM_DD/
│   ├── {handle}_{topic}.md
│   └── ...
└── YouTube_YYYY_MM_DD/
    ├── {video_title}.md
    └── ...
```

## Architecture Decision Records (ADR)

### ADR-0001: Async Parallel Processing for Multi-Source Tasks

**Status**: Accepted  
**Date**: 2026-04-29

#### Context
The workflow was expanded to support YouTube transcription via `yt2doc`. YouTube transcription is computationally intensive and can take anywhere from 5 to 80 minutes depending on video length and selected Whisper model. Threads scraping, by contrast, takes only a few seconds.

#### Decision
We decided to implement a **fire-and-poll** async strategy:
1. Identify all YouTube tasks first and launch their Docker containers in the background.
2. Immediately proceed to process all Threads tasks synchronously.
3. Once Threads tasks are cleared, enter a polling loop for the background YouTube jobs.

#### Rationale
This prevents slow, long-running transcription jobs from blocking the processing of fast social media tasks. It maximizes the throughput of the "Delegate" list clearance and provides a better user experience by getting social media summaries ready while videos are still transcribing.

#### Consequences
- **Positive**: Higher throughput, better responsiveness for fast tasks.
- **Negative**: Increased complexity in state management (tracking background job IDs).
- **Risks**: Docker resource contention if too many YouTube jobs are fired simultaneously (mitigated by recommending 8GB+ RAM).

### ADR-0002: Automatic Removal of Intermediate Transcription Files

**Status**: Accepted  
**Date**: 2026-04-29

#### Context
The `yt2doc` tool generates a standalone Markdown file (e.g., `v4F1gFy-hqg.md`) in the output directory. The `process-delegate-tasks` workflow then reads this file, generates a summary, and creates a final report which includes both the summary and the full raw transcript. This results in duplicate content in the `reports/` directory.

#### Decision
Automatically delete the intermediate file generated by `yt2doc` immediately after the final summary-inclusive report is written and verified.

#### Rationale
Removing the intermediate file prevents directory clutter and ensures that the `reports/` folder only contains the finalized, human-readable documents. Since the final report already contains the verbatim transcript, the intermediate file is redundant.

#### Consequences
- **Positive**: Reduced storage footprint, cleaner directory structure, improved searchability (no duplicate results).
- **Negative**: The raw, un-summarized file is lost (though its content persists in the summary report).
- **Risks**: If the deletion occurs before the final report is fully written/flushed, data could be lost (mitigated by verifying file existence before deletion).

### ADR-0003: Anti-Truncation Standard for Social Media Ingestion

**Status**: Accepted  
**Date**: 2026-04-30

#### Context
Threads and other SPA-based social platforms frequently mask content behind login modals (e.g., "Say more with Threads") or use lazy-loading/virtual scrolling that standard ref-based extraction misses. During the 2026-04-30 session, several posts were truncated because the content was "behind" a modal or required a scroll to trigger full loading.

#### Decision
We decided to implement a mandatory **"Scroll + Body-First"** extraction sequence for all social media ingestion:
1.  **Navigate** to the post.
2.  **Scroll Down** (minimum 1000px) to trigger lazy-loading and move past fixed overlays.
3.  **Extract Body** using `get text body` as the primary source for raw content, rather than specific DOM elements.

#### Rationale
Ensures 100% content capture regardless of UI overlays, obfuscated class names, or viewport-based lazy loading. Capturing the full body text ensures that even content masked by a "Say more with Threads" modal is ingested into the report.

#### Consequences
- **Positive**: Eliminated "silent truncation" errors, improved report completeness.
- **Negative**: Increased processing time per task by ~2-3 seconds due to mandatory scroll/wait.
- **Risks**: Potential ingestion of unrelated UI elements (sidebars, footers) which must be filtered during summarization.

### ADR-0004: User Goals Stored in AGENTS.md, Not Skill Assets

**Status**: Superseded by ADR-0005  
**Date**: 2026-04-30

#### Context
The `🏷️ AI 分析` section was expanded to score content against the user's current goals (Goal 1–3). A dedicated `assets/user_goals.md` file was initially created inside `.agents/skills/assets/` to store these goals. This felt architecturally off — a goals file is user intent, not a skill artifact.

#### Decision
Store user goals as a `## 🎯 My Current Goals` section directly in `AGENTS.md` at the project root.

#### Rationale
- `AGENTS.md` is already loaded automatically at the start of every conversation, so goals are always in context without any extra file read step in skill instructions.
- Goals are project-wide user intent, not a skill implementation detail. Putting them in a skill's `assets/` folder would break the conceptual boundary between "what the skill does" and "what the user wants."
- Any future skill that needs goal-aware scoring can reference `AGENTS.md` without cross-skill file path dependencies.

#### Consequences
- **Positive**: Goals are always in context, no extra file load needed, single edit point for the user.
- **Negative**: `AGENTS.md` now carries both behavioral rules and user intent — slightly wider scope for one file.
- **Risks**: None material; the file stays small and readable.

### ADR-0005: Goals Extracted to data/goals.md and Suggestion Feedback Loop

**Status**: Accepted (Supersedes ADR-0004)  
**Date**: 2026-05-07

#### Context
ADR-0004 placed user goals in `AGENTS.md`. While convenient, it conflated agent behavioral rules with user intent. Additionally, the `🏷️ AI 分析` section produced suggestions that were write-only — generated in reports but never reviewed or learned from. There was no mechanism for the user to provide feedback on whether suggestions were useful, nor to calibrate future suggestions based on preferences.

#### Decision
1. **Extract goals** from `AGENTS.md` into a dedicated `data/goals.md` file. Remove the goals section from `AGENTS.md` entirely.
2. **Introduce a suggestion feedback loop** with three new data files:
   - `data/suggestions_pending.md` — unreviewed suggestions (appended at ingestion, shrinks at review)
   - `data/suggestions_reviewed.md` — reviewed suggestions with Accept/Reject feedback (append-only)
   - `data/user_preferences.md` — distilled preference profile (regenerated after each review session)
3. **Add a new `review-suggestions` skill** that presents pending suggestions via Antigravity artifact, collects binary feedback, and regenerates the preference profile.
4. **Update output templates** to read `data/goals.md` and `data/user_preferences.md` before generating `AI 分析`.
5. **Add backlog append steps** (6Tb, 6Yb) so suggestions are written to `data/suggestions_pending.md` at report generation time.

#### Rationale
- **Separation of concerns**: Goals are user intent; `AGENTS.md` is agent behavior. They belong in separate files.
- **Two-file split (pending/reviewed)**: Avoids read-modify-write on a single growing file. Pending is append-at-ingestion + shrink-at-review; reviewed is append-only.
- **Markdown over JSON**: AI agent is the primary consumer. Markdown is human-readable, git-diff-friendly, and consistent with the entire `data/` directory.
- **Binary feedback (Accept/Reject)**: Defer was rejected as ambiguous — provides no signal for preference learning.
- **Recency-weighted preferences**: 14-day window at 2× weight prevents stale preferences from overriding recent behavior.
- **Append at ingestion time**: The skill already knows the metadata at report generation time — no scanning needed.

#### Consequences
- **Positive**: Closed-loop feedback enables better-calibrated suggestions. User can review all suggestions in one place with links to original articles.
- **Negative**: Additional write step per ingested report. Preference profile requires ≥5 reviews for meaningful patterns.
- **Risks**: Unbounded pending file if never reviewed (mitigated by today/backlog split in review UI).

---

## Quality & Precision Guardrails

1. **Zero Hallucination Guarantee:** Summaries MUST be 100% based on the extracted content.
2. **Docker Dependency:** YouTube processing requires Docker to be running. If Docker is missing, the task fails gracefully but doesn't block other tasks.
3. **Anti-Truncation Standard:** Threads extraction mandates a `scroll down 1000` followed by `get text body` to capture content behind modals and lazy-loaded segments.
4. **Verbatim Raw Content:** Reports must contain the *entire* raw transcript or post content for archival integrity.
5. **Log Transparency:** All tool calls and background job statuses are visible in the conversation logs.
6. **Ephemeral Cleanup:** Temporary diagnostic files and screenshots are deleted post-execution.

## Changelog

| Version | Date | Change Summary |
|---|---|---|
| v1.0.0 | 2026-04-20 | Initial workflow: fetch tasks from "Delegate" list, scrape Threads content. |
| v1.1.0 | 2026-04-20 | Migrated to minimal `gws-tasks` skill. |
| v1.2.0 | 2026-04-20 | Enforced iterative processing and defined batching strategy. |
| v1.2.1 | 2026-04-20 | Added Ephemeral Cleanup guardrail. |
| v1.3.0 | 2026-04-29 | **Major Update**: Renamed to `process-delegate-tasks`. Added YouTube support via `yt2doc`. Implemented ADR-0001 (Async Parallel Processing). |
| v1.3.1 | 2026-04-29 | Added automatic intermediate file cleanup. Implemented ADR-0002. |
| v1.3.2 | 2026-04-30 | **Anti-Truncation Standard**: Implemented mandatory scrolling and body-first extraction to fix incomplete ingestion issues. Added ADR-0003. |
| v1.4.0 | 2026-04-30 | **Output template extraction**: Moved inline Threads and YouTube report templates out of `SKILL.md` into `assets/output_template.md` for standalone editability. `SKILL.md` now references the template by name. |
| v1.5.0 | 2026-04-30 | **AI 分析 section**: Added a new `🏷️ AI 分析` section to both the Threads and YouTube report formats in `assets/output_template.md`. Includes 分類（技術/商業/心態/靈感）, 價值判斷（High/Mid/Low）, and 建議行動（具體）for actionable, prioritizable knowledge distillation. |
| v1.5.1 | 2026-04-30 | **Section reorder**: Adjusted `🏷️ AI 分析` placement per format — after Key Highlights in Threads reports; after Action Items (last section before transcript) in YouTube reports. |
| v1.6.0 | 2026-04-30 | **AI 分析 expanded to 5 fields**: Replaced 3-field AI 分析 (分類, 價值判斷, 建議行動) with full 5-field decision framework — 分類, 價值評分, 可行動性評估, 建議下一步（非常具體）, 決策建議（Action/Store/Drop）. Scoring now uses decision logic aligned to user's current goals. |
| v1.6.1 | 2026-04-30 | **Goals config moved to AGENTS.md**: Removed `assets/user_goals.md`. User goals now live in the `🎯 My Current Goals` section of `AGENTS.md`, which is always in context. SKILL.md and output_template.md updated to reference AGENTS.md. See ADR-0004. |
| v1.7.0 | 2026-05-07 | **Suggestion feedback loop**: Goals extracted from `AGENTS.md` to `data/goals.md` (ADR-0004 superseded by ADR-0005). Added Steps 6Tb and 6Yb to append AI analysis suggestions to `data/suggestions_pending.md` at report generation time. Output template updated to read `data/goals.md` and `data/user_preferences.md` for preference-calibrated scoring. Integrates with new `review-suggestions` skill for closed-loop feedback. |
