---
name: implement_task
description: Start the Autonomous AI Developer Pipeline sequence with a planned feature. Use this skill whenever the user types `/implement_task <feature_name>` or asks to implement a planned task end-to-end — picking the next pending task from the task list, writing tests, implementing code, running CI, and running a full code review loop until the PR is approved and merged. Trigger this skill for any request to execute a task that already has a plan and tasks list in place using the established agent pipeline.
---

When the user types `/implement_task <feature_name>`, orchestrate the development process strictly using `AGENTS.md` and `.agents/skills/`.

### Implementation Review Board Model

Use the implementation pipeline as an automated implementation review board:

- **Scope Orchestrator:** The parent agent reads the RFC, plan, and task list; selects only the user-approved task scope; and prevents task drift.
- **Implementer:** The **engineer** sub-agent executes the approved scope with `incremental_implement` and `test-driven-development`.
- **Test Red-Team Reviewer:** The **code-reviewer** sub-agent challenges whether the RED test actually proves the acceptance criteria, whether important negative or regression cases are missing, and whether the verification commands are sufficient.
- **Code Risk Reviewer:** The **code-reviewer** sub-agent attacks the PR for bugs, security issues, reliability regressions, hidden coupling, scope creep, over-engineering, and maintainability problems.
- **Release Readiness Reviewer:** The **deploy** sub-agent verifies merge readiness after human approval: CI status, PR approval state, migration or rollback notes, branch target, and worktree cleanup plan.
- **Decision Orchestrator:** The parent agent passes artifacts between agents, enforces review rounds, prevents agents from ignoring constraints, and halts when an unresolved high-severity risk lacks a fix or an explicit user-approved deferral.

Every phase should produce structured artifacts rather than relying on conversational confidence. Capture scope decisions, test evidence, implementation summary, review findings, unresolved risks, score changes, and release readiness notes.

### Implementation Scorecard

During implementation and review, score the PR from 1 to 10 on:

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

The scorecard is not a substitute for passing tests, CI, or review. Any high-severity issue in correctness, security, data safety, or scope control blocks progress until fixed or explicitly escalated to the user.

### Execution Sequence:

1. **Pre-Flight Scope Verification (Parent Agent):**
   - Open `docs/plans/tasks_<feature_name>.md` and identify all pending tasks (marked with `[ ]`).
   - Read the plan (`docs/plans/plan_<feature_name>.md`) and the RFC (`docs/rfcs/rfc_<feature_name>.md`).
   - Build a structured scope artifact containing:
     - Pending task candidates.
     - Recommended execution scope.
     - Known dependencies and blockers.
     - Simpler/smaller viable execution option when one exists.
     - Expected verification commands from the plan.
     - Tradeoff risks: cross-reference the RFC's Architecture Tradeoff Checklist appendix against the task scope. Flag any task touching a dimension with unresolved or high-risk tradeoffs as an implementation risk.
     - Initial implementation risks.
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
   - After each approved task or cohesive batch, produce a structured implementation artifact:
     - Approved scope executed.
     - Files changed.
     - RED test evidence and command output summary.
     - GREEN verification evidence and command output summary.
     - Full-suite/build verification evidence.
     - Implementation scorecard using the **Implementation Scorecard** criteria.
     - Risks introduced, risks retired, and any unresolved risks.
   - **Failure Behavior:** If any task in a batch fails, halt immediately, keep the worktree intact for debugging, and present the failure details to the user (treat the batch as a single cohesive unit).
   - Once all approved tasks pass verification locally, push the branch, create the Pull Request, and wait for CI checks to pass.
   - Once CI passes and the PR is ready for review, update the task checklist in `docs/plans/tasks_<feature_name>.md` to mark all successfully completed tasks in the batch as complete (`[x]`).

3. **Phase 2 — Code Review Phase:**
   - Invoke the **code-reviewer** sub-agent.
   - Review the Pull Request against the RFC, Plan, Tasks, implementation artifact, test evidence, CI results, and coding standards.
   - Perform the review in three explicit passes:
     - **Test Red-Team Pass:** Challenge test quality, missing edge cases, weak assertions, false-positive RED tests, inadequate regression coverage, and missing plan verification.
     - **Code Risk Pass:** Challenge bugs, security issues, reliability regressions, hidden coupling, scope creep, over-engineering, maintainability, backward compatibility, and operational readiness.
     - **Tradeoff Compliance Pass:** Verify the implementation respects the tradeoff decisions documented in the RFC's Architecture Tradeoff Checklist appendix. Flag any divergence as a review finding.
   - Re-score the PR using the **Implementation Scorecard** after each review round.
   - **Internal Loop:** If review fails, provide structured feedback to the **engineer** sub-agent to revise the PR. Repeat implementation revision, verification, scorecard update, and review until approved internally. Cap the internal review loop at three rounds unless a blocking risk remains unresolved.
   - **Inversion (Wait for User):** Halt execution and present the PR to the user. Wait for the user to review and input "Approved". If feedback is given, revert to the engineer and reviewer sub-agents to revise.

4. **Phase 3 — Deployment Phase:**
   - Invoke the **deploy** sub-agent.
   - Before merging, perform a release readiness check:
     - Confirm the user explicitly approved the PR.
     - Confirm CI is still passing for the latest pushed commit.
     - Confirm the PR targets the intended base branch.
     - Confirm checklist updates match only the completed approved scope.
     - Confirm migration, rollback, or operational notes are documented when relevant.
     - Confirm no high-severity review findings remain unresolved.
   - Merge the approved Pull Request using `gh pr merge --squash --delete-branch`.
   - Perform cleanup of the isolated worktree (`git worktree remove` and `git worktree prune`).
