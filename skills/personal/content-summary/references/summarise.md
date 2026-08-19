# Content Summarisation Rules

All content summaries produced by ingest skills must follow these quality standards.

## Language

Check `data/user_preferences.md` for the `Preferred Output Language` configuration under the `## Configuration` section:
- Write all report headers, section titles, summaries, and contents in the configured preferred output language.
- If the configuration is missing, empty, or invalid, default to **English**.

## Quality Standards (Two-Zone Rule)

The report is divided into two distinct zones to balance strict factual extraction with personalized judgement:

| Zone | Sections | Rule |
|---|---|---|
| **Zone A: Extraction** | TL;DR, What Can I Learn From It, Core Thesis, Reasoning Map, Visual Map | **Zero Hallucination**: Only source-faithful facts and author's explicit arguments. No external knowledge or unstated inference. |
| **Zone B: Judgement** | Reading Decision (incl. 💡 真正的新資訊), AI Analysis | **Grounded Inference**: Inference allowed based on Zone A facts. Read `data/goals.md` to ground relevance in user priorities. No external facts. |

- **全面性（Comprehensiveness）**：不可為了過度精簡而犧牲資訊完整度，必須涵蓋來源中的核心論點與關鍵證據。
- **客觀性（Objectivity）**：保持中立的語氣，不加入任何個人評論、總結性讚美或情緒化字眼。

## Thesis-Driven Analysis Guidance

Each report follows the thesis-driven framework to directly answer four core reading questions: "Should I read this?", "What can I learn?", "What's the core argument?", and "How does the author prove it?"

### ⚠️ Internal Reasoning Order vs Visual Output Order (Two-Step CoT)
To preserve zero-hallucination accuracy while serving <5-second triage UX:
1. **Internal CoT Step**: Perform Zone A factual extraction (TL;DR, What Can I Learn From It, Thesis, Reasoning Map) internally first, then synthesize Zone B evaluation against `data/goals.md`.
2. **Visual Output Rendering**: Format the Markdown starting with `## ⭐ Reading Decision` immediately below Metadata, followed by `## 📝 TL;DR`, `## 🧠 What Can I Learn From It`, `## 🎯 Core Thesis`, etc.

---

### 1. ⭐ Reading Decision (Zone B upfront for immediate triage)
回答「**我**（使用者）是否應該讀這篇？」，錨定 `data/goals.md`：

| 星級評估 | 評判標準 (Criteria) |
|---|---|
| ★★★★★ | 突破性新框架 / 新做法，直接對應當前核心目標，必讀 |
| ★★★★☆ | 具高價值新資訊且與目標高度相關，值得全文細讀 |
| ★★★☆☆ | 良好背景知識，無突破性新意，閱讀 TL;DR / 摘要即可 |
| ★★☆☆☆ | 邊緣相關或已知觀念重述，可快速跳過 |
| ★☆☆☆☆ | 無實質新資訊、標題黨或重複內容，建議直接忽略 |

包含子區塊 **💡 真正的新資訊**：標示原文中最具有價值的全新觀念或洞察；若無新意則誠實寫「`主要重新整理已知觀念`」。

### 2. 📝 TL;DR
- 3–5 句話精準概括：說明主題背景、探討的核心問題以及主要結論。

### 3. 🧠 What Can I Learn From It
- 列出 2–5 個從此內容可帶走的核心學習點。
- 每個學習點必須是具體的知識、技能、方法論或洞察，而非模糊的主題描述。
  - ❌ "了解 AI Agent 的發展趨勢"
  - ✅ "LLM Agent 在多步驟任務中需要結構化記憶回放機制才能維持一致性"
- 從讀者視角撰寫：「讀完這篇，我學到了什麼？」
- 此為 Zone A 區塊：僅從原文提取，禁止加入外部推論或個人化建議。
- 每條學習點必須有獨立價值，不可與其他 bullet 重疊。

### 4. 🎯 Core Thesis
- **一句話核心結論**：作者試圖說服讀者接受的最核心主張。
  - 品質要求：必須是命題/主張層級（Thesis-level），而非主題敘述（Topic description）。
  - ❌ "本文章討論了 AI Agent 的發展與應用。"
  - ✅ "LLM Agent 必須結合長期記憶與結構化環境反饋，才能真正替代複雜的多步驟人類工作流程。"
- **支撐論點**：2–3 個直接支持核心結論的主要次要論點。

### 5. 🗺️ Reasoning Map Templates
Agent 根據文章類型自適應選擇一種模板，追蹤作者的**推論邏輯流程**而非段落順序：

| 模板 | 適用文章類型 | 結構說明 |
|---|---|---|
| **Linear Chain** | 研究報告、論述型文章 | Ordered list: 1. → 2. → ... → Conclusion |
| **Parallel Arguments** | 觀點評論、多角度文章 | Core Thesis ← 角度 A + 角度 B + 角度 C |
| **Minimal** | 新聞報導、資訊整理、低訊號文章 | 無推導鏈，直列事實重點 |

**證據類型指引（Evidence Type Guidance）**：撰寫 sub-bullet 時，辨識以下證據類型，優先列出具體證據（Data、Case Study、Quote、Research、Personal Experience）。若該步驟僅有純邏輯推論（Reasoning），可省略 sub-bullet。不需在輸出中標註證據類型名稱。

### 6. 🗺️ Visual Map
- **條件式生成**：僅當 Reading Decision 為 **★★★★☆** 或 **★★★★★** 時才生成 Mermaid 流程圖，放在 Reasoning Map 之後以視覺化推論鏈。
- 若評級為 ★☆☆☆☆ ~ ★★★☆☆，請寫：`*(閱讀決定評級低於 ★★★★☆，省略視覺化圖表)*`

### 7. 🤖 AI Analysis Guidance (Zone B)
保留並提煉原 4-7 層的引導問題，進行個人化分析：

- **個人相關性（Personal Relevance）**：讀取 `data/goals.md`，這與目前的工作有何交集？是否解決了目前的痛點？揭示了新機會？
- **可行動性（Actionability）**：現在可以做什麼？有什麼本週可以測試的實驗？必須具體且有時間限制，嚴禁寫「研究看看」。
- **靈感觸發（Idea Generation）**：這讓我想到什麼？這可以與什麼結合？哪些產業還沒開始用？觸發了什麼新專案想法？
- **反思與預測（Reflection & Prediction）**：二階效應是什麼？誰獲益，誰受損？什麼變得更有價值，什麼被淘汰？

## Self-Verification (6 Checks)

產出摘要前，請以「審稿專家」角色執行 6 項 self-verification：

1. **Core Thesis 是否真的是「一句話」？** 如果超過兩句，必須重寫精簡為單一句子。
2. **Reasoning Map 是否追蹤作者的邏輯流程而非段落順序？** 若只是逐段摘錄，必須重新整理為邏輯推導。
3. **Reading Decision 的星級是否有錨定 goals.md？** 必須根據使用者目標給出專屬評級。
4. **Zone A sections 是否包含任何原文沒有的推論？** 如有，必須移除以確保零幻覺。
5. **若原文模糊或資訊不足，是否誠實標示？** （例如「*原文未詳細說明此數據來源*」），絕不自行補全或猜測。
6. **「What Can I Learn From It」是否為具體學習點而非主題描述？** 每個 bullet 必須是可帶走的知識或洞察，且從讀者視角撰寫。

## Teaser Detection

If the source content is extremely short (e.g., a newsletter preview with no full article body), flag in `⚠️ 資訊免責聲明`:

> 「此內容為精簡預告版，完整內容需透過原文連結閱讀，摘要僅反映信件中可見的有限資訊。」

Present whatever limited summary is possible. **Do not fabricate missing fields.**
