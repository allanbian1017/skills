# study-github-repo

Analyze a GitHub repository and generate a comprehensive study report covering 14 dimensions: purpose, mental model, entry points, folder structure, core abstractions, state management, decision logic, feedback loops, DX, tests, tradeoffs, repo health, engineering taste, and hidden architectural flaws.

## Usage

Provide a GitHub repo URL:
- `study this repo: https://github.com/owner/repo`
- `analyze https://github.com/owner/repo`
- `what does owner/repo do?`

## Prerequisites

- `gh` CLI installed and authenticated (`gh auth login`)

## How It Works

1. Fetches repo metadata via GitHub API (`gh api`)
2. Shallow-clones the repo to `.tmp/github_study/` for local code analysis
3. Systematically studies the codebase across 14 dimensions, tracing execution flow end-to-end
4. Generates a comprehensive report in the configured output language (defaulting to English) at `reports/GitHub/{owner}_{repo}.md`
5. Cleans up the local clone

## Output

Reports are saved to `reports/GitHub/{owner}_{repo}.md`. Re-running against the same repo overwrites the previous report.

## Limitations

- Report quality scales with repo size — small libraries get thorough reports; large monorepos may have gaps
- Private repos are supported (via `gh` auth) but community health metrics may be sparse
- Shallow clone only; git history analysis is done via API, not local git log

## Changelog

- **2026-05-20**: Added a 14th dimension to identify 5 hidden architectural flaws in plain sight, complete with file paths, line numbers, and maintainability impact. See `docs/rfc/add-hidden-architectural-flaws.md`.
- **2026-06-16**: Made output language globally configurable, defaulting to English and preferring Traditional Chinese.
