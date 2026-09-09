---
name: flow-tracer
description: >
  Trace an endpoint or function's complete code flow through the codebase and produce a structured
  documentation artifact with Mermaid sequence diagrams, infrastructure details (Redis keys, queues,
  DB tables), and abstract step-by-step flow descriptions. Use this skill whenever the user asks to
  "trace a flow", "document an endpoint", "show me the code flow for X", "how does X work end to end",
  "what happens when X is called", "map out the flow of X", "trace the call chain of X",
  or any request to understand, visualize, or document how a specific endpoint, handler, function,
  or feature flows through the codebase — even if they don't explicitly say "trace" or "flow".
---

# Flow Tracer

Trace an endpoint or function's complete execution path through a codebase, then produce a
structured, human-readable document that tells the full story of how a request travels from
entry to completion.

This skill is **language-agnostic** and **repo-portable**. It works on any codebase in any
language by relying on `codebase-memory-mcp` for code discovery.

## Prerequisites

This skill **requires** `codebase-memory-mcp` to be available and the target repository to be
indexed. If the repo is not indexed:

1. Run `index_repository` on the target repo first
2. Wait for indexing to complete (`index_status` to check)
3. Then proceed with the trace

Do NOT fall back to grep-based tracing. The knowledge graph is essential for reliable
cross-boundary tracing.

## Workflow

### Phase 1: Understand the Request

1. **Parse the user's request** — identify the target endpoint, function, or feature.
2. **Disambiguate if needed** — if the name matches multiple entry points, use `search_graph`
   to find candidates and present them to the user. Ask which one they mean before proceeding.
3. **Check output intent** — default to producing an Antigravity artifact. If the user says
   "save this to X" or "commit this," switch to file output with relative links.

### Phase 2: Trace (Progressive — Narrate in Chat)

Narrate your findings in chat as you go. The user should see the exploration happening in
real-time so they can redirect if you're tracing the wrong path.

#### Step 1: Understand the Repo Architecture

```
Tool: get_architecture
```

Get a high-level understanding of the repo — what language, frameworks, layering patterns,
and conventions are used. This orients all subsequent tracing.

Share a brief summary in chat: *"This is a [language] [framework] project with [pattern]
architecture..."*

#### Step 2: Locate the Entry Point

```
Tool: search_graph (name_pattern=".*<EndpointName>.*")
```

Find the route registration, handler declaration, or function definition that serves as the
entry point. Look for:
- Route/URL registrations (HTTP routers, gRPC service definitions)
- Controller/handler method declarations
- Event listener registrations
- CLI command definitions

Share what you found: *"Found the entry point at [file:line] — it maps to [handler]..."*

#### Step 3: Trace the Call Chain

```
Tool: trace_path (function_name="<handler>", direction="outbound")
```

Follow the outbound call chain from the entry point through each layer:
1. **Transport/routing layer** — request decoding, middleware
2. **Handler/controller layer** — orchestration, validation, error mapping
3. **Service/business logic layer** — core operations, external calls
4. **Data access layer** — database queries, cache operations, API clients

At each layer, identify:
- **Injected dependencies** being called
- **External system boundaries** being crossed (DB, cache, APIs, queues)
- **Async handoffs** (message queue publishes, event emissions, background job dispatches)

Use `get_code_snippet` to read the source of key functions when you need to understand
the implementation detail.

Share progress: *"The handler calls [ServiceMethod], which acquires a Redis lock, then
calls [ExternalAPI]..."*

#### Step 4: Follow Async Boundaries

When you encounter an async boundary (message queue publish, event dispatch, scheduled job):

1. Note the **task/event name** and **payload structure**
2. Use `search_graph` to find the **consumer/worker/subscriber** that handles this task
3. Trace the consumer's call chain as a new entry point (repeat Step 3)

Share the boundary: *"Found an async boundary — publishes to [queue] with task name
[taskName]. The consumer is [WorkerClass] at [file:line]..."*

#### Step 5: Collect Infrastructure Details

As you trace, collect every stateful resource the flow touches:

**Databases:**
- Table/collection name
- Operations (SELECT, INSERT, UPDATE, DELETE)
- Key columns/fields and conditions

**Cache/Store (Redis, Memcached, etc.):**
- Key pattern (with placeholders like `<userID>`)
- Data type (String, List, Hash, Set, etc.)
- Purpose (lock, cache, queue, counter)
- TTL if applicable

**Message Queues (RabbitMQ, Kafka, SQS, etc.):**
- Queue/topic name
- Task/event name
- Payload schema (JSON structure with key fields)
- Consumer identity

**Request/Response Schemas:**
- Entry point request schema (protobuf, JSON, struct — key fields)
- Entry point response schema
- Inter-service request/response schemas (if the flow calls other services)

#### Step 6: Map Error Paths

Identify notable error handling:
- Error types/codes and what triggers them
- Retry logic (backoff, max attempts, delay)
- Circuit breakers or rate limiting
- Dead-letter queues or failure queues
- Fallback behaviors

### Phase 3: Compose the Artifact

Once the trace is complete, produce the final artifact. Use the output format below.

---

## Output Format

Produce a **Markdown artifact** with these sections. Omit any section that doesn't apply
to the traced flow.

### Section 1: Overview

A 2-3 sentence summary: what this flow does, who triggers it, what the end result is.

### Section 2: Sequence Diagram

A Mermaid `sequenceDiagram` showing interactions between participants.

**Participant rules:**
- Use short, recognizable aliases (e.g., `participant api AS OrderService`)
- Map code-level names to logical participants:
  - The caller → "User", "Client", or the upstream service name
  - Internal service layers → collapse into the service name (don't show internal methods)
  - Databases → "DB" or the specific database name
  - Caches → "Redis", "Cache", etc.
  - External APIs → the provider name (e.g., "Stripe", "Twilio")
  - Message queues → "RabbitMQ", "Kafka", "MQ", etc.
  - Background workers → "Worker" or the specific worker name

**Arrow rules:**
- Sync calls: `->>+` (with activation) and `->>-` (deactivation on return)
- Async dispatches: `-->>` (dashed arrow)
- Add `Note over ...` to mark async boundaries clearly

**Granularity:**
- Show each call that crosses a **service boundary** or **external system boundary**
- Collapse internal method calls within the same service
- Each distinct external operation (e.g., separate Redis lock vs. Redis queue push) gets its own arrow

### Section 3: Data Model

Document ALL stateful structures the flow touches.

#### Request/Response Schemas

Show the entry point's input/output contract with key fields:

```
Request: CreateOrderRequest {
  user_id: string
  items: []OrderItem { product_id, quantity, price }
  payment_method_id: string
}

Response: CreateOrderResponse {
  order_id: string
  status: string
  total_amount: decimal
}
```

#### Database Tables

| Table | Operations | Key Columns |
|-------|-----------|-------------|
| `orders` | INSERT, UPDATE | `id`, `user_id`, `status`, `total_amount` |

#### Cache/Store Keys

| Key Pattern | Type | Purpose | TTL |
|------------|------|---------|-----|
| `order-lock-<userID>` | String | Idempotency lock | 30s |

#### Message Queue Payloads

| Queue | Task Name | Payload | Consumer |
|-------|-----------|---------|----------|
| `order-notifications` | `sendConfirmation` | `{"orderId": "<id>", "email": "<email>"}` | `NotificationWorker` |

### Section 4: Abstract Flow Steps

A numbered list of logical actions grouped by phase. For each step:
- State the **action** in plain English
- Reference the **key function(s)** with clickable file links
- Note infrastructure interactions inline

Group by phase when async boundaries exist:

```markdown
## Sync Phase — API Request
1. **Validate order items and payment method**
   → [`validateOrder`](file:///path/to/handler.go#L45)
   - Checks item availability, validates payment method ownership

2. **Create order record**
   → [`createOrder`](file:///path/to/service.go#L100)
   - Inserts into `orders` table with status `pending`
   - Acquires idempotency lock: `order-lock-<userID>` (TTL: 30s)

## Async Phase — Worker Processing
3. **Process payment**
   → [`processPayment`](file:///path/to/worker.go#L30)
   - Calls Stripe `charges.create` with idempotency key `order-<orderID>`
```

### Section 5: Error Handling

| Error | Code/Status | Trigger | Behavior |
|-------|-------------|---------|----------|
| `ItemOutOfStock` | 409 Conflict | Item unavailable at checkout | Returns error, no charge |
| `PaymentFailed` | 402 Payment Required | Stripe charge declined | Retries 3x with exponential backoff |

### Section 6: Related Flows (Best-Effort)

If you naturally discovered related flows during tracing, list them:
- **Triggered by this flow**: e.g., "Order confirmation email via NotificationWorker"
- **Triggers this flow**: e.g., "Called by the Checkout page via API Gateway"

Only include this section if you actually found related flows — don't do extra research.

---

## Output Persistence

**Default**: Produce an Antigravity artifact with `file:///` links for source references.

**On user request**: If the user says "save this to `docs/flows/`" or "commit this," write
the document to the specified path and convert all `file:///` links to relative paths
(per repository portability conventions).

---

## Tips for Better Traces

- **Follow the interfaces**: When you see an interface/abstract method call, use
  `search_graph` to find the concrete implementation — check DI registration if applicable.
- **Check for middleware**: Auth, logging, metrics, and tracing middleware may wrap handlers.
  Note them if they affect the flow (e.g., auth middleware rejecting requests).
- **Look for feature flags**: Conditional logic may fork the flow. Document the conditions.
- **Cross-reference tests**: Integration tests often exercise the full flow and can confirm
  your understanding of the call sequence.
- **Note idempotency**: Many flows use idempotency keys. Document the key format — it's
  critical for debugging duplicate processing.
