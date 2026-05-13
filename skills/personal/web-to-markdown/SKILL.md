---
name: web-to-markdown
description: Converts any website URL into a clean Markdown file using the Jina Reader API. Use this skill whenever the user wants to convert a webpage to Markdown, save a website as Markdown, parse a URL into readable text, or extract content from a web page as Markdown. Triggers include 'convert this page to markdown', 'save this URL as markdown', 'parse this website', 'get markdown from URL', 'web to markdown', or any request to turn a web resource into a Markdown file. Prefer this skill over manual browser scraping when the goal is a Markdown file from a URL.
---

# Web to Markdown

Converts any website URL into a clean Markdown file via the Jina Reader API (`r.jina.ai`).

## How It Works

Prepend `https://r.jina.ai/` to the target URL and fetch with `read_url_content`. Jina handles JavaScript rendering, ad removal, and Markdown conversion server-side.

## Steps

1. **Validate input.** Ensure the user provided a valid URL (must start with `http://` or `https://`).
2. **Fetch Markdown.** Call `read_url_content` with URL `https://r.jina.ai/<target URL>`.
3. **Extract content.** The response contains metadata lines (`Title:`, `URL Source:`, `Published Time:`) followed by `Markdown Content:`. Extract the title from the `Title:` line and the body from everything after `Markdown Content:`.
4. **Format output.** Assemble the final Markdown using the template below.
5. **Save file.** Write to the output path (see Saving section).

## Output Template

```markdown
# [Title from Jina response]

**Source**: [original URL]
**Date**: [Published Time, or 'Unknown']

---

[Markdown body from Jina response]
```

## Saving the Output

Unless the user specifies a path, save to: `./reports/Articles_YYYY_MM_DD/[slugified_title].md`

Derive `slugified_title` from the page title: lowercase, replace spaces/special chars with underscores, truncate to 80 chars. Confirm the saved path to the user in one sentence.

## Error Handling

- If Jina returns an error or empty content, report the failure and suggest the user try `content-cleaner` skill as fallback (which uses direct `read_url_content` + manual cleaning).
- If the URL is behind authentication or a paywall, Jina may return partial content. Note this to the user.
