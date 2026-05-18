# Content Summarisation Rules

All content summaries produced by ingest skills must follow these quality standards.

## Language

Output in **Traditional Chinese（繁體中文）** unless the user specifies otherwise.

## Quality Standards (Two-Zone Rule)

The report is divided into two distinct zones to balance strict factual extraction with deep synthesis:

| Zone | Sections | Rule |
|---|---|---|
| **Zone 1: Extraction** | 核心總結, 關鍵重點, Layers 2–3 | **Zero Hallucination**: Only source-faithful facts. No external knowledge or inference. |
| **Zone 2: Synthesis** | Layers 4–7 | **Grounded Inference**: Inference allowed based on Zone 1 facts. Read `data/goals.md` to ground relevance in user priorities. No external facts. |

- **全面性（Comprehensiveness）**：不可為了過度精簡而犧牲資訊完整度，必須涵蓋來源中的「所有」獨立重點。
- **客觀性（Objectivity）**：保持中立的語氣，不加入任何個人評論、總結性讚美或情緒化字眼。

## 7 Layers of Learning Framework

Each report must follow the 7 layers of learning framework to transform information into knowledge. Each layer heading is fixed, but the content beneath is free-form. Use the following guiding questions:

**Layer 1 — Core Idea** (in `📝 核心總結`):
- What's the central claim? Why does this matter? What's the underlying principle?
- Quality bar: thesis-level, not surface description.
  - ❌ "AI agents are trending."
  - ✅ "LLMs become dramatically more useful when combined with memory + tools + feedback loops."

**Layer 2 — Signal vs Noise**:
- Durable or hype? Apply the 3-year test. Paradigm shift or local optimization?
- Does this change economics, workflows, or incentives?

**Layer 3 — Mechanism Understanding**:
- Why does this happen? What are the inputs, outputs, constraints?
- What tradeoffs exist? What breaks this model?
- Quality bar: causality, not conclusions.
  - ❌ "RAG improves performance."
  - ✅ "RAG offloads knowledge retrieval from transformer attention into external retrieval systems, reducing context pressure and improving freshness."

**Layer 4 — Personal Relevance** (Zone 2):
- Read `data/goals.md` (or equivalent context). Where does this intersect with current work?
- Does this solve a current pain point? Reveal a new opportunity?

**Layer 5 — Actionability** (Zone 2):
- What experiment can I run? What should I try this week?
- Must be concrete and time-bounded. No "研究看看" allowed.

**Layer 6 — Idea Generation** (Zone 2):
- What does this remind me of? What can this combine with?
- What industries are still not using this? New project ideas triggered?

**Layer 7 — Reflection & Prediction** (Zone 2):
- Second-order effects? Who benefits, who loses?
- What becomes more valuable? What becomes obsolete?

All 7 layers always present. Low-signal sources produce terse layers (1–2 lines each), not empty ones.

## Self-Verification

Before outputting the summary, review it as a "審稿專家":

1. Is any key point from the original source missing? If yes, add it.
2. Does the summary contain any term, background knowledge, or inference not present in the source? If yes, remove it immediately.
3. If any part of the source is ambiguous, reflect this honestly (e.g., 「*原文未詳細說明此數據來源*」). Never guess.

## Teaser Detection

If the source content is extremely short (e.g., a newsletter preview with no full article body), flag in `⚠️ 資訊免責聲明`:

> 「此內容為精簡預告版，完整內容需透過原文連結閱讀，摘要僅反映信件中可見的有限資訊。」

Present whatever limited summary is possible. **Do not fabricate missing fields.**
