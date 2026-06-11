# rubric-grader Skill

## Overview

The `rubric-grader` skill implements a two-tier quality gate for AI-generated suggestions before they enter the user's review queue. By applying a combination of deterministic blocklist checks and soft rubric scoring (Actionability, Preference Alignment, Goal Relevance), it filters out low-signal suggestions, raising the user's final acceptance rate.

---

## Problem Statement

The suggestion pipeline previously appended all generated suggestions directly to the pending queue without quality control. This resulted in:
1.  **High rejection rate**: ~29% of suggestions were rejected by the user.
2.  **Ambiguous/vague suggestions**: The generator frequently violated its own "no abstract descriptions" rule.
3.  **Low-signal suggestions**: Topic categories explicitly avoided by the user (such as Claude Code or GPU memory optimizations) were repeatedly presented.
4.  **Legacy metadata clutter**: Legacy fields like 價值評分 and 決策建議 were poorly calibrated and ignored by the user.

---

## Solution

The `rubric-grader` skill acts as a unified gatekeeper. Suggestions must pass both the deterministic blocklist and score a composite score of **$\ge 4$ out of 6** to reach the pending review backlog.

### Key Features

1.  **Hard-Veto Blocklist**: Deterministic filtering of unwanted topics (blockchain, GPU clustering, Claude Code) and ambiguity phrases (研究看看, 了解一下) at zero token cost.
2.  **3-Dimension Rubric Scoring**: Soft evaluation of Actionability, Preference Alignment, and Goal Relevance.
3.  **Stratified Backtest Suite**: Inline backtesting capability using historical reviews to calculate Precision, Recall, and Accuracy.
4.  **Interactive Blocklist Maintenance**: Automatic detection of rejected topic patterns (3+ repeats), presented to the user in chat for approval before blocking.
5.  **Score Calibration**: Auto-calibration of threshold scores based on bucket acceptance rates.

---

## File Structure

```
rubric-grader/
├── SKILL.md                    # Mode definitions and execution steps
├── README.md                   # This file
└── references/
    └── rubric.md               # Detailed rubric criteria and guidelines
```

### Related Data Files

```
data/
├── rubric_blocklist.md         # Seeded topic and ambiguity veto patterns
├── suggestions_pending.md      # Approved suggestions awaiting review
├── suggestions_filtered.md     # Ephemeral log of rejected suggestions
└── suggestions_reviewed.md     # History of reviewed entries with feedback
```

---

## Skill Modes

### 1. Grade Mode (Programmatic Ingestion)
Executed automatically during ingestion (e.g. website, threads, youtube, newsletter):
*   Reads suggestion details.
*   Checks [rubric_blocklist.md](file:///Users/allanbian/my-ai-workflow/data/rubric_blocklist.md). Vetoes if matched.
*   Grades A, P, G dimensions (0, 1, or 2).
*   If composite $\ge 4$: Appends with `📊` format to [suggestions_pending.md](file:///Users/allanbian/my-ai-workflow/data/suggestions_pending.md).
*   If composite $< 4$: Appends to [suggestions_filtered.md](file:///Users/allanbian/my-ai-workflow/data/suggestions_filtered.md).

### 2. Backtest Mode (Chat Trigger)
Triggered by asking the agent to "backtest the rubric":
*   Samples 20 Accepted and 20 Rejected entries.
*   Scores them against the rubric.
*   Outputs Accuracy, Precision, Recall, and threshold validation matrix.

### 3. Maintain Mode (Post-Review Loop)
Invoked automatically at the end of suggestion reviews:
*   Scans rejects for 3+ keyword repeats. Prompts the user in the chat to approve additions to the blocklist.
*   If $\ge 30$ rubric-scored entries are reviewed, outputs bucket calibration metrics.

---

## Quality Guardrails

1.  **Deterministic Veto First**: If a suggestion matches any blocked topic or ambiguity phrase, it is immediately discarded before calling LLM grading.
2.  **Strict 0/1/2 Scale**: Simple scoring minimizes criteria drift.
3.  **Human-in-the-Loop Maintenance**: New veto blocks are suggested to the user, not written silently.

---

## Dependencies

*   `content-summary` reference library — delegates suggestion grading to `rubric-grader` during ingestion.
*   `review-suggestions` skill — invokes `rubric-grader` (Maintain mode) after updating the preference profile.

---

## Changelog

| Version | Date | Change Summary |
|---|---|---|
| v1.0.0 | 2026-06-11 | Initial release: Implemented Grade, Backtest, and Maintain modes. Seeded blocklists, filtered suggestions log, and threshold scoring. |
