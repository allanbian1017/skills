# 🥋 `decision-sparring` Skill

> A Socratic sparring partner that stress-tests difficult decisions, eliminates cognitive biases, resolves analysis paralysis, and dismantles procrastination using Nicolas Cole's 9 Decision Mental Models.

---

## 📖 Overview

`decision-sparring` is an autonomous cognitive advisory skill designed for software engineers, architects, and knowledge workers. Whenever you find yourself hesitating between technical paths, dreading a high-friction task, or over-analyzing a project bet, this skill acts as a relentless Socratic sparring partner. 

Unlike standard LLM interactions that offer polite, sycophantic lists of pros and cons, `decision-sparring` actively exposes your hidden operational bottlenecks, challenges comforting rationalizations, and forces concrete resolution through an actionable **4-Part Decision Action Contract**.

---

## 🎯 Problem Statement

When faced with ambiguity, builders frequently succumb to three cognitive traps:

1. **The Analysis Paralysis Trap**: Deliberating for days over easily reversible technical choices (e.g., SQLite vs. DuckDB for small logs). Standard LLMs exacerbate this by providing wishy-washy *"It depends on your needs"* responses that fail to force a decision.
2. **The Procrastination Disguise**: Delaying important tasks (e.g., writing an ADR or refactoring a module) under the rationalization of *"I need a quiet 4-hour uninterrupted block,"* when the true underlying blocker is an unstated fear of failure or API friction.
3. **The Open-Loop Trap**: Running a quick experiment or spike without pre-committed success/reversal criteria, leading straight back into post-test hesitation and decision drift.

---

## 🧠 The 9 Decision Mental Models

Synthesized from Nicolas Cole and 朱騏, `decision-sparring` operationalizes 9 structured lenses:

| # | Mental Model | Core Question | Cognitive Bias Dismantled |
|---|---|---|---|
| **1** | **Bottleneck Analysis (瓶頸分析)** | *"What is the single factor actually blocking execution today?"* | Confusing surface symptoms with root constraints |
| **2** | **Inverting the Question (反轉問題)** | *"What specific choices guarantee this will blow up in your face?"* | Confirmation bias & blind optimism |
| **3** | **New Information Test (關鍵新資訊)** | *"What realistic datum would flip your call? If none, decide now."* | Information-gathering addiction |
| **4** | **Value Relative to Time (時間相對價值)** | *"If this two-way door takes < 15 mins to undo, why debate it for days?"* | Treating reversible doors as catastrophic one-way doors |
| **5** | **Regret Minimization (後悔最小化)** | *"At age 80, will you regret attempting and failing, or never trying?"* | Short-term social discomfort & status anxiety |
| **6** | **Hell Yeah or No (絕對肯定律)** | *"Does this spark genuine energy? If it's not a Hell Yeah, it's a NO."* | People-pleasing & FOMO commitments |
| **7** | **Buying Optionality (購買選擇權)** | *"What 15-minute throwaway probe buys 80% clarity without committing?"* | Binary false dilemmas (all-or-nothing thinking) |
| **8** | **Documentary vs. Horror (正向校正)** | *"What does the boring, matter-of-fact reality of success look like?"* | Worst-case catastrophic projection |
| **9** | **Future-Me Mentorship (未來導師)** | *"What would 1-year-future you tell you to stop caring about?"* | Myopic focus on operational weeds |

---

## 🏗️ Execution Architecture & Workflow

The skill follows an **Adaptive Hybrid Lifecycle** with progressive rendering:

```mermaid
graph TD
    UserPrompt["User Prompt / Decision Dilemma"] --> IntakeCheck{"Phase 1: Input Depth Check"}
    IntakeCheck -->|Sparse / Vague (1-2 sentences)| DiagnosticQ["Ask Exactly 1 Diagnostic Question in Chat"]
    DiagnosticQ --> UserClarification["User Clarifies Blocker"]
    UserClarification --> LensSelect
    IntakeCheck -->|Rich Context / Quick Request| LensSelect["Phase 2: Screen 9 Models & Pick Top 3-4 Lenses"]
    
    LensSelect --> InlineSparring["Phase 3: Socratic Sparring Inline in Chat<br/>• Zero Sycophancy<br/>• Unmask Real Bottleneck vs Surface Excuse"]
    InlineSparring --> FinalContract["Phase 4: Render 4-Part Action Contract as Dedicated Artifact<br/>(decision_contract.md)"]
    FinalContract --> OptionalPersist["Optional: Offer Save to docs/decisions/YYYY-MM-DD_slug.md"]
```

### The 4 Phases

1. **Phase 1: Input Depth Check**:
   - If the prompt is brief or vague, ask **1 high-leverage question** inline in chat to surface the true constraint before offering advice.
   - If rich context is provided, proceed immediately to analysis.
2. **Phase 2: Targeted Lens Selection**:
   - Rather than flooding the user with all 9 models, dynamically filter and display the **top 3–4 most discriminating lenses** matching the problem domain:
     - *Technical Architecture*: Bottleneck + Inversion + Value Relative to Time + Optionality.
     - *Procrastination & Resistance*: Bottleneck + Documentary vs. Horror + Value Relative to Time + Future-Me.
     - *Shiny Commitments & Distractions*: Hell Yeah or No + Regret Minimization + Inversion + New Information.
     - *Career & High-Stakes Direction*: Regret Minimization + Future-Me + Optionality + New Information.
3. **Phase 3: Socratic Sparring**:
   - Deliver high-density, no-fluff diagnosis directly in the chat conversation to keep momentum high.
4. **Phase 4: Action Contract Delivery**:
   - Render the finalized decision as a dedicated **Artifact** (`decision_contract.md`) using [assets/action_contract_template.md](assets/action_contract_template.md).

---

## 📋 The 4-Part Action Contract (Format B)

Every concluded sparring session produces a structured contract with four mandatory sections:

```markdown
### 1. 🎯 The Primary Constraint (True Blocker)
- Surface excuse vs. real underlying friction (e.g., fearing unfamiliar API syntax rather than lack of time).

### 2. ⚡ The 15-Minute Micro-Experiment (Two-Way Door Probe)
- An isolated, standalone test taking ≤ 15 minutes that generates empirical data without touching production code.

### 3. 🛑 The Stop List (What to Cease Agonizing Over)
- Specific activities the user is explicitly forbidden from doing (e.g., reading benchmarks, comparing 5 options).

### 4. 🏁 Decision Checkpoint (Go / No-Go Rules)
- A concrete evaluation deadline (e.g., "Today at 5:00 PM") with binary conditional rules:
  - If the micro-experiment succeeds → GO (commit to next 1-hour milestone).
  - If the micro-experiment hits unexpected friction → NO-GO (kill/defer the topic for 90 days).
```

---

## 🚀 Usage & Triggering

Trigger this skill naturally whenever you face indecision or friction:

### Trigger Phrases
* *"Help me decide on [Option A vs. Option B]"*
* *"Stress-test my decision on [architecture / refactoring]"*
* *"I'm procrastinating on [task / document]"*
* *"Break my analysis paralysis on [feature bet]"*
* *"Decision sparring on [topic]"*
* *"幫我決策 / 猶豫不決"*

### Example Walkthrough

```
User: "I can't decide whether to migrate our local data storage to a new vector database 
       (like LanceDB) or stick with SQLite. I've been hesitating for a week."

Agent: [Runs Phase 2 & 3 inline in chat]
       - Bottleneck: You aren't actually blocked by SQLite speed; you dread the friction 
         of learning a new database API and debugging migration scripts.
       - Time-Value: This is a reversible two-way door. Spending 7 days debating it cost 
         more attention than writing the migration.
       - Optionality: You don't need a full migration; you need a 20-line test script.

       [Phase 4: Renders Artifact `decision_contract.md`]
       1. Primary Constraint: Setup friction fear, not performance.
       2. 15-Min Micro-Experiment: Standalone Python script inserting 10 dummy rows in LanceDB.
       3. Stop List: Stop reading online vector DB benchmarks.
       4. Decision Checkpoint: Today at 5:00 PM: If script runs in < 15 mins → GO; if errors occur → NO-GO.
```

---

## 🏛️ Architecture Decision Records (ADRs)

The design of `decision-sparring` was rigorously stress-tested through `/grill-me`. The resulting decisions are recorded below:

| ADR | Title | Decision Summary | Status | Key Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **[ADR-0001](#adr-0001-operational-scope--boundary-vs-grill-me)** | Operational Scope & Boundary | Covers both engineering trade-offs and personal/career dilemmas | Accepted | Single sparring partner for all analysis paralysis, distinguished from `/grill-me` by cognitive state. |
| **[ADR-0002](#adr-0002-adaptive-hybrid-cadence-sparse-vs-rich-input)** | Adaptive Hybrid Cadence | 1 diagnostic question if sparse; direct contract if rich context | Accepted | Prevents interrogation fatigue while preventing blind hallucination of hidden constraints. |
| **[ADR-0003](#adr-0003-targeted-top-34-lenses-vs-mandatory-9-model-grid)** | Targeted Top 3–4 Lenses | Screen all 9 models internally; surface only top 3–4 discriminating lenses | Accepted | Maximizes token and signal density; removes irrelevant analogies. |
| **[ADR-0004](#adr-0004-progressive-delivery-in-chat-sparring-to-final-artifact)** | Progressive Delivery | In-chat dialogue during sparring → final contract as an Artifact | Accepted | Keeps conversational momentum fast; gives permanent, clean UI for final action plan. |
| **[ADR-0005](#adr-0005-4-part-action-contract-with-gono-go-decision-checkpoints)** | 4-Part Contract Structure | Mandatory Decision Checkpoint with concrete deadline and Go / No-Go rules | Accepted | Closes the decision loop; prevents post-experiment drift back into hesitation. |
| **[ADR-0006](#adr-0006-zero-script-pure-markdown-architecture)** | Zero-Script Pure Markdown | Pure prompt Lean Spine (< 100 lines) with zero bespoke Python/CLI scripts | Accepted | Eliminates maintenance debt and external runtime dependencies. |

---

### ADR-0001: Operational Scope & Boundary vs. `/grill-me`

* **Status**: Accepted
* **Date**: 2026-09-04
* **Deciders**: User & Antigravity Agent

#### Context
The user already has `/grill-me` installed, which interviews users about technical implementation plans and architectures. We needed to establish a distinct operational scope for `decision-sparring` without confusing triggering overlap.

#### Considered Options
1. *Personal & career dilemmas only* (excluding all engineering topics).
2. *Engineering technical trade-offs only*.
3. *Unified cognitive boundary*: Handle personal dilemmas, career prioritization, and engineering trade-offs, distinguished strictly by user cognitive state.

#### Decision
Adopt **Option 3**: `decision-sparring` triggers when the user is in **analysis paralysis, hesitation, or procrastination** between competing options or dreading a task. `/grill-me` remains dedicated to stress-testing an already drafted specification or architecture plan down every branch of the design tree.

#### Consequences
* **Positive**: High flexibility; gives the user a single sparring partner for breaking deadlocks whether they are technical (DB choice) or personal (side projects).
* **Negative**: Prompt descriptions must be pushy and explicit about the cognitive triggers to prevent undertriggering.

---

### ADR-0002: Adaptive Hybrid Cadence (Sparse vs. Rich Input)

* **Status**: Accepted
* **Date**: 2026-09-04
* **Deciders**: User & Antigravity Agent

#### Context
When users seek decision advice, their initial prompts vary from brief 1-sentence complaints (*"I'm procrastinating on X"*) to multi-paragraph contextual breakdowns.

#### Considered Options
1. *Strict multi-turn Socratic interview* (always ask 2–3 questions before giving an answer).
2. *Strict one-shot* (always deliver the full contract on turn 1).
3. *Adaptive Hybrid*: Single high-leverage question if sparse; direct contract if rich.

#### Decision
Adopt **Option 3 (Adaptive Hybrid)**. If the input is sparse, ask exactly **1 sharp diagnostic question** to locate the hidden constraint. If the input is rich or explicitly requests a rapid verdict, proceed directly to analysis and contract delivery.

#### Consequences
* **Positive**: Prevents interrogation fatigue when the user has already provided rich context, while preventing blind hallucinations when context is missing.
* **Negative**: Requires agent discipline to avoid asking more than one question in the sparse branch.

---

### ADR-0003: Targeted Top 3–4 Lenses vs. Mandatory 9-Model Grid

* **Status**: Accepted
* **Date**: 2026-09-04
* **Deciders**: User & Antigravity Agent

#### Context
The underlying framework contains 9 distinct mental models. Displaying all 9 models on every query dilutes token density and introduces irrelevant analogies (e.g., invoking an "80-year regret horizon" when choosing between Python and Bash).

#### Considered Options
1. *Full 9-model grid on every invocation*.
2. *Targeted top 3–4 lenses selected by dilemma category*.
3. *User-selected single model*.

#### Decision
Adopt **Option 2 (Targeted Top 3–4 Lenses)**. The agent's background reference maintains all 9 models, but the output surfaces only the top 3–4 most discriminating lenses matching the dilemma category using the **Lens Selection Matrix**.

#### Consequences
* **Positive**: Maximizes signal-to-noise ratio; eliminates conversational bloat; focuses attention on the exact friction point.
* **Negative**: User must explicitly ask if they want an exhaustive review of all 9 models.

---

### ADR-0004: Progressive Delivery (In-Chat Sparring to Final Artifact)

* **Status**: Accepted
* **Date**: 2026-09-04
* **Deciders**: User & Antigravity Agent

#### Context
Per user design preferences, comprehensive proposals and review documents belong in Artifacts to avoid chat clutter, but conversational dialogue belongs inline in chat.

#### Considered Options
1. *Inline chat only* (ephemeral, no artifact).
2. *Artifact immediately on turn 1* (tab-switching during dialogue).
3. *Progressive Delivery*: In-chat interactive sparring $\rightarrow$ dedicated Artifact upon reaching the final conclusion.

#### Decision
Adopt **Option 3 (Progressive Delivery)**. Conduct exploration and Socratic diagnosis inline in chat to maintain conversational velocity. Once the decision reaches resolution, render the final 4-part Action Contract as a dedicated Artifact (`decision_contract.md`), with an optional offer to persist it to `docs/decisions/`.

#### Consequences
* **Positive**: Preserves natural chat cadence while giving the user a clean, dedicated UI artifact for the finalized action plan.
* **Negative**: None.

---

### ADR-0005: 4-Part Action Contract with Go/No-Go Decision Checkpoints

* **Status**: Accepted
* **Date**: 2026-09-04
* **Deciders**: User & Antigravity Agent

#### Context
Recommending a 15-minute micro-experiment often leaves the decision loop open: once the experiment finishes, the user still faces indecision regarding whether to adopt or reject.

#### Considered Options
1. *3-Part Contract* (Primary Constraint, 15-Min Micro-Experiment, Stop List).
2. *4-Part Contract* (Adding a Decision Checkpoint with explicit Go / No-Go binary rules).

#### Decision
Adopt **Option 2 (4-Part Contract)**. Every contract must include **Section 4: Decision Checkpoint** defining a specific evaluation deadline and explicit *If-This-Then-That* rules (e.g., if prototype runs smoothly $\rightarrow$ GO; if setup fails $\rightarrow$ NO-GO for 90 days).

#### Consequences
* **Positive**: Completely eliminates post-experiment hesitation; ensures the decision loop closes definitively.
* **Negative**: Requires setting a realistic evaluation deadline.

---

### ADR-0006: Zero-Script Pure Markdown Architecture

* **Status**: Accepted
* **Date**: 2026-09-04
* **Deciders**: User & Antigravity Agent

#### Context
Repository guidelines emphasize *Minimal Code Scope* and the user's explicit preference for *Zero-Script Agent Skill Design* (avoiding bespoke single-use scripts that create maintenance debt).

#### Considered Options
1. *CLI Python helper tool* in `scripts/`.
2. *Pure markdown skill with Lean Spine and bundled references*.

#### Decision
Adopt **Option 2 (Pure Markdown Lean Spine)**. The skill consists exclusively of `SKILL.md` (90 lines), `references/mental_models.md`, `assets/action_contract_template.md`, and `evals/evals.json`.

#### Consequences
* **Positive**: Zero maintenance overhead; zero runtime dependencies; 100% portable across Antigravity and Claude environments.
* **Negative**: Relies entirely on LLM prompt adherence (mitigated by automated `validate_skill.py` and structured evals).

---

## 📂 File Structure

```
decision-sparring/
├── README.md                          # Documentation & Architecture Decision Records (this file)
├── SKILL.md                           # Lean Spine (<100 lines): frontmatter, triggers, execution phases
├── references/
│   └── mental_models.md               # 9 models, diagnostic heuristics, Lens Selection Matrix
├── assets/
│   └── action_contract_template.md    # 4-part contract markdown template with Go/No-Go rules
└── evals/
    └── evals.json                     # Automated evaluation benchmark test cases
```

---

## 🧪 Verification & Quality Gates

* **Skill Frontmatter Validation**:
  ```bash
  python3 scripts/validate_skill.py .agents/skills/decision-sparring/SKILL.md
  ```
* **Structural Assertions**:
  - `SKILL.md` line count: 90 lines (Budget: < 200 lines).
  - All 4 contract sections verified.
  - Zero executable script overhead.
  - All 31 repository skills pass validation.

---

## 📜 Changelog

| Version | Date | Changes |
|---|---|---|
| **v1.0.0** | 2026-09-04 | Initial release of `decision-sparring` skill with 9 Mental Models, Adaptive Hybrid Cadence, Go/No-Go Decision Checkpoints, and ADRs 0001–0006. |
