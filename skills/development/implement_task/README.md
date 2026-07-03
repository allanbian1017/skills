# 🛠️ `implement_task` Skill

> **Autonomous AI Developer Pipeline** — picks the approved pending task scope, implements it with full TDD discipline, creates a PR, runs an implementation review board loop, and waits for your final approval.

---

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [How to Use](#how-to-use)
- [Pipeline Walkthrough](#pipeline-walkthrough)
  - [Phase 1 — Implementation](#phase-1--implementation)
  - [Phase 2 — Implementation Review Board](#phase-2--implementation-review-board)
- [File Conventions](#file-conventions)
- [Related Skills](#related-skills)
- [When NOT to Use](#when-not-to-use)
- [Changelog](#changelog)

---

## Overview

`implement_task` is the **execution arm** of the autonomous agent pipeline. It orchestrates specialized sub-agents to execute a three-phase pipeline with an implementation review board model: scope is selected deliberately, implementation evidence is captured as an artifact, reviewers challenge tests and code separately, and deployment only happens after release readiness is confirmed.

```
┌─────────────────────────────────────────────────────────┐
│  Phase 1: Implementation (Engineer sub-agent)           │
│                                                         │
│  Scope artifact → Load context → RED (failing test)     │
│    → GREEN (minimal impl) → Full suite → Build          │
│    → Commit → Verify → Implementation scorecard         │
│                                                         │
├─────────────────────────────────────────────────────────┤
│  Phase 2: Implementation Review Board                   │
│                                                         │
│  Test red-team pass → Code risk pass → Score PR         │
│    → Internal feedback loop (Engineer revises/verifies) │
│    → Halt → Wait for USER "Approved"                    │
│                                                         │
├─────────────────────────────────────────────────────────┤
│  Phase 3: Deployment (Deploy sub-agent)                 │
│                                                         │
│  Release readiness check → Merge PR → Clean worktree    │
└─────────────────────────────────────────────────────────┘
```

### Implementation Review Board Roles

| Role | Owner | Purpose |
|---|---|---|
| Scope Orchestrator | Parent agent | Reads RFC, plan, and task list; selects only user-approved scope; prevents task drift |
| Implementer | `engineer` | Executes the approved scope with TDD and `incremental_implement` |
| Test Red-Team Reviewer | `code-reviewer` | Challenges whether tests actually prove the acceptance criteria |
| Code Risk Reviewer | `code-reviewer` | Attacks bugs, security risks, regressions, hidden coupling, scope creep, and maintainability problems |
| Release Readiness Reviewer | `deploy` | Confirms CI, approval, base branch, checklist state, operational notes, and cleanup plan before merge |
| Decision Orchestrator | Parent agent | Enforces review rounds and halts on unresolved high-severity risks |

### Implementation Scorecard

Each implementation pass is scored from 1 to 10 on:

- Scope control
- Correctness
- Test evidence
- Simplicity
- Reliability
- Security
- Backward compatibility
- Observability or debuggability
- CI stability
- Maintainability

The scorecard does not replace tests, CI, or review. High-severity issues in correctness, security, data safety, or scope control block progress until fixed or explicitly escalated to the user.

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

The agent invokes the **engineer** sub-agent to execute a strict TDD + incremental delivery loop, constrained to the user-approved scope.

#### Step-by-step

1. **Read the task list** — opens `docs/plans/tasks_<feature_name>.md` and identifies pending tasks.
2. **Build the scope artifact** — reads the plan and RFC, identifies dependencies, recommends either `[Take 1]` or a coupled `[Take All]` batch, and waits for your explicit choice.
3. **Read acceptance criteria** — opens `docs/plans/plan_<feature_name>.md` and loads the corresponding task details, constraints, and verification steps.
4. **Execute sub-skills** — the `engineer` invokes `incremental_implement` (for PR lifecycle) alongside `test-driven-development` (for TDD enforcement).
5. **Load context** — reads existing code, type definitions, and established patterns relevant to the task scope.
6. **RED** — writes a failing test that expresses the expected behavior. The test must fail before any implementation is written.
7. **GREEN** — writes the minimum production code required to make the test pass. No over-engineering.
8. **Full test suite** — runs all existing tests to catch regressions.
9. **Build verification** — runs the project build to confirm compilation succeeds.
10. **Atomic commit** — commits changes with a descriptive message following the project's commit conventions.
11. **Verify** — executes the verification method defined in the plan. Execution does **not** proceed until this passes.
12. **Capture implementation artifact** — records approved scope, files changed, RED/GREEN evidence, full-suite/build evidence, scorecard, and unresolved risks.
13. **Update task list** — after CI passes and the PR is ready for review, marks only the completed approved task scope as done in `docs/plans/tasks_<feature_name>.md`.

> **Scope discipline:** The agent implements only the user-approved scope: either `[Take 1]` or the explicitly approved coupled `[Take All]` batch. It will not expand scope silently.

---

### Phase 2 — Implementation Review Board

The agent invokes the **code-reviewer** sub-agent to validate the implementation as a structured review board.

#### Step-by-step

1. **Review the PR** — inspects the submitted Pull Request against:
   - `docs/rfcs/rfc_<feature_name>.md` (technical design compliance)
   - `docs/plans/plan_<feature_name>.md` (acceptance criteria)
   - `docs/plans/tasks_<feature_name>.md` (scope correctness)
   - Implementation artifact (scope, test evidence, scorecard, unresolved risks)
   - CI results
   - General code quality standards (readability, naming, test coverage)

2. **Test red-team pass** — challenges test quality, missing edge cases, weak assertions, false-positive RED tests, inadequate regression coverage, and missing plan verification.

3. **Code risk pass** — challenges bugs, security issues, reliability regressions, hidden coupling, scope creep, over-engineering, maintainability, backward compatibility, and operational readiness.

4. **Score the PR** — updates the implementation scorecard after each review round.

5. **Internal pipeline loop** — if issues are found, the **code-reviewer** passes structured feedback back to the **engineer** sub-agent, which revises and re-verifies the PR. This loop repeats until the **code-reviewer** approves internally. The loop is capped at three rounds unless a blocking risk remains unresolved.

6. **Inversion — Wait for User** — once internally approved, the agent **halts** and presents the PR to you for final review.
   - If you provide feedback → the **engineer** revises → **code-reviewer** re-reviews → loop repeats.
   - Once you input **`"Approved"`** → the pipeline proceeds to the Deployment Phase.

---

### Phase 3 — Deployment

The agent invokes the **deploy** sub-agent to verify release readiness, merge, and clean up.

#### Step-by-step

1. **Release readiness check** — confirms explicit user approval, latest CI pass, intended base branch, checklist state, migration/rollback or operational notes when relevant, and no unresolved high-severity findings.
2. **Merge the PR** — Merges the approved Pull Request using `gh pr merge --squash --delete-branch`.
3. **Clean up isolated worktree** — Returns to the original directory, removes the isolated worktree (`git worktree remove`), and prunes the worktree directory (`git worktree prune`).

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
- **You want unrelated tasks implemented in one shot** → this skill only batches tasks when pre-flight scope verification finds strong coupling and you explicitly approve `[Take All]`.
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

### ADR-0004: Implementation Review Board & Scorecard (v1.3.0)
*   **Context:** A single implementation plus code-review pass can miss weak tests, hidden scope creep, release risk, or operational gaps.
*   **Decision:** Treat implementation as a structured review board: scope orchestration, TDD implementation, test red-team review, code risk review, implementation scorecard, and release readiness review.
*   **Consequences:** Each PR must carry evidence for why it is correct and safe to merge, not just a passing test run.

---

## Changelog

### v1.3.0 — 2026-06-17
- **Implementation Review Board Model:** Added scope, implementer, test red-team, code risk, release readiness, and decision orchestration roles.
- **Implementation Scorecard:** Added scoring criteria for scope control, correctness, test evidence, reliability, security, compatibility, CI stability, and maintainability.
- **Structured Evidence:** Added implementation artifacts, review pass separation, and release readiness checks before merge.

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
