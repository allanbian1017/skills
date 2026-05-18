# AI Analysis (Suggestion Generation)

This analysis scores the content's relevance to the user's goals and generates a calibrated suggestion to be added to the pending backlog.
It is **no longer** appended to the content report directly.

*Note: The fields here (like Actionability) overlap with Layers 4-5 in the report template. This is intentional. Report layers are learning artefacts for human reading; this suggestion log is an action queue for programmatic review by `review-suggestions`.*

## Prerequisites — Read Before Generating

> ⚠️ 產生分析建議前，必須：
> 1. 讀取 `data/goals.md` 取得使用者當前目標
> 2. 若 `data/user_preferences.md` 存在，讀取使用者偏好檔案，用其校準：
>    - **建議下一步**：優先使用者偏好的行動類型，避免使用者常拒絕的類型
>    - **決策建議**：參考決策校準數據調整 Action/Store/Drop 判斷門檻
>    - **價值評分**：參考主題興趣偏好調整
>    - 注意「Shifting Interests」標記，避免推薦使用者已失去興趣的主題

## Fields required for the backlog

Use these definitions to determine the values for the suggestion log:

- **分類**（擇一）：技術 | 商業 | 心態 | 靈感 | 其他

- **價值評分**（High / Mid / Low）
  - 評分依據：是否直接幫助當前目標？是否可轉化為具體行動？是否有時效性？

- **可行動性評估**（High / Mid / Low）
  - High：可以立即開始（1~3 步內）
  - Mid：需要學習或準備
  - Low：難以落地

- **建議下一步**（非常具體）：[動作 + 對象 + 範圍]，例：「實作一個簡單 agent workflow（用現有架構）」、「測試這個工具的核心功能（10 分鐘內）」
  > ⚠️ 禁止抽象描述（例如：研究看看、了解一下）

- **決策建議**（只能選一個）：Action | Store | Drop
  - Action：值得立即轉為任務
  - Store：值得保存但不立即行動
  - Drop：不值得投入注意力
