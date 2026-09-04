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
- Executes mandatory Step 7 audit pass before completing.

### 3. Audit Mode (Verification & Remediation)
- Audits an existing `EvolutionLog.md` for broken links, nonexistent files, phantom commit hashes, and stats drift.
- Employs context-aware git history checking to separate hallucinated phantom files from legitimate historically deleted/renamed artifacts.
- Enforces an intent-driven, propose-then-confirm workflow: presents detailed findings/diffs in an Artifact and requires explicit user confirmation before applying in-place edits.

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
- `"Audit my evolution log"`
- `"Check evolution log for missing files or commits"`
- `"Clean up evolution log"`
- `"Document the development journey of this repository"`
- `"Chronicle project history from git and RFCs"`

---

## Quality Rules & Guidelines

1. **First-Person Narrative**: Written in first-person ("I discovered...", "We chose...") to capture the authentic engineering experience.
2. **Honesty About Failures**: Preserves post-mortem insights (RCAs), failed experiments, and over-engineering episodes (e.g., in dedicated *Sidebar* sections).
3. **Traceability**: All referenced RFCs, RCAs, and decision docs must use valid relative workspace Markdown links.
4. **Non-Destructive Updates**: In Update Mode, pre-existing phases are never overwritten or deleted.
5. **Ground Truth Verification**: All cited commit hashes must be validated in git (`git cat-file -t`); all cited files must be grounded on disk or in git history.

---

## Architecture Decision Records (ADRs)

### ADR-001: Zero-Script Agent-Pure Audit Function & Propose-then-Confirm Safety Gate

- **Status**: Accepted
- **Date**: 2026-09-04
- **Context**: When generating long-form development chronicles, LLMs frequently suffer from "template gravity" and hallucinate plausible-looking commit hashes (e.g. `dbf897c`) and test suite files (`tests/test_output_template.py`) that never existed in the repository. We required a robust audit mechanism to detect, report, and clean up these phantom artifacts without accumulating maintenance overhead.
- **Options Considered**:
  1. *Bespoke Helper Script (`scripts/audit_evolution_log.py`)*: A dedicated Python CLI tool with automated unit tests. Rejected: violates the repository's *Zero-Script Agent Skill Design* preference, adding maintenance burden and test harness overhead for a single-use skill script.
  2. *Prompt-Only Negative Constraints*: Explicit instructions telling the model "Never invent commits". Rejected: empirical testing proved abstract negative constraints are easily overridden by in-context narrative priors during long multi-step reasoning.
  3. *Agent-Pure Shell Inspection with Propose-then-Confirm Gate*: Chosen. Embeds deterministic shell inspection commands (`git cat-file -t`, `test -f`, inline Python one-liners) directly into `SKILL.md`. Uses git history checks to distinguish phantom files from legitimate historically deleted artifacts. Implements a propose-then-confirm gate before applying any in-place modifications to living documentation.
- **Consequences**:
  - Positive: Eliminates script maintenance overhead while guaranteeing 100% verification against actual git objects and the filesystem.
  - Positive: Propose-then-confirm workflow gives users complete oversight over file modifications.
  - Trade-off: Inspection steps execute as inline tool commands during agent turns rather than a single precompiled binary call.

---

## Changelog

### 2026-09-04
- Added **Audit Mode** for validating commit hashes, markdown links, and file references in existing Evolution Logs.
- Enforced mandatory **Step 7 (Save, Audit and Verify)** quality gate across Generate and Update modes to ensure zero phantom artifacts.
- Added ADR-001 documenting the Zero-Script Agent-Pure Audit architecture and Propose-then-Confirm safety gate.
- Expanded output template rules to mandate verified commit hashes and exact repository relative paths.
