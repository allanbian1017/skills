# Suggestion Log — Append to Pending Backlog

After generating the AI analysis (> 📄 Read ../content-summary/references/ai_analysis.md), append one entry to `data/suggestions_pending.md`.

## Format

```markdown
---

### YYYY-MM-DD | {SourceType} | [{Title}]({source_url})
- 🏷️ {分類} | 💎 {價值評分} | ⚡ {可行動性} | 🎯 {決策建議}
- 📋 建議：{建議下一步}
- 📄 [報告](file:///absolute/path/to/report.md)
```

Where `{SourceType}` is one of: `Newsletter`, `Threads`, `YouTube`, `Website`.

## Rules

- If `data/suggestions_pending.md` does not exist, create it first with the heading:
  ```
  # 📋 Pending Suggestions
  ```
- Always append — never overwrite existing entries.
- Confirm file write before marking the task as done.
