---
name: newsletter-summary
description: 抓取未讀電子報並產出 Markdown 摘要報表（On-Demand Newsletter Summary）。使用 gws-gmail 技能讀取所有標記為 `label:newsletter is:unread` 的未讀信件，以批次方式逐封分析並產出繁體中文 Markdown 摘要，儲存至 `./reports/Newsletter_YYYY_MM_DD/` 目錄，最後將信件標記為已讀並封存。當使用者說「幫我整理電子報」、「摘要電子報」、「處理未讀電子報」、「newsletter summary」、「讀取電子報」、「newsletter 摘要」，或任何需要從 Gmail 擷取並摘要電子報的情境，請務必使用此技能。
---

# Newsletter Summary 技能

此技能的目標是協助使用者抓取未讀的電子報，由 AI 進行內容摘要，產出 Markdown 報表，並更新信件狀態。此流程需「反覆迭代」直到所有未讀信件皆被處理完畢。

> **前置需求**：使用本技能前，確認已可使用 `gws` CLI（透過 `gws-gmail` 技能）。如需驗證或瞭解全域旗標，請先閱讀 `../gws-shared/SKILL.md`。

---

## 步驟 1：讀取未讀的電子報（批次處理）

- 使用 `gws-gmail` 技能與 `gws` CLI 抓取信件，**不需額外撰寫 Python 腳本**。
- 搜尋條件：`label:newsletter is:unread`。
- 每次抓取最新的 **10 封**信件作為一個批次。

```bash
gws gmail users messages list --params '{"userId": "me", "q": "label:newsletter is:unread", "maxResults": 10}'
```

⚠️ **若沒有找到任何未讀信件**，表示處理已全數完畢，請跳至「步驟 3」產出最終摘要。

---

## 步驟 2：分析與摘要模式

### 2-1. 讀取信件標頭與內文

取得每封信件的完整內容（含 `From`、`Subject` 標頭）：

```bash
# 使用 +read helpers 指令，自動處理 HTML 轉純文字與 Base64 解碼
gws gmail +read --id [MESSAGE_ID] --headers
```

**標頭完整性檢查**：`From` 與 `Subject` 欄位為必要資訊，用於產出正確的「來源」欄位與輸出檔案名稱。若輸出被截斷，請重新嘗試或調整指令以確保擷取完整標頭。

提取信件的標題與「純文字」內文（過濾不必要的 HTML 標籤與雜訊）。

### 2-2. 執行摘要（每封信件獨立處理）

依照以下設定對每封信件進行摘要。若一批次包含多封電子報，請務必**逐一**針對每一封產生**獨立且完整**的摘要，不可合併不同信件的重點。

**摘要系統設定（System Prompt）**：

> 你是一位「高精準電子報摘要專家」。你的核心職責是精確擷取電子報中的所有關鍵資訊，並進行嚴謹的交叉核對，確保產出的摘要 100% 基於原文，絕不產生幻覺或猜測未提供的資訊。

**Instructions**：
1. **全文解析與拆解**：仔細閱讀用戶提供的電子報全文，將內容邏輯拆分為不同的主題區塊。
2. **資訊地毯式擷取**：針對每個區塊，提取核心觀點、重要數據、人名/公司名、日期時間以及任何需要讀者採取行動的項目（Call to Action）。
3. **「內部事實查核」機制（自我驗證）**：在輸出摘要前，以「審稿專家」的視角，將準備輸出的重點與原文進行逐項比對：
   - 是否有任何原文段落的重點被遺漏？如果有，請補上。
   - 摘要中是否有任何原文未提及的詞彙、背景知識或延伸推論？如果有，請立即刪除。
4. **處理模糊或缺失資訊**：如果電子報中的某段資訊語意不清，請在摘要中如實反映（例如標註：「*原文未詳細說明此數據來源*」），切勿自行猜測或腦補。

**Constraints**：
- **零幻覺（Zero Hallucination）**：嚴禁引入任何外部知識或進行常識推斷。只說原文有說的話。
- **全面性（Comprehensiveness）**：不可為了過度精簡而犧牲資訊完整度，必須涵蓋電子報中的「所有」獨立重點。
- **客觀性（Objectivity）**：保持中立的語氣，不加入任何個人評論、總結性讚美或情緒化字眼。
- **語言**：以繁體中文輸出（除非用戶另有要求）。
- **精簡預告偵測（Teaser Detection）**：若電子報的正文字數極少（例如僅為文章摘要預告，缺乏完整內文），請在 `⚠️ 資訊免責聲明` 中明確標示：「此封電子報原文為精簡預告版，完整內容需透過原文連結閱讀，摘要僅反映信件中可見的有限資訊。」並如實呈現有限的摘要，**不需強行補全不存在的欄位**。

### 2-3. 摘要輸出格式

> 📄 完整的輸出格式模板請參閱 `assets/output_template.md`（含欄位說明與檔案命名規則）。

> 🎯 **產生「AI 分析」區塊前，必須遵照 `assets/output_template.md` 中的指示**讀取 `data/goals.md` 與 `data/user_preferences.md`（若存在）。

針對「每一封」電子報，嚴格依照模板格式獨立產生內容。確保每封信件產出**獨立完整**的 Markdown 檔案，不可合併不同信件的重點。

### 2-4. 寫入報表檔案

將本批次中**每一封電子報的摘要獨立寫入一個 Markdown 檔案**，路徑與命名規則見 `assets/output_template.md`。確保保留每個區塊的完整欄位，**寫入時嚴禁省略任何欄位**。

### 2-4b. 追加建議至待審清單

將本封電子報的 AI 分析建議追加至 `data/suggestions_pending.md`。使用以下格式：

```markdown
---

### YYYY-MM-DD | Newsletter | [標題](原文連結)
- 🏷️ {分類} | 💎 {價值評分} | ⚡ {可行動性} | 🎯 {決策建議}
- 📋 建議：{建議下一步}
- 📄 [報告](file:///absolute/path/to/report.md)
```

若 `data/suggestions_pending.md` 不存在，先建立檔案並寫入 `# 📋 Pending Suggestions` 標題。

### 2-5. 標記為已讀並封存

立即將這批信件標記為已讀並封存（同時移除 `UNREAD` 與 `INBOX` 標籤），避免重複抓取並保持收件匣整潔：

```bash
gws gmail users messages modify --params '{"userId": "me", "id": "[MESSAGE_ID]"}' --json '{"removeLabelIds": ["UNREAD", "INBOX"]}'
```

⚠️ **操作安全性**：在標記為已讀前，務必確認已成功產出該信件的摘要檔案。

### 2-6. 繼續下一批次

**重複執行「步驟 1」**，抓取下一批信件進行分析，直到搜尋不到未讀信件為止。

---

## 步驟 3：品質規範與最終報告

### 品質 Guardrails

- **零幻覺保證**：摘要內容必須 100% 取自原始信件內容。若有縮寫或術語原文未解釋，請直接標示原樣。
- **精簡預告處理**：若信件內容明顯僅為全文之一小部分（如 Substack 預告），必須在「免責聲明」中明確告知用戶。
- **操作安全性**：在標記為已讀前，務必確認已成功產出該信件的摘要檔案。

### 最終摘要報告

任務完成後，在對話框中向用戶報告：
- 本次任務共處理了幾封電子報
- 結果檔案所在的資料夾路徑（`./reports/Newsletter_YYYY_MM_DD/`）

---

## 💡 GWS CLI 指令速查

| 操作 | 指令 |
|------|------|
| 搜尋未讀電子報 ID | `gws gmail users messages list --params '{"userId": "me", "q": "label:newsletter is:unread", "maxResults": 10}'` |
| 讀取信件內文與標頭 | `gws gmail +read --id [MESSAGE_ID] --headers` |
| 標記已讀並封存 | `gws gmail users messages modify --params '{"userId": "me", "id": "[MESSAGE_ID]"}' --json '{"removeLabelIds": ["UNREAD", "INBOX"]}'` |

---

> 📋 **Changelog**: See [`docs/workflow/newsletter_summary.md`](../../../docs/workflow/newsletter_summary.md) for the full version history.
