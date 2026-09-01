# Architecture Tradeoff Checklist — [Feature Name]

<!-- Time target: ≤5 minutes for initial pass during RFC authoring. -->
<!-- Fill only sections relevant to your project domain(s). -->
<!-- For inapplicable items, mark N/A with a one-liner justification (e.g., "N/A — no mobile client in scope"). -->
<!-- Omit entire domain sub-headings from the RFC appendix if all items under that domain are N/A. -->
<!-- This checklist is appended to the RFC as "## Appendix: Architecture Tradeoff Checklist". -->

## 1. Latency & Concurrency

### Backend / API
- [ ] Sync vs. Async decision: ___
- [ ] Connection pool sizing: ___
- [ ] DB index paths reviewed: ___
- [ ] Rate limiter strategy: ___
- [ ] P99 latency SLO defined: ___ms

### AI Agent
- [ ] Parallel fan-out/fan-in vs. sequential pipeline decision: ___
- [ ] Observation/context compression strategy for latency control: ___
- [ ] Worker isolation model: ___

### Frontend / Web
- [ ] Local caching strategy: ___
- [ ] Virtual scroll / large list handling: ___
- [ ] Bundle size & code splitting plan: ___
- [ ] Background thread strategy (Web Workers): ___

### Mobile Client
- [ ] Local caching strategy: ___
- [ ] Virtual scroll / large list handling: ___
- [ ] Bundle size & code splitting plan: ___
- [ ] Background thread strategy (Coroutines / GCD): ___

## 2. Data Architecture & State Management

### Backend / API
- [ ] Single source of truth (SSOT) identified: ___
- [ ] Consistency model chosen (ACID / eventual / hybrid): ___
- [ ] Cache invalidation strategy: ___
- [ ] Schema evolution & migration plan: ___

### AI Agent
- [ ] Multi-turn state persistence approach: ___
- [ ] Parallel sub-agent isolation (stage-then-merge): ___
- [ ] Context pollution prevention: ___

### Frontend / Web
- [ ] Global vs. local state boundaries: ___
- [ ] Offline persistence & optimistic updates: ___
- [ ] Lifecycle state restoration: ___

### Mobile Client
- [ ] Global vs. local state boundaries: ___
- [ ] Offline persistence & optimistic updates: ___
- [ ] Lifecycle state restoration: ___

## 3. Availability, Resilience & Blast Radius

### Backend / API
- [ ] Circuit breaker / graceful degradation plan: ___
- [ ] Multi-region / zero-downtime deployment: ___
- [ ] Blast radius containment: ___

### AI Agent
- [ ] Multi-provider model router / fallback: ___
- [ ] Tool exception handling & safe exit: ___
- [ ] Per-task step/cost cap circuit breaker: ___

### Frontend / Web
- [ ] Error boundaries defined: ___
- [ ] Empty state & degraded UI: ___
- [ ] Exponential backoff retry: ___

### Mobile Client
- [ ] Error boundaries defined: ___
- [ ] Empty state & degraded UI: ___
- [ ] Exponential backoff retry: ___

## 4. Security, Privacy & Trust Boundaries

### Backend / API
- [ ] AuthN/AuthZ model (OAuth / JWT / RBAC): ___
- [ ] Input validation (SQLi / XSS prevention): ___
- [ ] Least privilege principle applied: ___

### AI Agent
- [ ] Tool capability firewall: ___
- [ ] Disposable single-use credential sandbox: ___
- [ ] Shell sandbox isolation: ___
- [ ] Prompt injection defense: ___

### Frontend / Web
- [ ] Secure storage strategy: ___
- [ ] Content Security Policy (CSP): ___
- [ ] Authentication gate: ___

### Mobile Client
- [ ] Secure storage (Keychain / Keystore): ___
- [ ] Content Security Policy: ___
- [ ] Biometric auth gate: ___

## 5. Verification, Testing & Observability

### Backend / API
- [ ] Test pyramid defined (Unit / Integration / E2E): ___
- [ ] Structured logging (JSON) + distributed tracing: ___
- [ ] SLO metrics & alerting: ___

### AI Agent
- [ ] Deterministic assertion tests: ___
- [ ] Output schema static validation: ___
- [ ] Eval benchmark / hallucination evaluation: ___

### Frontend / Web
- [ ] Component snapshot tests: ___
- [ ] E2E user flow tests: ___
- [ ] Crash monitoring + user telemetry: ___

### Mobile Client
- [ ] Component snapshot tests: ___
- [ ] E2E user flow tests: ___
- [ ] Crashlytics / crash monitoring: ___
- [ ] User behavior telemetry: ___
