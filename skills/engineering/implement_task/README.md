# 🛠️ `implement_task` Skill

> **Autonomous AI Developer Pipeline** — picks the next pending task, implements it with full TDD discipline, creates a PR, runs a code-review loop, and waits for your final approval.

---

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [How to Use](#how-to-use)
- [Pipeline Walkthrough](#pipeline-walkthrough)
  - [Phase 1 — Implementation](#phase-1--implementation)
  - [Phase 2 — Code Review](#phase-2--code-review)
- [File Conventions](#file-conventions)
- [Related Skills](#related-skills)
- [When NOT to Use](#when-not-to-use)
- [Changelog](#changelog)

---

## Overview

`implement_task` is the **execution arm** of the autonomous agent pipeline. It orchestrates specialized sub-agents to execute a three-phase pipeline:

```
┌─────────────────────────────────────────────────────────┐
│  Phase 1: Implementation (Engineer sub-agent)           │
│                                                         │
│  Read task → Load context → RED (failing test)          │
│    → GREEN (minimal impl) → Full suite → Build          │
│    → Commit → Verify → Mark task done                   │
│                                                         │
├─────────────────────────────────────────────────────────┤
│  Phase 2: Code Review (Code-Reviewer sub-agent)         │
│                                                         │
│  Review PR against RFC + Plan + Tasks                   │
│    → Internal feedback loop (Engineer revises)          │
│    → Halt → Wait for USER "Approved"                    │
│                                                         │
├─────────────────────────────────────────────────────────┤
│  Phase 3: Deployment (Deploy sub-agent)                 │
│                                                         │
│  Merge PR (gh pr merge) → Clean up isolated worktree    │
└─────────────────────────────────────────────────────────┘
```

---

## Prerequisites

Before invoking this skill, ensure the following files exist for `<feature_name>`:

| File | Purpose |
|---|---|
| `docs/plans/tasks_<feature_name>.md` | Checklist of pending / completed tasks |
| `docs/plans/plan_<feature_name>.md` | Detailed plan with acceptance criteria per task |
| `docs/rfcs/rfc_<feature_name>.md` | Technical design / RFC document |

> These files are typically produced by the [`request_feature`](../request_feature/SKILL.md) pipeline (`/request_feature <idea>`). If they don't exist yet, run that first.

The following sub-agents and sub-skills must also be available:

- **Sub-Agents:** `engineer`, `code-reviewer`, `deploy`
- [`incremental_implement`](../incremental_implement/SKILL.md) — isolated worktree, atomic commits, PR lifecycle, and CI gate
- [`test-driven-development`](../test-driven-development/SKILL.md) — enforces RED → GREEN → Refactor discipline

---

## How to Use

Type the following command in your AI agent chat:

```
/implement_task <feature_name>
```

**`<feature_name>`** must exactly match the suffix used in your plan/task/RFC filenames.

### Examples

```
/implement_task user_authentication
/implement_task payment_gateway
/implement_task dark_mode_toggle
```

The agent will automatically locate the relevant plan and task list files, pick the next unchecked task, and begin execution.

---

## Pipeline Walkthrough

### Phase 1 — Implementation

The agent invokes the **engineer** sub-agent to execute a strict TDD + incremental delivery loop.

#### Step-by-step

1. **Read the task list** — opens `docs/plans/tasks_<feature_name>.md` and selects the next pending (unchecked) task.
2. **Read acceptance criteria** — opens `docs/plans/plan_<feature_name>.md` and loads the corresponding task details, constraints, and verification steps.
3. **Execute sub-skills** — the `engineer` invokes `incremental_implement` (for PR lifecycle) alongside `test-driven-development` (for TDD enforcement).
4. **Load context** — reads existing code, type definitions, and established patterns relevant to the task scope.
5. **RED** — writes a failing test that expresses the expected behavior. The test must fail before any implementation is written.
6. **GREEN** — writes the minimum production code required to make the test pass. No over-engineering.
7. **Full test suite** — runs all existing tests to catch regressions.
8. **Build verification** — runs the project build to confirm compilation succeeds.
9. **Atomic commit** — commits changes with a descriptive message following the project's commit conventions.
10. **Verify** — executes the verification method defined in the plan (e.g., integration test, manual check script, acceptance test). Execution does **not** proceed until this passes.
11. **Update task list** — marks the completed task as done in `docs/plans/tasks_<feature_name>.md`.

> **Scope discipline:** Only ONE task is implemented per invocation. The agent will not proceed to subsequent tasks automatically.

---

### Phase 2 — Code Review

The agent invokes the **code-reviewer** sub-agent to validate the implementation.

#### Step-by-step

1. **Review the PR** — inspects the submitted Pull Request against:
   - `docs/rfcs/rfc_<feature_name>.md` (technical design compliance)
   - `docs/plans/plan_<feature_name>.md` (acceptance criteria)
   - `docs/plans/tasks_<feature_name>.md` (scope correctness)
   - General code quality standards (readability, naming, test coverage)

2. **Internal pipeline loop** — if issues are found, the **code-reviewer** passes structured feedback back to the **engineer** sub-agent, which revises the PR. This loop repeats until the **code-reviewer** approves internally.

3. **Inversion — Wait for User** — once internally approved, the agent **halts** and presents the PR to you for final review.
   - If you provide feedback → the **engineer** revises → **code-reviewer** re-reviews → loop repeats.
    - Once you input **`"Approved"`** → the pipeline proceeds to the Deployment Phase.

---

### Phase 3 — Deployment

The agent invokes the **deploy** sub-agent to merge and clean up.

#### Step-by-step

1. **Merge the PR** — Merges the approved Pull Request using `gh pr merge --squash --delete-branch`.
2. **Clean up isolated worktree** — Returns to the original directory, removes the isolated worktree (`git worktree remove`), and prunes the worktree directory (`git worktree prune`).

---

## File Conventions

| Path pattern | Role |
|---|---|
| `docs/plans/tasks_<feature_name>.md` | Task checklist (read + updated by this skill) |
| `docs/plans/plan_<feature_name>.md` | Detailed plan with acceptance criteria (read-only) |
| `docs/rfcs/rfc_<feature_name>.md` | RFC / technical design (read-only) |

Task list format expected by this skill:

```markdown
- [ ] Task 1: Implement login endpoint
- [ ] Task 2: Add JWT token validation
- [x] Task 0: Set up project scaffold   ← already completed
```

The agent marks tasks complete by changing `[ ]` to `[x]`.

---

## Related Skills

| Skill | Role in this pipeline |
|---|---|
| [`request_feature`](../request_feature/SKILL.md) | Upstream: generates the PRD, RFC, plan, and task list that this skill consumes |
| [`incremental_implement`](../incremental_implement/SKILL.md) | Sub-skill: handles worktree isolation, atomic commits, PR creation, and CI gate |
| [`test-driven-development`](../test-driven-development/SKILL.md) | Sub-skill: enforces RED → GREEN → Refactor cycle |
| [`planning-and-task-breakdown`](../planning-and-task-breakdown/SKILL.md) | Upstream: creates the structured task list format consumed here |

---

## When NOT to Use

- **No plan files exist yet** → run `/request_feature <idea>` first.
- **You want to implement multiple tasks in one shot** → this skill deliberately implements one task at a time to keep PRs atomic and reviewable.
- **You want to commit directly to `main`/`dev`** → `incremental_implement` (used internally) always works via isolated feature branches.
- **Simple one-off edits** → use a direct code edit; this pipeline is overhead for small changes.

## Architecture Decisions (ADRs)

The design and security boundaries of the `implement_task` pipeline are governed by the following Architecture Decision Records:

### ADR-0001: Three-Phase Pipeline & Role Isolation (v1.2.0)
*   **Context:** Allowing the `engineer` sub-agent to autonomously merge Pull Requests (`gh pr merge`) bypasses human oversight and risks committing unreviewed or buggy code to the production branch.
*   **Decision:** Split the pipeline into three distinct phases: Phase 1: Implementation (Engineer sub-agent, **no merge permissions**), Phase 2: Code Review (Code-Reviewer & Human Approval Gate), and Phase 3: Deployment (Deploy sub-agent).
*   **Consequences:** Enforces a strict human-in-the-loop validation boundary. The PR can only be squash-merged and cleaned up by the `deploy` sub-agent after the user explicitly inputs `"Approved"`.

### ADR-0002: Pre-Flight Scope Gating & Suggestion Mode (v1.2.0)
*   **Context:** Implementing a highly coupled set of tasks (e.g. dependencies + CI setup + mock suites) one-by-one introduces redundant worktree setups and CI latency, but automated batching violates the single-task safety rule.
*   **Decision:** Created a Pre-Flight Scope Verification step where the parent agent evaluates task dependencies. If logical coupling is detected, the agent halts and suggests batching, giving the user the option to choose: **[Take 1]** (single task) or **[Take All]** (batched run).
*   **Consequences:** Balances developer efficiency with safety. If the user selects a batched run, it is treated as a single cohesive transaction (halting in place without destructive rollbacks on failure).

### ADR-0003: Sub-Agent Context Guardrails (v1.2.0)
*   **Context:** Sub-agents need future architectural context (RFC, plan files) to avoid making short-sighted design decisions, but they must be constrained to only write code for the currently authorized task(s).
*   **Decision:** Sanitized the sub-agent prompt to pass the full RFC and Plan for context, but strictly filtered the active task checklist to ONLY show the approved tasks.
*   **Consequences:** Solves the "blind spot" issue while preventing task scope creep.

---

## Changelog

### v1.2.0 — 2026-06-04
- **Split merge/deploy permissions from the engineer sub-agent.**
- Introduced the `deploy` sub-agent responsible for merging pull requests and cleaning up worktrees after human approval.
- Restructured `implement_task` to use a 3-phase pipeline (Implementation → Code Review → Deployment).
- Implemented Pre-Flight Scope Gating for batch execution suggestions and prompt guardrails.

### v1.1.0 — 2026-05-06
- **Updated to use specialized sub-agents.**
- Phases now explicitly delegate to `engineer` and `code-reviewer` sub-agents.
- README updated to reflect the new architecture.

### v1.0.0 — 2026-05-06
- **Initial release.** Converted from `workflows/implement_task.md` to a formal agent skill.
- Two-phase pipeline: Engineer (TDD + incremental_implement) → Reviewer (internal loop + user approval gate).
- All operations from the original workflow preserved verbatim.

