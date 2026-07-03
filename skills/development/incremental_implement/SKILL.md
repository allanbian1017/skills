---
name: incremental_implement
description: Full PR lifecycle via isolated worktree, atomic commits, PR creation, and a strict verification loop (CI + review-work) until merged.
version: 1.1.0
pattern: Pipeline
---

# 🎯 Purpose
To execute a complete, safe Pull Request lifecycle. The skill isolates work in a sibling directory, implements requested changes via atomic commits, creates a PR, and enforces an unbounded verification loop (CI and AI peer review) until the code is proven stable and merged.

## The Increment Cycle

```
┌──────────────────────────────────────┐
│                                      │
│   Implement ──→ Test ──→ Verify ──┐  │
│       ▲                           │  │
│       └───── Commit ◄─────────────┘  │
│              │                       │
│              ▼                       │
│          Next slice                  │
│                                      │
└──────────────────────────────────────┘
```

# 🚪 Gating & Trigger Conditions
- **When to invoke:** When the user prompts 'create a PR', 'implement and PR', 'work on this and make a PR', 'implement issue', 'land this as a PR', 'work-with-pr', 'PR workflow', 'implement end to end', or 'implement X' (when context implies safe PR delivery).
- **When NOT to invoke:** - Directly committing to `master` or `dev` branches.
  - When the user explicitly requests working in the current active directory without isolation.
  - Simple file edits where no CI or verification is necessary.

# 📥 Input Specifications
- `TASK_SUMMARY`: The goal or issue description provided by the user.
- `CONSTRAINTS`: Any specific architectural or stylistic rules.
- **Inferred Context:** Repository name, current working directory (`$PWD`), and base branch (defaulting to `dev`).

# ⚙️ Execution Instructions (Workflow)

**1. Setup Isolated Worktree**
Create a sibling worktree to prevent polluting the user's uncommitted state.
- Resolve repo context: `REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)` and `BASE_BRANCH="dev"`.
- Generate branch name: `BRANCH_NAME="feature/$(echo "$TASK_SUMMARY" | tr '[:upper:] ' '[:lower:]-' | head -c 50)"`.
- Fetch and branch: `git fetch origin "$BASE_BRANCH"` then `git branch "$BRANCH_NAME" "origin/$BASE_BRANCH"`.
- Create worktree: `WORKTREE_PATH="../$(basename "$PWD")-wt/${BRANCH_NAME}"`, `mkdir -p "$(dirname "$WORKTREE_PATH")"`, `git worktree add "$WORKTREE_PATH" "$BRANCH_NAME"`.
- Enter worktree and install project dependencies using the appropriate package manager based on the repository's lockfiles.

**2. Implement & Pre-Validate**
- Implement EXACTLY ONE task from the `TASK_SUMMARY`. Keep scope strictly minimal to this single task. Do NOT implement multiple tasks or refactor unrelated code.
- You must halt and request human review BEFORE moving to any subsequent tasks. If a task is completed, you MUST wait for the user to initiate a brand-new chat session for the next task.
- Commit atomically using the `git-master` skill (e.g., 3+ files changed = 2+ commits).
- Run local validation before pushing (e.g., the project's native build, test, and linting scripts). Fix local failures and commit atomically before proceeding.

**3. PR Creation**
- Push branch: `git push -u origin "$BRANCH_NAME"`.
- Create PR: Execute `gh pr create` with base `dev`, head `$BRANCH_NAME`, and a formatted body containing "Summary", "Changes", and "Testing" checklists.
- Capture PR number: `PR_NUMBER=$(gh pr view --json number -q .number)`.

**4. Verification Loop**
Enter an unbounded `while` loop until both gates pass:
- **Gate A (CI Checks):** Run `gh pr checks "$PR_NUMBER" --watch --fail-fast`. 
  - *If failed:* Fetch logs (`gh run view "$RUN_ID" --log-failed`), fix the specific issue, commit, push, and restart the loop at Gate A.
- **Gate B (review-work):** Only execute if Gate A passes. Invoke the `review-work` skill sub-agent targeting `$BRANCH_NAME` and `$WORKTREE_PATH`.
  - *If failed:* Address blocking issues reported by the reviewers, commit, push, and restart the loop at Gate A (new code requires new CI).
- *Break loop* when both Gate A and Gate B pass simultaneously.

**5. Merge & Cleanup**
- Merge PR: `gh pr merge "$PR_NUMBER" --squash --delete-branch`.
- Cleanup: Return to the original directory (`cd "$ORIGINAL_DIR"`), run `git worktree remove "$WORKTREE_PATH"`, and `git worktree prune`.

**6. Fallback Behaviors**
- If an unrecoverable error occurs (e.g., merge conflicts with base), **DO NOT delete the worktree**.
- Output the `$WORKTREE_PATH` to the user and halt execution so they can manually inspect or resolve the state.

# 📤 Output Specifications
- A markdown-formatted summary report detailing:
  - PR Number and Title
  - Branch routing (`feature-branch` → `main`)
  - Number of iterations in the verification loop
  - Confirmation of CI and review-work passage
  - Worktree cleanup status
