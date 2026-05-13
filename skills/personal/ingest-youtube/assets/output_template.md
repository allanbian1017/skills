# YouTube Report — 影片報告輸出格式

**輸出目錄**：`reports/YouTube_YYYY_MM_DD/`（以執行當天日期命名）

> 📄 Read `../content-summary/references/filename_rules.md` for sanitisation rules.

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

---

## 📄 完整逐字稿（Full Transcript）

{paste the full yt2doc Markdown output here, verbatim — including TOC and all chapters}
```
