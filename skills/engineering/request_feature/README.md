# request_feature

> Autonomous AI Plan Pipeline — from raw idea to a reviewed, task-ready implementation plan.

## Overview

`request_feature` is an agent skill that orchestrates a **multi-phase, multi-persona planning pipeline** for turning a new feature idea into a fully-reviewed, task-broken-down implementation plan. It delegates work to specialized sub-agents (PM → Planner → Architect + Engineer → Planner → Engineer), with each phase producing concrete document artifacts and pausing for human approval at the major decision gates.

The pipeline is designed around **human-in-the-loop checkpoints** ("Inversions") and an internal architecture review board model. Designs are proposed, red-teamed, checked for implementation feasibility, scored against tradeoffs, compared with a simpler baseline, and revised before you are asked to approve the RFC.

This skill is planning-only. It may read relevant code to assess impact, but it must not modify application code, tests, configuration, dependencies, or implementation files. Implementation belongs to `/implement_task`.

---

## Trigger

Invoke the skill by typing:

```
/request_feature <idea>
```

**Examples:**
```
/request_feature Add OAuth2 login with Google and GitHub providers
/request_feature Build a real-time notification system using WebSockets
/request_feature Migrate the monolith checkout flow to a microservice
```

The agent will automatically detect this command and start the pipeline. You can also describe a feature idea in natural language and ask the agent to "kick off the feature pipeline" — the skill description is written to trigger on that intent too.

---

## Pipeline Overview

```
/request_feature <idea>
        │
        ▼
┌─────────────────────┐
│  1. Requirements    │  PM sub-agent → writes PRD
│     Phase           │  ⏸ Waits for "Approved"
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│  2. Technical       │  Planner sub-agent → writes RFC
│     Design Phase    │  Includes simpler baseline + scorecard
│                     │  (no human pause — flows into review)
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│  3. Design Review   │  Architect red-teams RFC
│     Phase           │  Engineer checks implementation feasibility
│                     │  Planner revises, scores, compares baseline
│                     │  ⏸ Waits for "Approved"
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│  4. Planning Phase  │  Engineer sub-agent → task breakdown
│                     │  Produces plan + tasks files
│                     │  ⏸ Presents for human review
└─────────────────────┘
```

---

## Phase-by-Phase Reference

### Phase 1 — Requirements

| Item | Detail |
|------|--------|
| **Sub-agent** | `pm` |
| **Sub-skill used** | `write_prd` + PRD Template (`assets/templates/prd_template.md`) |
| **Input** | `<idea>` provided in the command |
| **Output file** | `docs/prds/prd_<feature_name>.md` |
| **Human checkpoint** | ✅ Yes — loops until user types `"Approved"` |

The agent invokes the **pm** sub-agent and the `write_prd` skill to draft a Product Requirements Document using the PRD Template at `assets/templates/prd_template.md`. The PRD should clarify users and actors, traffic assumptions, latency goals, availability target, consistency requirements, compliance constraints, existing systems, non-goals, and unknowns when relevant. The pipeline halts after the PRD is saved. You review it, provide feedback (or edit the file directly), and the agent will revise until you approve.

---

### Phase 2 — Technical Design

| Item | Detail |
|------|--------|
| **Sub-agent** | `planner` |
| **Sub-skill used** | RFC Template (`assets/templates/rfc_template.md`) |
| **Input** | Approved `docs/prds/prd_<feature_name>.md` |
| **Output file** | `docs/rfcs/rfc_<feature_name>.md` |
| **Human checkpoint** | ❌ No — automatically transitions to Design Review |

Using the approved PRD, the agent invokes the **planner** sub-agent to generate a technical RFC (Request for Comments). This covers architecture approach, component design, and key technical decisions.

The RFC must include:

- A final recommended design candidate
- At least one simpler baseline alternative
- Rejected alternatives and rationale
- Service or module boundaries
- Data ownership
- API or interface contracts
- Event or control flows when relevant
- Failure scenarios
- Observability plan
- Security review
- Rollout strategy
- Open risks
- Initial decision scorecard

If the proposed design is more complex than the simpler baseline, the RFC must justify why the extra operational cost is necessary. The output feeds directly into Phase 3.

---

### Phase 3 — Design Review

| Item | Detail |
|------|--------|
| **Sub-agent** | `architect` (red-team reviewer) + `engineer` (feasibility reviewer) + `planner` (reviser) |
| **Sub-skill used** | None (internal sub-agent loop) |
| **Input** | `docs/rfcs/rfc_<feature_name>.md` |
| **Output file** | Updated `docs/rfcs/rfc_<feature_name>.md` |
| **Human checkpoint** | ✅ Yes — loops until user types `"Approved"` |

The **architect** sub-agent red-teams the RFC by looking for bottlenecks, weak assumptions, unclear ownership, failure modes, security risks, over-engineering, under-specified operations, and bad cost tradeoffs.

The **engineer** sub-agent performs a read-only implementation feasibility review. It checks codebase impact, migration complexity, required interfaces, testing strategy, rollout plan, backward compatibility, CI/CD implications, and operational readiness. This is still planning work; it must not implement anything.

The **planner** sub-agent revises the RFC using both reviews, re-scores the design, and compares it against the simpler baseline. The internal loop repeats until the **architect** approves the RFC and either the score no longer materially improves or all high-severity risks have documented mitigations. The loop is capped at three internal rounds unless a blocking risk remains unresolved.

Then the pipeline pauses for **your** review of the now-internally-approved RFC. If you provide further feedback, the Planner+Architect review loop repeats.

#### RFC Decision Scorecard

The RFC is scored from 1 to 10 on:

- Correctness
- Scalability
- Reliability
- Security
- Cost
- Simplicity
- Implementation effort
- Observability
- Maintainability

---

### Phase 4 — Planning

| Item | Detail |
|------|--------|
| **Sub-agent** | `engineer` |
| **Sub-skill used** | `planning-and-task-breakdown` |
| **Input** | Approved `docs/rfcs/rfc_<feature_name>.md` + relevant codebase sections |
| **Output files** | `docs/plans/plan_<feature_name>.md`, `docs/plans/tasks_<feature_name>.md` |
| **Human checkpoint** | ✅ Yes — presents plan for review |

The agent invokes the **engineer** sub-agent to read the approved RFC and the relevant parts of the codebase, then invokes the `planning-and-task-breakdown` skill, using the Implementation Plan Template at `assets/templates/plan_template.md`, to produce a detailed implementation plan. From the plan, a separate tasks file is generated with:

- **Dependency graph** between components
- **Vertical slicing** — each task is one complete end-to-end path, not a horizontal layer
- **Acceptance criteria** and **verification steps** per task
- **Checkpoints** between phases

The final plan is presented for your review before the pipeline ends.

Phase 4 produces implementation-ready planning artifacts only. It does not start implementation, stage code, run feature work, or modify application files.

---

## Output File Structure

After a complete run, you will find these artifacts in your project:

```
docs/
├── prds/
│   └── prd_<feature_name>.md        ← Product Requirements Document
├── rfcs/
│   └── rfc_<feature_name>.md        ← Technical design / RFC
└── plans/
    ├── plan_<feature_name>.md        ← Full implementation plan
    └── tasks_<feature_name>.md       ← Task list with criteria & verification
```

> **Note:** `<feature_name>` is derived from your idea — the agent will normalize it to a snake_case or kebab-case identifier automatically.

---

## Human Checkpoints ("Inversions")

Two explicit approval gates exist in the pipeline, followed by a final plan review handoff:

| Gate | Trigger condition | How to advance |
|------|-------------------|----------------|
| After PRD | Agent halts and asks for review | Type `Approved` |
| After RFC review | Agent halts and asks for RFC approval | Type `Approved` |
| After task planning | Agent presents the task-ready plan | Review before invoking `/implement_task` |

If you provide **any other response**, the agent interprets it as feedback and revises the relevant document before asking again.

---

## Dependencies

This skill orchestrates specialized sub-agents and other skills, respecting the project's `AGENTS.md`:

| Dependency | Purpose | Location |
|------------|---------|----------|
| `pm`, `planner`, `architect`, `engineer` | Specialized sub-agents used in each phase | `.gemini/agents/` |
| `write_prd` | Generates the PRD in Phase 1 | `.agents/skills/write_prd/` |
| `planning-and-task-breakdown` | Generates the plan and task list in Phase 4 | `.agents/skills/planning-and-task-breakdown/` |
| `AGENTS.md` | Defines Planning Process, Plan Format, and agent rules | Project root |

Ensure all are present and up to date before invoking this skill.

---

## File Structure

```
.agents/skills/request_feature/
├── SKILL.md
├── README.md
└── assets/
    └── templates/
        ├── plan_template.md
        ├── prd_template.md
        └── rfc_template.md
```

---

## Tips & Notes

- **Be specific in your idea.** The more context you give (`/request_feature <idea>`), the richer the PRD and RFC will be. A vague idea produces a vague PRD.
- **Edit files directly.** During checkpoints, you can edit the PRD or RFC file in your editor — the agent will read and incorporate your changes before asking again.
- **The internal architecture review loop is automatic.** You don't need to intervene while the planner, architect, and engineer debate the RFC — only respond when the agent pauses and explicitly asks for your approval.
- **The simpler baseline matters.** If a modular monolith, smaller change, or lower-operational-risk option can solve the problem, the RFC should make the more complex design prove its value.
- **Feasibility review is read-only.** The engineer checks whether the design can realistically be built, but implementation stays deferred to `/implement_task`.
- **Vertical slicing matters.** The task breakdown in Phase 4 intentionally avoids horizontal layers (e.g., "do all the DB migrations first"). Each task delivers a complete, testable slice of functionality.
- **Templates live under `assets/templates/`.** `SKILL.md` references the PRD, RFC, and Implementation Plan templates there so the reusable output scaffolds stay separate from the core skill instructions.

---

## Changelog

### v1.5.0 — 2026-06-17
- **PRD Template:** Added a standard PRD output template under `assets/templates/` and updated Phase 1 to use it.

### v1.4.0 — 2026-06-17
- **RFC & Implementation Plan Templates:** Added standard output templates under `assets/templates/` and updated the execution steps to enforce them.

### v1.3.0 — 2026-06-17
- **Architecture Review Board Model:** Updated README to document the red-team, implementation-feasibility, scorecard, baseline-comparison, and convergence loop added to `SKILL.md`.
- **Planning-Only Boundary:** Clarified that feasibility review may inspect code but must not modify implementation files.
- **RFC Expectations:** Added decision scorecard criteria and required RFC content.

### v1.2.0 — 2026-05-06
- **Planning-Only Constraint:** Explicitly restricted skill to documentation and planning; prohibited code implementation.
- **Checkbox Task Lists:** Updated Phase 4 to generate `tasks_<feature_name>.md` with Markdown checkboxes (`[ ]`) for better tracking.

### v1.1.0 — 2026-05-06
- **Updated to use specialized sub-agents.**
- Phases now explicitly delegate to `pm`, `planner`, `architect`, and `engineer` sub-agents.
- README updated to reflect the new architecture.

### v1.0.0 — 2026-05-06
- **Initial release** as an agent skill, converted from `workflows/request_feature.md`.
- Skill packaged under `.agents/skills/request_feature/SKILL.md` following the standard skill anatomy (`name`, `description` frontmatter + markdown body).
- Description updated with explicit trigger phrases and "pushy" wording to improve skill auto-detection.
- All four pipeline phases preserved exactly from the original workflow: Requirements, Technical Design, Design Review, Planning.
- All human checkpoints (Inversions), persona shifts, internal pipeline loops, sub-skill invocations, and output file paths carried over unchanged.
