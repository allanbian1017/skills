# AI Analysis (Suggestion Generation)

This analysis scores the content's relevance to the user's goals and generates a calibrated suggestion to be added to the pending backlog.
It is **no longer** appended to the content report directly.

*Note: The fields here (like Actionability) overlap with Layers 4-5 in the report template. This is intentional. Report layers are learning artefacts for human reading; this suggestion log is an action queue for programmatic review by `review-suggestions`.*

## Prerequisites — Read Before Generating

> ⚠️ 產生分析建議前，必須：
> 1. 讀取 `data/goals.md` 取得使用者當前目標
> 2. 若 `data/user_preferences.md` 存在，讀取使用者偏好檔案，用其校準：
>    - **建議下一步**：優先使用者偏好的行動類型，避免使用者常拒絕的類型
>    - 注意「Shifting Interests」標記，避免推薦使用者已失去興趣的主題

## Fields required for the backlog

Use these definitions to determine the values for the suggestion:

- **分類**（擇一）：技術 | 商業 | 心態 | 靈感 | 其他

- **建議下一步**（非常具體）：[動作 + 對象 + 範圍]，例：「實作一個簡單 agent workflow（用現有架構）」、「測試這個工具的核心功能（10 分鐘內）」
  > ⚠️ 禁止抽象描述（例如：研究看看、了解一下）

---

## Rubric Grading Delegation

After generating the properties above:
Use the `rubric-grader` skill (Grade mode) to score and filter the suggestion.
The `rubric-grader` skill will automatically determine the score, apply hard-veto blocklists, and write the suggestion to either `data/suggestions_pending.md` or `data/suggestions_filtered.md`. Do not write directly to the pending file yourself.
