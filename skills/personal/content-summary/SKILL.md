---
name: content-summary
description: "Shared content summarisation and AI analysis pipeline. Provides reusable references for thesis-driven analysis quality rules, AI analysis with user-preference calibration, and suggestion logging. Referenced by ingest skills (ingest-newsletter, ingest-threads, ingest-youtube, ingest-website). Do not invoke this skill directly."
---

# content-summary

Shared reference library for the content intelligence pipeline. **Do not invoke directly** — ingest skills reference these files during their execution.

This skill follows the same pattern as `gws-shared`: it provides reusable rules and templates that multiple skills need.

## Reference Files

| File | When to read | What it provides |
|---|---|---|
| `references/output_template.md` | Before structuring the report | Standard report structure (Thesis-Driven Analysis: TL;DR, Core Thesis, Reasoning Map, Reading Decision, Visual Map, AI Analysis) |
| `references/summarise.md` | Before generating any summary | Configurable output language rules, Two-Zone rule (Extraction/Judgement), and thesis-driven guiding questions |
| `references/ai_analysis.md` | Before generating the AI analysis | Field definitions, `data/goals.md` + `data/user_preferences.md` calibration instructions |
| `references/suggestion_log.md` | After generating the AI analysis | Append format and rules for `data/suggestions_pending.md` |
| `references/filename_rules.md` | Before writing any report file | Path sanitisation and directory naming convention |
