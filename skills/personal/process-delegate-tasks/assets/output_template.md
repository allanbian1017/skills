# Process Delegate Tasks — 報告輸出格式

此檔案定義了兩種任務類型的報告輸出格式：Threads 貼文與 YouTube 影片。

---

## Threads 報告格式

**檔案名稱規則**：由作者 handle + 主題推導，替換特殊路徑字元（`/`, `?`, `=`, `&`, 空格 → `_`）

範例：`@cooljerrett` + 主題「AI productivity」→ `cooljerrett_AI_productivity.md`

**輸出目錄**：`reports/Threads_YYYY_MM_DD/`（以執行當天日期命名）

```markdown
# @{handle} — {inferred_topic_title}

## 來源
- **作者**: @{handle}（{display_name}）
- **原文連結**: {threads_url}
- **擷取時間**: {timestamp}
- **任務 ID**: {google_tasks_task_id}

## 📝 核心總結（Executive Summary）
- [1–3 句話精準概括貼文主旨]

## 📌 關鍵重點（Key Highlights）
- **[主題分類 1]**: [詳細重點，包含原文具體細節]
- **[主題分類 2]**: [詳細重點]
- *(依此類推)*

## 🏷️ AI 分析

> ⚠️ 產生此區塊前，必須先讀取根目錄的 `AGENTS.md`，從「🎯 My Current Goals」區塊取得使用者的當前重點目標，所有評分與建議須對齊該目標。

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

## 🚀 行動呼籲 / 延伸思考（Action Items / Reflections）
- [原文中引導行動的內容，若無則填「無」]

## ⚠️ 資訊免責聲明（Disclaimers）
- [若原文有語意不清或資訊缺失之處，標注於此。若資訊完整清晰可省略]

---

## 📄 原始內容（Raw Content）

{paste the full structured output from fetch-threads-post here, verbatim}
```

---

## YouTube 影片報告格式

**輸出目錄**：`reports/YouTube_YYYY_MM_DD/`（以執行當天日期命名）

```markdown
# 📹 {Video Title} — YouTube 影片摘要

## 來源
- **原文連結**: {youtube_url}
- **Whisper Model**: {model}
- **轉錄完成時間**: {timestamp}
- **任務 ID**: {google_tasks_task_id}

## 📝 核心總結（Executive Summary）
- [1–3 句話精準概括影片主旨，繁體中文]

## 📌 關鍵重點（Key Highlights）
- **[主題分類 1]**: [詳細重點，繁體中文]
- **[主題分類 2]**: [詳細重點]
- *(依此類推)*

## 🚀 行動呼籲 / 延伸思考（Action Items / Reflections）
- [影片中引導行動的內容，若無則填「無」]

## 🏷️ AI 分析

> ⚠️ 產生此區塊前，必須先讀取根目錄的 `AGENTS.md`，從「🎯 My Current Goals」區塊取得使用者的當前重點目標，所有評分與建議須對齊該目標。

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

---

## 📄 完整逐字稿（Full Transcript）

{paste the full yt2doc Markdown output here, verbatim — including TOC and all chapters}
```
