# Review Template: `agent_rules_review.md`

Use this standard markdown structure when generating the review artifact for the user.

---

```markdown
# Agent Rules Audit & 3-Tier Refactoring Proposal: [Target File Path]

> **Target File**: `[Path, e.g., AGENTS.md or CLAUDE.md]`  
> **Date**: [YYYY-MM-DD]  
> **Auditor**: `agent-rules-reviewer` skill  

---

## 1. Attention Budget & Telemetry Summary

| Metric | Before Audit | Proposed Refactor | Delta (%) |
|---|---|---|---|
| **Total Lines** | [N] lines | [N] lines | -[X]% |
| **Estimated Tokens** | ~[N] tokens | ~[N] tokens | -[X]% |
| **Negative Constraints** (`NEVER`, `DO NOT`, `MUST NOT`) | [N] occurrences | [N] occurrences | -[X]% |
| **Structure** | Flat / Fragmented | Addy Osmani 3-Tier Architecture | Standardized |

---

## 2. Audit Findings by Vector

### Vector 1: Self-Duplication & Redundancies
* **[Topic 1]**: Stated in Line [X] and repeated in Line [Y]. *Remedy*: Consolidated into [Tier N].
* **[Topic 2]**: Repeated across multiple sections. *Remedy*: Preserved single canonical entry.

### Vector 2: Base LLM Baseline (Aphorisms & Generic Hygiene)
* **[Clause 1]**: Generic common sense ("..."). *Remedy*: Pruned / Replaced with automated test assertion.

### Vector 3: Host Environment & System Prompt Conflicts
* **[Conflict 1]**: Unscoped directive clashing with host environment (e.g. `file:///` links). *Remedy*: Explicitly scoped to committed workspace documents.

### Vector 4: Skill Domain Leakage
* **[Instruction 1]**: Operational detail belonging in specialized skill. *Remedy*: Delegated to relevant skill (`SKILL.md`).

### Vector 5: Negative Constraint Compaction
* Recompacted [N] prohibitive rules into positive Tier 1 conventions and [N] Tier 3 hard invariants.

---

## 3. Proposed 3-Tier Refactored Ruleset

The full proposed drop-in replacement for `[Target File Path]` is provided below:

```markdown
[Paste full 3-tier refactored markdown here]
```

---

## 4. User Review & Confirmation Checkpoint

> [!IMPORTANT]
> This proposal is currently staged in review mode. No changes have been written to disk.
> 
> - To approve and apply this refactoring in-place, reply: **"Approve"** or **"Apply"**.
> - To adjust specific rules, reply with your requested modifications.
> - To reject this proposal, reply: **"Reject"**.
```
