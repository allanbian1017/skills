# Context Engineering Principles for Agent Skills

This guide details the three pillars of modern Context Engineering for Claude agent skills:

---

## 1. Unhobbling (Over-Regulation Removal)

Legacy prompts and skills often suffer from "prompt over-regulation" — adding dozens of restrictive micro-rules (`MUST`, `NEVER`, `ALWAYS`, `DO NOT`) in an attempt to control the model. This artificially degrades model reasoning ("hobbling").

### Core Rules of Unhobbling
1. **Explain the WHY instead of imposing MUSTs**: Modern LLMs perform significantly better when given context and reasoning rationale rather than blind imperatives.
   - ❌ *Hobbled*: "MUST use bullet points. NEVER use paragraphs. DO NOT write intro text."
   - ✅ *Unhobbled*: "Present key findings in bullet format for rapid visual scanning. Skip conversational preamble so the report starts immediately with actionable data."
2. **Eliminate Micro-management**: Strip out instructions that enforce obvious formatting details (e.g. single spacing, capitalizing titles) unless strict machine parsing depends on it.
3. **Consolidate Redundant Rules**: Group fragmented rules into coherent intent blocks.

---

## 2. Design Interfaces (Semantic Interface Refactoring)

Freeform text examples in prompts are noisy, imprecise, and consume excessive tokens. Converting text examples into formal schemas improves reliability and token efficiency.

### Interface Design Patterns
1. **JSON / YAML Schema over Text Examples**:
   Define strict schema declarations with property descriptions, required fields, and types.
   ```yaml
   type: object
   properties:
     title: { type: string, description: "Descriptive title of the report" }
     status: { type: string, enum: ["pending", "in_progress", "completed", "failed"] }
     score: { type: number, minimum: 0, maximum: 10 }
   required: ["title", "status", "score"]
   ```
2. **Typed Enums for Discrete Values**: Replace vague textual descriptions ("high quality", "medium", "bad") with explicit Enum sets (`["critical", "major", "minor", "informational"]`).
3. **Structured Templates for Documents**: For Markdown reports, provide clean, macro-level templates with variable placeholders rather than multi-page example outputs.

---

## 3. Progressive Disclosure (Lean Spine Architecture)

Progressive Disclosure ensures that the agent's context window is only populated with information relevant to the immediate step.

### Context Hierarchy
1. **Level 1: Metadata (Frontmatter)** (~50-100 words)
   - Resides permanently in system prompt (`name` and `description`).
   - Contains trigger conditions and capability overview.
2. **Level 2: Lean Spine (`SKILL.md`)** (<200 lines)
   - Loaded when skill triggers.
   - Contains high-level workflow router, stage definitions, and references to Level 3 files.
3. **Level 3: Bundled References & Scripts (`references/`, `scripts/`)** (Unlimited)
   - Loaded conditionally when explicit workflow conditions are met.
   - Detailed schemas, domain knowledge bases, script utilities.
