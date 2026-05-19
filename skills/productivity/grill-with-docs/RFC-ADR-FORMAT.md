# RFC/ADR Format

RFC/ADRs live in `docs/rfc/` and use descriptive slug naming: `slug-name-of-the-proposal.md`.

When the user agrees to generate a proposal or architectural decision, use the following comprehensive template based on the 7-layers RFC standard.

## Template

```md
# RFC: {Descriptive Title of the Proposal}

## Summary
{1-2 paragraphs explaining the high-level goal and what this RFC accomplishes.}

## Status
**Proposed** — {YYYY-MM-DD}

## Motivation
{Why are we doing this? What is the current pain point or limitation? Concrete examples of the problem.}

## Detailed Design
{The technical blueprint. How does it work? Include architectures, new files, new concepts, and system workflows.}

## Drawbacks
{What are the negative consequences? Token costs, complexity, maintenance burden?}

## Alternatives Considered
### Alternative 1: {Name}
{Why was it rejected?}

## Unresolved Questions
{Any pending decisions that need to be figured out before execution. If none, write "None."}

## Implementation Plan
{A step-by-step checklist or reference to an external plan file (e.g., `docs/plan/...`).}

---

# ADR: {Title of the Architectural Decision}

## Status
Proposed — {YYYY-MM-DD}

## Context
{Brief summary of the context requiring a hard architectural decision.}

## Decision Drivers
- {List of technical or business requirements driving the decision}

## Decisions Made

### Decision 1: {Title}
**Context**: {What is the specific issue?}
**Decision**: {What did we decide?}
**Rationale**: {Why did we pick this over the alternatives?}

*(Repeat for as many core decisions as needed)*

## Consequences

### Positive
- {Benefits}

### Negative
- {Trade-offs}

## References
- {Links to previous RFCs, external docs, or related files}
```

## When to offer an RFC/ADR

All three of these must be true:

1. **Hard to reverse** — the cost of changing your mind later is meaningful
2. **Surprising without context** — a future reader will look at the code and wonder "why on earth did they do it this way?"
3. **The result of a real trade-off** — there were genuine alternatives and you picked one for specific reasons

If a decision is easy to reverse, skip it — you'll just reverse it. If it's not surprising, nobody will wonder why. If there was no real alternative, there's nothing to record beyond "we did the obvious thing."
