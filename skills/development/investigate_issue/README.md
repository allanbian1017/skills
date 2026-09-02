# 🔍 `investigate_issue` Skill

> **Autonomous Issue Resolution Pipeline** — triages a reported bug, investigates root cause with forensic evidence, produces a structured RCA with reproduction test, runs an internal quality review, waits for your approval, then implements and merges the fix.

---

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [How to Use](#how-to-use)
- [Pipeline Walkthrough](#pipeline-walkthrough)
  - [Phase 1 — Issue Triage](#phase-1--issue-triage)
  - [Phase 2 — Root Cause Investigation](#phase-2--root-cause-investigation)
  - [Phase 3 — Internal RCA Review](#phase-3--internal-rca-review)
  - [Phase 4 — Human Review Gate](#phase-4--human-review-gate)
  - [Phase 5 — Fix Implementation](#phase-5--fix-implementation)
  - [Phase 6 — Code Review](#phase-6--code-review)
  - [Phase 7 — Merge & Update RCA](#phase-7--merge--update-rca)
- [File Conventions](#file-conventions)
- [Related Skills](#related-skills)
- [When NOT to Use](#when-not-to-use)
- [Architecture Decisions (ADRs)](#architecture-decisions-adrs)
- [Changelog](#changelog)

---

## Overview

`investigate_issue` is the **diagnostic and resolution arm** of the autonomous agent pipeline. It orchestrates specialized sub-agents through a seven-phase pipeline with an investigation review board model: issues are triaged, root causes are identified with quantitative evidence, an internal reviewer challenges the diagnosis, the human approves the RCA, and the fix is implemented via TDD prove-it and delivered as a reviewed PR.

```
┌─────────────────────────────────────────────────────────┐
│  Phase 1: Issue Triage (Parent agent)                   │
│                                                         │
│  Parse input (#42 or inline text) → Generate slug       │
│    → Pass issue context to investigator                 │
│                                                         │
├─────────────────────────────────────────────────────────┤
│  Phase 2: Root Cause Investigation (Investigator)       │
│                                                         │
│  Explore codebase → Reproduce bug → Form hypotheses     │
│    → Reject with evidence → Write reproduction test     │
│    → Write RCA document                                 │
│                                                         │
├─────────────────────────────────────────────────────────┤
│  Phase 3: Internal RCA Review (RCA Reviewer)            │
│                                                         │
│  Challenge evidence → Validate root cause               │
│    → Check test quality → Review fix strategy           │
│    → Internal loop (max 3 rounds)                       │
│                                                         │
├─────────────────────────────────────────────────────────┤
│  Phase 4: Human Review Gate                             │
│                                                         │
│  Present RCA → Wait for USER "Approved"                 │
│    → If rejected: Investigator revises → RCA Reviewer   │
│    → Re-present (no cap on rounds)                      │
│                                                         │
├─────────────────────────────────────────────────────────┤
│  Phase 5: Fix Implementation (Engineer sub-agent)       │
│                                                         │
│  Copy test + RCA to worktree → Verify RED               │
│    → Implement fix (GREEN) → Full suite → PR            │
│                                                         │
├─────────────────────────────────────────────────────────┤
│  Phase 6: Code Review (Code Reviewer sub-agent)         │
│                                                         │
│  Review fix against RCA → Internal loop (max 3 rounds)  │
│    → Halt → Wait for USER "Approved"                    │
│                                                         │
├─────────────────────────────────────────────────────────┤
│  Phase 7: Merge & Update RCA                            │
│                                                         │
│  Merge PR → Clean worktree → Update RCA checklist       │
└─────────────────────────────────────────────────────────┘
```

### Investigation & Resolution Board Roles

| Role | Owner | Purpose |
|---|---|---|
| Issue Triage & Decision Orchestrator | Parent agent | Parses input, routes artifacts, copies files between worktrees, enforces gates |
| Root Cause Investigator | `investigator` | Reproduces bug, builds evidence-based RCA, writes reproduction test (RED) |
| RCA Quality Gate | `rca-reviewer` | Challenges evidence rigor, hypothesis completeness, test validity, fix strategy |
| Human Reviewer | User | Approves or rejects the RCA (no cap on review rounds) |
| Fix Implementer | `engineer` | Verifies RED test, implements minimal fix (GREEN), creates PR |
| Code Reviewer | `code-reviewer` | Reviews fix PR for correctness, regression risk, scope creep |

---

## Prerequisites

Before invoking this skill, ensure the following are available:

| Requirement | Purpose |
|---|---|
| `assets/templates/rca_template.md` | RCA document structure template |
| `docs/rcas/` directory | Output location for RCA documents |
| `gh` CLI authenticated | For GitHub Issue fetching and PR lifecycle |

The following sub-agents and sub-skills must also be available:

- **Sub-Agents:** `investigator`, `rca-reviewer`, `engineer`, `code-reviewer`
- [`incremental_implement`](../incremental_implement/SKILL.md) — isolated worktree, atomic commits, PR lifecycle, and CI gate
- [`test-driven-development`](../test-driven-development/SKILL.md) — enforces RED → GREEN → Refactor discipline
- [`git-master`](../git-master/SKILL.md) — atomic commits and git operations
- [`review-work`](../review-work/SKILL.md) — automated code review pipeline

---

## How to Use

Type the following command in your AI agent chat:

```
/investigate_issue <issue description or #number>
```

### Examples

```
/investigate_issue users can't log in when password contains special characters
/investigate_issue #42
/investigate_issue API returns 500 on empty payload to /api/v2/orders
```

The agent auto-detects the input format: `#<number>` fetches the GitHub Issue via `gh issue view`; otherwise the inline text is used directly.

---

## Pipeline Walkthrough

### Phase 1 — Issue Triage

The orchestrator is **thin** — it routes and gates, nothing more.

1. **Parse input** — if the argument matches `#<number>`, fetch the issue body via `gh issue view <number> --json title,body,labels`. Otherwise, use the inline text as-is.
2. **Generate slug** — derive a filename slug for artifacts:
   - GitHub Issue: `42_login-special-chars`
   - Inline text: `login-special-chars-bug`
3. **Delegate** — pass the issue context to the **investigator** sub-agent.

---

### Phase 2 — Root Cause Investigation

The **investigator** sub-agent performs forensic diagnosis with full command execution and write tools.

1. **Explore** — read relevant codebase sections, search for error messages, identify affected components.
2. **Reproduce** — run commands to trigger the bug. Capture actual vs. expected output as quantitative evidence.
3. **Hypothesize & Reject** — form alternative hypotheses. Systematically reject each with measured evidence. Unverifiable claims are labeled "Hypothesis" per AGENTS.md rules.
4. **Root Cause** — identify primary and contributing root causes with direct code/data evidence.
5. **Write Reproduction Test** — create a test file in the existing test directory following project conventions. The test must **fail** (RED), proving the bug exists.
   - If unable to reproduce: write a partial RCA with root cause labeled as "Hypothesis".
6. **Write RCA Document** — save to `docs/rcas/rca_<slug>.md` following the [RCA template](assets/templates/rca_template.md).
7. **Report** — return RCA file path and test file path to the orchestrator.

---

### Phase 3 — Internal RCA Review

The **rca-reviewer** sub-agent challenges the investigator's work before the human sees it.

Review criteria:
- **Evidence rigor** — are hypotheses rejected with quantitative data?
- **Root cause vs. symptom** — is it the actual root cause or a surface-level observation?
- **Reproduction test quality** — does the test prove the real bug?
- **Fix strategy soundness** — simplest viable approach?
- **Missing hypotheses** — unexplored alternatives?
- **Template compliance** — follows `.agents/skills/investigate_issue/assets/templates/rca_template.md`?

**Internal loop** (max 3 rounds): if blocking issues are found, the investigator revises and the reviewer re-reviews. Loop until approved or cap reached.

---

### Phase 4 — Human Review Gate

1. Present the internally-approved RCA to the user.
2. **If rejected** — user feedback goes back to the investigator. The revised RCA must pass the rca-reviewer again before re-presenting to the user. **No cap** on human review rounds.
3. **If approved** — proceed to the fix phase.

---

### Phase 5 — Fix Implementation

The **engineer** sub-agent implements the fix in an isolated worktree.

1. **Orchestrator setup** — create worktree via `incremental_implement`, copy the reproduction test and RCA document into it.
2. **Verify RED** — run the reproduction test, confirm it fails for the right reason. If the test is wrong, fix it first.
3. **GREEN** — implement the minimal fix to pass the test.
4. **Full suite** — run all tests. Fix regressions caused by the change; escalate unrelated failures.
5. **Refactor** — clean up without changing behavior.
6. **Commit & PR** — atomic commits, push, create PR.

---

### Phase 6 — Code Review

The **code-reviewer** sub-agent reviews the fix PR.

1. Review against the RCA, reproduction test, and coding standards.
2. Focus: fix correctness, regression risk, scope creep, test coverage.
3. **Internal loop** (max 3 rounds): engineer revises on feedback.
4. **Wait for User** — present the approved PR for final sign-off.

---

### Phase 7 — Merge & Update RCA

1. **Merge** — `gh pr merge --squash --delete-branch`.
2. **Cleanup** — `git worktree remove` + `git worktree prune`.
3. **Update RCA** — mark status checklist items complete, append verification results, record merged PR number.

---

## File Conventions

| Path pattern | Role |
|---|---|
| `docs/rcas/rca_<slug>.md` | RCA document (created by investigator, updated after merge) |
| `.agents/skills/investigate_issue/assets/templates/rca_template.md` | RCA template (read-only reference) |
| `tests/` (project convention) | Reproduction test file (created by investigator, committed in fix PR) |

RCA naming examples:

```
docs/rcas/rca_42_login-special-chars.md     ← from GitHub Issue #42
docs/rcas/rca_api-500-empty-payload.md      ← from inline description
```

---

## Related Skills

| Skill | Role in this pipeline |
|---|---|
| [`request_feature`](../request_feature/SKILL.md) | Sibling pipeline: handles feature planning (this skill handles bug resolution) |
| [`implement_task`](../implement_task/SKILL.md) | Sibling pipeline: handles planned feature implementation |
| [`incremental_implement`](../incremental_implement/SKILL.md) | Sub-skill: handles worktree isolation, atomic commits, PR creation, and CI gate |
| [`test-driven-development`](../test-driven-development/SKILL.md) | Sub-skill: enforces RED → GREEN → Refactor cycle (prove-it pattern for bugs) |
| [`review-work`](../review-work/SKILL.md) | Sub-skill: automated code review pipeline |

---

## When NOT to Use

- **Root cause is already known** → use `/implement_task` with TDD prove-it directly.
- **It's a feature request, not a bug** → use `/request_feature <idea>`.
- **The issue is in an external dependency or infrastructure** → investigate manually; this skill operates within the codebase.
- **Simple, obvious one-line fix** → direct edit is faster; this pipeline is overhead for trivial changes.

---

## Architecture Decisions (ADRs)

### ADR-0001: Thin Orchestrator Pattern (v1.0.0)

- **Context:** The orchestrator could either do meaningful pre-work (exploring codebase, identifying affected files) or simply route artifacts between sub-agents. A "fat" orchestrator duplicates work the investigator will do anyway.
- **Decision:** The orchestrator only parses input, generates the issue slug, routes artifacts between phases, copies files between worktrees, and enforces review gates. All investigation work is delegated to the `investigator` sub-agent.
- **Consequences:** Clean separation of concerns. The orchestrator is simple and predictable. Investigation quality depends entirely on the investigator agent's capabilities.

### ADR-0002: Dedicated Investigator Agent (v1.0.0)

- **Context:** The existing `engineer` agent is "focused on translating RFCs into production-ready applications" — a constructive persona. Investigation requires a forensic debugging persona: hypothesis-driven, evidence-gathering, and explicitly non-constructive (diagnose, don't fix).
- **Decision:** Created a dedicated `investigator` sub-agent with full command execution and write tools, but constrained by system prompt to only create new files (RCA + reproduction test) and never modify existing source code.
- **Consequences:** The investigator has the right mindset for diagnosis. Write tools are needed for the RCA document and reproduction test. The system prompt constraint (not tool restriction) prevents source code modification, consistent with how the `engineer` agent is constrained.

### ADR-0003: Investigator Writes Reproduction Test (v1.0.0)

- **Context:** The TDD prove-it pattern requires a failing reproduction test before any fix. Three options were considered: (1) engineer writes the test from RCA prose, (2) investigator includes a draft test in the RCA, (3) investigator writes the actual test file. Option 1 risks the engineer misinterpreting the RCA and fixing the wrong thing. Option 2 produces either a usable test (making the investigator an engineer) or a bad test (wasted work).
- **Decision:** The investigator writes the actual test file in the project's existing test directory. The engineer's first step is to verify the test fails for the right reason before implementing the fix.
- **Consequences:** The reproduction test IS the contract — eliminates ambiguity between diagnosis and fix. The engineer has a safety check (verify RED) to catch bad tests. The investigator needs `test-driven-development` skill awareness for test quality standards.

### ADR-0004: Dedicated RCA Reviewer Agent (v1.0.0)

- **Context:** RCA quality could be ensured by (1) reusing the existing `architecture-reviewer` agent with RCA-specific invocation prompts, or (2) creating a dedicated `rca-reviewer` agent. The `architecture-reviewer` is tuned for system design review (scalability, failure modes, cost tradeoffs) — different criteria than RCA review (evidence rigor, hypothesis completeness, reproduction test validity).
- **Decision:** Created a dedicated `rca-reviewer` sub-agent with review criteria specific to root cause analysis: evidence rigor, root cause vs. symptom distinction, hypothesis completeness, reproduction test validity, fix strategy soundness, and template compliance.
- **Consequences:** The reviewer is purpose-built for RCA quality. Adds one agent definition file. The review criteria are explicit and structured, producing actionable feedback with severity levels (Blocking/Suggestion).

### ADR-0005: Orchestrator File Handoff Between Worktrees (v1.0.0)

- **Context:** The investigator writes the reproduction test and RCA in the main worktree. The engineer works in an isolated worktree created by `incremental_implement`. Three options were considered: (1) share the worktree between investigator and engineer, (2) investigator commits to `dev` and engineer branches from it, (3) orchestrator copies files into the engineer's worktree.
- **Decision:** The orchestrator copies the reproduction test and RCA document from the main worktree into the engineer's isolated worktree, preserving directory structure. The investigator's files remain uncommitted in the main worktree.
- **Consequences:** Investigation and fix phases are fully decoupled — a rejected RCA doesn't leave a dirty worktree. The RCA and test become part of the fix PR (atomic traceability). No direct commits to `dev`.

### ADR-0006: Partial RCA with Hypothesis Labels (v1.0.0)

- **Context:** The investigator may be unable to reproduce the bug. Options: (1) halt the pipeline entirely, (2) produce a partial RCA with the root cause labeled as "Hypothesis", (3) add a clarification loop before the RCA.
- **Decision:** The investigator produces a partial RCA with the root cause explicitly labeled as "Hypothesis" per AGENTS.md rules. The existing human review gate handles the "need more info" case naturally — the user can reject with additional context.
- **Consequences:** No new pipeline mechanism needed. The human sees an honest assessment of diagnostic confidence. The user can approve a hypothesis-based RCA to proceed with a speculative fix, or reject and provide more reproduction context.

---

## Changelog

### v1.0.0 — 2026-09-02

- **Initial release.** Seven-phase pipeline: Issue Triage → Root Cause Investigation → Internal RCA Review → Human Review Gate → Fix Implementation → Code Review → Merge & Update RCA.
- **New sub-agents:** `investigator` (forensic debugging with reproduction tests) and `rca-reviewer` (RCA quality gate).
- **Investigator writes reproduction test:** Eliminates ambiguity between diagnosis and fix phases. Engineer verifies RED before implementing GREEN.
- **Internal RCA review loop:** `rca-reviewer` challenges evidence rigor, hypothesis completeness, and fix strategy before human review (max 3 rounds).
- **Human review gate:** No cap on rejection rounds. Each rejection triggers a full investigator → rca-reviewer cycle.
- **File handoff mechanism:** Orchestrator copies reproduction test and RCA from main worktree into engineer's isolated worktree.
- **Dual input format:** Supports both inline text and GitHub Issue references (`#<number>`).
