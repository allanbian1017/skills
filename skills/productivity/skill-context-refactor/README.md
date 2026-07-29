# Skill Context Refactoring Skill (`skill-context-refactor`)

## Overview

The `skill-context-refactor` skill optimizes Agent Skills using modern **Context Engineering** principles. It refactors bloated instructions to remove restrictive micro-rules, structures ad-hoc freeform examples into explicit machine-readable interfaces (schemas/enums), and partitions detailed domain guides into on-demand references, keeping the primary `SKILL.md` file as a lean, token-efficient workspace spine.

## Problem Statement

As AI agent systems scale, the instruction sets (skills) they load into the context window tend to grow excessively. Legacy skills often suffer from:
1. **Prompt Over-Regulation:** Restrictive instructions containing too many imperative keywords (`MUST`, `NEVER`, `ALWAYS`, `DO NOT`) that degrade model reasoning capability (hobbling).
2. **Token Bloat:** Large, freeform text examples and templates that consume thousands of unnecessary prompt tokens in every run.
3. **Monolithic Structure:** All workflow steps, edge cases, schemas, and references are packed into a single huge `SKILL.md` file, rather than disclosing information progressively.

## Solution

The `skill-context-refactor` skill provides a systematic 4-stage pipeline to restructure, simplify, and optimize agent skills for token efficiency and reasoning performance.

### Key Features

1. **Audit & Benchmark:** Measure skill dimensions (lines, token size, imperative counts) to establish baseline metrics.
2. **Unhobbling:** Replace rigid, micro-managing imperatives with rationale-driven explanations ("explain the why").
3. **Semantic Interface Design:** Convert free-text outputs or example formats into explicit JSON/YAML schemas or Enums.
4. **Progressive Disclosure (Lean Spine):** Shrink the core `SKILL.md` to under 200 lines (hard max 300) by offloading deep domain knowledge, templates, or scripts to the `references/` and `scripts/` directories.

## File Structure

```
skill-context-refactor/
├── SKILL.md                                # Core workflow and trigger spine
├── README.md                               # This file
├── evals/
│   └── evals.json                          # Benchmarks for refactoring validation
└── references/
    ├── context_engineering_principles.md   # Core design patterns and principles
    └── refactor_checklist.md               # Quality metrics and verification audit
```

## Triggering

This skill triggers when the user asks to:
- "refactor skill"
- "unhobble skill"
- "optimize skill context"
- "clean up skill instructions"
- "apply context engineering to skill"

## Quality Standards & Metrics

| Metric | Target Value |
|---|---|
| **Spine Budget** | `SKILL.md` body is under 200 lines (hard max 300 lines) |
| **Imperative Count** | Minimal strict imperatives (`MUST`, `NEVER`, etc.) — target < 5 |
| **Interface Coverage** | 100% of structured outputs defined via typed schemas or Enums |
| **Token Savings** | 40% to 60% reduction in system prompt / initial context impact |

## Changelog

| Version | Date | Change Summary |
|---|---|---|
| v1.0.0 | 2026-07-29 | Initial release of the `skill-context-refactor` skill featuring a 4-stage refactoring pipeline, context engineering principles reference guide, quality metrics checklist, and validation evals. |
