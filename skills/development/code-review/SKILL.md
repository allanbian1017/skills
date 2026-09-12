---
name: code-review
description: Comprehensive code review across style rubrics, spec compliance, and bug/security checklists with team preference learning and extensible multi-language support.
version: 1.1.0
pattern: Reviewer
---

# Code Review Skill

A standalone, composable skill that performs comprehensive code review across three dimensions: language-specific coding style enforcement via standardized rubrics, specification compliance against RFCs/Plans, and general bug/security/test verification. The skill learns project-specific team preferences from GitHub PR comments, supports polyglot pull requests, and provides an on-demand cognitive onboarding workflow for expanding to new languages.

## 1. Invocation Modes

The skill supports four invocation modes:

| Mode | Trigger | Input | Output |
|------|---------|-------|--------|
| **Internal** | Invocation from `implement_task` or engineer agent | `git diff` + optional RFC/Plan path | Structured findings returned in-memory to caller |
| **PR URL** | User provides GitHub PR URL (`gh pr review`) | `gh pr diff` + optional RFC/Plan path | Summary review + inline comments posted to GitHub |
| **Learn** | User requests learning from PR comments | `gh api` PR review comments | Propose-then-confirm entries appended to `preferences.md` |
| **Onboard** | User asks to add or transform a language style guide | Raw upstream guide (URL, file, text) | Propose-then-confirm rubric written to `references/<lang>.md` |

### Mode 1: Internal Mode (Pipeline Review)
- **Diff Input**: Capture local changes via `git diff --staged`, `git diff HEAD~1`, or `git diff $(git merge-base HEAD main)..HEAD`.
- **Spec Input**: RFC or Plan path provided in prompt (e.g., `docs/rfcs/rfc_feature.md` or `docs/plans/plan_feature.md`).
- **Output**: Returns the formatted Markdown review directly to the calling agent or pipeline.

### Mode 2: PR URL Mode (GitHub Native)
- **Diff Input**: Retrieve PR diff using GitHub CLI: `gh pr diff <pr_number> -R <owner/repo>`.
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
      -f 'comments[][body]=[STYLE] R-GO-01: Use %w for error wrapping'
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

### Mode 4: Style Guide Onboarding Mode (Language Expansion)
- **Trigger**: User asks to add, import, or transform a style guide for `<lang>` (e.g., *"Add Python style guide from `<source>`"*).
- **Onboarding Procedure (5-Step SOP)**:
  1. **Fetch & Ingest**: Save raw guide to `sources/<lang>.md` with header provenance (URL, commit/tag, date).
  2. **Strict Linter Exclusion**: Omit mechanical formatting (indentation, line length, quote style) and simple AST checks (unused variables, import order) enforced by standard formatters/linters (`gofmt`, `prettier`, `ruff`, `eslint`). Focus exclusively on semantic idioms, error contracts, resource safety, and concurrency boundaries.
  3. **Cognitive Classification**: Read `references/template.md` as schema contract. Extract binary pass/fail rules into `R-<LANG>-xx` and judgment-based guidelines into `C-<LANG>-xx`.
  4. **Propose-Then-Confirm Gate**: Present draft rubric to user for review in chat or an artifact.
  5. **Write & Register**: Upon confirmation, write to `references/<lang>.md` and register the extension in the registry below.

## 2. Style Guide Selection & Polyglot Routing

### Extension-to-Language Registry
| File Extensions | Language Key | Reference Path |
|---|---|---|
| `.go` | `golang` | `references/golang.md` |
| `.ts`, `.tsx`, `.js`, `.jsx` | `typescript` | `references/typescript.md` |
| `.py` | `python` | `references/python.md` |
| `.rs` | `rust` | `references/rust.md` |
| `.sql` | `sql` | `references/sql.md` |
| `.sh`, `.bash` | `shell` | `references/shell.md` |

### Language Auto-Detection & Polyglot Partitioning
1. Inspect file extensions across all changed files in the diff.
2. For each detected language with a guide in `references/`:
   - Load `references/<lang>.md`.
   - **Hunk Partitioning**: Evaluate each changed file strictly against its matching language rubric (e.g. Go files against `references/golang.md`, TypeScript files against `references/typescript.md`). Never test rules of one language against another.
3. For file extensions without a dedicated style guide, fall back to `references/common-review.md` and log:
   > *"No style guide available for `<ext>` files. Applied common review checklist."*

### Reference & Memory Loading Order
1. Load matching `references/<lang>.md` files for detected languages.
2. Load `references/common-review.md` (language-agnostic bug, security, and test checklist).
3. Load `memory/preferences.md` (learned project preferences).
4. Load target RFC or Plan document if supplied.

## 3. Runtime Preference Precedence Rules

When a learned preference in `memory/preferences.md` contradicts a baseline style guide rule in `references/<lang>.md`:
1. **Immutable Baseline**: The style guide file (`references/<lang>.md`) is **never modified or overwritten on disk**.
2. **Runtime Precedence**: During review evaluation (in memory), the agent **adopts the preference over the baseline rule**.
3. **Scoring Alignment**: Code conforming to the project preference is scored as compliant.
4. **Audit Transparency**: Note any active override in the review report:
   `Rule <ID> superseded at review time by project preference: <Preference Title>`.
5. **Reversibility**: Deleting an entry from `preferences.md` restores baseline rule enforcement immediately.

## 4. Confidence-Based Filtering

To eliminate review fatigue and noise, strictly apply these filtering rules:
- **Confidence Threshold**: Only report findings where you are **>80% confident** that a real defect or violation exists.
- **Changed Code Only**: Focus strictly on modified lines and immediate call sites. Do not flag pre-existing issues in untouched code unless they are CRITICAL security vulnerabilities.
- **Convention Driven**: Stylistic findings must cite a specific rubric rule (`R-<LANG>-xx`) or learned preference.
- **Consolidation**: Consolidate repetitive occurrences of the same issue into a single finding listing all affected locations.

## 5. Multi-Dimensional Review Process

Execute review across three distinct dimensions:

### Dimension 1: Style Review (Scored)
- **Rubric Rules (`R-<LANG>-xx`)**: Strict binary pass/fail checks contributing to the numerical score:
  $$\text{Style Score} = \left(\frac{\text{Passed Rubric Rules}}{\text{Total Evaluated Rubric Rules}}\right) \times 100\%$$
- **Contextual Guidelines (`C-<LANG>-xx`)**: Qualitative guidelines requiring engineering judgment, output as advisory notes.

### Dimension 2: Spec Compliance (Optional)
- Extract discrete requirements from RFC/Plan and verify against diff:
  - `✅ Implemented`: Requirement fully met.
  - `⚠️ Partial`: Incomplete edge-case handling or partial implementation.
  - `❌ Missing`: Requirement specified in RFC/Plan but absent in diff.

### Dimension 3: Bugs, Security & Tests
- Check against `references/common-review.md`:
  - **Security (CRITICAL)**: Hardcoded secrets, injection (SQL/command), XSS, path traversal, auth bypasses.
  - **Bugs (HIGH)**: Logic flaws, nil/null dereferences, race conditions, unhandled errors, resource leaks.
  - **Test Coverage (MEDIUM)**: Untested new execution branches, missing edge cases.

## 6. Verdict and Review Output Format

### Approval Criteria
- **Approve**: 0 CRITICAL, 0 HIGH, style rubric pass rate >= 80%, spec compliance >= 90%.
- **Warning**: 0 CRITICAL, but HIGH issues exist or style pass rate < 80%.
- **Block**: 1+ CRITICAL issues found, or major spec requirements missing.

### Output Structure
```markdown
## Code Review: <PR / Branch Title>

### Style: <Passed>/<Total> rubric rules passed (<Score>%)
<!-- For polyglot PRs, show per-language breakdown: -->
- Go: 9/10 passed (90%)
- TypeScript: 5/6 passed (83%)

| Rule | Language | Severity | Verdict | Location |
|------|----------|----------|---------|----------|
| R-GO-01: Error Wrapping | Go | HIGH | ❌ | pkg/handler.go:42 |
| R-GO-09: Avoid Mutable Globals | Go | HIGH | ✅ | — |
| R-TS-01: No Unsafe Type Assertions | TypeScript | HIGH | ❌ | web/app.tsx:18 |

*Active Overrides:* Rule R-GO-04 superseded by project preference: Prefer errors.Wrap

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
- C-GO-01: `pkg/handler.go:28` — Consider pointer receiver for large struct methods.

### Summary
| Severity | Count | Status |
|----------|:---:|:---:|
| CRITICAL | 1 | block |
| HIGH | 2 | warn |
| MEDIUM | 0 | pass |
| LOW | 0 | pass |

**Verdict**: ⛔ BLOCK — 1 CRITICAL issue must be resolved before merge.
```
