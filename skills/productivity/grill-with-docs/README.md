# grill-with-docs

A grilling session skill designed to challenge plans against an existing domain model, sharpen fuzzy terminology, and ensure strict alignment with established documentation (e.g., `CONTEXT.md`). It also handles the generation of Architectural Decision Records (ADRs) and Requests for Comments (RFCs) based on standardized templates.

## Usage
Trigger this skill when you want the agent to relentlessly interview you and stress-test an implementation plan against your project's documented language and decisions. The agent will walk down each branch of the design tree, resolving dependencies and forcing precise terminology before outputting RFCs.

## Output Artifacts
- **CONTEXT.md**: In-line updates to the project's domain glossary.
- **docs/rfc/*.md**: Comprehensive RFC/ADR documents capturing the technical blueprint and decision logic.

---

## Changelog

### v1.1.0 - 2026-05-19
- **Refactor**: Replaced legacy sequential ADR format with the comprehensive 7-layers RFC/ADR standard (`RFC-ADR-FORMAT.md`).
- **Refactor**: Updated `SKILL.md` to output documents to `docs/rfc/` and utilize descriptive slug naming (e.g., `slug-name-of-the-proposal.md`) instead of numerical indexing.

### v1.0.0
- **Init**: Created the original `grill-with-docs` skill focusing on `CONTEXT.md` updates and basic `docs/adr/` generation.
