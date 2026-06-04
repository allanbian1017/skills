---
name: implement_task
description: Start the Autonomous AI Developer Pipeline sequence with a planned feature. Use this skill whenever the user types `/implement_task <feature_name>` or asks to implement a planned task end-to-end — picking the next pending task from the task list, writing tests, implementing code, running CI, and running a full code review loop until the PR is approved and merged. Trigger this skill for any request to execute a task that already has a plan and tasks list in place using the established agent pipeline.
---

When the user types `/implement_task <feature_name>`, orchestrate the development process strictly using `AGENTS.md` and `.agents/skills/`.

### Execution Sequence:

1. **Pre-Flight Scope Verification (Parent Agent):**
   - Open `docs/plans/tasks_<feature_name>.md` and identify all pending tasks (marked with `[ ]`).
   - Read the plan (`docs/plans/plan_<feature_name>.md`) and the RFC (`docs/rfcs/rfc_<feature_name>.md`).
   - Evaluate if the tasks have strong logical coupling or sequential blocking dependencies (e.g. CI workflow setup depending on test suites).
   - If coupling is detected, the agent **MUST halt execution** and suggest batching all related tasks in one pass.
   - Ask the user to choose: **[Take 1]** (execute only the first pending task) or **[Take All]** (execute the suggested batch).
   - Proceed to Phase 1 only after receiving the user's explicit decision.

2. **Phase 1 — Implementation Phase:**
   - Invoke the **engineer** sub-agent.
   - **Sanitized Context Guardrail:**
     - Give the sub-agent access to the full RFC and Plan files for design context.
     - Constrain the sub-agent's prompt instructions to **ONLY execute the chosen task(s)** (either the single task or the approved batch).
   - Execute the implementation inside the isolated worktree via `incremental_implement` (stopping before Step 5: Merge & Cleanup) and `test-driven-development` skills:
     - Load relevant code and context.
     - Write a failing test (RED).
     - Write minimal code to pass the test (GREEN).
     - Verify with the full test suite and compilation build.
     - Commit atomically.
     - Repeat for all approved tasks in the batch.
   - **Failure Behavior:** If any task in a batch fails, halt immediately, keep the worktree intact for debugging, and present the failure details to the user (treat the batch as a single cohesive unit).
   - Once all approved tasks pass verification locally, push the branch, create the Pull Request, and wait for CI checks to pass.
   - Once CI passes and the PR is ready for review, update the task checklist in `docs/plans/tasks_<feature_name>.md` to mark all successfully completed tasks in the batch as complete (`[x]`).

3. **Phase 2 — Code Review Phase:**
   - Invoke the **code-reviewer** sub-agent.
   - Review the Pull Request against the RFC, Plan, Tasks, and coding standards.
   - **Internal Loop:** If review fails, provide feedback to the **engineer** sub-agent to revise the PR. Repeat until approved internally.
   - **Inversion (Wait for User):** Halt execution and present the PR to the user. Wait for the user to review and input "Approved". If feedback is given, revert to the engineer and reviewer sub-agents to revise.

4. **Phase 3 — Deployment Phase:**
   - Invoke the **deploy** sub-agent.
   - Merge the approved Pull Request using `gh pr merge --squash --delete-branch`.
   - Perform cleanup of the isolated worktree (`git worktree remove` and `git worktree prune`).

