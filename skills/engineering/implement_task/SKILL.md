---
name: implement_task
description: Start the Autonomous AI Developer Pipeline sequence with a planned feature. Use this skill whenever the user types `/implement_task <feature_name>` or asks to implement a planned task end-to-end — picking the next pending task from the task list, writing tests, implementing code, running CI, and running a full code review loop until the PR is approved and merged. Trigger this skill for any request to execute a task that already has a plan and tasks list in place using the established agent pipeline.
---

When the user types `/implement_task <feature_name>`, orchestrate the development process strictly using `AGENTS.md` and `.agents/skills/`.

### Execution Sequence:

1. **Implementation Phase:**
   - Invoke the **engineer** sub-agent.
   - Pick the next pending task from the tasks list `docs/plans/tasks_<feature_name>.md`.
   - Read the task's details and acceptance criteria from `docs/plans/plan_<feature_name>.md`.
   - Execute `incremental_implement` skill alongside `test-driven-development` skill to implement the task.
   - Load relevant context (existing code, patterns, types).
   - Write a failing test for the expected behavior (RED).
   - Implement the minimum code to pass the test (GREEN).
   - Run the full test suite to check for regressions.
   - Run the build to verify compilation.
   - Commit with a descriptive message.
   - Verify the implementation using the planned verify method. Only proceed when verification is completed and passes.
   - Once completed, update the task list `docs/plans/tasks_<feature_name>.md` to mark the task as completed (e.g., change `[ ]` to `[x]`).
2. **Code Review Phase:**
   - Invoke the **code-reviewer** sub-agent.
   - Review the Engineer's submitted Pull Request against the RFC (`docs/rfcs/rfc_<feature_name>.md`), Plan (`docs/plans/plan_<feature_name>.md`), Tasks (`docs/plans/tasks_<feature_name>.md`) and general code quality standards.
   - **Internal Pipeline Loop:** Provide feedback to the **engineer** sub-agent to revise the PR. Repeat until the **code-reviewer** sub-agent approves the PR.
   - **Inversion (Wait for User):** Halt execution. Ask the user for final PR approval. If the user provides feedback, revert to the **engineer** sub-agent to update, and **code-reviewer** sub-agent to re-review. Loop until the user inputs "Approved".
