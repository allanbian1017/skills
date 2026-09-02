---
name: investigate_issue
description: >-
  Orchestrates the full issue resolution lifecycle: triage, root cause investigation,
  internal RCA review, human-approved RCA, TDD-driven fix, code review, and merge.
  Use when the user types `/investigate_issue <issue>` or asks to debug, investigate,
  or fix a reported bug end-to-end.
version: 1.0.0
pattern: Pipeline
---

# 🎯 Purpose
To drive the complete issue resolution lifecycle from report to merged fix. The skill coordinates specialized sub-agents through a rigorous pipeline: forensic investigation with evidence-based RCA, internal quality review, human approval, TDD-driven fix implementation, code review, and merge.

# 🚪 Gating & Trigger Conditions
- **When to invoke:** When the user types `/investigate_issue <issue>` or `/investigate_issue #<number>`, or asks to debug, investigate, diagnose, or fix a reported bug end-to-end.
- **When NOT to invoke:**
  - Simple, obvious bugs where the root cause is already known and stated (use `implement_task` with TDD prove-it directly).
  - Feature requests or enhancements (use `request_feature`).
  - Issues in external dependencies or infrastructure outside the codebase.

# 📥 Input Specifications
- `ISSUE_INPUT`: Either an inline text description of the issue or a GitHub Issue reference (`#<number>`).
- **Inferred Context:** Repository name, current working directory, base branch (defaulting to `dev`).

# ⚙️ Execution Instructions (Workflow)

### Investigation & Resolution Board Model

| Role | Agent | Responsibility |
|------|-------|----------------|
| **Issue Triage & Decision Orchestrator** | Parent (orchestrator) | Parses input, routes artifacts, copies files between worktrees, enforces gates |
| **Root Cause Investigator** | `investigator` sub-agent | Reproduces, diagnoses, writes RCA + reproduction test |
| **RCA Quality Gate** | `rca-reviewer` sub-agent | Challenges RCA rigor before human review (max 3 internal rounds) |
| **Human Reviewer** | User | Approves or rejects RCA (no cap on rounds) |
| **Fix Implementer** | `engineer` sub-agent | Verifies RED, implements fix (GREEN), creates PR |
| **Code Reviewer** | `code-reviewer` sub-agent | Reviews fix PR (max 3 internal rounds) |

### Phase 1 — Issue Triage (Orchestrator)

The orchestrator is **thin** — it routes and gates, nothing more.

1. Parse the user's input:
   - If argument matches `#<number>` → fetch issue body via `gh issue view <number> --json title,body,labels`.
   - Otherwise → use the inline text as-is.
2. Generate the issue slug for file naming:
   - GitHub Issue: `<number>_<short-summary>` (e.g., `42_login-special-chars`).
   - Inline: slugify first few words (e.g., `login-special-chars-bug`).
3. Pass the issue context (title, body, labels if available) to the **investigator** sub-agent.

### Phase 2 — Root Cause Investigation (Investigator Sub-Agent)

Invoke the **investigator** sub-agent. The investigator has full command execution and write tools. Its job is forensic diagnosis and proving the bug exists.

1. **Explore**: Read relevant codebase sections, search for error messages, identify affected components.
2. **Reproduce**: Run commands to trigger the bug. Capture actual vs. expected output.
3. **Hypothesize & Reject**: Form alternative hypotheses. Systematically reject each with quantitative evidence (command output, grep results, measured counts). Per AGENTS.md: unverifiable claims are labeled "Hypothesis".
4. **Root Cause**: Identify primary and contributing root causes with direct code/data evidence.
5. **Write Reproduction Test**: Create a test file in the existing test directory, following project conventions. The test must **fail** (RED), proving the bug exists. Follows TDD prove-it pattern (RED phase only — the investigator does NOT implement a fix).
   - If unable to reproduce: write a partial RCA with root cause labeled as "Hypothesis". Skip the reproduction test or write a test based on the hypothesized behavior.
6. **Write RCA Document**: Save to `docs/rcas/rca_<slug>.md` following the [RCA Template](assets/templates/rca_template.md). Include:
   - Observed problem with reproduction evidence.
   - Alternative hypotheses with rejection evidence.
   - Root cause (primary + contributing).
   - Proposed fix strategy with automated verification method.
   - Path to the reproduction test file.
7. **Report**: Return RCA file path and test file path to the orchestrator.

### Phase 3 — Internal RCA Review (RCA Reviewer Sub-Agent)

Invoke the **rca-reviewer** sub-agent. The RCA reviewer challenges the investigator's work before the human sees it.

1. Review the RCA document against these criteria:
   - **Evidence rigor**: Are alternative hypotheses properly rejected with quantitative evidence?
   - **Root cause validity**: Is it a root cause or a symptom?
   - **Reproduction test quality**: Does the test prove the actual bug?
   - **Fix strategy soundness**: Simplest viable approach addressing the root cause?
   - **Missing hypotheses**: Alternative explanations not considered?
   - **Template compliance**: Follows `.agents/skills/investigate_issue/assets/templates/rca_template.md`?
2. Produce structured feedback with severity (Blocking/Suggestion), section, finding, and recommendation.
3. **Internal loop** (max 3 rounds):
   - If blocking issues found → pass feedback to **investigator** → investigator revises → **rca-reviewer** re-reviews.
   - If only suggestions remain or no issues → RCA reviewer approves.
4. Output an explicit verdict: "Approved" or "Blocked".

### Phase 4 — Human Review Gate (Wait for User)

1. Present the internally-approved RCA document to the user.
2. **Inversion (Wait for User):** Halt execution. Ask the user to review the RCA.
   - **If rejected**: Pass user feedback back to the **investigator** sub-agent. Investigator revises the RCA. The revised RCA goes through the **rca-reviewer** again (internal loop until approved), then back to the user. **No cap** on human review rounds.
   - **If approved**: Proceed to fix phase.

### Phase 5 — Fix Implementation (Engineer Sub-Agent)

Invoke the **engineer** sub-agent. The engineer receives the approved RCA and works in an isolated worktree.

1. **Orchestrator setup**:
   - Create isolated worktree via `incremental_implement` (Step 1: Setup).
   - **Copy** the reproduction test file and RCA document from the main worktree into the new worktree (preserving directory structure).
2. **Engineer execution**:
   - Read the RCA to understand the root cause and fix strategy.
   - **Verify RED**: Run the reproduction test → confirm it fails. Verify it fails *for the right reason* (failure message matches the root cause). If the test is wrong or insufficient → fix/rewrite the test first.
   - **GREEN**: Implement the minimal fix to pass the reproduction test.
   - **Full suite**: Run the entire test suite.
     - If tests break and are **clearly caused by the fix** → engineer fixes them.
     - If tests break and are **unrelated** → halt and escalate to user.
   - **Refactor**: Clean up without changing behavior.
   - Commit atomically via `git-master` skill.
   - Push branch, create PR.
3. **Failure Behavior**: If implementation fails, keep worktree intact for debugging and present failure details to the user.

### Phase 6 — Code Review (Code Reviewer Sub-Agent)

Invoke the **code-reviewer** sub-agent.

1. Review the fix PR against:
   - The RCA document (is the fix addressing the actual root cause?).
   - The reproduction test (is the RED test valid?).
   - Coding standards and AGENTS.md rules.
2. Focus areas: fix correctness, regression risk, scope creep (fixing only what the RCA identified), test coverage.
3. **Internal loop** (max 3 rounds): If issues found, provide structured feedback to **engineer**. Engineer revises, pushes, re-review.
4. **Inversion (Wait for User):** Present the internally-approved PR for final human sign-off. If user provides feedback, route back to **engineer** → **code-reviewer**. Loop until user approves.

### Phase 7 — Merge & Update RCA

1. Merge PR: `gh pr merge --squash --delete-branch`.
2. Clean up worktree: `git worktree remove` + `git worktree prune`.
3. Update `docs/rcas/rca_<slug>.md` status checklist:
   - Mark all items complete.
   - Append verification results (test output, CI link).
   - Record the merged PR number as a reference.

# 📤 Output Specifications
- **RCA Document**: `docs/rcas/rca_<slug>.md` — complete root cause analysis with evidence, hypotheses, and fix verification results.
- **Reproduction Test**: A failing test in the project's test directory that proves the bug existed and now serves as a regression test.
- **Merged PR**: A squash-merged pull request containing the fix, reproduction test, and RCA document.
- **Summary Report**: Markdown-formatted summary of the full lifecycle: issue → root cause → fix → merge.
