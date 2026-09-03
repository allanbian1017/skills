---
name: agent-rules-reviewer
description: Audit, streamline, and refactor agent steering documents (AGENTS.md, CLAUDE.md, .cursorrules). Eliminates redundancies, base-model knowledge bloat, and system prompt conflicts; applies Addy Osmani's 3-Tier Agent Rules Architecture (Always Do, Ask First, Never Do) and Attention Budget Governance to cut rule drift and minimize token consumption. Use whenever the user asks to "review AGENTS.md", "audit AGENTS.md", "clean up AGENTS.md", "refactor AGENTS.md", "apply 3-tier rules", "audit CLAUDE.md", "optimize agent rules", "review my agent instructions", or mentions "attention budget governance for rules".
---

# Agent Rules Reviewer (`agent-rules-reviewer`)

Audit, streamline, and restructure agent steering documents (`AGENTS.md`, `CLAUDE.md`, or custom rule files) using Addy Osmani's **3-Tier Agent Rules Architecture** and **Attention Budget Governance**.

This skill reduces token overhead by 40–50%, removes repetitive negative constraints (`DO NOT`, `NEVER`), eliminates generic aphorisms, and prevents rule drift while maintaining a strict **Propose-then-Confirm** safety gate.

---

## Reference Documents

Read these on-demand references during execution:

| File | When to Read | Purpose |
|---|---|---|
| `references/three_tier_architecture.md` | Before structuring tiers | Definitions, examples, and conversion heuristics for Tier 1 (Always Do), Tier 2 (Ask First), and Tier 3 (Never Do). |
| `references/audit_criteria.md` | During file analysis | 5-vector audit guidelines (Self-Duplication, Base LLM Baseline, System Conflicts, Skill Leakage, Negative Bloat). |
| `references/review_template.md` | Before generating artifact | Standard markdown schema for the `agent_rules_review.md` artifact. |

---

## 4-Stage Execution Workflow

```
[1. Measure & Audit] ──> [2. 5-Vector Triage] ──> [3. 3-Tier Restructuring] ──> [4. Artifact & Confirm Gate]
```

### Stage 1: Resolve Target File & Measure Baseline
1. Identify target file: Default to `./AGENTS.md` at the repository root if no argument is specified. If the user provides a custom path (e.g., `CLAUDE.md`, `.cursorrules`), target that file.
2. Read the file contents completely.
3. Compute baseline metrics via LLM inspection:
   - Total line count.
   - Estimated token count (~4 characters per token).
   - Frequency of restrictive keywords: `MUST`, `NEVER`, `ALWAYS`, `DO NOT`, `MUST NOT`.
   - Identified sections and structural organization.

### Stage 2: 5-Vector Audit & Pruning
Consult `references/audit_criteria.md` and evaluate every rule against the 5 vectors:
- **Vector 1 (Self-Duplication)**: Flag rules repeated across different sections (e.g. testing rules stated multiple times). Consolidate into a single canonical tier entry.
- **Vector 2 (Base LLM Baseline)**: Prune common-sense software engineering aphorisms ("write clean code", "don't make hacky fixes"). Replace with deterministic automated test gates where applicable.
- **Vector 3 (System Prompt Conflicts)**: Detect ambiguities or clashes with the host AI environment (e.g., scoping `file:///` URLs vs relative repo paths).
- **Vector 4 (Skill Domain Leakage)**: Identify deep domain rules that belong in specialized `SKILL.md` files (e.g., ingestion/summarization schemas) and delegate them.
- **Vector 5 (Negative Constraint Bloat)**: Reframe negative `DO NOT` clauses into positive Tier 1 conventions or concise Tier 3 invariants.

### Stage 3: Restructure into 3 Tiers
Consult `references/three_tier_architecture.md` to map all surviving rules into the 3 tiers:

1. **Tier 1: Always Do (Safe Defaults & Deterministic Automation)**:
   - Autonomous, zero-friction actions (automated test verifications, linting, directory deduplication scans, checking `known_issues.md`).
2. **Tier 2: Ask First (Human-in-the-Loop & Approval Gates)**:
   - Actions with high blast radius or ambiguity (architecture changes, database schema updates, RCA fix proposals, modifying core steering contracts).
3. **Tier 3: Never Do (Hard Invariants & Inviolable Boundaries)**:
   - Absolute red lines (committing raw credentials, tool circumvention / unauthorized fallback scripts, scope creep).

Aim for a **40–50% reduction in line count and token size**, keeping the refactored document concise, dense, and unambiguous.

### Stage 4: Deliver Artifact & Propose-then-Confirm Safety Gate
1. **Generate Review Artifact**: Write the complete audit findings, metrics comparison table, and full proposed refactored markdown to an artifact named `agent_rules_review.md` using the template in `references/review_template.md`.
2. **Inline Chat Summary**: Output a concise summary in the chat window highlighting:
   - Quantitative reductions (Lines, Tokens, Negative Keywords).
   - Key redundancies removed and conflicts resolved.
   - Link/pointer to the `agent_rules_review.md` artifact.
   - An explicit confirmation prompt asking the user to approve or adjust before applying.
3. **Wait for User Confirmation**:
   - **STOP**. Do NOT modify the target file on disk until the user explicitly confirms (e.g. "Approve" or "Apply").
   - Once confirmed, execute the in-place write to the target file.
   - If the user requests adjustments, refine the proposal and update the artifact.
