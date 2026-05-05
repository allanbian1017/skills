# Daily Distiller — Output Template

This file defines the output path, filename convention, and the full document structure for the Knowledge Distillation report.

---

## File Output Rules

- **Directory**: `reports/distillations/`
- **Filename format**: `Knowledge_Distillation_YYYY_MM_DD.md` (use today's local date)
- Re-running on the same day overwrites the existing file (treated as an updated version)

---

## Document Structure

The document contains four fixed sections in this order:

| Section | Purpose |
|---|---|
| **Executive Summary** | The overarching narrative of the day — answer "What is the big picture theme?" |
| **Major Pillars (2–4)** | Group insights into coherent technical themes across sources. Name each section after the *concept*, not the source. |
| **The Synthesis** | Explain how the pillars relate to each other as a *system*, not just a list. |
| **Strategic Takeaway** | One actionable, philosophically grounded call-to-action derived from the day's data. |

### Quality Standards

- **Avoid** one-to-one report-to-pillar mapping — the goal is to *reframe* raw inputs into a unified narrative
- The most valuable distillations surface **connections** that weren't obvious across individual reports

---

## Markdown Template

Use this exact structure when writing the output file:

```markdown
# Knowledge Distillation: [Topic/Title] (YYYY-MM-DD)

## 📝 Executive Summary
[High-level summary of the day's core insights. Focus on the "So What?" and the overarching theme.]

---

## 🏗️ 1. [First Major Pillar]
[Detailed breakdown of the first key concept.]

### [Sub-point / Component]
*   **[Key Term]**: [Explanation].
*   **[Key Term]**: [Explanation].

---

## 🧩 2. [Second Major Pillar]
[Detailed breakdown of the second key concept.]

### [Sub-point / Component]
*   **[Key Term]**: [Explanation].
*   **[Key Term]**: [Explanation].

---

## 🔗 3. The Synthesis: [How Concepts Interconnect]
[Explain the symbiotic relationship or broader system implications of the pillars above.]

1.  **[Synthesis Point 1]**: [Detail].
2.  **[Synthesis Point 2]**: [Detail].
3.  **[Synthesis Point 3]**: [Detail].

---

## 🚀 Strategic Takeaway
[Final "Call to Action" or core philosophy to adopt moving forward.]

---
*Synthesized from: [List of Sources / Reports]*
```
