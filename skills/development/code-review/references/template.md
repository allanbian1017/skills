# [Language Name] Style Guide Rubric Template

> **Reference Template**: This document defines the canonical schema contract for all language-specific style rubrics in `.agents/skills/code-review/references/<lang>.md`. Any new language style guide onboarded to the skill must conform to this structure.

---

## Rubric Authoring Principles

### The Strict Linter Exclusion Boundary
To maximize review signal and prevent burning expensive LLM tokens on mechanical tooling problems, **do not** include rules that are 100% enforced by standard formatters or static AST linters:
- **Exclude**: Spacing, tabs vs. spaces, indentation depth, bracket placement, line wrap length, trailing commas. (Handled by `gofmt`, `prettier`, `ruff`, `rustfmt`).
- **Exclude**: Unused imports, unused local variables, missing semicolons, basic unreachable code. (Handled by `golangci-lint`, `eslint`, `ruff`, `cargo clippy`).
- **Include**: Semantic idioms, error wrapping context, resource leaks, goroutine/thread lifetimes, nil/null boundary guards, defensive copies at API boundaries, interface segregation, type assertion safety.

---

## Category Index
- **Guidelines**: Core language idioms, safety, error handling, lifecycle, and concurrency.
- **Performance**: Allocations, string manipulation, and collection efficiency.
- **Style**: Semantic naming conventions, variable scoping, and declarations (non-mechanical).
- **Patterns**: Idiomatic structural, architectural, and testing patterns.

---

# Rubric Rules

Binary pass/fail checks evaluated during style reviews. Each rule impacts the automated numerical style compliance score. Rule IDs must strictly follow `R-<LANG>-<NUM>`.

### R-<LANG>-01: [Rule Title]
- **Severity**: HIGH | MEDIUM | LOW
- **Category**: Guidelines | Performance | Style | Patterns
- **Check**: Single-sentence imperative statement defining the binary condition that must be met.
- **Bad**:
  ```[ext]
  // Anti-pattern snippet showing the violation
  ```
- **Good**:
  ```[ext]
  // Compliant snippet showing the recommended resolution
  ```

### R-<LANG>-02: [Rule Title]
- **Severity**: HIGH | MEDIUM | LOW
- **Category**: Guidelines | Performance | Style | Patterns
- **Check**: Single-sentence imperative statement defining the binary condition that must be met.
- **Bad**:
  ```[ext]
  // Anti-pattern snippet showing the violation
  ```
- **Good**:
  ```[ext]
  // Compliant snippet showing the recommended resolution
  ```

---

# Contextual Guidelines

Judgment-based recommendations evaluated qualitatively during code reviews. These provide non-scoring advisory notes that require human engineering judgment. Guideline IDs must strictly follow `C-<LANG>-<NUM>`.

### C-<LANG>-01: [Guideline Title]
- **Category**: Guidelines | Performance | Style | Patterns
- **Description**: Concise explanation of the design tradeoff or contextual dilemma.
- **Guidance**: Concrete heuristics on when to prefer one approach over another (e.g. pointer vs. value receiver, sync.Mutex vs. channels, class vs. functional).

### C-<LANG>-02: [Guideline Title]
- **Category**: Guidelines | Performance | Style | Patterns
- **Description**: Concise explanation of the design tradeoff or contextual dilemma.
- **Guidance**: Concrete heuristics on when to prefer one approach over another.
