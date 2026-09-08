# 📬 Newsletter Subscription Audit Template

Standardized structure for rendering the audit artifact (`newsletter_subscription_audit_YYYY-MM-DD.md`).

---

```markdown
# 📬 Newsletter Subscription Audit ({Start_Date} ~ {End_Date})

> **評估摘要**：過去 30 天共追蹤 {Total_Sources} 個電子報來源、{Total_Reports} 篇報告；共產出 {Total_Reviewed} 條審查建議，其中 {Total_Accepted} 條採納、{Total_Rejected} 條拒絕、{Total_Filtered} 條遭規則過濾。

---

## 📊 總體量化數據與轉化評估

{Insert Markdown Table from `analyze_subscriptions.py`}

---

## 🟢 一、建議繼續訂閱（Strong Keep）

此類別具備高接受率（$\ge 60\%$）或高產出率（$\ge 20\%$），內容能直接轉化為專案核心技能、提示詞或重要職涯決策。

### 1. {Source Name}
- **數據指標**：收信 {N} 篇 ｜ 審查 {R} 條 ｜ 接受 {A} 條（接受率 {AccRate}% ｜ 產出率 {YieldRate}%）
- **核心價值與採納實例**：
  - `{Date}` — [{Title}]({URL})：{Suggestion Summary}
- **續訂理由**：{Qualitative explanation connecting content to user's workflow goals}

---

## 🔴 二、建議取消訂閱（Strong Unsubscribe）

此類別存在「高拒絕率（$>60\%$）」、「高規則否決率（$>50\%$）」或「高頻發信但產出率極低（$<8\%$）」，嚴重佔用注意力與信箱空間。

### 1. {Source Name}
- **數據指標**：收信 {N} 篇 ｜ 審查 {R} 條 ｜ 接受 {A} 條 ｜ 拒絕 {J} 條 ｜ 被過濾 {F} 條（接受率 {AccRate}% ｜ 產出率 {YieldRate}%）
- **主要問題**：
  - ❌ {Main issue: e.g. Hard-Vetoed topic, Paywalled teaser, Abstract theoretical diagrams}
  - 🗣️ **使用者歷史反饋**：*「{Rejection Comment}」*
- **建議處置**：
  - **Gmail 搜尋字串**：`{Search Query, e.g. from:example.com}`
  - **執行動作**：搜尋最新一封信件，點擊信尾「Unsubscribe」連結退訂。

---

## 🟡 三、建議保留但設定過濾規則（Adjust & Filter）

此類別核心技術內容具價值，但混雜了高頻且無關的子主題（如週末科普、實體機器人、純廣告）。建議保留訂閱，但透過 Gmail 篩選器排除雜訊。

### 1. {Source Name}
- **數據指標**：收信 {N} 篇 ｜ 審查 {R} 條 ｜ 接受 {A} 條 ｜ 被過濾 {F} 條
- **雜訊分析**：{Describe specific noise sub-topics, e.g. Sunday specials, robotics, bullet trains}
- **建議 Gmail 篩選器規則**：
  - **條件 (Matches)**：`from:{sender} {noise_keywords}`
  - **動作 (Do this)**：`Skip Inbox, Mark as read (或套用獨立低優先標籤)`

---

## ⚪ 四、持續觀察（Watch & Low Sample）

收信量較少或尚有未審查項目，暫維持現狀觀察下一週期。

- **{Source Name}**：收信 {N} 篇，{Reviewed_Summary}。

---

## ✅ 人工操作確認清單（Action Checklist）

- [ ] 在 Gmail 中搜尋退訂名單並執行退訂：
  - [ ] `{Source 1}`：`from:...`
  - [ ] `{Source 2}`：`from:...`
- [ ] 在 Gmail 中建立調整過濾規則：
  - [ ] `{Source 1}`：`from:...`
```
