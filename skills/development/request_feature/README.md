# request_feature

> Autonomous AI Plan Pipeline — from raw idea to a reviewed, task-ready implementation plan.

## Overview

`request_feature` is an agent skill that orchestrates a **multi-phase, multi-persona planning pipeline** for turning a new feature idea into a fully-reviewed, task-broken-down implementation plan. It delegates work to specialized sub-agents (PM → Architect → Architecture Reviewer + Engineer → Technical Writer → Planner), with each phase producing concrete document artifacts and pausing for human approval at the major decision gates.

The pipeline is designed around **human-in-the-loop checkpoints** ("Inversions") and an internal architecture review board model. Designs are proposed, red-teamed, checked for implementation feasibility, scored against tradeoffs, compared with a simpler baseline, validated through documentation drafting, and revised before you are asked to approve.

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
│  2. Technical       │  Architect sub-agent → writes RFC
│     Design Phase    │  Includes simpler baseline + scorecard
│                     │  (no human pause — flows into review)
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│  3. Design Review   │  Architecture-Reviewer red-teams RFC + Pre-Mortem
│     Phase           │  Engineer checks implementation feasibility
│                     │  Architect revises, scores, compares baseline
│                     │  ⏸ Waits for "Approved"
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│  4. Documentation   │  Technical-Writer sub-agent → drafts docs
│     Phase           │  ⏸ Waits for "Approved"
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│  5. Planning Phase  │  Planner sub-agent → task breakdown
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
| **Sub-agent** | `architect` |
| **Sub-skill used** | RFC Template (`assets/templates/rfc_template.md`) |
| **Input** | Approved `docs/prds/prd_<feature_name>.md` |
| **Output file** | `docs/rfcs/rfc_<feature_name>.md` |
| **Human checkpoint** | ❌ No — automatically transitions to Design Review |

Using the approved PRD, the agent invokes the **architect** sub-agent to generate a technical RFC (Request for Comments). This covers system architecture, component design, and key technical decisions.

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
- Completed **Architecture Tradeoff Checklist** (appended as `## Appendix: Architecture Tradeoff Checklist`)

The architect fills the [Architecture Tradeoff Checklist](assets/templates/tradeoff_checklist_template.md) for all relevant project domains (Backend/API, AI Agent, Frontend/Web, Mobile Client), marking inapplicable items as N/A with a one-liner justification. Checklist findings must be referenced when justifying the RFC Decision Criteria scorecard scores.

If the proposed design is more complex than the simpler baseline, the RFC must justify why the extra operational cost is necessary. The output feeds directly into Phase 3.

---

### Phase 3 — Design Review

| Item | Detail |
|------|--------|
| **Sub-agent** | `architecture-reviewer` (red-team reviewer) + `engineer` (feasibility reviewer) + `architect` (reviser) |
| **Sub-skill used** | None (internal sub-agent loop) |
| **Input** | `docs/rfcs/rfc_<feature_name>.md` |
| **Output file** | Updated `docs/rfcs/rfc_<feature_name>.md` |
| **Human checkpoint** | ✅ Yes — loops until user types `"Approved"` |

The **architecture-reviewer** sub-agent red-teams the RFC by looking for bottlenecks, weak assumptions, unclear ownership, failure modes, security risks, over-engineering, under-specified operations, and bad cost tradeoffs. It also validates the **Architecture Tradeoff Checklist** appendix — flagging any item left blank without justification or any tradeoff decision that contradicts the RFC design as a blocking review finding. Additionally, it conducts a mandatory **Pre-Mortem analysis**: assuming the feature launched and caused a critical production outage or user data loss one month later, then writing a post-mortem explaining what went wrong.

The **engineer** sub-agent performs a read-only implementation feasibility review. It checks codebase impact, migration complexity, required interfaces, testing strategy, rollout plan, backward compatibility, CI/CD implications, and operational readiness. This is still planning work; it must not implement anything.

The authoring **architect** sub-agent revises the RFC using both reviews, re-scores the design, and compares it against the simpler baseline. The internal loop repeats until the **architecture-reviewer** approves the RFC and either the score no longer materially improves or all high-severity risks have documented mitigations. The loop is capped at three internal rounds unless a blocking risk remains unresolved.

Then the pipeline pauses for **your** review of the now-internally-approved RFC. If you provide further feedback, the Architect+Reviewer review loop repeats.

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

### Phase 4 — Documentation

| Item | Detail |
|------|--------|
| **Sub-agent** | `technical-writer` |
| **Sub-skill used** | None (persona-driven) |
| **Input** | Approved `docs/rfcs/rfc_<feature_name>.md` |
| **Output files** | Draft documentation in `docs/` (e.g., API reference, README additions) |
| **Human checkpoint** | ✅ Yes — waits for approval before planning begins |

The **technical-writer** sub-agent reads the approved RFC and drafts external-facing documentation such as API references and README additions. This enforces **Docs-Driven Development**: if the writer cannot explain the feature clearly, the architecture may be too complex. Documentation drafts are saved to the `docs/` folder for the engineer to incorporate later during implementation.

---

### Phase 5 — Planning

| Item | Detail |
|------|--------|
| **Sub-agent** | `planner` |
| **Sub-skill used** | `planning-and-task-breakdown` |
| **Input** | Approved `docs/rfcs/rfc_<feature_name>.md` + relevant codebase sections |
| **Output files** | `docs/plans/plan_<feature_name>.md`, `docs/plans/tasks_<feature_name>.md` |
| **Human checkpoint** | ✅ Yes — presents plan for review |

The agent invokes the **planner** sub-agent to read the approved RFC and the relevant parts of the codebase, then invokes the `planning-and-task-breakdown` skill, using the Implementation Plan Template at `assets/templates/plan_template.md`, to produce a detailed implementation plan. From the plan, a separate tasks file is generated with:

- **Dependency graph** between components
- **Vertical slicing** — each task is one complete end-to-end path, not a horizontal layer
- **Acceptance criteria** and **verification steps** per task
- **Checkpoints** between phases

The final plan is presented for your review before the pipeline ends.

Phase 5 produces implementation-ready planning artifacts only. It does not start implementation, stage code, run feature work, or modify application files.

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

Four explicit approval gates exist in the pipeline:

| Gate | After Phase | Trigger condition | How to advance |
|------|-------------|-------------------|----------------|
| 1 | PRD (Phase 1) | Agent halts and asks for review | Type `Approved` |
| 2 | RFC Review (Phase 3) | Agent halts after internal Architect↔Reviewer loop | Type `Approved` |
| 3 | Documentation (Phase 4) | Agent halts after drafting docs | Type `Approved` |
| 4 | Planning (Phase 5) | Agent presents plan for review | Review before invoking `/implement_task` |

If you provide **any other response**, the agent interprets it as feedback and revises the relevant document before asking again.

---

## Dependencies

This skill orchestrates specialized sub-agents and other skills, respecting the project's `AGENTS.md`:

| Dependency | Purpose | Location |
|------------|---------|----------|
| `pm` | Writes PRD in Phase 1 | `.agents/agents/pm.md` |
| `architect` | Drafts RFC in Phase 2, revises in Phase 3 | `.agents/agents/architect.md` |
| `architecture-reviewer` | Red-teams RFC with Pre-Mortem in Phase 3 | `.agents/agents/architecture-reviewer.md` |
| `engineer` | Feasibility review in Phase 3 | `.agents/agents/engineer.md` |
| `technical-writer` | Drafts documentation in Phase 4 | `.agents/agents/technical-writer.md` |
| `planner` | Writes plan and tasks in Phase 5 | `.agents/agents/planner.md` |
| `write_prd` | Generates the PRD in Phase 1 | `.agents/skills/write_prd/` |
| `planning-and-task-breakdown` | Generates the plan and task list in Phase 5 | `.agents/skills/planning-and-task-breakdown/` |
| `AGENTS.md` | Defines agent rules and conventions | Project root |

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
        ├── rfc_template.md
        └── tradeoff_checklist_template.md
```

---

## Tips & Notes

- **Be specific in your idea.** The more context you give (`/request_feature <idea>`), the richer the PRD and RFC will be. A vague idea produces a vague PRD.
- **Edit files directly.** During checkpoints, you can edit the PRD or RFC file in your editor — the agent will read and incorporate your changes before asking again.
- **The internal architecture review loop is automatic.** You don't need to intervene while the architecture-reviewer, architect, and engineer debate the RFC — only respond when the agent pauses and explicitly asks for your approval.
- **The simpler baseline matters.** If a modular monolith, smaller change, or lower-operational-risk option can solve the problem, the RFC should make the more complex design prove its value.
- **Feasibility review is read-only.** The engineer checks whether the design can realistically be built, but implementation stays deferred to `/implement_task`.
- **Documentation validates design.** Phase 4 acts as a usability test — if the technical writer struggles to explain the feature, the architecture may need simplification.
- **Vertical slicing matters.** The task breakdown in Phase 5 intentionally avoids horizontal layers (e.g., "do all the DB migrations first"). Each task delivers a complete, testable slice of functionality.
- **Templates live under `assets/templates/`.** `SKILL.md` references the PRD, RFC, Architecture Tradeoff Checklist, and Implementation Plan templates there so the reusable output scaffolds stay separate from the core skill instructions.

## Architecture Decisions (ADRs)

### ADR-0001: Architecture Tradeoff Checklist Integration (v2.1.0)
*   **Context:** The pipeline's 9-dimension RFC Decision Scorecard and mandatory Pre-Mortem analysis covered high-level design quality, but architectural tradeoff analysis was scattered across prose instructions rather than structurally enforced. Key gaps included: Latency & Concurrency (PRD had a one-liner, RFC had no dedicated section), Data Architecture & State (open-ended "Detailed Design" with no forced SSOT or consistency model decision), AI Agent-specific tradeoffs (fan-out/fan-in, context pollution, provider fallback not prompted), and domain-adaptive filtering (no mechanism to activate relevant sections per project type). Inspired by Andrew Ng's "Software Engineering Foundations in the Agentic Coding Era."
*   **Decision:** Adopted a standalone Architecture Tradeoff Checklist template (`tradeoff_checklist_template.md`) with 5 dimensions × 4 domains and 67 checkbox items. The architect fills it during RFC authoring (Phase 2) and appends it as an RFC appendix. The architecture-reviewer validates completeness and challenges decisions during Design Review (Phase 3). Checklist findings inform scorecard scores without structural merge.
*   **Rejected Alternatives:**
    - Separate pipeline gate (Step 1.5): Redundant — architect repeats tradeoff work when writing the RFC.
    - Embedded in RFC template: Makes RFC ~200 lines; mixes narrative with checkbox format.
    - Separate files per domain: Loses forced cross-domain consideration.
*   **Consequences:** Architects are structurally forced to confront 67 specific concerns before proposing a design. Architecture-reviewers have a concrete checklist to validate. RFC files become longer (~50–100 lines of appendix). Risk of rubber-stamp filling is mitigated by the reviewer validation pass.

---

## Changelog

### v2.1.0 — 2026-09-01
- **Architecture Tradeoff Checklist:** Added `tradeoff_checklist_template.md` — a universal 5-dimension × 4-domain checklist (Latency & Concurrency, Data Architecture & State, Availability & Blast Radius, Security & Trust, Verification & Observability) with 67 structured checkpoint items.
- **Phase 2 Integration:** Architect must complete the checklist during RFC authoring and append it as an RFC appendix. Checklist findings must be referenced when justifying scorecard scores.
- **Phase 3 Integration:** Architecture-reviewer must validate checklist completeness and flag blank or contradictory items as blocking findings.

### v2.0.0 — 2026-08-11
- **Role Realignment:** Reassigned pipeline phases to match agent personas:
  - Phase 2 now uses `architect` (was `planner`) to write RFCs.
  - Phase 3 now uses `architecture-reviewer` (was `architect`) for red-team review.
  - Phase 5 now uses `planner` (was `engineer`) to write plans and tasks.
- **New Agent — `architecture-reviewer`:** Dedicated Devil's Advocate reviewer for Phase 3 with Pre-Mortem analysis baked into its persona. Replaces the previous `architect`-reviews-own-work pattern.
- **New Phase 4 — Documentation:** Added `technical-writer` sub-agent to draft external-facing docs before planning begins, enforcing Docs-Driven Development.
- **4 Human Review Gates:** Pipeline now has 4 explicit approval checkpoints (was 2).

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
