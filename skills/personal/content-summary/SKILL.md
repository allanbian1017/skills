---
name: content-summary
description: "Shared content summarisation and AI analysis pipeline. Provides reusable references for Traditional Chinese summarisation quality rules, AI analysis with user-preference calibration, and suggestion logging. Referenced by ingest skills (ingest-newsletter, ingest-threads, ingest-youtube). Do not invoke this skill directly."
---

# content-summary

Shared reference library for the content intelligence pipeline. **Do not invoke directly** — ingest skills reference these files during their execution.

This skill follows the same pattern as `gws-shared`: it provides reusable rules and templates that multiple skills need.

## Reference Files

| File | When to read | What it provides |
|---|---|---|
| `references/output_template.md` | Before structuring the report | Standard report structure, including the 7 Layers of Learning headings |
| `references/summarise.md` | Before generating any summary | TC summary quality rules, Two-Zone rule, and 7-layer guiding questions |
| `references/ai_analysis.md` | Before generating the AI analysis | Field definitions, `data/goals.md` + `data/user_preferences.md` calibration instructions |
| `references/suggestion_log.md` | After generating the AI analysis | Append format and rules for `data/suggestions_pending.md` |
| `references/filename_rules.md` | Before writing any report file | Path sanitisation and directory naming convention |
