---
name: skill-context-refactor
description: Refactor and optimize Agent Skills using modern Context Engineering principles. Removes 50%+ bloated micro-rules (Unhobbling), converts ad-hoc examples into explicit JSON/YAML schemas and Enums (Design Interfaces), and restructures SKILL.md into a Lean Spine (<200 lines) with on-demand references (Progressive Disclosure). Use this skill whenever asked to "refactor skill", "unhobble skill", "optimize skill context", "clean up skill instructions", "apply context engineering to skill", or when an agent skill is bloated, overly rigid, or hard to maintain.
---

# Skill Context Refactoring (`skill-context-refactor`)

Refactor existing Agent Skills to dramatically reduce context window overhead, eliminate restrictive micro-management instructions (unhobble), and establish typed semantic interfaces.

## Refactoring Workflow

Follow this 4-stage pipeline when refactoring any skill:

```
[1. Audit & Benchmark] ──> [2. Unhobble] ──> [3. Design Interfaces] ──> [4. Progressive Disclosure]
```

---

### Stage 1: Audit & Benchmark
1. Measure initial metrics: line count, line count of `SKILL.md`, estimated token size, and count of restrictive keywords (`MUST`, `NEVER`, `ALWAYS`, `DO NOT`).
2. Identify core capability vs. auxiliary details:
   - **Core Spine**: Workflow steps, triggering logic, essential parameters.
   - **Auxiliary**: Deep domain knowledge, edge-case handling rules, long output templates, verbose examples.

---

### Stage 2: Unhobble (Strip Micro-Regulations)
1. Eliminate micro-management rules that restrict reasoning without adding quality.
   - *Before*: "NEVER write more than 3 bullet points. ALWAYS use present tense. DO NOT use adjectives."
   - *After*: State the goal clearly and explain the rationale: "Keep summary bullet points concise and focused on actionable technical decisions so the reader can digest changes rapidly."
2. Remove redundant, duplicate, or contradictory constraints across sections.
3. Replace rigid MUST/NEVER directives with intent descriptions and boundary conditions.

---

### Stage 3: Design Interfaces (Semantic Interface Refactoring)
1. Replace free-text example blocks with typed JSON/YAML Schemas or TypeScript/Pydantic interface specs.
2. Define explicit Enums for categorical fields (e.g. status, severity, category).
3. Specify strict contract formats for inputs, outputs, and intermediate data structures.
4. Read `references/context_engineering_principles.md` for schema templates and design patterns.

---

### Stage 4: Progressive Disclosure (Lean Spine Architecture)
1. Restructure `SKILL.md` into a Lean Spine (<200 lines target).
2. Move auxiliary content into dedicated reference files:
   - `references/schema.md` or `references/<topic>.md` for schemas and templates.
   - `scripts/` for deterministic tasks, scripts, or parsers.
3. Add explicit triggers in `SKILL.md` specifying *when* to load reference files on-demand.
4. Verify using `references/refactor_checklist.md`.

---

## Verification & Metrics

After refactoring, verify against target benchmarks:
- **Token / Line Reduction**: Target >= 40-50% reduction in `SKILL.md` line count.
- **Strict Interfaces**: All structured outputs must have explicit schemas or Enums.
- **Spine Budget**: `SKILL.md` should be under 200 lines (hard max 300 lines).
