# ingest-newsletter Skill

## Overview

The `ingest-newsletter` skill fetches unread newsletters from Gmail and produces one independent Markdown summary report per email in the configured output language, stored in a daily directory. It uses a strict zero-hallucination extraction standard and marks each email as read/archived only after its report is confirmed written.

> **Renamed from `newsletter-summary` in v2.3.0** as part of the DRY refactoring of the content intelligence pipeline. All logic is preserved; shared summarisation and AI analysis rules now live in `content-summary/references/`.

## Problem Statement

Users receive numerous newsletters daily, leading to information overload and rapidly accumulating unread emails. Manually reading through them is time-consuming, while skipping them can result in missing important announcements, key metrics, event deadlines, or actionable items. Generic AI summarisation tools risk hallucination or over-compression, reducing trustworthiness.

## Solution

Iterative batch-processing with a strict zero-hallucination summarisation prompt, combined with an AI analysis suggestion loop that writes to a shared pending backlog for later review.

### Key Features

1. **Iterative Batch Fetching:** Retrieves unread emails with `label:newsletter is:unread` in batches of 10 until none remain.
2. **Shared Summarisation Rules:** Reads `content-summary/references/summarise.md` — single source of truth for Zero Hallucination, Comprehensiveness, Objectivity, and Teaser Detection.
3. **Structured Output:** Each newsletter produces a Markdown file with five sections (see `../content-summary/references/output_template.md`):
   - **來源**: Sender, title, URL.
   - **📝 核心總結**: 1–3 sentence overview.
   - **📌 關鍵重點**: Categorised bullet points with data, people, events.
   - **🚀 行動呼籲 / 期限**: CTAs and deadlines from the source.
   - **⚠️ 資訊免責聲明**: Flags unclear or incomplete source information.
4. **Separate AI Analysis Backlog:** AI analysis is not written to the report. Instead it is appended to `data/suggestions_pending.md` using the shared `content-summary/references/ai_analysis.md` and `suggestion_log.md` rules.
5. **Write-before-archive Safety:** Email is marked as read and archived only after its report file is confirmed written.

## File Structure

```
ingest-newsletter/
├── SKILL.md                    # Skill definition and workflow steps
├── README.md                   # This file
└── assets/
    └── output_template.md      # Newsletter-specific Markdown template
```

## Dependencies

- `content-summary` — shared summarisation rules, AI analysis field definitions, suggestion log format, filename rules.
- `gws-gmail` — fetching, reading, and modifying email state via the `gws` CLI.
- `gws-shared` — authentication context and global flags.

## Triggering

This skill triggers when the user says:
- 「幫我整理電子報」
- 「摘要電子報」
- 「處理未讀電子報」
- "newsletter summary"
- 「讀取電子報」
- 「newsletter 摘要」

Or when invoked by `daily-workflow` (Step 3).

## Output Location

```
reports/
└── Newsletter_YYYY_MM_DD/
    ├── [寄件者]_[電子報標題].md
    └── ...
```

## Architecture Decision Records (ADR)

### ADR-0001: User Goals Stored in AGENTS.md, Not Skill Assets

**Status**: Superseded by ADR-0002
**Date**: 2026-04-30

#### Context
The `🏷️ AI 分析` section was expanded to score content against the user's current goals. A dedicated `assets/user_goals.md` was initially created inside `.agents/skills/assets/` to hold these goals. This felt like the wrong layer — a goals file is user intent, not a skill artifact.

#### Decision
Store user goals as a `## 🎯 My Current Goals` section directly in `AGENTS.md`.

#### Rationale
- `AGENTS.md` is always loaded at session start, so goals are automatically in context without extra file-read instructions.
- Goals are project-wide intent, not an implementation detail of a single skill.

#### Consequences
- **Positive**: Zero overhead per skill invocation; single edit point; consistent across skills.
- **Negative**: `AGENTS.md` blends behavioral rules with user intent.

### ADR-0002: Goals Extracted to data/goals.md and Suggestion Feedback Loop

**Status**: Accepted (Supersedes ADR-0001)
**Date**: 2026-05-07

#### Context
ADR-0001 placed user goals in `AGENTS.md`. This conflated agent behavioral rules with user intent. The `🏷️ AI 分析` section produced write-only suggestions with no mechanism to collect feedback or calibrate future suggestions.

#### Decision
1. Extract goals to `data/goals.md`.
2. Introduce suggestion feedback loop: `data/suggestions_pending.md`, `data/suggestions_reviewed.md`, `data/user_preferences.md`.
3. Add `review-suggestions` skill for closed-loop feedback.
4. Add backlog-append step to ingestion skills.

#### Consequences
- **Positive**: Closed-loop feedback enables progressively better-calibrated suggestions.
- **Negative**: Skills have an additional write step. Preference profile requires ≥5 reviews to produce meaningful patterns.

### ADR-0003: DRY Refactoring — Extract Shared Logic to content-summary

**Status**: Accepted
**Date**: 2026-05-13

#### Context
Summarisation rules, AI analysis structure, suggestion logging logic, and filename conventions were duplicated across `newsletter-summary`, `process-delegate-tasks`, and their output templates. Adding a new analysis field required updating three separate files.

#### Decision
Extract shared logic into a `content-summary` reference library. Rename `newsletter-summary` → `ingest-newsletter`. Remove the AI 分析 block from the report template; write it only to `data/suggestions_pending.md`.

#### Consequences
- **Positive**: Single source of truth. Adding a new ingest source requires ~50 lines.
- **Negative**: Short migration period; two directories renamed.

---

## Changelog

| Version | Date | Change Summary |
|---|---|---|
| v1.0.0 | 2026-04-01 | Initial workflow: batch fetch unread newsletters, summarize, mark as read. |
| v1.1.0 | 2026-04-01 | Iterative batch fetching; `HHMM` timestamping for multiple daily runs. |
| v1.2.0 | 2026-04-01 | Enforced per-email strict summarisation; removed over-compression instructions. |
| v1.3.0 | 2026-04-01 | Archive processed emails (remove `INBOX` label). |
| v1.4.0 | 2026-04-02 | Write-as-you-go fix: write each batch immediately, not held until final step. |
| v1.5.0 | 2026-04-02 | Teaser Detection: flag short preview emails in `⚠️ 資訊免責聲明`. |
| v1.6.0 | 2026-04-07 | One Markdown file per newsletter in daily directory. |
| v1.7.0 | 2026-04-09 | Formalised Quality & Precision Guardrails section. |
| v1.8.0 | 2026-04-30 | Migrated from standalone workflow to reusable agent skill. |
| v1.9.0 | 2026-04-30 | Output template extracted to `assets/output_template.md`. |
| v2.0.0 | 2026-04-30 | Added `🏷️ AI 分析` section to output template. |
| v2.1.0 | 2026-04-30 | AI 分析 expanded to 5-field decision framework. |
| v2.1.1 | 2026-04-30 | Goals moved to `AGENTS.md` (ADR-0001). |
| v2.2.0 | 2026-05-07 | Suggestion feedback loop: append to `data/suggestions_pending.md` at ingestion (ADR-0002). |
| v2.3.0 | 2026-05-13 | **DRY refactoring (ADR-0003)**: Renamed to `ingest-newsletter`. Summarisation rules → `content-summary/references/summarise.md`. AI analysis → `content-summary/references/ai_analysis.md`. Suggestion log → `content-summary/references/suggestion_log.md`. AI 分析 block removed from report template. |
| v2.4.0 | 2026-05-14 | Unified output template moved to `content-summary/references/output_template.md`. |
| v2.5.0 | 2026-05-15 | **HTML-by-default (RCA-2026-05-15)**: Fetch full `text/html` body to prevent plain-text truncation. Explicitly omit the Raw Content section for newsletters to avoid HTML noise. |
| v2.6.0 | 2026-06-16 | Made output language globally configurable, defaulting to English and preferring Traditional Chinese. |
