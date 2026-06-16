---
name: ingest-newsletter
description: 抓取未讀電子報並產出 Markdown 摘要報表（On-Demand Newsletter Summary）。使用 gws-gmail 技能讀取所有標記為 `label:newsletter is:unread` 的未讀信件，以批次方式逐封分析並依設定之輸出語言（預設為英文）產出 Markdown 摘要，儲存至 `./reports/Newsletter_YYYY_MM_DD/` 目錄，最後將信件標記為已讀並封存。當使用者說「幫我整理電子報」、「摘要電子報」、「處理未讀電子報」、「newsletter summary」、「讀取電子報」、「newsletter 摘要」，或任何需要從 Gmail 擷取並摘要電子報的情境，請務必使用此技能。
---

# ingest-newsletter

抓取未讀電子報、產出 Markdown 摘要、更新信件狀態。此流程需「反覆迭代」直到所有未讀信件皆被處理完畢。

> **前置需求**：確認已可使用 `gws` CLI（透過 `gws-gmail` 技能）。如需驗證或全域旗標，先閱讀 `../gws-shared/SKILL.md`。

---

## 步驟 1：讀取未讀的電子報（批次處理）

搜尋條件：`label:newsletter is:unread`。每次抓取最新的 **10 封**。

```bash
gws gmail users messages list --params '{"userId": "me", "q": "label:newsletter is:unread", "maxResults": 10}'
```

⚠️ 若沒有找到任何未讀信件，跳至「步驟 3」產出最終摘要。

---

## 步驟 2：分析與摘要模式

### 2-1. 讀取信件標頭與內文

```bash
gws gmail +read --id [MESSAGE_ID] --headers --html
```

**標頭完整性檢查**：`From` 與 `Subject` 為必要欄位。若被截斷，重新嘗試確保完整擷取。

### 2-2. 執行摘要

> 📄 Read `../content-summary/references/summarise.md`

針對每封信件獨立產生完整摘要。同一批次多封信件必須**逐一**處理，不可合併。

### 2-3. 摘要輸出格式

> 📄 Read `../content-summary/references/output_template.md`

### 2-4. 寫入報表檔案

> 📄 Read `../content-summary/references/filename_rules.md`

每封電子報獨立寫入一個 Markdown 檔案。確認檔案寫入成功後再繼續。

### 2-4b. 產生 AI 分析並追加至待審清單

> 📄 Read `../content-summary/references/ai_analysis.md`

> 📄 Follow `../content-summary/references/suggestion_log.md`

`{SourceType}` = `Newsletter`

### 2-5. 標記為已讀並封存

```bash
gws gmail users messages modify --params '{"userId": "me", "id": "[MESSAGE_ID]"}' --json '{"removeLabelIds": ["UNREAD", "INBOX"]}'
```

⚠️ 確認摘要檔案已成功產出後才標記為已讀。

### 2-6. 繼續下一批次

重複「步驟 1」直到無未讀信件。

---

## 步驟 3：最終報告

任務完成後，在對話框中報告：
- 本次共處理幾封電子報
- 結果檔案所在路徑（`./reports/Newsletter_YYYY_MM_DD/`）

---

## 💡 GWS CLI 指令速查

| 操作 | 指令 |
|------|------|
| 搜尋未讀電子報 ID | `gws gmail users messages list --params '{"userId": "me", "q": "label:newsletter is:unread", "maxResults": 10}'` |
| 讀取信件內文與標頭 | `gws gmail +read --id [MESSAGE_ID] --headers` |
| 標記已讀並封存 | `gws gmail users messages modify --params '{"userId": "me", "id": "[MESSAGE_ID]"}' --json '{"removeLabelIds": ["UNREAD", "INBOX"]}'` |
