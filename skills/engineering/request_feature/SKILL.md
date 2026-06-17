---
name: request_feature
description: Start the Autonomous AI Plan Pipeline sequence with a new idea. Use this skill whenever the user types `/request_feature <idea>` or asks to kick off a full feature development pipeline — from requirements writing through PRD, RFC design review, and task breakdown planning. This skill focuses EXCLUSIVELY on feature planning and MUST NOT perform any code implementation or modifications to source files beyond documentation. Trigger this skill for any request to take a feature idea through the full autonomous planning lifecycle using the established agent pipeline.
---

When the user types `/request_feature <idea>`, orchestrate the development process strictly using `AGENTS.md` and `.agents/skills/`. This skill is limited to research and planning; implementation must be handled separately via `/implement_task`.

### Planning-Only Boundary

- Produce and revise documentation artifacts only: PRDs, RFCs, plans, task lists, scorecards, and decision rationale.
- Read relevant codebase sections when needed to assess feasibility and impact, but do not modify application code, tests, configuration, dependencies, or implementation files.
- Treat implementation feasibility as a design input, not as permission to implement. Any code changes must be deferred to `/implement_task`.

### Architecture Review Board Model

Use the request pipeline as an automated architecture review board:

- **Requirement Clarifier:** The **pm** sub-agent turns the idea into an agreed engineering brief before design begins.
- **Design Proposer:** The **planner** sub-agent writes the initial RFC and defends a concrete design.
- **Red-Team Reviewer:** The **architect** sub-agent critiques the RFC for bottlenecks, weak assumptions, unclear ownership, failure modes, security risks, over-engineering, under-specified operations, and bad cost tradeoffs.
- **Implementation Feasibility Reviewer:** The **engineer** sub-agent performs read-only analysis of codebase impact, migration complexity, interfaces, testing strategy, rollout, backward compatibility, CI/CD implications, and operational readiness.
- **Decision Orchestrator:** The main agent passes artifacts between sub-agents, enforces review rounds, prevents constraint drift, compares against a simpler baseline, and stops only when the design is stable enough for human approval.

Every design review response should be treated as a structured artifact, not as chat. Capture assumptions, risks, tradeoffs, open questions, score changes, and explicit decisions in the RFC.

### RFC Decision Criteria

During technical design and design review, score the RFC from 1 to 10 on:

- Correctness
- Scalability
- Reliability
- Security
- Cost
- Simplicity
- Implementation effort
- Observability
- Maintainability

The RFC must include the final recommended design, rejected alternatives, simpler baseline comparison, service or module boundaries, data ownership, API or interface contracts, event or control flows when relevant, failure scenarios, observability plan, security review, rollout strategy, open risks, and decision rationale.

### Execution Sequence:

1. **Requirements Phase:**
   - Invoke the **pm** sub-agent.
   - Execute the `write_prd` skill using the provided `<idea>`.
   - Ensure the PRD clarifies users and actors, traffic assumptions, latency goals, availability target, consistency requirements, compliance constraints, existing systems, non-goals, and unknowns when relevant.
   - Save the output to `docs/prds/prd_<feature_name>.md`.
   - **Inversion (Wait for User):** Halt execution. Ask the user to review the PRD. If the user provides feedback or modifies the file, read the changes and revise the PRD. Loop this sub-step until the user explicitly inputs "Approved".
2. **Technical Design Phase:**
   - Invoke the **planner** sub-agent.
   - Read the approved `docs/prds/prd_<feature_name>.md`.
   - Generate an initial RFC proposal following the **Planning Process** and **Plan Format**.
   - Include at least one simpler baseline alternative. If the proposed design is more complex than the baseline, justify why the extra operational cost is necessary.
   - Include an initial decision scorecard using the **RFC Decision Criteria**.
   - Save the output to `docs/rfcs/rfc_<feature_name>.md`.
3. **Design Review Phase:**
   - Invoke the **architect** sub-agent.
   - Read `docs/rfcs/rfc_<feature_name>.md` and red-team the design. Ask critical architecture questions, identify risks, and challenge unnecessary complexity.
   - Invoke the **engineer** sub-agent for a read-only implementation feasibility review. Do not implement. Review codebase impact, migration complexity, required interfaces, test strategy, rollout plan, backward compatibility, CI/CD implications, and operational readiness.
   - Pass architect and engineer feedback back to the **planner** sub-agent to revise the RFC.
   - Re-score the revised RFC using the **RFC Decision Criteria** and compare it against the simpler baseline.
   - **Internal Pipeline Loop:** Repeat critique, feasibility review, revision, baseline comparison, and scoring until the **architect** sub-agent explicitly approves the RFC and either scores no longer materially improve or all high-severity risks have documented mitigations. Cap the loop at three internal rounds unless a blocking risk remains unresolved.
   - **Inversion (Wait for User):** Once internally approved, halt execution. Ask the user for RFC approval. If the user provides feedback, revert to the **planner** sub-agent to update, then the **architect** sub-agent to re-review. Loop until the user inputs "Approved".
4. **Planning Phase:**
   - Invoke the **engineer** sub-agent.
   - Read `docs/rfcs/rfc_<feature_name>.md` and the relevant codebase sections.
   - Execute the `planning-and-task-breakdown` skill to plan the `<feature_name>`.
   - Save the output to `docs/plans/plan_<feature_name>.md`.
   - Read `docs/plans/plan_<feature_name>.md` and create tasks list `docs/plans/tasks_<feature_name>.md` using Markdown checkboxes (`[ ]`).
   - Identify the dependency graph between components
   - Slice work vertically (one complete path per task, not horizontal layers)
   - Write tasks with acceptance criteria and verification steps
   - Add checkpoints between phases
   - Present the plan for human review
