---
name: code-review
description: Comprehensive code review across style rubrics, spec compliance, and bug/security checklists with team preference learning.
version: 1.0.0
pattern: Reviewer
---

# Code Review Skill

A standalone, composable skill that performs comprehensive code review across three dimensions: language-specific coding style enforcement, specification compliance against RFCs/Plans, and general bug/security/test verification. The skill learns project-specific team preferences from GitHub PR comments and applies them in future reviews.

## 1. Invocation Modes

The skill supports three primary invocation modes:

| Mode | Trigger | Input | Output |
|------|---------|-------|--------|
| **Internal** | Invocation from `implement_task` or engineer agent | `git diff` + optional RFC/Plan path | Structured findings returned in-memory to caller |
| **PR URL** | User provides GitHub PR URL (`gh pr review`) | `gh pr diff` + optional RFC/Plan path | Summary review + inline comments posted to GitHub |
| **Learn** | User requests learning from PR comments | `gh api` PR review comments | Propose-then-confirm entries appended to `preferences.md` |

### Mode 1: Internal Mode (Pipeline Review)
- **Diff Input**: Capture local changes via `git diff --staged`, `git diff HEAD~1`, or `git diff $(git merge-base HEAD main)..HEAD`.
- **Spec Input**: RFC or Plan path provided in prompt (e.g., `docs/rfcs/rfc_feature.md` or `docs/plans/plan_feature.md`).
- **Output**: Returns the formatted Markdown review directly to the calling agent or pipeline.

### Mode 2: PR URL Mode (GitHub Native)
- **Diff Input**: Retrieve PR diff using GitHub CLI:
  ```bash
  gh pr diff <pr_number> -R <owner/repo>
  ```
- **Posting Review (Hybrid Model)**:
  - Post the summary table review comment:
    ```bash
    gh pr review <pr_number> -R <owner/repo> --comment --body "<summary_markdown>"
    ```
  - Post inline comments for **HIGH** and **CRITICAL** findings only:
    ```bash
    gh api repos/{owner}/{repo}/pulls/<pr_number>/reviews \
      -f event="COMMENT" \
      -f body="## Code Review Summary: Style & Critical Findings" \
      -f 'comments[][path]=path/to/file.go' \
      -f 'comments[][line]=42' \
      -f 'comments[][body]=[STYLE] R01: Use %w for error wrapping'
    ```

### Mode 3: Learn Mode (Preference Memory)
- **Fetch Comments**: Query review comments on PR:
  ```bash
  gh api repos/{owner}/{repo}/pulls/<pr_number>/comments \
    --jq '.[] | {id, body, path, line: .original_line, user: .user.login}'
  ```
- **Learning Procedure**:
  1. Filter out automated bot comments and extract human feedback.
  2. Classify feedback: distinguish enduring team preferences from one-off situational remarks.
  3. Formulate proposed entries conforming to `memory/preferences.md` structure.
  4. Present proposed rules to the user via a **propose-then-confirm gate**.
  5. Append confirmed rules to `.agents/skills/code-review/memory/preferences.md`.

## 2. Style Guide Selection & Loading

### Language Auto-Detection
1. Inspect file extensions in the diff (e.g., `.go` -> Go, `.ts`/`.tsx` -> TypeScript, `.py` -> Python).
2. For each detected language, locate `references/<lang>.md` relative to this skill:
   - **Matching Guide Found**: Load `references/<lang>.md`.
   - **User Override**: If user explicitly requests a guide (e.g., *"Review using Go style"*), load that guide.
   - **No Matching Guide**: Fall back to `references/common-review.md` and log:
     > *"No style guide available for `<ext>` files. Applied common review checklist."*

### Reference & Memory Loading Order
1. Load `references/<lang>.md` (hybrid rubric rules + contextual guidelines).
2. Load `references/common-review.md` (language-agnostic bug, security, and test checklist).
3. Load `memory/preferences.md` (learned project preferences).
4. Load target RFC or Plan document if supplied.

## 3. Runtime Preference Precedence Rules

When a learned preference in `memory/preferences.md` contradicts a baseline style guide rule in `references/<lang>.md`:

1. **Immutable Baseline**: The style guide file (`references/<lang>.md`) is **never modified or overwritten on disk**. It remains an intact upstream baseline.
2. **Runtime Precedence**: During review evaluation (in memory), the agent **adopts the preference over the baseline style guide rule**. The conflicting baseline rule is ignored.
3. **Scoring Alignment**: Code conforming to the project preference is scored as compliant. The code is not penalized against the conflicting baseline rule.
4. **Audit Transparency**: Note any active override in the review report:
   `Rule <ID> superseded at review time by project preference: <Preference Title>`.
5. **Reversibility**: If a preference entry is removed from `preferences.md`, baseline rule enforcement immediately resumes in subsequent reviews without disk modifications.

## 4. Confidence-Based Filtering

To eliminate review fatigue and noise, strictly apply these filtering rules:
- **Confidence Threshold**: Only report findings where you are **>80% confident** that a real defect or violation exists.
- **Changed Code Only**: Focus strictly on modified lines and immediate call sites. Do not flag pre-existing issues in untouched code unless they are CRITICAL security vulnerabilities.
- **Convention Driven**: Avoid subjective stylistic nitpicks unless governed by `references/<lang>.md` or `memory/preferences.md`.
- **Consolidation**: Consolidate repetitive occurrences of the same issue into a single finding listing all affected files and lines.

## 5. Multi-Dimensional Review Process

Execute review across three distinct dimensions:

### Dimension 1: Style Review (Scored)
- **Rubric Rules (`Rxx`)**: Strict binary pass/fail checks. Contributes to numerical score:
  `Style Score = (Passed Rules / Total Evaluated Rules) * 100%`.
- **Contextual Guidelines (`Cxx`)**: Qualitative guidelines requiring engineering judgment. Output as non-scoring advisory notes.

### Dimension 2: Spec Compliance (Optional)
- When an RFC or Plan is provided, extract discrete functional requirements.
- Verify each requirement against implementation in diff:
  - `✅ Implemented`: Requirement fully met.
  - `⚠️ Partial`: Incomplete edge case handling or partial implementation.
  - `❌ Missing`: Requirement specified in RFC/Plan but absent in diff.

### Dimension 3: Bugs, Security & Tests
- Check against `references/common-review.md`:
  - **Security (CRITICAL)**: Hardcoded secrets, injection (SQL/command), XSS, path traversal, auth bypasses.
  - **Bugs (HIGH)**: Logic flaws, nil/null dereferences, race conditions, unhandled errors, memory leaks.
  - **Test Coverage (MEDIUM)**: Untested new execution branches, missing edge cases.

## 6. Verdict and Review Output Format

### Approval Criteria
- **Approve**: 0 CRITICAL, 0 HIGH, style rubric pass rate >= 80%, spec compliance >= 90%.
- **Warning**: 0 CRITICAL, but HIGH issues exist or style pass rate < 80%.
- **Block**: 1+ CRITICAL issues found, or major spec requirements missing.

### Output Structure
Use the following markdown template:

```markdown
## Code Review: <PR / Branch Title>

### Style: <Passed>/<Total> rubric rules passed (<Score>%)
| Rule | Severity | Verdict | Location |
|------|----------|---------|----------|
| R01: Error Wrapping | HIGH | ❌ | pkg/handler.go:42 |
| R02: Import Ordering | LOW | ✅ | — |

*Active Overrides:* Rule R05 superseded by project preference: Prefer errors.Wrap

### Spec Compliance: <RFC/Plan Path>
| Requirement | Status | Location |
|-------------|--------|----------|
| JWT authentication middleware | ✅ Implemented | auth/middleware.go:15 |
| Rate limiting (100 req/min) | ❌ Missing | — |

### Bugs & Security
| # | Severity | Category | File | Issue | Suggestion |
|---|----------|----------|------|-------|------------|
| 1 | CRITICAL | SECURITY | config.go:12 | Hardcoded API key | Move credential to environment variable |
| 2 | HIGH | BUG | store.go:88 | Potential nil pointer dereference | Add nil guard before dereferencing |

### Advisory Notes (Contextual, No Score Impact)
- C01: `pkg/handler.go:28` — Consider pointer receiver for large struct methods.

### Summary
| Severity | Count | Status |
|----------|-------|--------|
| CRITICAL | 1     | block  |
| HIGH     | 1     | warn   |
| MEDIUM   | 0     | pass   |
| LOW      | 0     | pass   |

**Verdict**: ⛔ BLOCK — 1 CRITICAL issue must be resolved before merge.
```
