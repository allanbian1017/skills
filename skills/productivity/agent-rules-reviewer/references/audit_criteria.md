# Audit Criteria & Evaluation Rubric (5-Vector Audit Model)

Use these five audit vectors to systematically evaluate every line and section in an agent steering document (`AGENTS.md`, `CLAUDE.md`, `.cursorrules`).

---

## Vector 1: Self-Duplication & Fragmentation

### Definition
Direct repetition or paraphrase of the same constraint across multiple headers or bullet points.

### Detection Patterns
- Testing requirements mentioned under `Constraints`, `Conventions`, and `Issue Resolution Workflow`.
- Anti-overengineering warnings repeated under general principles, task instructions, and tone rules.
- Dead code preservation stated under adjacent sub-bullets (e.g. "don't delete dead code" + "don't remove pre-existing dead code").
- Bug/RCA instructions split across general process and project-specific directories.

### Remediation Heuristic
Consolidate into a single canonical entry within the appropriate Tier (usually Tier 1 for testing structure, Tier 2 for approval gates, Tier 3 for scope boundaries). Eliminate all secondary copies.

---

## Vector 2: Base LLM Baseline Knowledge (Aphorisms & Generic Hygiene)

### Definition
Generic software development hygiene, common sense, or moral aphorisms that frontier models already follow by default without explicit instruction.

### Detection Patterns
- "When identifying a bug, find root causes, not symptoms. Do not make temporary or hacky fixes."
- "Write clean, readable, maintainable code."
- "Be polite, objective, and professional."
- "Think carefully before writing code."

### Remediation Heuristic
- **Delete pure aphorisms**: If a rule cannot be evaluated deterministically (e.g., "don't make hacky fixes"), remove it.
- **Replace with concrete verification gates**: Instead of "find root causes", mandate: "Any bug must be documented with quantitative evidence and an automated verification test in an RCA document."

---

## Vector 3: Host Environment & System Prompt Conflicts

### Definition
Rules that directly clash with or create ambiguity against the host AI assistant's system prompt, built-in tooling, or workspace sandbox.

### Detection Patterns
- **Link Schemes**: A rule banning `file:///` paths in general without distinguishing between chat UI links (where the host requires `file:///` for clickable links) and committed documentation files (where host-specific paths break portability).
- **Tool Fallbacks**: Rules advising the use of terminal commands or shell hacks when specific MCP or agent tools are natively registered.
- **Scratch Paths**: Ambiguities between host system scratch paths (`.tmp/` vs `<appDataDir>/brain/...`).

### Remediation Heuristic
Explicitly scope the contextual boundary:
- *Bad*: "Never use absolute `file:///` paths."
- *Good*: "In committed repository documentation (`docs/`, `reports/`), use relative workspace links instead of host-specific `file:///` paths."

---

## Vector 4: Skill Domain Leakage

### Definition
Detailed operational procedures, schemas, or domain rules that belong inside specialized Agent Skills (`SKILL.md`) rather than the global project steering document.

### Detection Patterns
- Summarization rules (e.g., Two-Zone extraction vs judgement, zero-hallucination standards) embedded in global `AGENTS.md` when a dedicated `content-summary` skill exists.
- Scraping deduplication details or API retry logic embedded in global instructions.

### Remediation Heuristic
Move domain-specific instructions into the relevant skill's `SKILL.md` or `references/`. In `AGENTS.md`, retain only high-level cross-cutting policies (e.g., language selection policy or strict tool enforcement).

---

## Vector 5: Negative Constraint Bloat & Attention Budget Overdraft

### Definition
Excessive density of prohibitive phrases (`NEVER`, `DO NOT`, `MUST NOT`, `ALWAYS`, `UNDER NO CIRCUMSTANCES`) that clutter context and trigger rule drift.

### Detection Patterns
- Long lists of negative prohibitions: "Do not add comments. Do not use external libraries. Do not change variable names. Do not refactor."
- Total file length exceeding 60 lines for a general repository steering document.

### Remediation Heuristic
1. Reframe into positive Tier 1 conventions: "Maintain existing style and touch only code directly involved in the change."
2. Restrict Tier 3 to 3–5 inviolable red lines (secrets, unapproved tools, out-of-scope edits).
3. Aim for a **40–50% reduction in total lines and token count**.
