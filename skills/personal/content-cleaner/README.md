# Content Cleaner Skill

A specialized Antigravity skill designed to extract pure article text from raw, noisy web content. 

## Overview

When scraping or copying content from the web, the raw text is often polluted with advertisements, navigation menus, related links, and hidden JSON metadata. The `content-cleaner` skill automates the process of sanitizing this data, ensuring that you only retain the core article content formatted cleanly in Markdown.

## Features

- **Multi-Input Support:** Provide a URL, a raw text file, or paste raw HTML/text directly into the chat.
- **Noise Reduction:** Automatically strips out website navigation, sidebars, header/footer links, and "subscribe" prompts.
- **Ad Blocking:** Removes advertisement placeholders (e.g., "廣告-請繼續往下閱讀"), sponsored content blocks, and social media sharing buttons.
- **Metadata Sanitization:** Cleans up hidden JSON-LD (Schema.org) blocks, raw HTML tags, and unnecessary script code.
- **Structured Output:** Generates a standardized Markdown file including Title, Author, Date, and the clean article body.
- **Auto-Archiving:** Automatically saves the cleaned output into an organized directory structure (e.g., `./reports/Articles_YYYY_MM_DD/`).

## Usage

You can trigger this skill naturally during your conversation by asking Antigravity to clean a URL or a piece of text.

### Example Prompts

**Using a URL:**
> "Please use the content-cleaner skill to extract the main article from `https://example.com/news/123`."

**Using a local file:**
> "I have a messy HTML dump in `./raw/article.txt`. Run the content-cleaner on it to give me just the main text."

**Pasting text directly:**
> "Can you clean up this raw text I copied? Remove all the ads and menus and output a clean Markdown file."

## Integration & Tools

- When given a URL, the skill will automatically utilize either the `read_url_content` tool for fast, static pages, or the `agent-browser` skill for sites that require JavaScript rendering.
- The output will always be written directly to a `.md` file, preventing the chat interface from being overwhelmed by long text blocks.

## Customization

If you notice specific types of noise or advertisements consistently slipping through, you can easily improve this skill by editing the `Cleaning Guidelines` section in `SKILL.md` to include those specific patterns.
