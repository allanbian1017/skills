# Agent Skills Repository

A centralized library of original AI agent skills designed to automate software engineering, streamline decision-making, enforce quality gates, and orchestrate personal intelligence workflows.

---

## Overview

AI agents are most effective when given specialized, domain-focused procedures rather than ambiguous generic instructions. Each skill in this repository encapsulates a discrete operational capability—combining YAML metadata, structured directives, automated validation gates, and on-demand reference materials.

### Skill Anatomy

Each skill is self-contained within its own directory under `skills/<category>/<skill-name>/`:

```
skills/<category>/<skill-name>/
├── SKILL.md             # Primary instruction spine (YAML frontmatter + directives)
├── README.md            # Optional human-readable documentation
├── references/          # On-demand domain guides, rubrics, and templates
└── scripts/             # Deterministic helper scripts & validation tools
```

---

## Repository Structure

The repository is organized into five active functional domains, plus an archive directory for retired assets:

- [**`development/`**](skills/development): Original planning, implementation orchestration, code review, and issue investigation skills; integrates with external development skills in `dep-skills`.
- [**`engineering/`**](skills/engineering): System-level architecture inspection, execution tracing, and quantitative root cause analysis.
- [**`productivity/`**](skills/productivity): Agent steering governance, technical analysis, and context engineering.
- [**`financial/`**](skills/financial): Fixed-income and equity valuation, duration/credit/FX scenario modeling, primary filing verification, and risk-adjusted hurdle return analysis.
- [**`personal/`**](skills/personal): End-to-end content intelligence, multi-source media ingestion (newsletters, YouTube, Threads, web), daily distillation, and recommendation grading.
- [**`deprecated/`**](skills/deprecated): Historical archive of superseded or retired skills (e.g., `devcontainer-bridge`, `newsletter-summary`, `process-delegate-tasks`). Kept strictly for historical reference.

---

## Core Workflow Pipelines

### 1. Autonomous Software Development Lifecycle

An autonomous pipeline orchestrating end-to-end feature delivery: from a raw idea to an approved PRD, RFC, vertically-sliced tasks, isolated git worktree implementation, Red-Green-Refactor testing, and automated code review.

```mermaid
flowchart LR
    Idea([Feature Idea]) --> prd["/write-prd\nRequirements Review"]
    prd --> rfc["/request-feature\nRFC & Architecture Review"]
    rfc --> planning["planning-and-task-breakdown (dep-skills)\nVertical Task Slices"]
    planning --> orchestrator["/implement-task\nPipeline Orchestrator"]
    
    subgraph Implementation ["Implementation Loop (Isolated Worktree)"]
        direction TB
        incremental["incremental-implement (dep-skills)\nWorktree & CI Loop"]
        tdd["test-driven-development (dep-skills)\nRed-Green-Refactor"]
        git_master["git-master (dep-skills)\nAtomic Commits"]
        code_review["code-review\nMulti-Pass Review"]
        incremental --> tdd --> git_master --> code_review
    end

    orchestrator --> Implementation
    Implementation --> PR([Merged PR & Clean Worktree])
```

---

### 2. Content Intelligence & Daily Distillation Pipeline

An automated knowledge pipeline that polls inbox tasks, ingests multi-format media, extracts core theses, clusters daily insights, and routes actionable suggestions through a multi-dimensional rubric to a human-in-the-loop review board.

```mermaid
flowchart TD
    Tasks([Tasks / URLs]) --> daily_wf["daily-workflow\nPipeline Orchestrator"]
    
    subgraph Ingestion ["Multi-Source Ingestion"]
        daily_wf --> ingest_news["ingest-newsletter\n(Gmail)"]
        daily_wf --> ingest_yt["ingest-youtube / yt2doc\n(YouTube Transcripts)"]
        daily_wf --> ingest_threads["ingest-threads\n(Threads Discussions)"]
        daily_wf --> ingest_web["ingest-website\n(Web Articles)"]
    end

    Ingestion --> cleaner["content-cleaner & content-summary\nText Normalization & Thesis Extraction"]
    cleaner --> distiller["daily-distiller\nTopic Clustering & Synthesis"]
    cleaner --> grader["rubric-grader\n3-Dimension Quality Scoring"]
    grader --> review["review-suggestions\nHuman-in-the-Loop Feedback"]
```

---

## Skills Catalog

### Development Skills (`skills/development/`)

| Skill | Pattern / Role | Description | Invocation |
|:------|:---------------|:------------|:-----------|
| [`write-prd`](skills/development/write-prd) | Inversion / PM | Turn raw feature ideas into rigorous, approved Product Requirements Documents. | `/write-prd <idea>` |
| [`request-feature`](skills/development/request-feature) | Pipeline | Orchestrate full planning lifecycle: PRD → RFC → Architecture Review → Task List. | `/request-feature <idea>` |
| [`implement-task`](skills/development/implement-task) | Pipeline | Drive planned tasks end-to-end with tests, CI, and multi-agent review to a merged PR. | `/implement-task <feature>` |
| [`code-review`](skills/development/code-review) | Auditor | Multi-dimensional code review across style rubrics, spec compliance, and security checklists. | `/review-work` or `Use @code-review` |
| [`investigate-issue`](skills/development/investigate-issue) | Diagnostic | Full issue resolution lifecycle: triage, root cause diagnosis, RCA review, and fix. | `Use @investigate-issue` or `/investigate-issue <issue>` |

---

### Engineering Skills (`skills/engineering/`)

| Skill | Pattern / Role | Description | Invocation |
|:------|:---------------|:------------|:-----------|
| [`evolution-log`](skills/engineering/evolution-log) | Chronicler | Generate, update, or audit narrative development histories across iterative decision cycles. | `update my evolution log` |
| [`flow-tracer`](skills/engineering/flow-tracer) | Static Analysis | Trace complete code execution paths across the codebase and output sequence diagrams. | `trace the flow of <target>` |
| [`rca`](skills/engineering/rca) | Diagnostic | Structured Root Cause Analysis enforcing quantitative hypotheses and verification tests. | `run rca on <issue>` |

---

### Productivity Skills (`skills/productivity/`)

| Skill | Pattern / Role | Description | Invocation |
|:------|:---------------|:------------|:-----------|
| [`agent-rules-reviewer`](skills/productivity/agent-rules-reviewer) | Governance | Audit and refactor `AGENTS.md` and `CLAUDE.md` using 3-tier rules architecture. | `review AGENTS.md` |
| [`skill-context-refactor`](skills/productivity/skill-context-refactor) | Refactorer | Optimize skills via Context Engineering (Lean Spine <200 lines + Progressive Disclosure). | `refactor skill <name>` |
| [`tech-deconstructor`](skills/productivity/tech-deconstructor) | Analyst | Deconstruct papers, RFCs, and architectures into a structured 4-part analytical breakdown. | `deconstruct this paper` |

---

### Financial Skills (`skills/financial/`)

| Skill | Pattern / Role | Description | Invocation |
|:------|:---------------|:------------|:-----------|
| [`bond-valuation-skill`](skills/financial/bond-valuation-skill) | Fixed-Income Analyst | Relative valuation for bond ETFs and bonds with duration/credit/FX scenarios and reverse-priced entry hurdles. | `value bond ETF <ticker>` or `analyze TLT` |
| [`equity-valuation`](skills/financial/equity-valuation) | Valuation Analyst | Analyze whether a public company is overvalued using 5-year fundamentals, scenarios, and a 10% hurdle. | `分析 2454` or `Is NVDA overvalued?` |

---

### Personal & Content Intelligence Skills (`skills/personal/`)

| Skill | Pattern / Role | Description | Invocation |
|:------|:---------------|:------------|:-----------|
| [`daily-workflow`](skills/personal/daily-workflow) | Orchestrator | Chain content ingestion, text cleaning, thesis extraction, distillation, and scoring. | `run daily workflow` |
| [`daily-distiller`](skills/personal/daily-distiller) | Synthesizer | Synthesize daily ingestion reports into topic clusters and actionable knowledge briefs. | `distill today's reports` |
| [`decision-sparring`](skills/personal/decision-sparring) | Sparring Partner | Stress-test decisions and break analysis paralysis using 9 structured mental models. | `spar with me on <decision>` |
| [`ingest-newsletter`](skills/personal/ingest-newsletter) | Ingestion | Ingest unread newsletters from Gmail (`label:newsletter is:unread`) into markdown digests. | `ingest newsletters` |
| [`ingest-youtube`](skills/personal/ingest-youtube) | Ingestion | Transcribe and summarize YouTube videos into structured markdown reports. | `transcribe this YouTube video` |
| [`ingest-threads`](skills/personal/ingest-threads) | Ingestion | Fetch Threads posts and discussion threads, producing structured intelligence reports. | `ingest threads post <url>` |
| [`ingest-website`](skills/personal/ingest-website) | Ingestion | Fetch generic websites via Jina Reader API and produce structured summaries. | `ingest this article <url>` |
| [`web-to-markdown`](skills/personal/web-to-markdown) | Converter | Convert any webpage URL into clean Markdown using the Jina Reader API. | `convert this page to markdown` |
| [`yt2doc`](skills/personal/yt2doc) | CLI Wrapper | Transcribe and organize YouTube videos into documentation using the local yt2doc CLI. | `turn this video into a document` |
| [`fetch-threads-post`](skills/personal/fetch-threads-post) | Scraper | Headless browser extraction of Threads post content, authors, and replies. | `fetch threads post <url>` |
| [`content-cleaner`](skills/personal/content-cleaner) | Normalizer | Extract pure article text from raw text files, HTML dumps, or URLs. | `clean article text from <source>` |
| [`content-summary`](skills/personal/content-summary) | Shared Pipeline | Shared thesis-driven summarization and analytical framework for ingested content. | `summarize content with thesis` |
| [`rubric-grader`](skills/personal/rubric-grader) | Evaluator | Score AI suggestions across a 3-dimension rubric and route to backlogs. | `grade suggestions` |
| [`review-suggestions`](skills/personal/review-suggestions) | Review Board | Present unreviewed suggestions as an artifact to collect user Accept/Reject feedback. | `review my suggestions` |
| [`review-newsletter-subscriptions`](skills/personal/review-newsletter-subscriptions) | Auditor | Audit newsletter subscriptions by conversion rate and propose keep/unsubscribe actions. | `review my newsletter subscriptions` |
| [`study-github-repo`](skills/personal/study-github-repo) | Research | Comprehensive architectural and code quality study of any GitHub repository. | `study this repo <github-url>` |

---

## External Skill Dependencies

Third-party skills and local adaptations are maintained separately in the private [dep-skills](https://github.com/allanbian1017/dep-skills) repository. They are no longer bundled here. Access to that repository is required to install them.

| Skill | Purpose |
|:------|:--------|
| [agent-browser](https://github.com/allanbian1017/dep-skills/blob/main/skills/personal/agent-browser/SKILL.md) | Browser automation CLI skill and supporting references. |
| [git-master](https://github.com/allanbian1017/dep-skills/blob/main/skills/development/git-master/SKILL.md) | Atomic commits, rebase/squash, and git history analysis. |
| [architecture-decision-records](https://github.com/allanbian1017/dep-skills/blob/main/skills/productivity/architecture-decision-records/SKILL.md) | Architecture Decision Record templates and guidance. |
| [caveman](https://github.com/allanbian1017/dep-skills/blob/main/skills/productivity/caveman/SKILL.md) | Compressed communication mode. |
| [documentation](https://github.com/allanbian1017/dep-skills/blob/main/skills/productivity/documentation/SKILL.md) | Documentation workflow bundle. |
| [grill-me](https://github.com/allanbian1017/dep-skills/blob/main/skills/productivity/grill-me/SKILL.md) | Design interviews with the existing local preference-learning customization. |
| [memory-engine](https://github.com/allanbian1017/dep-skills/blob/main/skills/deprecated/memory-engine/SKILL.md) | Deprecated memory management skill, retained for historical reference. |
| [planning-and-task-breakdown](https://github.com/allanbian1017/dep-skills/blob/main/skills/development/planning-and-task-breakdown/SKILL.md) | Implementation planning and vertically sliced task breakdown. |
| [test-driven-development](https://github.com/allanbian1017/dep-skills/blob/main/skills/development/test-driven-development/SKILL.md) | Red → Green → Refactor and bug reproduction guidance. |
| [incremental-implement](https://github.com/allanbian1017/dep-skills/blob/main/skills/development/incremental-implement/SKILL.md) | Isolated worktrees, atomic commits, PR lifecycle, and CI gate. |
| [insight](https://github.com/allanbian1017/dep-skills/blob/main/skills/productivity/insight/SKILL.md) | Analyze agent conversations and suggest workflow improvements. |

The planning and development pipelines use `planning-and-task-breakdown`, `incremental-implement`, `test-driven-development`, and `git-master`; content workflows may use `agent-browser`. Install the required external skills alongside this repository's skills so agents can discover both collections by name. CLI dependencies such as `agent-browser` must also be installed separately.

Clone the private repository alongside this one:

```bash
git clone git@github.com:allanbian1017/dep-skills.git ../dep-skills
```

For example, from this repository, install `git-master` for Codex:

```bash
mkdir -p ~/.agents/skills
ln -s "$(cd ../dep-skills && pwd)/skills/development/git-master" ~/.agents/skills/git-master
```

For Antigravity, use `~/.gemini/antigravity/skills/` instead. See the [dep-skills README](https://github.com/allanbian1017/dep-skills#readme) for the full collection and migration details.

---

## How to Use in Agent Environments

### Google Antigravity

Antigravity discovers skills from both global configuration and workspace directories:

1. **User Global Installation**: Symlink or copy desired skills to `~/.gemini/antigravity/skills/` (or `~/.gemini/config/skills/`):
   ```bash
   ln -s "$(pwd)/skills/development/write-prd" ~/.gemini/antigravity/skills/write-prd
   ```
2. **Workspace-Level Skills**: Keep this repository open as an active workspace or link skills into your project's `.agent/skills/` directory.
3. **Triggering**: Invoke registered slash commands (e.g., `/write-prd`, `/implement-task`) or mention `@skill-name` directly in conversation.

### Claude Code

Claude Code reads steering instructions from `CLAUDE.md` and `AGENTS.md`:

1. Keep the root [`CLAUDE.md`](CLAUDE.md) pointer directing the agent to [`AGENTS.md`](AGENTS.md).
2. Reference skills directly by path (e.g. `skills/development/write-prd/SKILL.md`) in prompts or slash command aliases.

### General Agent Platforms (Cursor, Codex, OpenHands)

All skills strictly conform to the Agent Skill standard:
- Place skill folders into your project root or `.agent/skills/`.
- The entrypoint `SKILL.md` contains self-describing YAML frontmatter (`name`, `description`) enabling automated tool discovery and prompt injection.

---

## Contributing & Adding Skills

When contributing new skills or optimizing existing ones:
1. **Context Engineering**: Follow [`skill-context-refactor`](skills/productivity/skill-context-refactor) principles—keep `SKILL.md` instruction spines lean (<200 lines) and place large guidelines or schemas into `references/`.
2. **Deterministic Scripts**: For tasks requiring accurate calculations, statistics, or multi-file parsing, use dedicated Python scripts in `scripts/` rather than relying on LLM mental arithmetic.
3. **No Unnecessary Tests**: Pure markdown documentation and skill guides are exempt from code-level test suites. Focus automated testing on executable scripts and tool code.
