# Skill Refactoring Checklist & Quality Metrics

Use this checklist during Stage 4 of `skill-context-refactor` to verify quality before completing refactoring.

---

## 📋 Refactoring Audit Checklist

### 1. Frontmatter Description Check
- [ ] Includes concise summary of what the skill does.
- [ ] Includes explicit triggering contexts, user phrases, and scenarios.
- [ ] Contains no redundant body instructions in description.

### 2. Unhobbling Audit
- [ ] Removed all unnecessary `MUST`, `NEVER`, `ALWAYS` imperatives.
- [ ] Replaced rigid constraints with clear rationale ("why it matters").
- [ ] No micro-management of basic LLM formatting skills.
- [ ] No duplicate or contradictory guidelines across sections.

### 3. Interface Design Check
- [ ] Ad-hoc output examples replaced with structured JSON/YAML schemas or Enums.
- [ ] Discrete parameters (status, priority, categories) use explicit Enum types.
- [ ] Markdown templates use macro place-holders rather than multi-page examples.

### 4. Progressive Disclosure & Structure
- [ ] `SKILL.md` body is under 200 lines (hard max 300 lines).
- [ ] Detailed reference tables, deep domain guides, or full schemas moved to `references/`.
- [ ] Standard utility code moved to `scripts/`.
- [ ] Clear pointers in `SKILL.md` indicating *when* to load Level 3 files.

---

## 📊 Quantitative Target Metrics

| Metric | Pre-Refactor Baseline | Post-Refactor Target | Target Delta |
| :--- | :--- | :--- | :--- |
| `SKILL.md` Line Count | Raw line count | < 200 lines | -50% or more |
| Imperative Count (`MUST`/`NEVER`) | Count of strict keywords | Minimal (< 5) | -70%+ |
| Structured Schemas | Free-text examples | Typed Schema / Enums | 100% Schema coverage |
| Token Window Impact | Initial token estimate | Lean Spine tokens | -40% to -60% |
