# Threads Report — 報告輸出格式

**輸出目錄**：`reports/Threads_YYYY_MM_DD/`（以執行當天日期命名）

**檔案名稱規則**：由作者 handle + 主題推導。

> 📄 Read `../content-summary/references/filename_rules.md` for sanitisation rules.

範例：`@cooljerrett` + 主題「AI productivity」→ `cooljerrett_AI_productivity.md`

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

## 🚀 行動呼籲 / 延伸思考（Action Items / Reflections）
- [原文中引導行動的內容，若無則填「無」]

## ⚠️ 資訊免責聲明（Disclaimers）
- [若原文有語意不清或資訊缺失之處，標注於此。若資訊完整清晰可省略]

---

## 📄 原始內容（Raw Content）

{paste the full structured output from fetch-threads-post here, verbatim}
```
