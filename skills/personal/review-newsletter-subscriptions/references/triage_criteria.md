# 🎯 Newsletter Triage Criteria & Decision Heuristics

This reference document defines the multi-dimensional evaluation criteria used by `review-newsletter-subscriptions` to classify newsletters into actionable triage categories.

---

## 📐 Metrics & Telemetry Definitions

| Metric | Formula | Description | High Quality Threshold | Poor Quality Threshold |
|---|---|---|:---:|:---:|
| **Reports Received ($N$)** | Total files in `reports/Newsletter_YYYY_MM_DD/` | Raw volume of newsletter emails received. | — | — |
| **Reviewed ($R$)** | Count in `data/suggestions_reviewed.md` | Suggestions that passed initial filtering and received human review. | — | — |
| **Accepted ($A$)** | Count of `✅ Accept` | Suggestions approved by the user for implementation or prompts. | — | — |
| **Rejected ($J$)** | Count of `❌ Reject` | Suggestions explicitly turned down by the user. | — | — |
| **Filtered ($F$)** | Count in `data/suggestions_filtered.md` | Suggestions filtered out by Rubric (< 4 pts) or blocked by Hard-Vetoes. | — | — |
| **Acceptance Rate** | $A / R$ (when $R > 0$) | How often reviewed suggestions from this source are approved. | $\ge 60\%$ | $< 40\%$ |
| **Overall Yield** | $A / N$ (when $N > 0$) | Conversion efficiency: how many accepted actions per email received. | $\ge 20\%$ | $< 8\%$ |

---

## 🚦 The 4 Triage Categories

### 1. 🟢 Keep (繼續訂閱)

High-signal publications that deliver actionable, high-ROI engineering ideas, prompt templates, or career strategies.

**Quantitative Criteria**:
- Acceptance Rate $\ge 60\%$ with $R \ge 2$, OR
- Overall Yield $\ge 20\%$.

**Qualitative Indicators**:
- Suggestions result in accepted pull requests, new agent skills (e.g. `agent-rules-reviewer`, `decision-sparring`), or core prompt library updates (`data/prompts/`).
- Minimal marketing clutter or paywalled teasers.
- Low volume with very high punchiness (e.g. 朱騏, Ally Hsieh).

---

### 2. 🔴 Unsubscribe (建議取消訂閱)

High-noise or misaligned publications that consistently generate rejected proposals, trigger user-defined hard vetoes, or offer little practical value.

**Quantitative Criteria (Triggers on ANY)**:
1. **Low Acceptance**: $R \ge 3$ and Acceptance Rate $< 40\%$.
2. **Zero Acceptance with Prior Reviews**: $R \ge 2$ and $A = 0$.
3. **High Veto Ratio**: $F \ge 4$ and Overall Yield $< 8\%$, or $F \ge 3$ and $F / (R + F) \ge 50\%$ with Acceptance Rate $< 50\%$.
4. **Volume Fatigue with Negligible Yield**: $N \ge 10$ and Overall Yield $< 8\%$ with Acceptance Rate $< 60\%$.

**Qualitative Indicators**:
- **Hard-Veto Violations**: Frequently hits user blocklists (e.g., Hugging Face Daily Papers triggering "Paper reading tasks / 論文研讀", Gary Chen triggering "Claude Code / Cursor").
- **Paywall / Teaser Clutter**: Emails that only provide brief summaries while locking all actionable prompts or architecture diagrams behind paid tiers (e.g., Patreon, Substack paid).
- **Theoretical Interview Prep vs. Engineering Practice**: High-level, abstract diagrams or course advertisements without hands-on applicability to the current workflow (e.g., ByteByteGo, System Design One).

---

### 3. 🟡 Adjust / Filter (調整過濾規則)

Publications that provide valuable core technical content, but also distribute noisy sub-topics (such as weekend specials, robotics/hardware news, or promotional broadcasts) that can be cleanly separated via Gmail filters.

**Quantitative Criteria**:
- High Volume ($N \ge 15$),
- Accepted Suggestions ($A \ge 2$), AND
- Noticeable Filtered Noise ($F \ge 3$ or Acceptance Rate between $40\% \sim 60\%$).

**Action Strategy**:
- Do **not** unsubscribe from the entire sender.
- Propose exact Gmail filter rules (e.g., `from:superhuman subject:"Sunday Special" -> Skip Inbox, Archive`) to strip out known noise categories while preserving high-signal weekday editions.

---

### 4. ⚪ Watch (持續觀察)

Low-sample publications ($N < 5$ or $R < 2$) without strong negative signals, or publications with valuable suggestions currently pending user review.

**Action Strategy**:
- Keep subscribed for another 30-day evaluation cycle until sample size reaches statistical significance.
