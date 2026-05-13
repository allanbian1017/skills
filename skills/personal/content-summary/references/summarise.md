# Content Summarisation Rules

All content summaries produced by ingest skills must follow these quality standards.

## Language

Output in **Traditional Chinese（繁體中文）** unless the user specifies otherwise.

## Quality Standards

- **零幻覺（Zero Hallucination）**：嚴禁引入任何外部知識或進行常識推斷。只說原文有說的話。
- **全面性（Comprehensiveness）**：不可為了過度精簡而犧牲資訊完整度，必須涵蓋來源中的「所有」獨立重點。
- **客觀性（Objectivity）**：保持中立的語氣，不加入任何個人評論、總結性讚美或情緒化字眼。

## Self-Verification

Before outputting the summary, review it as a "審稿專家":

1. Is any key point from the original source missing? If yes, add it.
2. Does the summary contain any term, background knowledge, or inference not present in the source? If yes, remove it immediately.
3. If any part of the source is ambiguous, reflect this honestly (e.g., 「*原文未詳細說明此數據來源*」). Never guess.

## Teaser Detection

If the source content is extremely short (e.g., a newsletter preview with no full article body), flag in `⚠️ 資訊免責聲明`:

> 「此內容為精簡預告版，完整內容需透過原文連結閱讀，摘要僅反映信件中可見的有限資訊。」

Present whatever limited summary is possible. **Do not fabricate missing fields.**
