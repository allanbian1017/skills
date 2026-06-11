---
name: review-suggestions
description: "Review pending AI suggestions from processed reports. Presents unreviewed suggestions as an artifact, collects Accept/Reject feedback, and updates the user preference profile. Use when the user says 'review my suggestions', '幫我看建議', 'check my suggestions', 'review AI suggestions', or any request to review AI analysis recommendations."
---

# review-suggestions

Review pending AI suggestions, collect feedback, and update the user preference profile to calibrate future AI analysis.

---

## Step 1 — Load pending suggestions

Read `data/suggestions_pending.md`.

If the file doesn't exist or contains no suggestion entries (only the heading), tell the user:

> "No pending suggestions. All caught up! 🎉"

And stop.

---

## Step 2 — Split into two groups

Parse each suggestion entry (each starts with `### `) and split by date:

- **Today's suggestions**: entries where the date field matches today's local date
- **Backlog**: all other entries, sorted newest first

---

## Step 3 — Present as artifact

Create an artifact with `RequestFeedback: true`. Number each suggestion sequentially for easy reference.

Support both legacy and new rubric metadata formats dynamically.

Use this format:

```markdown
# 📋 AI Suggestion Review

> 共 {N} 條待審建議 | 今日：{T} 條 | 歷史：{B} 條
>
> 回覆方式：
> - "Accept 1, 3. Reject 2."
> - "#1 accept — 我週末來試. #2 reject — 太抽象"
> - 也可以加上整體偏好，例如："I prefer hands-on tasks under 30 minutes"
> - 不提到的建議會保持待審狀態

---

## 📅 今日建議

### #1 — [Title](source_url)
- 📂 Newsletter | 🏷️ 技術 | 📊 5/6 (A:2 P:1 G:2)
- 📋 **建議**：在本地使用 pgvector 實作混合查詢流程
- 📄 [完整報告](file:///path/to/report.md)

---

## 📂 歷史待審

### #3 — [Title](source_url)
- 📂 Threads | 🏷️ 技術 | 💎 Mid | ⚡ Mid | 🎯 Store
- 📋 **建議**：將這個觀點加入 learnings/lessons.md
- 📄 [完整報告](file:///path/to/report.md)
```

If there are no today's suggestions, omit the `📅 今日建議` section.
If there is no backlog, omit the `📂 歷史待審` section.

---

## Step 4 — Parse user feedback

Accept natural-language responses. Parse for:

- **Per-suggestion actions**: Match `#N`, suggestion number, or title keywords to Accept/Reject
  - Examples: `"Accept 1, 3. Reject 2."`, `"#1 accept — I'll try this weekend"`, `"All accept except #3"`
- **Free-text comments**: Any text attached to a specific suggestion (after `—` or `:`)
- **Global preference statements**: Unattached declarations about interests or preferences
  - Examples: `"I prefer hands-on tasks"`, `"不要再推薦閱讀論文類的建議"`

Suggestions **not mentioned** in the user's response remain in `suggestions_pending.md`.

---

## Step 5 — Update both files

For each suggestion the user provided feedback on:

1. **Append** to `data/suggestions_reviewed.md` — the original suggestion entry plus feedback:

```markdown
---

### 2026-05-07 | Newsletter | [Title](source_url)
- 🏷️ 技術 | 📊 5/6 (A:2 P:1 G:2)
- 📋 建議：在本地使用 pgvector 實作混合查詢流程
- 📄 [報告](file:///path/to/report.md)
- **Feedback**: ✅ Accept
- **Comment**: 我週末來試 pgvector
- **Reviewed**: 2026-05-07T14:00:00+08:00
```

*(Note: Legacy entries are appended keeping their original `💎 | ⚡ | 🎯` fields.)*

2. **Rewrite** `data/suggestions_pending.md` — keep only the entries the user did NOT provide feedback on. Preserve the `# 📋 Pending Suggestions` heading.

---

## Step 6 — Regenerate preference profile

Read the full `data/suggestions_reviewed.md` and existing `data/user_preferences.md` (if any).

Analyze **all** reviewed entries to produce the updated preference profile. Write to `data/user_preferences.md` with the following structure:

### 6-1. Summary Statistics

Count total reviewed, accept count/rate, reject count/rate.

### 6-2. Topic Preferences (recency-weighted)

- Compute accept rate per topic/category
- **Recency weighting**: entries from the last 14 days count at 2× weight
- **High interest**: accept rate > 60%
- **Low interest**: accept rate < 40%

### 6-3. Action Type Preferences

- Cluster `建議` texts by action type (e.g., "implement prototype", "add to AGENTS.md", "test tool", "read article")
- Identify which types the user consistently accepts vs. rejects

### 6-4. Shifting Interests (Conflict Detection)

- For each topic, compare the last-14-day accept rate vs. all-time accept rate
- If the delta exceeds 30%, flag it as a shifting interest with both rates shown
- This prevents stale preferences from overriding recent behavior

### 6-5. Explicit Preferences

- Collect all free-text comments and global preference statements
- More recent explicit statements **override** older conflicting ones
- Present as a bullet list of active preference declarations

### Conflict Resolution Rules

1. **Recency wins**: If recent (14-day) data contradicts older data, recent data takes precedence
2. **Explicit overrides statistical**: A direct user statement always overrides pattern-based inference
3. **Transparent flagging**: Never silently resolve conflicts — always note them in "Shifting Interests"

### Output Format

```markdown
# User Preference Profile

> Last updated: YYYY-MM-DD | Based on {N} reviewed suggestions

## Summary Statistics
- Total reviewed: {N}
- Accept: {A} ({A%}) | Reject: {R} ({R%})

## Topic Preferences
### High Interest (accept rate > 60%)
- [topic 1]
- [topic 2]

### Low Interest (accept rate < 40%)
- [topic 1]

## Action Type Preferences
### Preferred (user acts on these)
- [action type 1]

### Avoided (user rejects these)
- [action type 1]

## Shifting Interests
- [topic]: all-time {A}% → last 14 days {B}%. Treating as {level}.

## Explicit Preferences
- [direct user statement 1]
- [direct user statement 2]
```

### 6-6. Auto-Maintenance & Calibration

After writing `data/user_preferences.md`, invoke the `rubric-grader` skill in **Maintain mode** to perform blocklist verification and threshold score calibration.

---

## Step 7 — Confirm to user

Report the results:

> "✅ Reviewed {N} suggestions ({A} accepted, {R} rejected). Preference profile updated."

---

## Summary

| Step | Action | File(s) Affected |
|---|---|---|
| 1 | Load pending | `data/suggestions_pending.md` (read) |
| 2 | Split today vs. backlog | — |
| 3 | Present artifact | Antigravity artifact |
| 4 | Parse feedback | — |
| 5 | Update files | `suggestions_pending.md` (rewrite), `suggestions_reviewed.md` (append) |
| 6 | Regenerate profile | `suggestions_reviewed.md` (read), `user_preferences.md` (write), invokes `rubric-grader` (maintain) |
| 7 | Confirm | — |
