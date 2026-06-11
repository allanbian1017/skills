# Rubric Definition

This document defines the 3 active quality dimensions used to score AI-generated suggestions, and 2 future dimensions for reference.

Composite score threshold is **$\ge 4$ out of 6** to pass.

---

## Active Quality Dimensions

### 1. Actionability (A)
Measures how concrete, clear, and ready to execute the suggestion is.

*   **0 (Fail)**: Abstract, vague, or non-actionable. Uses banned words or generic commands.
    *   *Examples*: "研究看看這個工具", "了解一下 Agent 的進展", "評估看看 Sandwich 架構的好處".
*   **1 (Pass)**: Specific action and object are clearly defined.
    *   *Examples*: "實作一個簡單的 LangGraph POC，模擬 Supervisor 架構", "在本地安裝並測試 `google-agents-cli` 核心功能".
*   **2 (Strong)**: Specific action, object, and scope/time estimate are defined.
    *   *Examples*: "測試這個工具的核心功能（10 分鐘內）", "撰寫一個 pre-commit hook 檢查指令載入開銷（30 分鐘內）".

### 2. Preference Alignment (P)
Measures how well the suggestion aligns with the user's explicit preferences and topic interest levels.

*   **0 (Fail)**: Matches low-interest topics or contains neutral/passive recommendations.
    *   *Examples*: Suggestions about general system design patterns, or topics explicitly rejected/marked avoided in [user_preferences.md](file:///Users/allanbian/my-ai-workflow/data/user_preferences.md).
*   **1 (Pass)**: Matches medium-interest or general topics without explicit alignment.
*   **2 (Strong)**: Matches high-interest topics AND aligns with preferred action types (e.g. adding prompts to library, learning from weakness).
    *   *Examples*: Adding specific prompt templates to `prompts.md`, creating RCA docs for errors.

### 3. Goal Relevance (G)
Measures the suggestion's contribution to goals defined in [goals.md](file:///Users/allanbian/my-ai-workflow/data/goals.md).

*   **0 (Fail)**: No connection to any goal in `goals.md` (e.g., general news/opinion summaries).
*   **1 (Pass)**: Indirect or secondary connection to a goal.
*   **2 (Strong)**: Directly advances a specific goal defined in `goals.md`.

---

## Future Dimensions (Not Active)

### 4. Source Grounding
*   **Trigger to activate**: If post-launch reviews show suggestions passing the rubric but rejected due to mismatching source content (e.g., "suggested action is not supported by the cited paper").
*   **Definition**: Verify if the suggestion is strictly grounded in the parsed source material without hallucination.

### 5. Novelty
*   **Trigger to activate**: If post-launch reviews show suggestions passing the rubric but rejected for being "already done" or redundant.
*   **Definition**: Verify that the suggestion provides new insight or actions beyond what has already been implemented or stored.

---

## Future Improvement: Retry Mechanism
*   **Prerequisite**: A separate grader pass (distinct LLM call) must be implemented. Self-grading retry runs the risk of model gaming the output (e.g. appending dummy text to pass Actionability).
*   **Rules**:
    *   Only retry on Actionability failure (score 0).
    *   Limit to exactly 1 retry.
    *   Feed the failure reason back to the generator for re-generation.
