# content-summary Skill

## Overview

`content-summary` is a **reference library** for the content intelligence pipeline. It provides shared rules and templates consumed by `ingest-newsletter`, `ingest-threads`, and `ingest-youtube`. It is never invoked directly.

This follows the same pattern as `gws-shared`: a central dependency that multiple skills read from, eliminating copy-paste duplication.

## Problem Statement

Before this library existed, summarisation rules, AI analysis structure, suggestion logging logic, and filename conventions were copy-pasted across `newsletter-summary`, `process-delegate-tasks`, and their output templates. Adding a new analysis field required updating three separate places, creating drift and maintenance risk.

## Solution

Extract all shared logic into four canonical reference files. Each ingest skill reads the relevant file(s) at the appropriate step using progressive disclosure (`> 📄 Read ../content-summary/references/...`).

## File Structure

```
content-summary/
├── SKILL.md                        # Index of reference files and when to use them
├── README.md                       # This file
└── references/
    ├── summarise.md                # TC summary quality rules (Zero Hallucination, etc.)
    ├── ai_analysis.md              # AI analysis field definitions and calibration instructions
    ├── suggestion_log.md           # Append format for data/suggestions_pending.md
    └── filename_rules.md           # Path sanitisation and directory naming convention
```

## Reference Files

| File | When to read | What it provides |
|---|---|---|
| `references/summarise.md` | Before generating any summary | Zero Hallucination, Comprehensiveness, Objectivity, Teaser Detection |
| `references/ai_analysis.md` | Before generating AI analysis | Field definitions, `data/goals.md` + `data/user_preferences.md` calibration |
| `references/suggestion_log.md` | After generating AI analysis | Append format and rules for `data/suggestions_pending.md` |
| `references/filename_rules.md` | Before writing any report file | Path sanitisation, `{SourceType}_YYYY_MM_DD/` directory convention |

## Consumers

| Skill | References used |
|---|---|
| `ingest-newsletter` | `summarise.md`, `ai_analysis.md`, `suggestion_log.md`, `filename_rules.md` |
| `ingest-threads` | `summarise.md`, `ai_analysis.md`, `suggestion_log.md`, `filename_rules.md` |
| `ingest-youtube` | `summarise.md`, `ai_analysis.md`, `suggestion_log.md`, `filename_rules.md` |
| `daily-workflow` | All four (directly, for YouTube post-processing step) |

## Do Not Invoke Directly

This skill has no trigger phrases. It has no executable procedure. If you find yourself writing "use content-summary to…", you are doing it wrong — use an ingest skill instead.

## Changelog

| Version | Date | Change Summary |
|---|---|---|
| v1.0.0 | 2026-05-08 | Initial creation: extracted `summarise.md`, `ai_analysis.md`, `filename_rules.md` from `newsletter-summary` and `process-delegate-tasks`. |
| v1.1.0 | 2026-05-13 | Added `suggestion_log.md` (was missing from initial extraction). Updated `SKILL.md` table to include it. |
