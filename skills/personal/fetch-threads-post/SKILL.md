---
name: fetch-threads-post
description: "Fetch all content from a Threads (threads.net / threads.com) post URL using agent-browser. Use when the user provides a Threads post URL and wants to extract the full post text, author info, media URLs, engagement metrics, and reply thread. Triggers: 'fetch this Threads post', 'scrape Threads', 'get content from Threads URL', 'extract Threads post', or any request involving a threads.net/threads.com post link."
allowed-tools: Bash(agent-browser:*)
---

# fetch-threads-post

Extract all content from a Threads post using `agent-browser` (browser automation via CDP).

## Supported URL Formats

- `https://www.threads.net/@{username}/post/{shortcode}/`
- `https://www.threads.com/@{username}/post/{shortcode}`
- `https://www.threads.net/t/{shortcode}/`

> URLs may include query parameters (e.g. `?xmt=...`). These are harmless and can be kept as-is.

## Prerequisites

- `agent-browser` must be installed and available in PATH.
- If not installed: `npm i -g agent-browser && agent-browser install`

---

## Procedure

Follow these steps **in order**. Use a dedicated session to avoid polluting other browser state.

### Step 1 — Navigate to the Post

```bash
agent-browser --session threads open "<THREADS_URL>"
agent-browser --session threads wait --load networkidle
agent-browser --session threads wait 2000
```

> The extra 2-second wait ensures dynamic SPA content finishes hydrating.

### Step 2 — Check for Login Wall

```bash
agent-browser --session threads snapshot -i
```

Inspect the snapshot output:
- If you see a **login form**, **"Log in" button**, or **modal overlay blocking content**, the post requires authentication. Jump to [Authenticated Access](#authenticated-access).
- If the post content is visible (you can see post text, author info), continue to Step 3.

### Step 3 — Extract Post Author

```bash
agent-browser --session threads snapshot -i
```

From the snapshot, identify the author elements:
- **Handle**: Look for text starting with `@` near the top of the post. Use `agent-browser --session threads get text @ref` on the element.
- **Display name**: Usually adjacent to or above the handle.

### Step 4 — Expand Long Posts ("Read more")

Threads truncates long posts with a "Read more" link. You **MUST** check for this to avoid capturing incomplete content:

```bash
# Look for "Read more" in the snapshot
agent-browser --session threads snapshot -i

# If found, click it by text or ref
agent-browser --session threads click "Read more"
agent-browser --session threads wait 1500
```

> **Crucial**: If the post remains truncated after clicking or the button is unreachable, use the `get text body` fallback in Step 5 to capture the hidden text from the DOM.

### Step 5 — Extract Post Text

Identify the main post text container from the snapshot refs, then:

```bash
agent-browser --session threads get text @<post-body-ref>
```

If you cannot reliably identify the post container from the snapshot, or if the post is very long and spans multiple containers:

```bash
# Extract full page text to ensure no segment is missed
agent-browser --session threads get text body
```

Then parse the post content from the output. Verify that the extracted text matches the expected flow of the post (e.g., it doesn't end abruptly or skip sections).

### Step 6 — Extract Media

From the snapshot, look for `[img]` or `[video]` elements within the post container:

```bash
# For images
agent-browser --session threads get attr @<img-ref> src

# For videos
agent-browser --session threads get attr @<video-ref> src
```

Collect all media URLs. If no media elements are found, note "No media" in the output.

### Step 7 — Extract Engagement Metrics

From the snapshot, look for elements containing like/reply/repost counts. These are typically near the bottom of the post. Use `get text` on the relevant refs:

```bash
agent-browser --session threads get text @<likes-ref>
agent-browser --session threads get text @<replies-ref>
agent-browser --session threads get text @<reposts-ref>
```

> Threads may display metrics as "123 likes" or just "123" with an icon. Extract whatever is visible.

### Step 8 — Extract Timestamp

Look for a time element or relative date text (e.g. "2h", "Apr 10") in the snapshot:

```bash
agent-browser --session threads get text @<time-ref>
# Or try getting the datetime attribute for precise timestamps
agent-browser --session threads get attr @<time-ref> datetime
```

### Step 9 — Extract Replies (if present)

Scroll down to load replies:

```bash
agent-browser --session threads scroll down 800
agent-browser --session threads wait 1500
agent-browser --session threads snapshot -i
```

For each visible reply, extract:
- Reply author handle
- Reply text content

Repeat the scroll → wait → snapshot → extract cycle until:
- No new replies appear in successive snapshots, OR
- You have collected a reasonable number of replies (20+ is sufficient unless the user asks for more)

```bash
# For each reply
agent-browser --session threads get text @<reply-author-ref>
agent-browser --session threads get text @<reply-text-ref>
```

### Step 10 — Cleanup

```bash
agent-browser --session threads close
```

### Step 11 — Assemble Output

Format the collected data as follows:

```markdown
# Threads Post by @{handle}

## Author
- **Handle**: @{username}
- **Display Name**: {display_name}

## Post Content
{full_text_of_the_post}

## Media
- {media_url_1}
- {media_url_2}
(or "No media attached")

## Engagement
- Likes: {N}
- Replies: {N}
- Reposts: {N}

## Timestamp
{date_time}

## Source URL
{original_url}

---

## Replies

### @{reply_user_1}
{reply_text_1}

### @{reply_user_2}
{reply_text_2}

(... more replies ...)
```

---

## Authenticated Access

If the post is behind a login wall:

1. **Check for saved state**:
   ```bash
   # If you have a previously saved Threads auth state, load it
   agent-browser --session threads state load threads-auth.json
   agent-browser --session threads reload
   agent-browser --session threads wait --load networkidle
   agent-browser --session threads wait 2000
   ```

2. **If no saved state exists**, inform the user:
   > "This Threads post requires login. Please run `agent-browser --session threads --headed open <URL>` to log in manually, then run `agent-browser --session threads state save threads-auth.json` to save the session for future use."

3. After auth state is loaded, return to **Step 3** and continue extraction.

---

## Troubleshooting

### Content not loading
```bash
# Try a longer wait
agent-browser --session threads wait 5000
agent-browser --session threads snapshot -i
```

### Obfuscated DOM / can't identify elements
Threads uses obfuscated class names. **Always rely on the accessibility tree snapshot** (`snapshot -i`) rather than CSS selectors. The snapshot provides semantic element types and visible text, which are stable even when class names change.

If the snapshot is too large or cluttered:
```bash
# Scope to main content area
agent-browser --session threads snapshot -d 4
```

### CAPTCHA or rate limiting
If you encounter a CAPTCHA:
```bash
agent-browser --session threads screenshot captcha.png
```
Report to the user: "Threads is showing a CAPTCHA. Please solve it manually using `agent-browser --session threads --headed open <URL>`."

### Fallback: Raw text extraction
If structured extraction fails, extract everything as raw text:
```bash
agent-browser --session threads get text body > /tmp/threads-raw.txt
```
Then parse the output manually to identify post content, author, and replies from the text flow.

---

## Tips

- **Session isolation**: Always use `--session threads` to avoid interfering with other browser sessions.
- **Snapshot is your eyes**: Re-snapshot after every navigation, scroll, or wait. Refs are invalidated on page changes.
- **Be patient with SPA**: Threads is a heavy SPA. After `networkidle`, wait 1-2 extra seconds.
- **Anti-Truncation**: Long posts on Threads are notoriously difficult to capture via simple ref-based extraction. Always prefer `get text body` for long posts and verify the output against the visible post structure (using `screenshot` or `snapshot`) to ensure you haven't missed the middle or end of the text.
- **Media quality**: Image `src` attributes may point to CDN URLs with size parameters. These URLs are directly usable.
