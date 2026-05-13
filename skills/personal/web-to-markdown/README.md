# web-to-markdown Skill

## Overview

The `web-to-markdown` skill converts any publicly accessible website URL into a clean Markdown file by calling the [Jina Reader API](https://r.jina.ai/). It is a lightweight, browser-free alternative to manual web scraping or the `content-cleaner` skill.

## Problem Statement

Extracting readable text from web pages typically requires either browser automation (slow, heavy) or manual HTML stripping (fragile, noisy). Neither approach is suitable for a fast, repeatable agent workflow.

## Solution

Use the Jina Reader API (`r.jina.ai`) as a single HTTP call. Prepending `https://r.jina.ai/` to any URL returns structured Markdown with title, publication date, and body — no browser or parsing logic needed.

### Key Features

1. **Zero browser dependency:** Uses `read_url_content` only — no Playwright or agent-browser overhead.
2. **Structured response:** Jina returns `Title:`, `URL Source:`, `Published Time:`, and `Markdown Content:` fields, enabling clean extraction.
3. **Server-side rendering:** Jina handles JavaScript-heavy pages transparently.
4. **Graceful degradation:** Falls back to recommending `content-cleaner` on error or authentication-blocked pages.

## File Structure

```
web-to-markdown/
├── SKILL.md      # Skill definition, steps, output template, error handling
└── README.md     # This file
```

## Dependencies

- None. Uses the built-in `read_url_content` tool only.
- External service: [Jina Reader API](https://r.jina.ai/) — free, no API key required up to 20 RPM.

## Rate Limits

| Tier | Limit |
|---|---|
| No API key (default) | 20 RPM |
| Free API key | 500 RPM |
| Paid API key | 5,000 RPM |

For personal agent use, the keyless 20 RPM limit is sufficient.

## Triggering

This skill triggers when the user says:
- "convert this page to markdown"
- "save this URL as markdown"
- "parse this website"
- "get markdown from URL"
- Provides a `http://` or `https://` URL where the goal is a readable Markdown file

Prefer this skill over `content-cleaner` when the input is a URL and the goal is Markdown output. Use `content-cleaner` when the input is raw HTML text or the URL is behind authentication.

## Output Location

```
reports/
└── Articles_YYYY_MM_DD/
    └── {slugified_title}.md
```

## Design Decision

**Why Jina Reader over `markdown.new`?**

`markdown.new` was the originally proposed backend but returns HTTP 403 on all programmatic requests — it is a browser-only tool with no documented API and unknown rate limits. Jina Reader was chosen because it:
- Works as a plain HTTP GET (no browser needed)
- Has documented rate limits and a free tier
- Uses the same URL-prefix pattern (`<service>/<target URL>`)

## Changelog

| Version | Date | Change Summary |
|---|---|---|
| v1.0.0 | 2026-05-13 | Initial skill: Jina Reader API, `read_url_content`-only implementation. |
