# Evolution Log — Output Template

## File Output Rules

- **Default path**: `EvolutionLog.md` at the repo root
- **Single file**: Always produce one Markdown file (not split across multiple files)
- **Language**: Match the language of the existing Evolution Log if updating; otherwise default to English unless the user specifies otherwise

## Document Structure

```markdown
# Evolution Log

A chronicle of how this project evolved — told through the problems I discovered, the options I weighed, the decisions I made, and the new problems that emerged.

---

## The Starting Point

**Date**: [First commit date or project start date]

[1–3 paragraphs: What was the original motivation? What problem was I trying to solve? What was the very first version?]

---

## How to Read This Document

Each section follows the same pattern:

> **🔍 Problem** → **🛤️ Options** → **⚖️ Decision** → **📊 Result** → 🔁 *...which revealed a new problem*

This isn't linear. Solving one problem always uncovered the next. The document traces the actual chain of discoveries as they happened.

---

## Phase N: [Descriptive Title]

**Period**: [Start date] – [End date]
**Key commits**: [Notable commit hashes or references]
[Optional: **Key RFC**: [link], **Key RCA**: [link]]

### 🔍 Problem

[What pain point was discovered? State it as a real experience, not an abstract requirement.]

### 🛤️ Options

1. [Option A] — [brief tradeoff]
2. [Option B] — [brief tradeoff]
3. [Option C] — [brief tradeoff, if rejected state why]

### ⚖️ Decision

[Which option was chosen and why. Explain the reasoning, not just the choice.]

### 📊 Result

[What happened after implementing the decision. Be specific — metrics, behavior changes, new capabilities.]

> 🔁 **New problem discovered**: [What solving this problem revealed — the bridge to the next Phase.]

---

[Repeat Phase sections as needed]

---

## Sidebar: [Title] (optional)

[For notable tangent stories that don't fit the main Phase sequence — e.g., an experiment that was tried and abandoned, or a particularly instructive over-engineering episode. Use the same Problem → Decision → Result format but keep it self-contained.]

---

## Where It Stands Today

**Date**: [Current date]
**Stats**: [commit count] commits, [other relevant stats]

[Architecture diagram or current state description — text-based ASCII art or Mermaid diagram]

### The Evolution at a Glance

| Phase | Period | Core Problem | Key Decision | Outcome |
|:---:|:---|:---|:---|:---|
| 1 | [dates] | [problem] | [decision] | [outcome] |
| 2 | [dates] | [problem] | [decision] | [outcome] |
| ... | ... | ... | ... | ... |

### Key Recurring Patterns

1. **[Pattern name].** [Description of a recurring pattern observed across phases.]
2. **[Pattern name].** [Description.]

---

## What's Next

[2–4 bullet points describing potential next problems/directions, with links to relevant RFCs or backlog items if they exist.]

---

*Last updated: [Today's date]*
```

## Style Notes

- **First person**: "I discovered...", "I chose...", "We built..." — this is a personal narrative
- **Honest about failures**: Don't sanitize — hallucinating agents, over-engineered systems, wrong bets are the interesting parts
- **Specific over generic**: Name actual tools, files, commit hashes, metrics
- **Verified Commit Hashes Only**: Only cite commit hashes verified directly via `git log` or `git cat-file -t`. Never fabricate or simulate commit hashes. If a phase does not have discrete isolated commits, omit the `**Key commits**:` header entirely or use milestone titles instead.
- **Ground Referenced Files in Reality**: Every referenced file or document link must exist in the repository or have verified historical git commits. Never invent unwritten unit test files, phantom templates, or nonexistent backlog anchors.
- **Normalize File Paths**: Use exact repository-relative paths (e.g. `data/user_preferences.md`, `.agents/skills/...`) so references resolve cleanly on disk.
- **Cross-reference with links**: Use relative links to RFCs, RCAs, and other source docs (e.g., `[skill-redesign-dry.md](docs/rfc/skill-redesign-dry.md)`)
- **Bridge between Phases**: Every Phase must end with a "New problem discovered" that connects to the next Phase
- **Summary table**: Must match Phase content exactly — it's the quick-scan entry point for readers
