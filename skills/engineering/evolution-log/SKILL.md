---
name: evolution-log
description: "Generate or update an Evolution Log — a narrative document that tells the development history of a project through iterative problem-solving cycles (Problem → Options → Decision → Result → New Problem). Use this skill whenever the user says 'update my evolution log', 'generate evolution log', 'write the project history', 'document the development journey', 'update EvolutionLog', 'add recent changes to evolution log', 'chronicle the project evolution', or any request to create or maintain a narrative development history from git commits, RFCs, RCAs, ADRs, or other decision documents."
---

# Evolution Log

Generate or update a narrative development history that tells the story of a project's evolution through iterative problem-solving cycles.

The core idea: every meaningful project change starts with **discovering a problem**, choosing between **options**, making a **decision**, observing the **result**, and often discovering a **new problem** — which starts the next cycle.

## Output Format

The Evolution Log is a single Markdown file. Read `references/output_template.md` for the exact structure and formatting rules before writing any content.

## Workflow

### Mode Detection

Determine which mode to run:

- **Generate mode**: No Evolution Log exists yet at the target path → full generation from scratch.
- **Update mode**: An Evolution Log already exists → identify new material since the last update and integrate it.

Default target path: `EvolutionLog.md` at the repo root. The user can override this.

---

### Step 1: Discover Source Material

Scan the repository for decision documents and history. These are the raw inputs for constructing the narrative. Different repos organize these differently, so adapt to what's available.

**Always available:**
```bash
# Full commit timeline with dates
git log --format="%ad %s" --date=short --reverse

# Feature and refactor milestones
git log --format="%ad %s" --date=short --reverse | grep -E "feat:|refactor:"

# Total commit count and date range
git rev-list --count HEAD
git log --format="%ad" --date=short --reverse | head -1
git log --format="%ad" --date=short | head -1

# Agent Skills landscape & evolution history
ls -la .agents/skills/ skills/ 2>/dev/null
git log --format="%ad %s" --date=short --reverse -- '.agents/skills/*' 'skills/*' 2>/dev/null

# README evolution
git log --format="%ad %s" --date=short --reverse -- README.md
```

**Look for (paths vary by repo):**

| Source type | What it provides | Common locations |
|:---|:---|:---|
| RFCs / Design docs | Problem → Options → Decision | `docs/rfc/`, `docs/design/`, `rfcs/` |
| ADRs | Architectural decisions | `docs/adr/`, `adr/`, `docs/decisions/` |
| RCAs / Post-mortems | Problems discovered from failures | `docs/rca/`, `docs/postmortems/` |
| Implementation plans | Decision → Execution details | `docs/plan/`, `docs/plans/` |
| Agent Skills / Capabilities | Skill architecture evolution & capability additions | `.agents/skills/`, `skills/`, `.claude/skills/` |
| README | System overview & architectural evolution | `README.md` |
| Changelogs | Milestone markers | `CHANGELOG.md`, `CHANGES.md` |
| Backlog / TODO | Next iteration's problems | `backlog.md`, `TODO.md` |

If a document type doesn't exist in the repo, skip it — work with what's available. Git history alone is enough to produce a useful Evolution Log.

### Step 2: Build the Timeline

From the collected material, construct a chronological timeline of the project's evolution. Group related changes into **Phases** — each Phase represents a coherent period of work driven by a shared problem or theme.

**How to identify Phase boundaries:**
- A Phase ends when its core problem is resolved and a meaningfully different problem emerges
- Look for shifts in the *type* of work: architecture → quality → performance → reliability
- RFCs/ADRs that supersede earlier ones mark natural Phase transitions
- Don't force a fixed number of Phases — let the material dictate the structure

**For update mode:** Read the existing Evolution Log. Identify the last Phase and its end date. Only process material after that date. Determine whether new material extends the current Phase or warrants a new one.

### Step 3: Construct the Narrative

For each Phase, extract the iterative cycle:

| Element | Where to find it | Guidance |
|:---|:---|:---|
| 🔍 **Problem** | RFC problem statements, RCA observed problems, commit messages that describe *why* | State it as a real pain point the developer experienced, not an abstract requirement |
| 🛤️ **Options** | RFC alternatives sections, ADR options, commit messages showing abandoned approaches | List real options that were considered — including the ones not chosen |
| ⚖️ **Decision** | RFC decisions, ADR outcomes, the actual commit that implemented the change | Explain *why* this option won, not just *what* was chosen |
| 📊 **Result** | RFC outcomes, follow-up commits, metrics if available | Concrete outcomes — what improved, what changed |
| 🔁 **New Problem** | The next RFC/RCA in the timeline, or explicit mentions of discovered issues | The bridge to the next Phase — what solving this problem revealed |

**Writing principles:**
- Write in first person ("I discovered...", "I chose...") — this is a personal development journey
- Be specific over generic — name the actual tools, files, and metrics involved
- Don't sanitize the failures — a hallucinating agent or an over-engineered logging system are interesting stories
- Cross-reference source documents with relative links so readers can dive deeper
- When options were considered, explain the tradeoffs honestly — don't just justify the winner

### Step 4: Write the Summary Table

After all Phases, add a summary table (see output template) that lets readers scan the entire evolution at a glance.

### Step 5: Identify Patterns

Look across all Phases for recurring patterns — things like:
- Quality improvements creating speed problems
- Duplication signaling a missing abstraction
- Over-engineering followed by simplification
- Bugs revealing design gaps

Include these as "Key Recurring Patterns" — they're the meta-lessons of the project.

### Step 6: Write What's Next

From the backlog, open issues, or incomplete RFCs, identify 2–4 threads that could trigger the next Phase. Frame each as a potential problem that hasn't been solved yet.

### Step 7: Save and Verify

Write the Evolution Log to the target path. Verify the output:
- Links to source documents are valid relative paths
- Phase dates are chronologically ordered
- Every Phase has all five cycle elements (Problem, Options, Decision, Result, New Problem)
- The summary table matches the Phase content
- The "Last updated" date is today

---

## Update Mode Details

When updating an existing Evolution Log:

1. Read the current file and parse the last Phase's date range and content
2. Identify new source material since the last update date:
   ```bash
   git log --format="%ad %s" --date=short --since="YYYY-MM-DD" --reverse
   ```
3. Check for new RFCs, RCAs, ADRs, or plan documents added since the last update
4. Decide:
   - **Extend current Phase**: If new material continues the same problem/theme
   - **Add new Phase**: If the problem has shifted meaningfully
   - **Update "What's Next"**: If items from the previous "What's Next" have been addressed
5. Update the summary table and "Last updated" date
6. Preserve all existing content — only append or update, never delete prior Phases
