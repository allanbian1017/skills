# request_feature

> Autonomous AI Plan Pipeline — from raw idea to a reviewed, task-ready implementation plan.

## Overview

`request_feature` is an agent skill that orchestrates a **multi-phase, multi-persona planning pipeline** for turning a new feature idea into a fully-reviewed, task-broken-down implementation plan. Each phase adopts a different professional persona (Product Manager → Planner → Architect → Engineer), produces a concrete document artifact, and pauses for human approval before advancing to the next stage.

The pipeline is designed around **human-in-the-loop checkpoints** ("Inversions") so that nothing proceeds until you explicitly sign off, keeping you in control of quality at every gate.

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
│  1. Requirements    │  Product Manager persona → writes PRD
│     Phase           │  ⏸ Waits for "Approved"
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│  2. Technical       │  Planner persona → writes RFC
│     Design Phase    │  (no human pause — flows into review)
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│  3. Design Review   │  Architect persona → critiques RFC
│     Phase           │  Internal Planner↔Architect loop
│                     │  ⏸ Waits for "Approved"
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│  4. Planning Phase  │  Engineer persona → task breakdown
│                     │  Produces plan + tasks files
│                     │  ⏸ Presents for human review
└─────────────────────┘
```

---

## Phase-by-Phase Reference

### Phase 1 — Requirements

| Item | Detail |
|------|--------|
| **Persona** | Product Manager |
| **Sub-skill used** | `write_prd` |
| **Input** | `<idea>` provided in the command |
| **Output file** | `docs/prds/prd_<feature_name>.md` |
| **Human checkpoint** | ✅ Yes — loops until user types `"Approved"` |

The agent adopts the Product Manager persona and invokes the `write_prd` skill to draft a Product Requirements Document. The pipeline halts after the PRD is saved. You review it, provide feedback (or edit the file directly), and the agent will revise until you approve.

---

### Phase 2 — Technical Design

| Item | Detail |
|------|--------|
| **Persona** | Planner |
| **Sub-skill used** | Planning Process + Plan Format (from `AGENTS.md`) |
| **Input** | Approved `docs/prds/prd_<feature_name>.md` |
| **Output file** | `docs/rfcs/rfc_<feature_name>.md` |
| **Human checkpoint** | ❌ No — automatically transitions to Design Review |

Using the approved PRD, the agent shifts to the Planner persona and generates a technical RFC (Request for Comments). This covers architecture approach, component design, and key technical decisions. The output feeds directly into Phase 3.

---

### Phase 3 — Design Review

| Item | Detail |
|------|--------|
| **Persona** | Architect (reviewer) + Planner (reviser) |
| **Sub-skill used** | None (internal persona loop) |
| **Input** | `docs/rfcs/rfc_<feature_name>.md` |
| **Output file** | Updated `docs/rfcs/rfc_<feature_name>.md` |
| **Human checkpoint** | ✅ Yes — loops until user types `"Approved"` |

The Architect persona critically reviews the RFC — asking hard architecture questions, identifying risks, and providing critique. The feedback is passed back to the Planner persona internally, which updates the RFC. This internal loop repeats until the Architect is satisfied. Then the pipeline pauses for **your** review of the now-internally-approved RFC. If you provide further feedback, the Planner+Architect loop repeats.

---

### Phase 4 — Planning

| Item | Detail |
|------|--------|
| **Persona** | Engineer |
| **Sub-skill used** | `planning-and-task-breakdown` |
| **Input** | Approved `docs/rfcs/rfc_<feature_name>.md` + relevant codebase sections |
| **Output files** | `docs/plans/plan_<feature_name>.md`, `docs/plans/tasks_<feature_name>.md` |
| **Human checkpoint** | ✅ Yes — presents plan for review |

The Engineer persona reads the approved RFC and the relevant parts of the codebase, then invokes the `planning-and-task-breakdown` skill to produce a detailed implementation plan. From the plan, a separate tasks file is generated with:

- **Dependency graph** between components
- **Vertical slicing** — each task is one complete end-to-end path, not a horizontal layer
- **Acceptance criteria** and **verification steps** per task
- **Checkpoints** between phases

The final plan is presented for your review before the pipeline ends.

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

Two explicit approval gates exist in the pipeline:

| Gate | Trigger condition | How to advance |
|------|-------------------|----------------|
| After PRD | Agent halts and asks for review | Type `Approved` |
| After RFC review | Agent halts and asks for RFC approval | Type `Approved` |

If you provide **any other response**, the agent interprets it as feedback and revises the relevant document before asking again.

---

## Dependencies

This skill orchestrates two other skills and respects the project's `AGENTS.md`:

| Dependency | Purpose | Location |
|------------|---------|----------|
| `write_prd` | Generates the PRD in Phase 1 | `.agents/skills/write_prd/` |
| `planning-and-task-breakdown` | Generates the plan and task list in Phase 4 | `.agents/skills/planning-and-task-breakdown/` |
| `AGENTS.md` | Defines Planning Process, Plan Format, and agent rules | Project root |

Ensure all three are present and up to date before invoking this skill.

---

## File Structure

```
.agents/skills/request_feature/
├── SKILL.md      ← Agent instructions & frontmatter (triggers + pipeline)
└── README.md     ← This file
```

---

## Tips & Notes

- **Be specific in your idea.** The more context you give (`/request_feature <idea>`), the richer the PRD and RFC will be. A vague idea produces a vague PRD.
- **Edit files directly.** During checkpoints, you can edit the PRD or RFC file in your editor — the agent will read and incorporate your changes before asking again.
- **The internal Architect loop is automatic.** You don't need to intervene during Phase 3's internal review — only respond when the agent pauses and explicitly asks for your approval.
- **Vertical slicing matters.** The task breakdown in Phase 4 intentionally avoids horizontal layers (e.g., "do all the DB migrations first"). Each task delivers a complete, testable slice of functionality.
- **`AGENTS.md` is authoritative.** The Planning Process and Plan Format used in Phase 2 and Phase 4 are defined in your project's `AGENTS.md`. Keeping that file current ensures the pipeline produces consistent output.

---

## Changelog

### v1.0.0 — 2026-05-06
- **Initial release** as an agent skill, converted from `workflows/request_feature.md`.
- Skill packaged under `.agents/skills/request_feature/SKILL.md` following the standard skill anatomy (`name`, `description` frontmatter + markdown body).
- Description updated with explicit trigger phrases and "pushy" wording to improve skill auto-detection.
- All four pipeline phases preserved exactly from the original workflow: Requirements, Technical Design, Design Review, Planning.
- All human checkpoints (Inversions), persona shifts, internal pipeline loops, sub-skill invocations, and output file paths carried over unchanged.
