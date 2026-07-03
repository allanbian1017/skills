---
name: review-work
description: Reviews uncommitted code changes using a dynamic pipeline that scales from a single reviewer to parallel specialized reviewers (Bug Hunter, Rules Auditor) based on diff size.
version: 1.0.0
pattern: Pipeline
---

# 🎯 Purpose
To ensure code quality, security, and project compliance by automatically capturing git diffs and routing them through a scalable, multi-persona AI reviewer pipeline before committing changes.

# 🚪 Gating & Trigger Conditions
- **When to invoke:** After completing substantial implementation work, prior to creating a commit/PR, or when manually invoked by the user (e.g., `/review-work`).
- **When NOT to invoke:** When the working tree is clean (no uncommitted changes), during read-only exploration tasks, or when syntax errors prevent the code from compiling/running.

# 📥 Input Specifications
- `diff_stat`: String containing the output of `git diff --stat HEAD`.
- `diff_full`: String containing the output of `git diff HEAD`.
- `test_results`: (Optional) String containing the output of the project's test suite, if applicable and configured.
- `project_rules`: Context from the project's centralized rule file (e.g., `AGENTS.md`, `CONTRIBUTING.md`, or system prompt context).

# ⚙️ Execution Instructions (Workflow)

1. **Capture the Diff Context:**
   - Execute `git diff --stat HEAD` and store as `diff_stat`.
   - Execute `git diff HEAD` and store as `diff_full`.
   - *Fallback:* If git commands fail, prompt the user to initialize a git repository or stage files properly.
   - If a test command is known/configured for the project, execute it and append the output to `test_results`. Test failures are treated as high-priority inputs.

2. **Determine Review Scale:**
   - Parse `diff_stat` to count the total lines changed.
   - If lines changed < 50: Proceed to **Step 3A (Single Reviewer)**.
   - If lines changed >= 50: Proceed to **Step 3B (Parallel Specialist Reviewers)**.

3. **Execute Reviewers (Read-Only Mode):**
   - **Step 3A (Single Reviewer):** Invoke a single read-only LLM inference call.
     - *System Prompt:* "You are a code reviewer. Read the project rules, then review this diff. Check ONLY for real issues (Bugs, Security, Compliance, Tests). Do not nitpick style unless it causes a bug. If no issues found in a category, say 'No issues found.' Output format: `[high|medium|low] file:line — Description. Reason: ...`"
     - *Input:* `diff_full`, `test_results`, `project_rules`.
   - **Step 3B (Parallel Specialist Reviewers):** Concurrently invoke two distinct read-only LLM inference calls.
     - *Agent 1 (Bug Hunter):* Focus strictly on **Bugs** (logic, state, async, null handling) and **Security** (secrets, validation, injections). Ignore style and compliance. 
     - *Agent 2 (Rules Auditor):* Focus strictly on **Compliance** (architecture, project rules) and **Tests** (coverage gaps, structural assertions). Ignore general code quality/security.
     - *Input (Both):* `diff_full`, `test_results`, `project_rules`.

4. **Evaluate Findings (The Judge):**
   - Combine the outputs from Step 3A or 3B.
   - Critically evaluate each finding against the broader conversation context (which the read-only reviewers lacked).
   - Assign a verdict to each finding:
     - *Valid (high/medium):* Automatically fix the issue if possible, or prep for the user.
     - *Valid (low):* Note it, but defer fixing unless explicitly asked.
     - *False Positive:* Reject with a one-line explanation.

# 📤 Output Specifications
- A markdown-formatted summary table presented to the user, strictly following this structure:

```markdown
## Code Review Results

Reviewed by: Automated Pipeline [Single Reviewer | Parallel Specialists]
Reviewed X files, Y lines changed.

| # | Verdict | Category | File | Issue | Action |
|---|---------|----------|------|-------|--------|
| 1 | Fixed | BUG | file.ts:42 | Null check missing | Fixed |
| 2 | Rejected | COMPLIANCE | config.ts:10 | Not a real violation | False positive |
| 3 | Noted | TESTS | util.ts | No unit tests | Deferred |