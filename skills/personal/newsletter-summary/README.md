# Newsletter Summary Skill

## Overview

The `newsletter-summary` skill provides an automated, zero-hallucination approach to reading and extracting key information from newsletters. It leverages the `gws-gmail` skill to process unread newsletters with high precision, producing one independent Markdown report per newsletter stored in a daily directory.

> This skill was migrated from the standalone `newsletter_summary` workflow (`.agents/workflows/newsletter_summary.md`) in v1.8.0. All logic and operational details are preserved.

## Problem Statement

Users receive numerous newsletters daily, leading to information overload and rapidly accumulating unread emails. Manually reading through them is time-consuming, while skipping them can result in missing important announcements, key metrics, event deadlines, or actionable items. Simply using a generic AI summarization tool often risks hallucination (adding unverified information) or over-summarization (losing critical details), which reduces the trustworthiness and utility of the summaries.

## Solution

The `newsletter-summary` skill addresses this by combining a structured iterative batch-processing loop with a strict zero-hallucination summarization prompt, ensuring that every extracted fact is 100% grounded in the source email.

### Key Features

1. **Iterative Batch Fetching:** Automatically retrieves unread emails labeled `newsletter` directly using the `gws-gmail` CLI without requiring custom scripts. Processes them in iterative batches of 10 until no unread newsletters remain.
2. **Strict Extraction Rules:**
   - **Zero Hallucination:** Only parses actual provided text, strictly prohibiting external inferences or hallucinated information.
   - **Comprehensiveness & Objectivity:** Extracts all essential data points objectively without subjective commentary.
3. **Structured Output:** Each newsletter produces a Markdown file with six fixed sections (see `assets/output_template.md` for the full format):
   - **來源 (Source):** Sender, title, and URL tracking.
   - **📝 核心總結 (Executive Summary):** Quick 1–3 sentence overview.
   - **📌 關鍵重點 (Key Highlights):** Categorized bullet points containing data, people, and events.
   - **🚀 行動呼籲 / 期限 (Action Items / Deadlines):** Clear identification of CTAs and due dates from the source.
   - **⚠️ 資訊免責聲明 (Disclaimers):** Flags unclear or incomplete information from the original text.
   - **🏷️ AI 分析 (AI Analysis):** Structured decision framework appended last — five fields scored against the user's current goals in `data/goals.md` and calibrated by the user preference profile in `data/user_preferences.md` (if available):
     - **分類**: 技術 / 商業 / 心態 / 靈感 / 其他
     - **價值評分（High/Mid/Low）**: Does it directly help current goals? Is it timely? Can it become action?
     - **可行動性評估（High/Mid/Low）**: Can it start immediately (High), needs prep (Mid), or hard to land (Low)?
     - **建議下一步（非常具體）**: `動作 + 對象 + 範圍` — no vague language like "研究看看".
     - **決策建議**: Action / Store / Drop — exactly one, chosen by the decision logic.
4. **State Management:** Marks each processed email as read and archived (removes `UNREAD` and `INBOX` labels) only **after** its summary file has been successfully written, preventing data loss and keeping the inbox clean.
5. **Markdown Reporting:** Each newsletter summary is stored as an independent Markdown file in a daily directory (`./reports/Newsletter_YYYY_MM_DD/`). File names follow the format `[寄件者]_[電子報標題].md` and are automatically sanitized for invalid path characters.

## File Structure

```
newsletter-summary/
├── SKILL.md                    # Skill definition and workflow steps
├── README.md                   # This file
└── assets/
    └── output_template.md      # Full per-newsletter Markdown template and file naming rules
```

> `assets/output_template.md` is the single source of truth for the output format. Edit it to change the report structure, section names, or add/remove fields — no need to touch `SKILL.md`.

## Quality & Precision Guardrails

1. **Zero Hallucination Guarantee:** Summaries must be 100% based on provided text. If technical terms or acronyms appear without definition, describe them as they appear in the original or flag them in the Disclaimers section — never infer external meanings.
2. **Teaser Detection Protocol:** If the content is clearly a snippet or paywall preview (e.g., Substack teaser), explicitly label it as a teaser in the `⚠️ 資訊免責聲明` section to manage user expectations. Do not fabricate missing content.
3. **Header Integrity:** Always retrieve and verify the `From` and `Subject` headers before summarization to ensure the file title and "Source" section are accurate. Re-fetch if output is truncated.
4. **Write-before-archive Safety:** A newsletter is only marked as read/archived after its Markdown file has been confirmed written to disk.

## Dependencies

- `gws-gmail` skill — used for fetching, reading, and modifying email state via the `gws` CLI.
- `gws-shared` skill — provides authentication context and global flags for `gws` commands.

## Triggering

This skill triggers when the user says phrases like:
- 「幫我整理電子報」
- 「摘要電子報」
- 「處理未讀電子報」
- "newsletter summary"
- 「讀取電子報」
- 「newsletter 摘要」

Or any request involving reading, summarizing, or batch-processing newsletters from Gmail.

## Output Location

```
./reports/
└── Newsletter_YYYY_MM_DD/
    ├── [寄件者]_[電子報標題].md
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
Store user goals as a `## 🎯 My Current Goals` section directly in `AGENTS.md` at the project root.

#### Rationale
- `AGENTS.md` is always loaded at the start of every conversation, so goals are automatically in context without any extra file-read instruction inside skills.
- Goals are project-wide intent, not an implementation detail of any single skill. Placing them in `assets/` would create an awkward cross-skill dependency.
- Any future skill needing goal-aware scoring gets it for free by referencing `AGENTS.md`.

#### Consequences
- **Positive**: Zero overhead per skill invocation; single edit point for the user; consistent across all skills.
- **Negative**: `AGENTS.md` now blends behavioral rules with user intent — slightly wider responsibility for one file.
- **Risks**: None material.

### ADR-0002: Goals Extracted to data/goals.md and Suggestion Feedback Loop

**Status**: Accepted (Supersedes ADR-0001)  
**Date**: 2026-05-07

#### Context
ADR-0001 placed user goals in `AGENTS.md`. While this was convenient, it conflated two concerns: agent behavioral rules and user intent. Additionally, the `🏷️ AI 分析` section produced suggestions (next steps, decision recommendations) that were write-only — generated in reports but never reviewed or learned from. There was no mechanism to collect user feedback on whether suggestions were useful, nor to calibrate future suggestions based on user preferences.

#### Decision
1. **Extract goals** from `AGENTS.md` into a dedicated `data/goals.md` file. Remove the goals section from `AGENTS.md` entirely.
2. **Introduce a suggestion feedback loop** with three new data files:
   - `data/suggestions_pending.md` — unreviewed suggestions (appended at ingestion time, shrinks at review)
   - `data/suggestions_reviewed.md` — reviewed suggestions with Accept/Reject feedback (append-only)
   - `data/user_preferences.md` — distilled preference profile (regenerated after each review session)
3. **Add a new `review-suggestions` skill** that presents pending suggestions as an Antigravity artifact, collects binary (Accept/Reject) feedback via conversation, and regenerates the preference profile.
4. **Update output templates** for `newsletter-summary` and `process-delegate-tasks` to read `data/goals.md` and `data/user_preferences.md` before generating the `AI 分析` block.
5. **Add backlog append steps** (Steps 2-4b, 6Tb, 6Yb) to ingestion skills so suggestions are written to `data/suggestions_pending.md` at report generation time.

#### Rationale
- **Separation of concerns**: Goals are user intent; `AGENTS.md` is agent behavior. They belong in separate files.
- **Two-file split (pending/reviewed)**: Avoids read-modify-write on a single growing file. Pending is append-at-ingestion + shrink-at-review; reviewed is append-only. This minimizes update conflicts.
- **Markdown over JSON**: The AI agent is the primary consumer of all data files. Markdown is human-readable, git-diff-friendly, and consistent with `goals.md` and `user_preferences.md`.
- **Binary feedback (Accept/Reject)**: Defer was considered but rejected as ambiguous — it provides no signal for preference learning. Skipped suggestions remain pending implicitly.
- **Recency-weighted preference profile**: Prevents stale preferences from overriding recent behavior. A 14-day window at 2× weight captures shifting interests while retaining historical patterns. Explicit user statements always override statistical inference.
- **Append at ingestion time**: More efficient than scanning all reports. The ingestion skill already has the metadata when generating the report.

#### Consequences
- **Positive**: Closed-loop feedback enables progressively better-calibrated suggestions. Goals file is cleaner and independently editable. User can review all suggestions in one place with links to original articles.
- **Negative**: Skills now have an additional write step (appending to `suggestions_pending.md`). The preference profile requires ≥5 reviews to produce meaningful patterns.
- **Risks**: If the user never reviews suggestions, the pending file grows unbounded (mitigated by the review skill splitting today vs. backlog).

---

## Changelog

| Version | Date | Change Summary |
|---|---|---|
| v1.0.0 | 2026-04-01 | Initial workflow: batch fetch unread newsletters, summarize with high-precision prompt, mark as read, compile final Markdown report. |
| v1.1.0 | 2026-04-01 | Updated architecture to support iterative batch fetching; implemented `HHMM` timestamping for Markdown reports to allow multiple daily executions without data loss. |
| v1.2.0 | 2026-04-01 | Enforced strict per-email detailed summarization and `<details>` wrapping; removed concise aggregation instructions to prevent over-compression of large batch summaries. |
| v1.3.0 | 2026-04-01 | Updated State Management to archive processed emails by removing the `INBOX` label alongside `UNREAD` to maintain a clean inbox. Added quality filtering guidance to skip low-value or near-empty emails. |
| v1.4.0 | 2026-04-02 | **Write-as-you-go fix**: Each batch's summaries are now written to file immediately after summarization (Step 2) instead of being held in memory until Step 3. Root cause: output token budget exhaustion during single-pass final compilation silently dropped Key Highlights and Action Items in later batches. |
| v1.5.0 | 2026-04-02 | **Teaser detection (Option C)**: Added `精簡預告偵測（Teaser Detection）` constraint to the summarization prompt. When an email body contains only a short preview paragraph, the model now explicitly flags it in `⚠️ 資訊免責聲明` instead of producing a silently-short summary. |
| v1.6.0 | 2026-04-07 | Changed output format to generate one independent Markdown file per newsletter stored in a daily directory (`./reports/Newsletter_YYYY_MM_DD/`), replacing the previous single-file append approach to improve focused reading. |
| v1.7.0 | 2026-04-09 | Formally added "Quality & Precision Guardrails" section to explicitly enforce Zero Hallucination, Teaser Detection, and Header Integrity protocols. |
| v1.8.0 | 2026-04-30 | **Migrated to agent skill**: Converted the standalone workflow (`.agents/workflows/newsletter_summary.md`) into a reusable agent skill at `.agents/skills/newsletter-summary/`. All operational logic, prompt content, CLI commands, and quality guardrails are preserved unchanged. Skill `description` frontmatter added for auto-triggering. |
| v1.9.0 | 2026-04-30 | **Output template extraction**: Moved the inline per-newsletter Markdown format and file naming rules out of `SKILL.md` into `assets/output_template.md` for standalone editability. `SKILL.md` now references the template file instead of embedding the format. |
| v2.0.0 | 2026-04-30 | **AI 分析 section**: Added a new `🏷️ AI 分析` section to `assets/output_template.md` with three structured fields — 分類（技術/商業/心態/靈感）, 價值判斷（High/Mid/Low）, and 建議行動（具體）— to turn each summary into an actionable intelligence item. |
| v2.0.1 | 2026-04-30 | **Section reorder**: Moved `🏷️ AI 分析` to the end of the report (after `⚠️ 資訊免責聲明`) so the distillation layer doesn't interrupt the factual content flow. |
| v2.1.0 | 2026-04-30 | **AI 分析 expanded to 5 fields**: Replaced 3-field AI 分析 with full 5-field decision framework — 分類, 價值評分, 可行動性評估, 建議下一步（非常具體）, 決策建議（Action/Store/Drop）. Includes decision logic and anti-vagueness guardrail for 建議下一步. |
| v2.1.1 | 2026-04-30 | **Goals config moved to AGENTS.md**: Removed `assets/user_goals.md`. User goals now live in the `🎯 My Current Goals` section of `AGENTS.md`, always in context. See ADR-0001. |
| v2.2.0 | 2026-05-07 | **Suggestion feedback loop**: Goals extracted from `AGENTS.md` to `data/goals.md` (ADR-0001 superseded by ADR-0002). Added Step 2-4b to append AI analysis suggestions to `data/suggestions_pending.md` at report generation time. Output template updated to read `data/goals.md` and `data/user_preferences.md` for preference-calibrated scoring. Integrates with new `review-suggestions` skill for closed-loop feedback. |
