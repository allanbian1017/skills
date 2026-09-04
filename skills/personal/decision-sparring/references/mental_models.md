# 9 Decision Mental Models & Sparring Heuristics

This reference details the 9 mental models (synthesized from Nicolas Cole & 朱騏) used to stress-test decisions, break analysis paralysis, and dismantle procrastination.

---

## 1. The 9 Mental Models

### 1. Bottleneck Analysis (瓶頸分析)
* **Core Premise**: Every system or decision has exactly one primary rate-limiting constraint (Theory of Constraints). Agonizing over non-bottlenecks is procrastination in disguise.
* **Diagnostic Question**: *"If you removed all other friction, what is the single factor that actually prevents this from moving forward today?"*
* **Cognitive Bias Fixed**: Confusing symptoms with causes (e.g., believing you lack time when you actually dread setting up an unfamiliar tool).

### 2. Inverting the Question (反轉問題)
* **Core Premise**: Borrowed from Carl Jacobi and Charlie Munger: *"Invert, always invert."* Instead of asking how to succeed, ask what actions or choices guarantee catastrophic failure, then avoid them.
* **Diagnostic Question**: *"What specific action or oversight would guarantee that this decision blows up in your face?"*
* **Cognitive Bias Fixed**: Confirmation bias and unrealistic optimism.

### 3. New Information Test (關鍵新資訊)
* **Core Premise**: Decisions stall when we wait for "more information" indefinitely. If no realistic new piece of data would change your mind, further delay is pure friction.
* **Diagnostic Question**: *"What specific, obtainable fact would cause you to reverse your current leaning? If none exists, why aren't you deciding right now?"*
* **Cognitive Bias Fixed**: Information-gathering addiction / analysis paralysis.

### 4. Value Relative to Time (時間相對價值)
* **Core Premise**: Jeff Bezos's One-Way Door vs. Two-Way Door framework. Low-cost, easily reversible decisions should be made quickly with 70% information. The cognitive cost of delaying exceeds the cost of a mistake.
* **Diagnostic Question**: *"If you make this choice and it turns out wrong, how many minutes or dollars does it take to undo? If it's easily reversible, why is this taking more than 15 minutes?"*
* **Cognitive Bias Fixed**: Treating reversible two-way doors as high-stakes irreversible catastrophes.

### 5. Regret Minimization (後悔最小化)
* **Core Premise**: Project your perspective forward to age 80. Look back and evaluate which path leaves the deepest regret: trying and failing, or never attempting it at all?
* **Diagnostic Question**: *"When you look back on this season of your life at age 80, which outcome will you regret more: the pain of attempting this and failing, or the silence of never having tried?"*
* **Cognitive Bias Fixed**: Short-term social discomfort and risk aversion over long-term fulfillment.

### 6. Hell Yeah or No (絕對肯定律)
* **Core Premise**: Derek Sivers's filter. When overwhelmed by commitments or opportunities, if an option does not evoke an immediate, visceral *"Hell Yeah!"*, the answer is an automatic **NO**.
* **Diagnostic Question**: *"Does the thought of doing this right now give you genuine energy, or does it feel like an obligation you are rationalizing? If it's not a Hell Yeah, why isn't it a No?"*
* **Cognitive Bias Fixed**: People-pleasing, FOMO, and attention fragmentation.

### 7. Buying Optionality (購買選擇權)
* **Core Premise**: You do not have to make an all-or-nothing binary commitment. You can execute a low-cost micro-experiment that "buys options" and yields empirical data before deciding fully.
* **Diagnostic Question**: *"What 15-to-30 minute probe or throwaway prototype can you run today that buys you 80% of the clarity without committing you to the full path?"*
* **Cognitive Bias Fixed**: Binary false dilemma (thinking you must choose 0% or 100%).

### 8. Documentary vs. Horror Movie (正向校正)
* **Core Premise**: The human brain is hardwired for threat detection and naturally directs a "horror movie" in your imagination. Actively balance the mental scale by visualizing a sober, matter-of-fact "documentary" of realistic success.
* **Diagnostic Question**: *"Your brain is imagining worst-case disaster scenarios. What does the boring, realistic documentary of this going smoothly actually look like step-by-step?"*
* **Cognitive Bias Fixed**: Catastrophic projection and anxiety-induced hesitation.

### 9. Future-Me Mentorship (未來導師)
* **Core Premise**: Adopt the perspective of your future self (1 year or 3 years out) who has already solved this problem, achieved the milestone, and matured through it.
* **Diagnostic Question**: *"Imagine speaking to the version of you who successfully resolved this 12 months from now. What advice would they give you about what to stop caring about?"*
* **Cognitive Bias Fixed**: Being trapped in the immediate operational weeds and emotional turbulence.

---

## 2. Lens Selection Matrix

Instead of overwhelming the user with all 9 models, select the **top 3–4 most discriminating lenses** based on the dilemma category:

| Dilemma Category | Typical Scenario | Primary Mental Models |
|---|---|---|
| **Technical Architecture & Tooling** | Choosing database, refactoring vs. new feature, library selection | 1. Bottleneck Analysis<br>2. Inverting the Question<br>3. Value Relative to Time<br>4. Buying Optionality |
| **Procrastination & Avoidance** | Putting off an ADR, delaying a difficult email, stalling on a task | 1. Bottleneck Analysis<br>2. Documentary vs. Horror<br>3. Value Relative to Time<br>4. Future-Me Mentorship |
| **Shiny Opportunities & Commitments** | Side projects, hackathons, invites, tool-hopping | 1. Hell Yeah or No<br>2. Regret Minimization<br>3. Inverting the Question<br>4. New Information Test |
| **Career & High-Stakes Direction** | Role transition, major portfolio shift, large project bet | 1. Regret Minimization<br>2. Future-Me Mentorship<br>3. Buying Optionality<br>4. New Information Test |

---

## 3. Socratic Sparring Principles

1. **Zero Sycophancy**: Never validate rationalizations or comfort excuses (e.g., *"I'm waiting until I have a full 4-hour block"* $\rightarrow$ challenge: *"You don't need 4 hours; you need 15 minutes to write a 10-line test"*).
2. **Expose Hidden Fears**: Procrastination is almost always an unstated emotional fear (fear of failure, fear of judgment, fear of tricky setup). Uncover it without judgment.
3. **Enforce Decision Velocity**: High-performing builders maximize the velocity of reversible decisions. Fast two-way-door execution always beats slow analysis.
