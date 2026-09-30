# Rubric Definition

This document defines the 3 active quality dimensions used to score AI-generated suggestions, and 2 future dimensions for reference.

Composite score threshold is **$\ge 4$ out of 6** to pass.

---

## Active Quality Dimensions

### 1. Actionability (A)
Measures how concrete, clear, and ready to execute the suggestion is.

*   **0 (Fail)**: Abstract, vague, or non-actionable. Uses banned words or generic commands.
    *   *Examples*: "研究看看這個工具", "了解一下 Agent 的進展", "評估看看 Sandwich 架構的好處".
*   **1 (Pass)**: Specific action and object are clearly defined, but lacks clear scope, archetype declaration, or time estimate.
    *   *Examples*: "實作一個簡單的 LangGraph POC", "測試 `google-agents-cli` 核心功能".
*   **2 (Strong)**: Specific action, object, and scope/time estimate are defined for an actionable archetype (`JIRA_BACKLOG`, `ADR_DOC`, `PROMPT_TEMPLATE`, `TEST_FIXTURE`).
    *   *Examples*:
        - `JIRA_BACKLOG`: "整理為 Jira 待辦項目提案（目標 Epic: AW-3），包含具體驗收條件與架構設計邊界（15 分鐘內）"
        - `ADR_DOC`: "整理為 1 篇技術決策紀錄存入 docs/adr/，明確定義選型邊界（15 分鐘內）"
        - `PROMPT_TEMPLATE`: "整理為 1 個模擬面試結構化評分提示詞存入 data/prompts/...（15 分鐘內）"
        - `TEST_FIXTURE`: "針對並發異常行為撰寫 1 組 pytest 邊界測試案例存入 tests/...（15 分鐘內）"

### 2. Preference Alignment (P)
Measures how well the suggestion aligns with the user's explicit preferences, topic interest levels, and **Archetype-Content Fit**.

*   **0 (Fail)**: Matches low-interest topics, rejected patterns, OR exhibits **Forced Prompt Wrapping** (packaging macro news, industry events, or theoretical architecture into a dummy `data/prompts/` template).
    *   *Examples*: Suggestions about general system design or news forced into a prompt template, topics explicitly rejected/marked avoided in [user_preferences.md](file:///Users/allanbian/my-ai-workflow/data/user_preferences.md).
*   **1 (Pass)**: Matches medium-interest or general topics with weak or borderline archetype alignment.
*   **2 (Strong)**: Matches high-interest topics AND aligns with preferred action types through appropriate **Archetype-Content Fit**:
    *   System architecture / state machines / data replicas $\to$ `JIRA_BACKLOG` (AW-1..AW-7) or `ADR_DOC`
    *   Interactive interview / negotiation / judge tools $\to$ `PROMPT_TEMPLATE`
    *   Edge cases / failure modes $\to$ `TEST_FIXTURE`
    *   General news / industry trend $\to$ `TAKEAWAY_ONLY` (routed directly to filtered/distillation, bypassing pending queue)

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
