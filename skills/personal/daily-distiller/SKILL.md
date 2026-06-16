---
name: daily-distiller
description: Reviews today's reports in ./reports/ and generates a synthesized Knowledge Distillation document in reports/distillations/. Use this skill whenever the user asks to "summarize today's reports", "distill today's knowledge", "run daily distillation", or "update the knowledge distillation document". It ensures technical insights about AI Agents and Context Engineering are preserved and systematized.
---

# Daily Distiller

This skill automates reviewing today's intelligence reports and synthesizing them into a high-quality Knowledge Distillation document — capturing what's technically significant, how concepts connect, and what actions follow.

## Workflow

### Step 1: Discover Today's Reports
Find all `.md` files created today in the `./reports/` directory, **excluding** `reports/distillations/`. Use today's local date.

```bash
find reports -not -path "reports/distillations/*" -type f -name "*.md" -newermt "YYYY-MM-DD" ! -newermt "YYYY-MM-DD+1"
```

If no reports are found, notify the user and stop.

### Step 2: Read All Reports
Read every report file in full. Note:
- **Source / Author**: newsletter name, Threads handle, etc.
- **Key technical insights**: Especially those about AI Agents, Context Engineering, Workflow Optimization, and System Architecture.
- **Cross-cutting themes**: Patterns that appear across multiple sources deserve to become a Pillar.

### Step 3: Load the Output Template
Read `assets/output_template.md` — it contains the file output rules (path, filename format), document structure guide, and the full markdown template to follow.

### Step 4: Synthesize
Check `data/user_preferences.md` for the `Preferred Output Language` configuration, and produce the distillation document in that language (defaulting to **English** if not configured). Follow the template structure:

1. **Executive Summary** — Overarching narrative. What is the "big picture theme" of today?
2. **Major Pillars (2–4 sections)** — Group insights into coherent technical themes (not one per source). Name each section for the concept, not the source.
3. **The Synthesis** — Explain how the pillars relate to each other as a system, not just a list.
4. **Strategic Takeaway** — One actionable, philosophical call-to-action grounded in the day's data.

**Quality bar**: Avoid one-to-one report-to-section mapping. The goal is to *reframe* raw inputs into a unified technical narrative. The most valuable distillations surface **connections** that weren't obvious in the individual reports.

### Step 5: Save Output
Follow the file output rules in `assets/output_template.md`:
```
reports/distillations/Knowledge_Distillation_YYYY_MM_DD.md
```
Use today's local date in the filename.

---

## Principles (from docs/workflow/synthesis.md)
- **System over Model**: Prioritize insights that improve the *system* (context, workflows, rules), not just the model output.
- **Explicit vs. Implicit**: Actively identify "Explicit Knowledge" that can be codified into AI Skills vs. "Implicit Knowledge" that remains a human edge.
- **Compounding Experience**: High-quality outputs become templates. Treat this document as a long-term asset.
