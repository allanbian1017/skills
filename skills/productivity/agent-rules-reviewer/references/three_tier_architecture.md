# 3-Tier Agent Rules Architecture & Attention Budget Governance

## 1. Overview & Core Philosophy

Addy Osmani's **3-Tier Agent Rules Architecture** organizes AI steering rules into three explicit, unambiguous operational tiers. 

Traditional rule files (like `AGENTS.md` or `CLAUDE.md`) often deteriorate into unstructured lists of negative micro-regulations (`DO NOT write more than 5 lines`, `NEVER use X`, `ALWAYS do Y`). This causes **Attention Degradation (Rule Drift)**: as negative constraints accumulate, the model's effective attention budget is consumed by suppression filters, paradoxically increasing the chance that critical invariant rules are ignored during complex tasks.

The 3-Tier Architecture resolves this by separating:
1. What the agent should do autonomously (**Always Do**).
2. Where the agent must stop and ask (**Ask First**).
3. What the agent must never do (**Never Do**).

---

## 2. The Three Tiers Defined

```
┌─────────────────────────────────────────────────────────────┐
│  Tier 1: Always Do (Safe Defaults & Autonomous Automation)  │
│  - Non-intrusive operations executed without asking         │
│  - Automated testing & assertion verification               │
│  - Format/linter checks and deterministic hygiene           │
├─────────────────────────────────────────────────────────────┤
│  Tier 2: Ask First (Human-in-the-Loop & Approval Gates)     │
│  - High-blast-radius or architecture-altering operations    │
│  - Ambiguous intent, multiple viable design paths           │
│  - Core steering contract mutations (e.g. AGENTS.md diffs)  │
├─────────────────────────────────────────────────────────────┤
│  Tier 3: Never Do (Hard Invariants & Inviolable Boundaries) │
│  - Absolute system boundaries and security redlines         │
│  - Tool circumvention & arbitrary fallback scripts          │
│  - Scope creep and unrequested refactoring                  │
└─────────────────────────────────────────────────────────────┘
```

### Tier 1: Always Do (Safe Defaults & Autonomous Automation)
- **Concept**: Actions the agent should execute autonomously without prompting the user. These provide zero-friction productivity while guaranteeing quality.
- **Characteristics**: Deterministic, reversible, verifiable via automated tests or scripts, low blast radius.
- **Typical Examples**:
  - Automatically run tests after modifying code.
  - Scan directories for existing duplicates before batch ingestion.
  - Run skill validators (`scripts/validate_skill.py`) when modifying `SKILL.md`.
  - Check `known_issues.md` at session start.
  - Use `.tmp/` for staging temporary scratch files.

### Tier 2: Ask First (Human-in-the-Loop & Approval Gates)
- **Concept**: High-risk, irreversible, or architecture-altering operations where human judgment is mandatory before executing code mutations or system changes.
- **Characteristics**: Significant blast radius, structural impact, ambiguity in user requirements, trade-offs between multiple viable designs.
- **Typical Examples**:
  - Modifying database schemas or external API contracts.
  - Introducing new external libraries or system dependencies.
  - Modifying the core steering files (`AGENTS.md`, `CLAUDE.md`).
  - Proposing Root Cause Analysis (RCA) fixes and verification plans before writing code.
  - Deleting non-isolated or pre-existing code.

### Tier 3: Never Do (Hard Invariants & Inviolable Boundaries)
- **Concept**: Absolute red lines that the agent must never cross under any circumstances.
- **Characteristics**: Security violations, severe anti-patterns, unauthorized system manipulation, deceptive reporting.
- **Typical Examples**:
  - Never commit or log raw API keys, credentials, or secrets.
  - Never propose manual testing when automated tests can verify behavior.
  - Never write custom fallback scripts or use unapproved alternative tools when a documented tool in `SKILL.md` fails (fail-fast rule).
  - Never touch or "clean up" adjacent code or files outside the agreed change scope.
  - Never write project files outside designated workspace boundaries.

---

## 3. Attention Budget Governance

### What is Attention Budget?
Every token in a system prompt or `AGENTS.md` competes for attention during the transformer's self-attention operations. Research indicates:
- **Negative micro-rules have high cognitive cost**: Prohibitive rules like *"Never write more than 3 sentences"* or *"Do not use adjective X"* require the model to perform continuous negative suppression, leading to attention fatigue.
- **Instruction clumping causes rule drift**: When 20+ disparate rules are presented in a flat bulleted list, rules in the middle of the document suffer from recency and primacy biases, resulting in frequent rule violations.

### Conversion Heuristics (Negative to Positive / Tier Compaction)

When reviewing an existing rule file, apply these transformation heuristics:

1. **Convert negative micro-rules into positive defaults (Tier 1)**:
   - *Bad*: "Do not forget to test your code with assertions. Never commit untested code."
   - *Good (Tier 1)*: "Verify all code changes with automated test assertions before marking complete."
2. **Move approval boundaries to Tier 2**:
   - *Bad*: "You are not allowed to decide on architecture or rewrite libraries on your own."
   - *Good (Tier 2)*: "Obtain user approval on proposed architectures, RFCs, and RCA fixes before implementation."
3. **Reserve Tier 3 for non-negotiable invariants**:
   - Limit Tier 3 to 3–5 high-impact, inviolable constraints (e.g. credentials, fail-fast tool enforcement, scope boundaries).
4. **Prune Baseline Aphorisms**:
   - Eliminate common-sense aphorisms that frontier models already know (e.g., "Write clean code", "Don't make hacky fixes", "Be professional").
