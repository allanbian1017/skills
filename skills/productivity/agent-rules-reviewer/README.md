# Agent Rules Reviewer (`agent-rules-reviewer`)

## Overview

The `agent-rules-reviewer` skill audits, streamlines, and refactors agent steering documents (such as `AGENTS.md`, `CLAUDE.md`, and `.cursorrules`). It eliminates self-duplications, cuts baseline LLM knowledge bloat, resolves system prompt conflicts, and restructures rules into Addy Osmani's **3-Tier Agent Rules Architecture** with **Attention Budget Governance** (addressing [backlog.md](../../../backlog.md) Item #63).

The skill follows a strict **Propose-then-Confirm** safety gate: it calculates quantitative attention metrics, identifies redundancies, and presents a complete 3-tier drop-in proposal inside a Brain Artifact (`agent_rules_review.md`) before requesting explicit user approval to apply any changes in-place.

---

## Problem Statement

As AI agent systems evolve, project steering documents (`AGENTS.md`) accumulate negative micro-rules, redundant directives, and ad-hoc instructions across different sessions. This causes:

1. **Semantic Redundancy (40–50% token bloat)**: Critical constraints (such as automated testing mandates or anti-overengineering rules) end up repeated 3 to 4 times across different sections.
2. **Attention Degradation ("Rule Drift")**: Dense lists of negative constraints (`DO NOT`, `NEVER`, `MUST NOT`) exhaust the model's self-attention budget, paradoxically increasing rule violation rates during complex multi-step reasoning.
3. **Baseline Knowledge Bloat**: Common-sense software development aphorisms ("write clean code", "don't make hacky fixes") consume prompt tokens without providing verifiable enforcement mechanisms.
4. **Environment & Host Conflicts**: Rules forbidding specific link schemes (e.g. `file:///`) create unresolved tension with IDEs or host AI assistants that natively require clickable URI links in conversation streams.

---

## Solution: 4-Stage Audit Workflow

The skill executes a 4-stage Lean Spine pipeline:

```
[1. Measure & Audit] ──> [2. 5-Vector Triage] ──> [3. 3-Tier Restructuring] ──> [4. Artifact & Confirm Gate]
```

1. **Measure & Audit**: Calculate baseline metrics (total lines, estimated tokens, frequency of negative keywords `MUST`, `NEVER`, `ALWAYS`, `DO NOT`).
2. **5-Vector Triage**: Classify existing rules across 5 evaluation vectors:
   - *Vector 1 (Self-Duplication)*: Consolidate scattered copies of the same constraint into a single canonical tier entry.
   - *Vector 2 (Base LLM Baseline)*: Prune common-sense aphorisms; replace with deterministic automated test gates.
   - *Vector 3 (System Prompt Conflicts)*: Clarify boundaries (e.g., scoping `file:///` restrictions to committed workspace docs vs chat responses).
   - *Vector 4 (Skill Domain Leakage)*: Move deep operational procedures to specialized `SKILL.md` files.
   - *Vector 5 (Negative Constraint Bloat)*: Reframe negative prohibitions into positive conventions or concise invariants.
3. **3-Tier Restructuring**: Organize surviving directives into:
   - **Tier 1: Always Do** (Autonomous safe defaults, testing, linting, directory scans).
   - **Tier 2: Ask First** (Human-in-the-loop review gates, architecture changes, core contract edits).
   - **Tier 3: Never Do** (Hard invariant redlines, raw credentials, tool circumvention, scope creep).
4. **Deliver Artifact & Confirmation Gate**: Render the full audit report, before/after metrics table, and proposed replacement inside an `agent_rules_review.md` artifact alongside an inline chat summary. Halts until explicit user approval is granted.

---

## File Structure

```
agent-rules-reviewer/
├── SKILL.md                          # Lean Spine (<200 lines) defining triggers and workflow
├── README.md                         # This file: documentation, architecture, and ADRs
├── evals/
│   └── evals.json                    # Benchmark test scenarios (AGENTS.md, CLAUDE.md, legacy rules)
└── references/
    ├── three_tier_architecture.md    # Addy Osmani 3-Tier model & Attention Budget Governance
    ├── audit_criteria.md             # Detailed rubric for the 5 audit vectors
    └── review_template.md            # Standard markdown schema for the review artifact
```

### Related Workspace Documents

* **RFC**: [docs/rfc/agent-rules-reviewer.md](../../../docs/rfc/agent-rules-reviewer.md)
* **Plan**: [docs/plan/agent-rules-reviewer-plan.md](../../../docs/plan/agent-rules-reviewer-plan.md)
* **Task Checklist**: [docs/plan/agent-rules-reviewer-task.md](../../../docs/plan/agent-rules-reviewer-task.md)
* **Test Suite**: [tests/test_agent_rules_reviewer.py](../../../tests/test_agent_rules_reviewer.py)

---

## Triggering

This skill triggers whenever the user asks to:
* *"review AGENTS.md"* / *"audit AGENTS.md"* / *"clean up AGENTS.md"*
* *"refactor AGENTS.md"* / *"apply 3-tier rules"*
* *"audit CLAUDE.md"* / *"review my agent instructions"*
* *"optimize agent rules"* / *"attention budget governance for rules"*

---

## Architecture Decision Records (ADRs)

### ADR-001: Adopt Addy Osmani 3-Tier Agent Rules Architecture & Attention Budget Governance
* **Status**: Accepted
* **Context**: Monolithic, flat rule files with dozens of negative micro-rules (`NEVER`, `DO NOT`) cause attention saturation and rule drift in frontier LLMs.
* **Decision**: Adopt the 3-Tier model (Tier 1: Always Do, Tier 2: Ask First, Tier 3: Never Do). Reframe negative micro-rules into positive autonomous defaults or concise hard invariants.
* **Consequences**:
  * *Positive*: Achieves 40–50% token reduction, clarifies human-in-the-loop boundaries, eliminates rule drift.
  * *Negative*: Legacy unclassified rules require one-time triage to map into tiers.

### ADR-002: Zero-Script Pure LLM Inspection Architecture
* **Status**: Accepted
* **Context**: We evaluated bundling a Python CLI script (`scripts/audit_rules.py`) to measure line counts, token estimates, and regex duplicates.
* **Decision**: Rely purely on agent LLM reasoning and inspection without auxiliary scripts to eliminate codebase maintenance overhead.
* **Consequences**:
  * *Positive*: Zero extra code dependencies or script maintenance in `scripts/`.
  * *Negative*: Token counts are calculated via heuristic character ratios (~4 chars/token) rather than exact byte tokenizers.

### ADR-003: Propose-then-Confirm Safety Gate via Brain Artifact
* **Status**: Accepted
* **Context**: `AGENTS.md` is the central steering contract for agent behavior. Autonomous in-place rewrites risk deleting vital project constraints without human oversight.
* **Decision**: Enforce an explicit two-stage gate. The skill generates a comprehensive audit and proposed draft in a dedicated Brain Artifact (`agent_rules_review.md`), outputs a concise chat summary, and halts execution until the user explicitly responds with approval.
* **Consequences**:
  * *Positive*: High safety, zero accidental loss of rules, dedicated UI artifact for granular commenting and diff review.
  * *Negative*: Requires an interactive two-turn confirmation rather than a single-turn automatic overwrite.

### ADR-004: Multi-Platform Rule Scope
* **Status**: Accepted
* **Context**: Different AI developer tools and environments rely on different configuration files (e.g. `AGENTS.md`, `CLAUDE.md`, `.cursorrules`).
* **Decision**: Default to `./AGENTS.md` at workspace root when invoked without arguments, but accept an optional file path parameter to support multi-platform and cloud environments.
* **Consequences**:
  * *Positive*: Zero-friction default workflow with multi-platform flexibility.
  * *Negative*: Requires path existence verification when custom paths are provided.

---

## Quality Standards & Benchmarks

| Dimension | Standard | Target Metric |
|---|---|---|
| **Lean Spine Budget** | Core `SKILL.md` line count | < 200 lines (currently 78 lines) |
| **Attention Savings** | Reduction in target rule file lines & tokens | $\ge 40\%$ reduction |
| **Negative Compaction** | Density of `DO NOT` / `NEVER` / `MUST NOT` | Reframed into positive Tier 1 or $\le 5$ Tier 3 invariants |
| **Safety Gate** | In-place file modification | Mandatory explicit user confirmation before disk write |
| **Frontmatter Validation** | `scripts/validate_skill.py` | Exit code 0 |

---

## Changelog

| Version | Date | Changes |
|---|---|---|
| **v1.0.0** | 2026-09-03 | Initial release: Lean Spine `SKILL.md`, 5-vector audit model, 3-Tier architecture references, review artifact template, evals benchmark, and automated unit test suite. |
