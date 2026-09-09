# Flow Tracer

A portable, language-agnostic agent skill that traces any endpoint or function's complete
code flow through a codebase and produces structured documentation with Mermaid sequence
diagrams, data models, and abstract flow steps.

## What It Does

Given an endpoint, handler, or function name, this skill:

1. **Traces the complete execution path** — from entry point through handler → service →
   data access layers, following async boundaries into workers/consumers
2. **Produces a structured artifact** containing:
   - **Sequence diagram** (Mermaid) — service-to-service and external system interactions
   - **Data model** — DB tables, cache keys, queue payloads, request/response schemas
   - **Abstract flow steps** — logical actions with function links, grouped by phase
   - **Error handling** — error types, codes, retry behavior, fallback paths
3. **Narrates the trace progressively** in chat so you can follow along and redirect

## Requirements

- **codebase-memory-mcp** — the target repo must be indexed. The skill uses `get_architecture`,
  `search_graph`, `trace_path`, and `get_code_snippet` for code discovery.

## Usage

Trigger phrases:
- "Trace the Cashout30 flow"
- "How does the payment capture endpoint work end to end?"
- "Show me the code flow for CreateOrder"
- "What happens when the webhook handler is called?"
- "Document the notification worker flow"

## File Structure

```
flow-tracer/
├── SKILL.md                        ← Main skill instructions
├── README.md                       ← This file
└── references/
    └── example-output.md           ← Generic example output (e-commerce Place Order)
```

## Output Modes

| Mode | Trigger | Link Format |
|------|---------|-------------|
| **Artifact** (default) | Any trace request | `file:///` absolute paths |
| **Committed file** | "Save this to `docs/flows/`" | Relative paths |

---

## Architecture Decision Records

### ADR-001: Generic & Portable over Repo-Specific

**Status**: Accepted  
**Date**: 2026-09-09  
**Context**: The initial draft included monetize-specific patterns (Go struct injection tags,
FastWeb handler naming conventions, specific file paths like `fw_convpay_new.go`). This made
traces more reliable for the monetize repo but locked the skill to one codebase.  
**Decision**: Make the skill fully generic and language-agnostic. Rely on `codebase-memory-mcp`
for runtime code discovery instead of baking in repo-specific knowledge.  
**Rationale**: "The whole idea is making this agent skill portable to any repo." The value is
in the *tracing methodology*, not repo-specific shortcuts. A sharp methodology + good discovery
tool scales across any codebase.  
**Consequences**: The skill may take slightly longer on the first trace of a new repo (needs to
understand architecture first via `get_architecture`), but works everywhere.

---

### ADR-002: codebase-memory-mcp Required (No Fallback)

**Status**: Accepted  
**Date**: 2026-09-09  
**Context**: Not every repo the user works with will be indexed in codebase-memory-mcp. A
graceful fallback to grep/ripgrep was considered.  
**Decision**: Make codebase-memory-mcp a hard requirement. If the repo isn't indexed, instruct
the agent to run `index_repository` first.  
**Rationale**: The knowledge graph provides structured call-chain tracing (`trace_path`) and
semantic search (`search_graph`) that grep cannot replicate. Allowing fallback would produce
inconsistent, lower-quality traces.  
**Consequences**: Users must wait for indexing on first use with a new repo. Subsequent traces
benefit from the indexed graph.

---

### ADR-003: Progressive Output Delivery

**Status**: Accepted  
**Date**: 2026-09-09  
**Context**: The skill could trace silently and deliver a complete artifact, or narrate
findings in chat as it traces.  
**Decision**: Progressive delivery — narrate tracing progress in chat, produce the final
artifact only after the full trace is complete.  
**Rationale**: Aligns with the user's preference for chat-to-artifact progressive rendering.
Allows the user to redirect early if the agent is tracing the wrong path, avoiding wasted work.  
**Consequences**: Chat history is slightly more verbose, but the user has full visibility.

---

### ADR-004: Service-to-Service + External Diagram Granularity

**Status**: Accepted  
**Date**: 2026-09-09  
**Context**: Sequence diagrams could show every function call (very detailed), only external
system calls (very high-level), or service boundaries + external calls (middle ground).  
**Decision**: Show inter-service calls and external system boundaries. Collapse internal method
calls within the same service into the service participant.  
**Rationale**: Matches the user's Cashout30 example where ConvPay was one participant but
Redis, Stripe, RabbitMQ, and Worker were separate. Internal detail belongs in the abstract flow
steps section.  
**Consequences**: Diagrams stay readable even for complex flows. Function-level detail is
available in the abstract flow steps.

---

### ADR-005: Data Model = All Stateful Structures

**Status**: Accepted  
**Date**: 2026-09-09  
**Context**: "Data model" could mean just database tables, or could encompass all stateful
resources the flow touches.  
**Decision**: Include all stateful structures: database tables, cache/store keys, message queue
payloads, AND request/response schemas (protobuf, structs, interfaces).  
**Rationale**: The user wants the complete picture of "what data moves where" — not just
persistence, but the full state surface area including the API contract and infrastructure.  
**Consequences**: The data model section is comprehensive but may be long for complex flows.

---

### ADR-006: No Prescribed Output Location

**Status**: Accepted  
**Date**: 2026-09-09  
**Context**: The skill could prescribe a default directory for committed flow docs
(e.g., `docs/flows/`).  
**Decision**: Default to ephemeral artifact output. Let the user decide per-invocation whether
and where to persist.  
**Rationale**: "Sometimes I just want to know how this flow works, and not a precise document
for the team. I will decide once I request it."  
**Consequences**: No opinionated directory structure. The user has full control.

---

## Changelog

### v1.0.0 — 2026-09-09

**Initial release** after grill-me design session.

- **SKILL.md**: Complete rewrite from initial draft
  - Generic, language-agnostic tracing methodology (6-step process)
  - `codebase-memory-mcp` as required discovery tool
  - Progressive output delivery (narrate in chat → final artifact)
  - Ambiguity handling (ask user to clarify when multiple matches)
  - Output persistence mode (artifact default, committed file on request)
  - Expanded data model section (DB + cache + queues + request/response schemas)
  - Service-to-service + external granularity for sequence diagrams
  - Async boundary detection (document when present, don't force)
  - Error handling as dedicated section
  - Related flows as best-effort
  - Logical-action granularity for abstract flow steps

- **references/example-output.md**: Generic e-commerce "Place Order" example
  - Demonstrates all output sections with realistic content
  - Language-neutral, not tied to any specific codebase

- **Deleted**: `references/monetize-patterns.md` (repo-specific, contradicts portability)
- **Deleted**: `references/example-cashout30.md` (replaced by generic example)

#### Design Decisions Resolved

13 design decisions resolved via grill-me session — see ADRs above for the 6 most
significant. Full decision log:

| # | Decision | Resolution |
|---|----------|-----------|
| 1 | Consumer | Both ad-hoc (artifact) and team docs (committed file) |
| 2 | Output location | No prescribed path; user decides |
| 3 | Scope | Generic, portable across any repo and language |
| 4 | Discovery | codebase-memory-mcp required |
| 5 | Data model | All stateful structures + request/response schemas |
| 6 | Diagram granularity | Service-to-service + external boundaries |
| 7 | Async boundaries | Call out when present, don't force |
| 8 | Error handling | Keep as dedicated section |
| 9 | Language | Any language (language-agnostic) |
| 10 | Example | Generic fictional example |
| 11 | Ambiguity | Ask user to clarify |
| 12 | Flow step depth | Logical-action granularity |
| 13 | Related flows | Best-effort |
| 14 | Req/resp schemas | Include in data model |
| 15 | Output delivery | Progressive (narrate → artifact) |
