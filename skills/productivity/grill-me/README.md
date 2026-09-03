# grill-me

A design interview skill that stress-tests plans and architectural decisions through relentless, structured questioning — and **learns your preferences over time** to provide increasingly calibrated recommendations.

## What It Does

When you invoke `/grill-me`, the skill walks through every branch of your design's decision tree, asking one question at a time. For each question, it provides a recommended answer. Over time, those recommendations become personalized based on rationale you've shared in past sessions.

## How It Works

The skill operates in 4 phases per session:

| Phase | What Happens |
|---|---|
| **1. Load Preferences** | Reads `preferences.md` for known user preferences from prior sessions |
| **2. Preference-Aware Questioning** | Interviews you about the plan, biasing recommendations toward known preferences and surfacing contradictions inline |
| **3. Propose Session End** | When all branches are resolved, proposes summarizing learned preferences |
| **4. Batch Learning** | Presents candidate preferences for you to confirm, edit, or reject before persisting |

### Learning Mechanism

The skill captures preferences using **rationale-gating**: only answers where you provide explicit reasoning ("I prefer X **because** Y") are flagged as candidate preferences. One-off plan decisions without rationale are not captured.

When your answer contradicts an existing preference, the skill surfaces it immediately during the session — this is the only time it interrupts the normal interview flow, because your rationale for changing your mind is the most valuable kind of learning.

## Files

| File | Purpose |
|---|---|
| [`SKILL.md`](SKILL.md) | Skill instructions (the 4-phase workflow) |
| [`preferences.md`](preferences.md) | Persistent user preferences (grows over time, human-editable) |

### Preference Entry Format

Each learned preference is stored as:

```markdown
### [Preference Title]
- **Preference**: [What the user prefers]
- **Rationale**: [Why — in the user's own words]
- **Learned**: [Date] — [Session context]
```

Categories are emergent — no predefined structure. The file can be manually edited at any time.

## Usage

```
/grill-me
```

Works in any project. Preferences are stored globally and apply across all projects.

---

## Architecture Decision Records

### ADR-0001: Global-Only Preference Storage

**Status**: Accepted — 2026-09-03

**Context**: The skill needs persistent storage for learned preferences. Options were project-specific (per-repo), global (per-user), or both layers with merge logic. The user concluded that design preferences are personal values that transcend project boundaries — adding a project layer would create merge complexity without clear benefit.

**Decision**: Store preferences globally only.

**Consequences**: Single source of truth with no merge logic. Preferences learned in any project benefit all future projects. Tradeoff: a preference learned in a CLI project context will surface in distributed system sessions — mitigated by ADR-0006 (never skip questions, so the user can always override).

---

### ADR-0002: Rationale-Gated Preference Capture

**Status**: Accepted — 2026-09-03

**Context**: During a grill session, the user gives many answers — some plan-specific ("use Redis here"), others revealing deeper preferences ("I prefer in-memory caches because network hops add latency"). The skill needs a heuristic to distinguish capturable preferences from one-off decisions. Alternatives considered: generality-gating (agent judges if generalizable) and both combined. The user's rationale: "If I explicitly point out my rationale, that's the most important thing I want you to memorize."

**Decision**: Only flag answers as candidate preferences when the user provides explicit rationale. If the user explains "why," that's the signal. Don't infer preferences the user hasn't explicitly reasoned about.

**Consequences**: High precision — captured preferences are always intentional. May miss casually stated preferences, mitigated by the end-of-session confirmation step where the user can add anything missed.

---

### ADR-0003: End-of-Session Batch Learning

**Status**: Accepted — 2026-09-03

**Context**: The skill could capture preferences continuously (acknowledging each one inline) or in a batch at the end. The user saw no benefit from live capture — the grill session's purpose is to reach shared understanding on the plan, and interrupting the flow to confirm preferences breaks the rhythm.

**Decision**: Accumulate candidate preferences silently during the session. Present all candidates as a batch at session end for the user to confirm, edit, or reject. **Exception**: contradictions to existing preferences are surfaced inline (see ADR-0004).

**Consequences**: Uninterrupted interview flow. Clean decision point at the end for reviewing all candidates with full session context.

---

### ADR-0004: Inline Contradiction Surfacing

**Status**: Accepted — 2026-09-03

**Context**: When a user's answer contradicts a stored preference, should this be deferred to the batch phase (consistent with ADR-0003) or surfaced inline? The user explicitly requested inline surfacing — the rationale for why their thinking changed is the most valuable kind of learning, and the contradiction needs resolution immediately because the agent's remaining recommendations depend on which preference is current.

**Decision**: Surface contradictions inline immediately: "You previously said [X] because [Y]. Now you're saying [Z]. What changed?" This is the **only** exception to the batch learning rule.

**Consequences**: Captures the highest-value learning (evolution of thinking with rationale). Ensures the agent's remaining recommendations stay calibrated. Breaks the batch-only rule, but the interruption is lightweight and directly relevant to the current question.

---

### ADR-0005: Emergent Categories Over Predefined Structure

**Status**: Accepted — 2026-09-03

**Context**: The `preferences.md` file needs organizational structure as it grows. Options were predefined categories (Architecture & Design, Code Style, Process, Tradeoffs) or emergent categories (flat list, reorganize later). The user's rationale: "I don't have a predefined category in mind, and it should be very different when it comes to different projects and for different kinds of plans."

**Decision**: Start with a flat list. Reorganize into natural groupings only after enough real preferences accumulate to reveal patterns.

**Consequences**: No cognitive overhead during confirmation. Categories emerge from real data, not assumptions. File may feel unorganized with 10+ entries, but entries are self-contained and scannable.

---

### ADR-0006: Bias Recommendations, Don't Skip Questions

**Status**: Accepted — 2026-09-03

**Context**: When the skill loads known preferences, it could skip questions already answered, bias recommendations to align with preferences, or actively challenge old preferences. The user wanted the preference shown as the recommended option but still wants to double-check whether they hold the same thought each time.

**Decision**: Bias recommendations toward known preferences — show the preference as the recommended answer ("Based on your preference, I'd recommend X because [your rationale]. Does this still apply here?") — but never skip questions.

**Consequences**: Sessions feel increasingly personalized. User retains full control — overriding a recommendation is a natural signal the preference may need updating. Sessions don't get shorter, which maintains plan scrutiny. Combined with ADR-0001 (global preferences), this ensures cross-project preferences can always be overridden per-context.

---

## Changelog

### v2.0.0 — 2026-09-03

Added persistent learning from user feedback. The skill now captures design preferences with rationale and uses them to calibrate future recommendations.

**Added**:
- 4-phase workflow: Load Preferences → Preference-Aware Questioning → Propose Session End → Batch Learning
- `preferences.md` — persistent, human-editable preference store (global scope)
- Rationale-gated capture — only learns from answers with explicit "because"
- Inline contradiction surfacing — surfaces conflicts with stored preferences during the session
- End-of-session batch confirmation — user reviews all candidate preferences before persisting
- Biased recommendations — known preferences shown as recommended answers, questions never skipped

**Removed**:
- Project-level skill override (`.agents/skills/grill-me/`) — consolidated to global skill only

### v1.0.0 — Pre-2026-09-03

Original skill. Stateless design interview — no learning, no preference persistence. Interviewed the user relentlessly about a plan until reaching shared understanding, one question at a time.
