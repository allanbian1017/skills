#!/bin/bash
# fetch-thread.sh — Quick text extraction from a Threads post
# Usage: ./fetch-thread.sh <threads-url>
#
# Outputs raw text content from the Threads post to stdout.
# For structured extraction (media, metrics, replies), use the
# full SKILL.md procedure instead.

set -euo pipefail

URL="${1:?Usage: $0 <threads-url>}"
SESSION="threads-fetch"

echo "--- Fetching Threads post: $URL" >&2

# Navigate and wait for SPA to hydrate
agent-browser --session "$SESSION" open "$URL"
agent-browser --session "$SESSION" wait --load networkidle
agent-browser --session "$SESSION" wait 2000

# Extract page title for context
TITLE=$(agent-browser --session "$SESSION" get title 2>/dev/null || echo "Unknown")
echo "--- Page title: $TITLE" >&2

# Extract full page text
agent-browser --session "$SESSION" get text body

# Cleanup
agent-browser --session "$SESSION" close >/dev/null 2>&1

echo "" >&2
echo "--- Done" >&2
