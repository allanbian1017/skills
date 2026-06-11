---
name: rubric-grader
description: "Score AI-generated suggestions against a 3-dimension rubric, check hard-vetos, and route to pending or filtered backlog. Run backtest accuracy analyses, and interactively maintain the blocklist and calibration metrics."
---

# rubric-grader

Owns all suggestion quality gates and preference alignment checks.

## Mode 1: Grade (Self-Grading Pipeline)

When grading a suggestion generated during ingestion:

1.  **Read References**:
    *   Read [references/rubric.md](file:///Users/allanbian/my-ai-workflow/.agents/skills/rubric-grader/references/rubric.md)
    *   Read [rubric_blocklist.md](file:///Users/allanbian/my-ai-workflow/data/rubric_blocklist.md)

2.  **Hard-Veto Check**:
    *   Compare the suggestion title and content against patterns in the `## Topic Blocks` section of [rubric_blocklist.md](file:///Users/allanbian/my-ai-workflow/data/rubric_blocklist.md).
    *   If matched → **VETO**. Append entry to [suggestions_filtered.md](file:///Users/allanbian/my-ai-workflow/data/suggestions_filtered.md) with reason `Hard-veto: {Topic}`. Exit.

3.  **Ambiguity Check**:
    *   Check if `建議下一步` contains any phrase listed in the `## Ambiguity Blocklist` of [rubric_blocklist.md](file:///Users/allanbian/my-ai-workflow/data/rubric_blocklist.md).
    *   If matched → **VETO**. Append entry to [suggestions_filtered.md](file:///Users/allanbian/my-ai-workflow/data/suggestions_filtered.md) with reason `Ambiguity blocklist: {Phrase}`. Exit.

4.  **Rubric Scoring**:
    *   Score the suggestion on the 3 active dimensions (Actionability, Preference Alignment, Goal Relevance) defined in [references/rubric.md](file:///Users/allanbian/my-ai-workflow/.agents/skills/rubric-grader/references/rubric.md) (0, 1, or 2).
    *   Calculate composite score $total = A + P + G$.

5.  **Pass/Fail Routing**:
    *   **Pass ($\ge 4$)**: Form entry replacing legacy fields with `🏷️ {分類} | 📊 {total}/6 (A:{a} P:{p} G:{g})` and append to [suggestions_pending.md](file:///Users/allanbian/my-ai-workflow/data/suggestions_pending.md).
    *   **Fail ($< 4$)**: Form entry replacing legacy fields with `🏷️ {分類} | 📊 {total}/6 (A:{a} P:{p} G:{g})` and append to [suggestions_filtered.md](file:///Users/allanbian/my-ai-workflow/data/suggestions_filtered.md) with reason `Below threshold ({total} < 4)`.

---

## Mode 2: Backtest

When requested to "backtest the rubric":

1.  **Read History**:
    *   Read [suggestions_reviewed.md](file:///Users/allanbian/my-ai-workflow/data/suggestions_reviewed.md).

2.  **Sample Data**:
    *   Extract reviewed entries. Stratified sample up to $N$ (default 20) accepted entries (`Feedback: ✅ Accept`) and $N$ (default 20) rejected entries (`Feedback: ❌ Reject`).

3.  **Evaluate Sample**:
    *   Use the rubric grading criteria (from Mode 1) to evaluate each sample entry's text (original suggestion content). Score A, P, G, and check hard-vetos.
    *   Classify rubric decision:
        *   **Rubric Pass**: Score $\ge 4$ and no veto.
        *   **Rubric Fail**: Score $< 4$ or vetoed.

4.  **Compute Metrics**:
    *   Calculate:
        *   **True Positive (TP)**: Actual Accept $\cap$ Rubric Pass
        *   **False Positive (FP)**: Actual Reject $\cap$ Rubric Pass
        *   **True Negative (TN)**: Actual Reject $\cap$ Rubric Fail
        *   **False Negative (FN)**: Actual Accept $\cap$ Rubric Fail
        *   **Accuracy** = $(TP + TN) / (TP + TN + FP + FN)$
        *   **Precision** = $TP / (TP + FP)$
        *   **Recall** = $TP / (TP + FN)$

5.  **Generate Report**:
    *   Write the report to `.tmp/rubric_backtest_report.md`.
    *   Output the metrics, sample details, and recommendations in the chat.

---

## Mode 3: Maintain

When invoked by `review-suggestions` at the end of Step 6:

1.  **Interactive Blocklist Proposal**:
    *   Scan [suggestions_reviewed.md](file:///Users/allanbian/my-ai-workflow/data/suggestions_reviewed.md) for suggestions with `Feedback: ❌ Reject`.
    *   Identify repeating keywords, phrases, or topics in the comments/suggestions (appearing $\ge 3$ times).
    *   If a repeating topic is found that is **not** currently in [rubric_blocklist.md](file:///Users/allanbian/my-ai-workflow/data/rubric_blocklist.md):
        *   **Stop and prompt the user in the chat**:
            ```
            💡 **Blocklist Suggestion**: Detected 3+ rejections regarding the topic: "[Topic Name]".
            - Examples of rejected comments:
              - "..."
              - "..."
            Would you like to add "[Topic Name]" to the hard-veto blocklist?
            ```
        *   Do **NOT** write to [rubric_blocklist.md](file:///Users/allanbian/my-ai-workflow/data/rubric_blocklist.md) automatically. Only write to it when the user replies affirmatively in the chat.

2.  **Rubric Score Calibration**:
    *   Count all entries in [suggestions_reviewed.md](file:///Users/allanbian/my-ai-workflow/data/suggestions_reviewed.md) that contain a `📊 {total}/6` rubric score.
    *   If total count is $\ge 30$:
        *   Calculate the accept rate for each score bucket (4, 5, 6).
        *   Recommend adjusting the threshold if necessary (e.g. if bucket 4 acceptance is $< 60\%$, suggest raising threshold to 5).
        *   Output calibration report to the chat.
    *   If total count is $< 30$:
        *   Output: `📊 Rubric calibration: {N}/30 — collecting more data.`
