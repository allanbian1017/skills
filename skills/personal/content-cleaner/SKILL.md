---
name: content-cleaner
description: Extracts pure article text from a raw text file, HTML dump, or URL. Use this skill whenever the user asks to clean up content, remove ads/navigation from text, or extract the main article from a noisy source.
---

# Content Cleaner Skill

This skill transforms noisy web content (like raw HTML dumps, messy copy-pastes with JSON/navigation, or URLs) into clean, readable Markdown articles.

## Input Handling
- **If the user provides a URL:** Use the `read_url_content` tool or the `agent-browser` skill to fetch the raw page content.
- **If the user provides raw text or a file:** Read the content directly.

## Cleaning Guidelines
When processing the content, ALWAYS apply the following rules:
1. **Remove Noise:** Strip out all website navigation menus, header/footer links, sidebar content, search bars, and "Log In / Subscribe" prompts.
2. **Remove Ads & Promos:** Exclude all advertisement placeholders (e.g., "廣告-請繼續往下閱讀"), sponsored content blocks, related article links (e.g., "延伸閱讀", "相關文章"), and social media sharing buttons.
3. **Remove Metadata Bloat:** Strip out raw JSON-LD (Schema.org) blocks, raw HTML tags, and unnecessary script code.
4. **Retain Core Information:** Keep the main article title, author name, publication date (if available), and the complete article body. Keep all heading structures within the article body intact.

## Output Format
ALWAYS format the final output as a clean Markdown file. Use this exact template:

```markdown
# [Article Title]

**Author**: [Author Name or 'Unknown']  
**Date**: [Publication Date or 'Unknown']  

---

[Cleaned Article Body]
```

## Saving the Output
Unless the user specifies otherwise, save the output to a clearly named Markdown file in a dated directory, for example: `./reports/Articles_YYYY_MM_DD/[source_name_snake_case].md`. Do not summarize the entire article in the chat window; just provide the path to the saved file and a 1-sentence confirmation.
