# Development Skills

A collection of AI agent skills that cover the full software development lifecycle — from feature ideation to merged PR. These skills can be used independently or chained together as an automated pipeline.

---

## Overview

### Feature Delivery Pipeline

```mermaid
flowchart LR
    Idea([Idea]) --> prd["/write-prd\n(PRD)"]
    prd --> rfc["/request-feature\n(RFC & Design Review)"]
    rfc --> planning["planning-and-task-breakdown (dep-skills)\n(Vertical Tasks)"]
    planning --> orchestrator["/implement-task\n(Pipeline Orchestrator)"]
    
    subgraph Implementation ["Implementation Loop (Isolated Worktree)"]
        direction TB
        incremental["incremental-implement (dep-skills)\n(Worktree & PR)"]
        tdd["test-driven-development (dep-skills)\n(Red-Green-Refactor)"]
        git_master["git-master (dep-skills)\n(Atomic Commits)"]
        code_review["code-review\n(Verification Gate)"]
        incremental --> tdd --> git_master --> code_review
    end

    orchestrator --> Implementation
    Implementation --> Merge([Merged PR])
```

### Bug Triage & Remediation Pipeline

```mermaid
flowchart LR
    Report([Bug Report / Issue]) --> triage["/investigate-issue\n(Triage & Diagnosis)"]
    triage --> rca["Forensic RCA\n+ RED Reproduction Test"]
    rca --> rca_review["RCA Quality Review\n+ User Approval"]
    rca_review --> fix["TDD Fix Implementation\n(GREEN in Worktree)"]
    fix --> review["code-review\n(Verification Pass)"]
    review --> merge_fix([Merged Fix])
```

| Skill | Pattern | One-liner |
|:------|:--------|:----------|
| [write-prd](#write-prd) | Inversion / PM | Turn a raw idea into an approved PRD |
| [request-feature](#request-feature) | Pipeline | Orchestrate PRD → RFC → Plan in one command |
| [implement-task](#implement-task) | Pipeline | Execute a planned task end-to-end with full review board |
| [code-review](#code-review) | Auditor | Multi-dimensional code review (style rubrics, specs, security) |
| [investigate-issue](#investigate-issue) | Pipeline | End-to-end bug triage, root-cause RCA, and TDD-driven remediation |

---

[planning-and-task-breakdown](https://github.com/allanbian1017/dep-skills/blob/main/skills/development/planning-and-task-breakdown/SKILL.md), [incremental-implement](https://github.com/allanbian1017/dep-skills/blob/main/skills/development/incremental-implement/SKILL.md), [test-driven-development](https://github.com/allanbian1017/dep-skills/blob/main/skills/development/test-driven-development/SKILL.md), and [git-master](https://github.com/allanbian1017/dep-skills/blob/main/skills/development/git-master/SKILL.md) are external dependencies maintained in the private [dep-skills](https://github.com/allanbian1017/dep-skills) repository. Install them alongside these skills before running the planning and implementation workflows.

## Skills

### `write-prd`

**Purpose:** Turn a raw feature idea into a rigorous, approved Product Requirements Document (PRD).

**When to use:**
- You have a new feature idea and want structured requirements before writing any code.
- You need to document functional and non-functional requirements for stakeholder alignment.

**When NOT to use:**
- The feature already has an approved PRD or clear requirements.
- The task is pure code generation, debugging, or Q&A.

**How to invoke:**
```
/write-prd <your idea>
```

**What it does:**
1. Analyzes your idea and asks clarifying questions if ambiguous.
2. Drafts a PRD with Context, Problem Statement, and Requirements sections.
3. Saves to `docs/prds/prd_<feature_name>.md`.
4. **Pauses** and asks for your approval before concluding.
5. Iterates on your feedback until you say "Approved".

---

### `request-feature`

**Purpose:** Orchestrate the full planning pipeline — from a single idea through PRD, RFC, architecture review, and task breakdown — using a multi-agent review board.

**When to use:**
- You have a new idea and want a complete, reviewed technical plan ready for implementation.
- You need an RFC with design alternatives, scored against engineering criteria.

**When NOT to use:**
- You already have an approved RFC and task list. Use `implement-task` instead.
- The change is too small to warrant a formal design process (simple config changes, minor bug fixes).

**How to invoke:**
```
/request-feature <idea>
```

**What it does:**
1. **Requirements Phase** — Runs `write-prd`. Pauses for your PRD approval.
2. **Technical Design Phase** — Generates an RFC with a simpler baseline alternative and a decision scorecard.
3. **Design Review Phase** — Red-teams the RFC with an architect agent, runs an implementation feasibility review with an engineer agent, revises until internally approved. Pauses for your RFC approval.
4. **Planning Phase** — Produces `docs/plans/plan_<feature>.md` and `docs/plans/tasks_<feature>.md` with checkboxes.

> **Tip:** This skill is planning-only. No application code is modified. Implementation is handled by `implement-task`.

---

### `implement-task`

**Purpose:** Execute an already-planned task end-to-end — writing tests, implementing code, running CI, and completing a full code review loop until the PR is approved and merged.

**When to use:**
- You have an approved RFC, plan, and task list from `request-feature`.
- You want to pick the next pending task and drive it all the way to a merged PR automatically.

**When NOT to use:**
- No plan or task list exists yet. Run `request-feature` first.
- You only want to implement without a review process.

**How to invoke:**
```
/implement-task <feature_name>
```

**What it does:**
1. **Pre-Flight** — Reads `docs/plans/tasks_<feature>.md`, identifies pending tasks, detects tightly coupled batches, and asks you: **[Take 1]** or **[Take All]**.
2. **Implementation Phase** — Runs `incremental-implement` + `test-driven-development` inside an isolated worktree. Produces an implementation scorecard.
3. **Code Review Phase** — Two review passes: Test Red-Team (test quality, missing cases) and Code Risk (bugs, security, coupling, scope creep). Internal fix loop, then pauses for **your** approval.
4. **Deployment Phase** — Confirms CI is green, PR is approved, then merges and cleans up the worktree.

**Scorecard dimensions:** Scope control, Correctness, Test evidence, Simplicity, Reliability, Security, Backward compatibility, Observability, CI stability, Maintainability.

---

### `code-review`

**Purpose:** Multi-dimensional, scalable code review before committing or merging. Evaluates diffs against language-specific style rubrics, RFC/Plan specification compliance, and language-agnostic bug/security checklists while honoring learned team preferences.

**When to use:**
- After substantial implementation work, before creating a commit or PR.
- Manually with `/review-work` or `Use @code-review` when you want a comprehensive quality check.
- Automatically delegated to by `implement-task` during Phase 2 (Code Review).

**When NOT to use:**
- Working tree is clean (nothing to review).
- Read-only exploration tasks.
- Code doesn't compile or has syntax errors.

**How to invoke:**
```
/review-work
```
Or:
```
Use @code-review
```

**What it does:**
1. **Captures diff & context**: Reads git diff, RFC specifications, and plan acceptance criteria.
2. **Dimension 1 (Style Review)**: Evaluates changed code against language rubrics (e.g. `golang.md`), enforcing binary pass/fail rules (`R-<LANG>-xx`) and surfacing contextual guidelines (`C-<LANG>-xx`).
3. **Dimension 2 (Spec Compliance)**: Validates implementation completeness against RFC requirements and Plan acceptance criteria (`✅ Implemented`, `⚠️ Partial`, `❌ Missing`).
4. **Dimension 3 (Bugs, Security & Tests)**: Checks for null dereferences, race conditions, injection vulnerabilities, and test coverage gaps.
5. **Team Preferences**: Prioritizes learned project conventions from `memory/preferences.md` over baseline rules.

**Output format:**

| # | Verdict | Category | File | Issue | Action |
|---|---------|----------|------|-------|--------|
| 1 | Fixed | BUG | file.ts:42 | Null check missing | Fixed |

---

### `investigate-issue`

**Purpose:** Orchestrate the complete issue resolution lifecycle — from issue triage and forensic diagnosis to human-approved RCA, TDD-driven fix implementation, multi-pass code review, and merge.

**When to use:**
- You have a bug report, unexpected failure, or GitHub issue (`/investigate-issue #<number>` or `/investigate-issue <description>`).
- You need evidence-backed diagnosis that systematically tests and rejects alternative hypotheses before touching application code.

**When NOT to use:**
- Simple, obvious bugs where the root cause is already known and stated (use `@test-driven-development` with Prove-It pattern directly).
- New feature requests or architectural redesigns (use `/request-feature`).
- Issues originating entirely in external infrastructure outside the codebase.

**How to invoke:**
```
/investigate-issue <issue description or #number>
```

**What it does:**
1. **Issue Triage (Orchestrator)** — Parses input or fetches the issue body via GitHub CLI (`gh issue view`). Generates an issue slug.
2. **Root Cause Investigation (Investigator Sub-Agent)** — Forensically explores the code, reproduces the failure, forms and quantitatively rejects competing hypotheses, and writes a failing **RED** reproduction test without implementing a fix.
3. **RCA Quality Gate (RCA Reviewer Sub-Agent)** — Red-teams the RCA for evidence rigor, hypothesis testing, and blast radius before human presentation.
4. **Human Approval Gate (Inversion)** — Pauses for user approval of the RCA and reproduction test.
5. **Fix Implementation (Engineer Sub-Agent)** — Executes minimal TDD implementation in an isolated worktree via `incremental-implement` (RED → GREEN).
6. **Code Review & Deployment** — Reviews the fix via `code-review` and merges upon passing review.

---

## Recommended Workflows

### New Feature (Full Pipeline)

```
/request-feature <idea>
   └─ write-prd (PRD + approval)
   └─ RFC generation + architecture review
   └─ planning-and-task-breakdown
      └─ tasks_<feature>.md created

/implement-task <feature>
   └─ incremental-implement (worktree)
      └─ test-driven-development (RED → GREEN → REFACTOR)
      └─ git-master (atomic commits)
      └─ code-review (CI + multi-dimensional review)
   └─ Merge + cleanup
```

### Bug Investigation & Remediation (Forensic RCA Pipeline)

```
/investigate-issue <issue>
   └─ Issue triage & slug generation
   └─ Investigator: reproduce + reject hypotheses + write RED test
   └─ RCA Quality Gate (rca-reviewer red-team review)
   └─ Human approval gate (Inversion)
   └─ Engineer: TDD implementation (RED → GREEN) in isolated worktree
   └─ Code review (code-review verification pass)
   └─ Squash-merge & clean worktree
```

### Quick Bug Fix (Root Cause Known)

```
/review-work                           # baseline check
@test-driven-development to fix <bug>  # Prove-It pattern (RED -> GREEN)
@git-master to commit                   # atomic commit
```

### Cleanup Before a PR

```
@git-master to squash my WIP commits   # REBASE mode
/review-work                           # final quality gate
```

---

## File Conventions

Skills that generate planning artifacts write to:

| File | Created by |
|------|-----------|
| `docs/prds/prd_<feature>.md` | `write-prd`, `request-feature` |
| `docs/rfcs/rfc_<feature>.md` | `request-feature` |
| `docs/plans/plan_<feature>.md` | `request-feature`, `planning-and-task-breakdown` |
| `docs/plans/tasks_<feature>.md` | `request-feature` |
| `docs/rcas/rca_<issue>.md` | `investigate-issue` |
