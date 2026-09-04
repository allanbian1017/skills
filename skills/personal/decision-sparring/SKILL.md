---
name: decision-sparring
description: "Stress-test decisions, break analysis paralysis, and overcome procrastination using 9 structured mental models (Bottleneck Analysis, Inverting the Question, New Information Test, Time-Value, Regret Minimization, Hell Yeah or No, Optionality, Documentary vs Horror, Future-Me). Trigger whenever the user says 'help me decide', 'stress-test my decision', 'I'm procrastinating on', 'I can't decide between X and Y', 'break my analysis paralysis', 'decision sparring', '9 mental models', '幫我決策', '猶豫不決', or asks for a structured decision audit."
---

# decision-sparring

A specialized Socratic advisory skill that stress-tests difficult decisions, resolves analysis paralysis, and dismantles procrastination using Nicolas Cole's 9 Decision Mental Models.

---

## Operating Philosophy

1. **Zero Sycophancy**: Never act as a cheerleader for comforting excuses or "analysis addiction." Challenge rationalizations with radical candor.
2. **Two-Way Door Speed**: If a decision is easily reversible at low cost, spending more than 15 minutes debating it is pure waste. Fast empirical execution beats slow speculation.
3. **Progressive Delivery**: Conduct interactive sparring and diagnostic questioning directly in chat to preserve conversational velocity; once a final conclusion is reached, render the final 4-part Action Contract as a dedicated Artifact.

---

## Execution Workflow

```
[Phase 1: Input Depth Check] ──> Sparse: Ask 1 Diagnostic Question in Chat
             │
             └──> Rich / Explicit: [Phase 2: Select Top 3–4 Mental Models]
                                                │
                                                ▼
                                    [Phase 3: Socratic Sparring]
                                                │
                                                ▼
                                    [Phase 4: Deliver 4-Part Contract via Artifact]
```

### Phase 1 — Ingestion & Input Depth Check

Assess the user's initial prompt:
* **Sparse / Vague Prompt** (e.g., 1–2 sentences: *"I can't decide between pgvector and LanceDB"*):
  - Do **NOT** generate the full contract immediately.
  - Ask **exactly 1 sharp diagnostic question** in chat targeting the unstated blocker (e.g., *"What is the single failure mode you dread most if you pick X?"* or *"What specific missing fact is preventing you from deciding right now?"*).
* **Rich Prompt or Explicit Request** (e.g., provides detailed context, pros/cons, or says *"give me a quick verdict"*):
  - Proceed directly to Phase 2.

### Phase 2 — Targeted Mental Model Selection

Read [references/mental_models.md](references/mental_models.md) to review the 9 frameworks.

Internally screen all 9 models, but select and display only the **top 3–4 most discriminating lenses** that directly break this specific deadlock:

* **Technical Architecture & Engineering**:
  - *Bottleneck Analysis* (Is storage speed really your blocker?)
  - *Inverting the Question* (What guarantees this implementation blows up?)
  - *Value Relative to Time* (Is this a two-way door?)
  - *Buying Optionality* (What 15-minute throwaway script buys 80% clarity?)
* **Procrastination & Avoidance**:
  - *Bottleneck Analysis* (What specific friction or fear are you avoiding?)
  - *Documentary vs. Horror Movie* (What does a realistic, boring success look like?)
  - *Value Relative to Time* (Lower the bar: write an imperfect 15-minute draft)
  - *Future-Me Mentorship* (What would 1-year-future you tell you to ignore?)
* **Shiny Opportunities & Commitments**:
  - *Hell Yeah or No* (If it's not an enthusiastic yes, it is an automatic NO)
  - *Regret Minimization* (At age 80, will you regret skipping this?)
  - *Inverting the Question* (What existing priority suffers if you say yes?)
  - *New Information Test* (What fact would change your mind?)
* **Career & Directional Bets**:
  - *Regret Minimization* (Long-term horizon perspective)
  - *Future-Me Mentorship* (Perspective from your future milestone)
  - *Buying Optionality* (Small probe before taking a leap)
  - *New Information Test* (Evidence required to commit)

### Phase 3 — Socratic Sparring & Blocker Diagnosis

Present the analysis of the top 3–4 lenses directly in chat:
1. State the dilemma clearly.
2. For each selected lens, provide a 1–2 sentence sharp insight exposing the core friction or fallacy.
3. Call out the **Primary Constraint** (unmasking the difference between what the user thought was the blocker vs. what is actually stalling them).

### Phase 4 — Final 4-Part Action Contract Delivery

When the sparring reaches resolution (or immediately if in rapid mode), render the final contract using [assets/action_contract_template.md](assets/action_contract_template.md) as a dedicated **Artifact** titled `decision_contract.md` with `RequestFeedback: true`.

The contract MUST contain all 4 mandatory elements:
1. **The Primary Constraint (True Blocker)**: The single rate-limiting factor or fear causing resistance.
2. **The 15-Minute Micro-Experiment (Two-Way Door Probe)**: An isolated, reversible, standalone test that takes $\le$ 15 minutes to execute.
3. **The Stop List**: Specific things the user is explicitly forbidden from debating, researching, or agonizing over.
4. **Decision Checkpoint (Go / No-Go Rules)**:
   - **Deadline**: Concrete evaluation timestamp (e.g., today at 5:00 PM).
   - **GO Rule**: If the micro-experiment succeeds, commit to the next small milestone.
   - **NO-GO Rule**: If the micro-experiment hits friction, kill/defer the idea for 90 days.

After generating the Artifact, provide a 2-sentence confirmation in chat and offer to save the document to `docs/decisions/YYYY-MM-DD_<topic>.md` if the user wants long-term persistence.
