---
name: request_feature
description: Start the Autonomous AI Plan Pipeline sequence with a new idea. Use this skill whenever the user types `/request_feature <idea>` or asks to kick off a full feature development pipeline — from requirements writing through PRD, RFC design review, and task breakdown planning. Trigger this skill for any request to take a feature idea through the full autonomous planning lifecycle using the established agent pipeline.
---

When the user types `/request_feature <idea>`, orchestrate the development process strictly using `AGENTS.md` and `.agents/skills/`.

### Execution Sequence:

1. **Requirements Phase:**
   - Adopt the **Product Manager** persona.
   - Execute the `write_prd` skill using the provided `<idea>`.
   - Save the output to `docs/prds/prd_<feature_name>.md`.
   - **Inversion (Wait for User):** Halt execution. Ask the user to review the PRD. If the user provides feedback or modifies the file, read the changes and revise the PRD. Loop this sub-step until the user explicitly inputs "Approved".
2. **Technical Design Phase:**
   - Shift context
   - Adopt the **Planner** persona.
   - Read the approved `docs/prds/prd_<feature_name>.md`.
   - Follow the **Planning Process** to generate an plan which followed the **Plan Format**
   - Save the output to `docs/rfcs/rfc_<feature_name>.md`.
3. **Design Review Phase:**
   - Shift context
   - Adopt the **Architect** persona.
   - Read `docs/rfcs/rfc_<feature_name>.md` and ask critical architecture questions or provide critique.
   - **Internal Pipeline Loop:** Pass feedback back to the **Planner** persona to update the RFC. Repeat until the **Architect** persona explicitly approves the RFC.
   - **Inversion (Wait for User):** Once internally approved, halt execution. Ask the user for RFC approval. If the user provides feedback, revert to the **Planner** persona to update, then the **Architect** persona to re-review. Loop until the user inputs "Approved".
4. **Planning Phase:**
   - Shift context
   - Adopt the **Engineer** persona.
   - Read `docs/rfcs/rfc_<feature_name>.md` and the relevant codebase sections.
   - Execute the `planning-and-task-breakdown` skill to plan the `<feature_name>`.
   - Save the output to `docs/plans/plan_<feature_name>.md`.
   - Read `docs/plans/plan_<feature_name>.md` and create tasks list `docs/plans/tasks_<feature_name>.md`.
   - Identify the dependency graph between components
   - Slice work vertically (one complete path per task, not horizontal layers)
   - Write tasks with acceptance criteria and verification steps
   - Add checkpoints between phases
   - Present the plan for human review
