# Suggestion Log — Format Definition

The entry format generated and managed by the `rubric-grader` skill.

## Format

```markdown
---

### YYYY-MM-DD | {SourceType} | [{Title}]({source_url})
- 🏷️ {分類} | 📊 {total}/6 (A:{n} P:{n} G:{n})
- 📋 建議：{建議下一步}
- 📄 [報告](file:///absolute/path/to/report.md)
```

Where `{SourceType}` is one of: `Newsletter`, `Threads`, `YouTube`, `Website`.
`{total}` is the composite score, and `A`, `P`, `G` represent Actionability, Preference Alignment, and Goal Relevance.

## Parameters

### `SuggestionOutputPath` (optional)

When a `SuggestionOutputPath` is provided by the caller:
- Write the suggestion JSON to that path instead of the default `data/suggestions_pending.md`.
- Use the format: `data/suggestions_pending/suggestion_<type>_<item_id>.json`
- This enables parallel subagents to write without file contention.

When omitted:
- Use the default location (`data/suggestions_pending.md`) — behavior is unchanged.

## Rules

- This format is written by the `rubric-grader` skill (Grade mode).
- If `data/suggestions_pending.md` does not exist, it is created with the heading:
  ```
  # 📋 Pending Suggestions
  ```
- Checked and routed automatically. Do not manually append to `suggestions_pending.md` in ingestion skills.
