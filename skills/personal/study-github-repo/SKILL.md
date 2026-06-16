---
name: study-github-repo
description: "Analyze a GitHub repository and generate a comprehensive study report covering architecture, design decisions, code quality, and repo health. Use this skill whenever the user provides a GitHub repo URL and wants to understand it deeply, says 'study this repo', 'analyze this GitHub project', 'what does this repo do', 'how is this repo designed', or any request to understand a GitHub repository's architecture, codebase, or engineering quality. Also use when the user wants a repo breakdown, code review, or architecture analysis of a GitHub project."
---

# study-github-repo

Clone a GitHub repository locally, study it systematically across 14 dimensions, and produce a comprehensive report in the configured output language (defaulting to English).

> **Prerequisite**: `gh` CLI installed and authenticated. Verify with `gh auth status`.

---

## Procedure

### Step 1 — Parse Input

Extract `{owner}` and `{repo}` from the GitHub URL. Accept any of these formats:
- `https://github.com/{owner}/{repo}`
- `github.com/{owner}/{repo}`
- `{owner}/{repo}`

### Step 2 — Gather Repo Metadata

Fetch metadata via `gh api` before cloning (lightweight, fast):

```bash
# Repo overview
gh api 'repos/{owner}/{repo}' --jq '{
  description, stargazers_count, forks_count,
  language, license: .license.spdx_id,
  topics, created_at, updated_at, open_issues_count,
  default_branch, archived, size
}'

# Language breakdown
gh api 'repos/{owner}/{repo}/languages'

# Recent releases (last 5)
gh api 'repos/{owner}/{repo}/releases?per_page=5' --jq '.[].tag_name'

# Contributors (top 10)
gh api 'repos/{owner}/{repo}/contributors?per_page=10' --jq '.[] | {login, contributions}'

# Recent commits (last 30)
gh api 'repos/{owner}/{repo}/commits?per_page=30' --jq '.[] | {date: .commit.author.date, message: .commit.message | split("\n")[0]}'

# Recent issues (last 10, all states)
gh api 'repos/{owner}/{repo}/issues?state=all&per_page=10' --jq '.[] | {number, title, state, labels: [.labels[].name]}'

# Recent PRs (last 10, all states)
gh api 'repos/{owner}/{repo}/pulls?state=all&per_page=10' --jq '.[] | {number, title, state, merged_at}'
```

### Step 3 — Clone Locally

```bash
mkdir -p .tmp/github_study
gh repo clone {owner}/{repo} .tmp/github_study/{owner}_{repo} -- --depth=1 \
  -c url.https://github.com/.insteadOf=git@github.com:
```

Use `--depth=1` for a shallow clone (faster, smaller). The `-c url...insteadOf` flag forces HTTPS to avoid SSH key issues. Full history is not needed — commit metadata is already fetched via API.

### Step 4 — Phase 1: Orientation

Build a rough mental map of the repo. Read these in order:

1. **README** — Extract the problem statement, claimed solution, and target audience
2. **Directory tree** — Run `find .tmp/github_study/{owner}_{repo} -not -path '*/.git/*' -not -path '*/node_modules/*' -not -path '*/__pycache__/*' -not -path '*/dist/*' -not -path '*/build/*' -not -path '*/.venv/*' | head -200` to see the structure (or use `tree -L 3 -I '...'` if available)
3. **Config files** — Read package.json / pyproject.toml / Cargo.toml / go.mod / Makefile / docker-compose.yml (whichever exist) to understand dependencies, scripts, and build setup
4. **Docs directory** — If `docs/` or similar exists, scan for architecture docs, guides, or design documents
5. **Examples** — If `examples/` exists, read a representative example to understand typical usage

### Step 5 — Phase 2: Trace Execution Flow

Follow one real execution path from input to output:

1. **Find entry points** — Look for `main.py`, `index.ts`, `server.js`, `app.ts`, `src/index.*`, `cmd/`, `bin/`, CLI entry files, API routers
2. **Trace the critical path** — Starting from the primary entry point, follow the code through orchestration → business logic → infrastructure layer. Read every file along this path.
3. **Identify the data flow** — Map: Input → Processing → Output. What transformations happen? What side effects occur?

There is no artificial file cap. Use engineering judgment to determine when you have enough understanding to explain how the repo delivers on its README promise. For large repos, focus on the core module rather than peripheral utilities.

### Step 6 — Phase 3: Deep Analysis

Using your understanding from Phases 1-2, now systematically investigate each dimension:

1. **Core Abstractions** — Find interfaces, base classes, schemas, protocols, type definitions. What primitives is the system built on?
2. **State Management** — Where does state live? Who owns it? How is it updated? Is there persistence/checkpointing?
3. **Decision Logic** — Find planners, routers, evaluators, scoring systems, retry policies, fallback mechanisms
4. **Feedback Loops** — Look for logging, telemetry, metrics, evaluation pipelines, retry/correction loops
5. **Tests** — Read test files. What types exist (unit, integration, e2e)? What do they reveal about intended behavior and edge cases?
6. **DX signals** — Evaluate setup instructions, documentation quality, naming conventions, type safety, scripts
7. **Hidden Architectural Flaws** — Identify exactly 5 architectural flaws hidden in plain sight. Pinpoint the exact file paths and line numbers, and evaluate their impact on future maintainability.

Use `grep_search` / ripgrep to search for patterns across the codebase without reading full files. Examples:
- `grep -r "class.*Base\|class.*Abstract\|interface " --include="*.py" --include="*.ts"`
- `grep -r "log\.\|logger\.\|console\.log\|logging\." --include="*.py" --include="*.ts" -l`
- `grep -r "test\|describe\|it(" --include="*test*" --include="*spec*" -l`

### Step 7 — Write Report

Check `data/user_preferences.md` for the `Preferred Output Language` configuration, and write the report in that language (defaulting to **English** if not configured).

> 📄 Read `assets/output_template.md` for the full report template.

Write the report to `reports/GitHub/{owner}_{repo}.md`. Every section must contain substantive content — no empty sections. If a dimension is not applicable (e.g., "State Management" for a pure utility library), explain why it's not relevant rather than leaving it blank.

The four executive summary questions must be answered:
1. What problem does this repo solve?
2. How is it designed?
3. Can I trust/use/extend it?
4. What can I learn from it?

For private/internal repos with sparse community metrics (0 stars, no releases), note this factually in Repo Health: "This appears to be a private/internal repository; community health metrics are not applicable."

### Step 8 — Cleanup

```bash
rm -rf .tmp/github_study/{owner}_{repo}
```

Confirm to the user: `"✅ Report saved to reports/GitHub/{owner}_{repo}.md. Clone cleaned up."`

---

## Error Handling

- **`gh` not authenticated**: Stop with `"⚠️ GitHub CLI is not authenticated. Run 'gh auth login' first."`
- **Repo not found / no access**: Stop with `"⚠️ Repository {owner}/{repo} not found or you don't have access."`
- **Clone fails**: Report the error and suggest the user check network/permissions.
