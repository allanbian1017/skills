# Daily Distiller Skill

## Overview

The `daily-distiller` skill automates the synthesis of today's intelligence reports into a single, high-quality **Knowledge Distillation** document. Instead of surfacing a list of summaries, it reframes raw inputs into a unified technical narrative — capturing what's significant, how concepts connect across sources, and what actions follow.

## Problem Statement

After processing newsletters, Threads posts, and YouTube videos daily, the raw reports pile up in `./reports/`. Reading them one-by-one is time-consuming and makes it easy to miss cross-cutting patterns. The real value is in the *connections* between ideas, not the individual summaries themselves.

## Solution

The skill discovers all of today's reports, reads them holistically, and synthesizes a structured Knowledge Distillation document organized around emergent themes rather than source-by-source recaps.

### Key Features

1. **Automatic Discovery:** Scans `./reports/` for all `.md` files created today (excluding `reports/distillations/`) using file timestamps.
2. **Cross-Source Synthesis:** Groups insights into 2–4 thematic "Major Pillars" named after *concepts*, not sources.
3. **System Thinking:** Includes a "Synthesis" section that explains how pillars relate to each other as a system.
4. **Actionable Takeaway:** Produces a single strategic call-to-action grounded in the day's data.
5. **Idempotent Output:** Re-running on the same day overwrites the existing file (treated as an updated version).

## File Structure

```
daily-distiller/
├── SKILL.md                    # Skill definition and workflow steps
└── assets/
    └── output_template.md      # Output path rules, document structure, and full markdown template
```

> `assets/output_template.md` is the single source of truth for the output format. Edit it to change the document structure, section names, or markdown styling — no need to touch `SKILL.md`.

## Output Location

```
reports/
└── distillations/
    └── Knowledge_Distillation_YYYY_MM_DD.md
```

## Document Structure

Each distillation contains four fixed sections (see `assets/output_template.md` for the full markdown template):

| Section | Purpose |
|---|---|
| **📝 Executive Summary** | The overarching narrative — "What is the big picture theme today?" |
| **🏗️ / 🧩 Major Pillars (2–4)** | Coherent technical themes grouped across sources, named after concepts |
| **🔗 The Synthesis** | How the pillars relate as a system, not just a list |
| **🚀 Strategic Takeaway** | One actionable, philosophically grounded call-to-action |

## Triggering

This skill triggers when the user says:
- "summarize today's reports"
- "distill today's knowledge"
- "run daily distillation"
- "update the knowledge distillation document"

## Quality Standards

- **No 1:1 mapping** — each Pillar must group insights from *multiple* sources
- **Connections over recaps** — the most valuable distillations surface patterns that weren't obvious in individual reports
- **System-level thinking** — prioritize insights that improve the *workflow system*, not just model output

## Changelog

| Version | Date | Change Summary |
|---|---|---|
| v1.0.0 | 2026-04-29 | Initial skill: auto-discover today's reports, synthesize into Knowledge Distillation document with 4-section structure. |
| v1.1.0 | 2026-04-30 | **Output template extraction**: Moved inline document structure and markdown template out of `SKILL.md` into `assets/distillation_v1.md` for easier modification. |
| v1.2.0 | 2026-04-30 | **Template consolidation**: Merged `assets/distillation_v1.md` and `assets/output_template.md` into a single `assets/output_template.md`. Translated all skill content to English. |
| v1.3.0 | 2026-06-16 | Made output language globally configurable, defaulting to English and preferring Traditional Chinese. |
