# evolution-log Skill

## Overview

`evolution-log` is an automated skill for generating and maintaining a narrative development history (**Evolution Log**) of a project. It tells the story of a software project's evolution through iterative problem-solving cycles:

> **🔍 Problem** → **🛤️ Options** → **⚖️ Decision** → **📊 Result** → 🔁 **New Problem**

It compiles evidence from repository artifacts—including Git commit logs, RFC documents (`docs/rfc/`), Root Cause Analysis reports (`docs/rca/`), Architecture Decision Records (`docs/adr/`), Implementation Plans (`docs/plan/`), `README.md` changes, and Agent Skills (`.agents/skills/`)—into a unified `EvolutionLog.md` file.

---

## Problem Statement

As projects mature over months of development, engineering decisions, trade-offs, and lessons learned become scattered across hundreds of Git commits, design documents, and post-mortems. New contributors or team members struggle to understand:
- *Why* the current architecture was chosen over alternatives.
- *What* problems prompted key refactorings or system redesigns.
- *How* past failures (RCAs) led to current guardrails and system safety checks.

`evolution-log` solves this by synthesizing technical artifacts into a single, chronological narrative document.

---

## File Structure

```
.agents/skills/evolution-log/
├── SKILL.md                        # Main skill instructions & trigger definitions
├── README.md                       # Documentation & usage guide (this file)
├── references/
│   └── output_template.md          # Canonical Markdown layout & narrative format
└── evals/
    └── evals.json                  # Test prompts for evaluating skill performance
```

---

## Core Capabilities & Modes

The skill operates in two distinct modes depending on whether an `EvolutionLog.md` already exists:

### 1. Generate Mode (From Scratch)
- Scans full Git commit history and all discovery paths (`docs/rfc/`, `docs/rca/`, `.agents/skills/`, `README.md`, etc.).
- Groups history into chronological **Phases** based on major technical shifts and architectural decisions.
- Formats each phase using the 5-element narrative cycle.
- Generates a complete `EvolutionLog.md` with an executive introduction, phase breakdown, summary table, recurring patterns, and "What's Next" section.

### 2. Update Mode (Incremental)
- Reads the existing `EvolutionLog.md` and parses the timestamp of the last recorded phase.
- Diffs git history and scans for newly added decision documents since the last update:
  ```bash
  git log --format="%ad %s" --date=short --since="YYYY-MM-DD" --reverse
  ```
- Appends new phases or extends the active phase without mutating or deleting historical phases.
- Updates the summary matrix, recurring patterns, and "Last updated" metadata.

---

## Source Material Discovery

The skill searches for evidence across standard repository locations:

| Source Type | Extracted Knowledge | Target Locations / Commands |
|:---|:---|:---|
| **Git Commit Timeline** | Milestone dates & commit context | `git log --format="%ad %s" --date=short --reverse` |
| **RFCs & Design Docs** | Problems, considered options, decision rationale | `docs/rfc/`, `docs/design/`, `rfcs/` |
| **RCAs & Post-Mortems** | Triggering failures & corrective guardrails | `docs/rca/`, `docs/postmortems/` |
| **Implementation Plans** | Execution breakdown & verification criteria | `docs/plan/`, `docs/plans/` |
| **Agent Skills** | Capability evolution & tool refactoring | `.agents/skills/`, `skills/`, `.claude/skills/` |
| **README.md** | Core system overview & architectural changes | `README.md` |
| **Backlog & Issues** | Future problems for "What's Next" | `backlog.md`, `TODO.md` |

---

## Invocation & Triggers

This skill can be invoked via natural language prompts, including:
- `"Update my evolution log"`
- `"Add recent changes to the evolution log"`
- `"Generate an evolution log for this project"`
- `"Document the development journey of this repository"`
- `"Chronicle project history from git and RFCs"`

---

## Quality Rules & Guidelines

1. **First-Person Narrative**: Written in first-person ("I discovered...", "We chose...") to capture the authentic engineering experience.
2. **Honesty About Failures**: Preserves post-mortem insights (RCAs), failed experiments, and over-engineering episodes (e.g., in dedicated *Sidebar* sections).
3. **Traceability**: All referenced RFCs, RCAs, and decision docs must use valid relative workspace Markdown links.
4. **Non-Destructive Updates**: In Update Mode, pre-existing phases are never overwritten or deleted.
