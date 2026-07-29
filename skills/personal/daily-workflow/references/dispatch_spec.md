# Daily Workflow Dispatch Specification & Schemas

This reference file defines the data schemas, dispatch prompt specs, and output specifications for the `daily-workflow` skill.

---

## 1. Task Queue Classification Schema

When discovering tasks from Google Tasks (`Delegate` list), classify each item based on URL patterns:

| Queue Enum | Matching Condition | Subagent Target Skill |
|---|---|---|
| `threads_queue` | URL contains `threads.net` or `threads.com` | `ingest-threads` |
| `youtube_queue` | URL contains `youtube.com` or `youtu.be` | `ingest-youtube` |
| `website_queue` | Any other `http` / `https` URL | `ingest-website` |
| `skip` | No URL found in task title, links, or notes | Log and skip item |

Newsletter count is checked via Gmail search (`label:newsletter is:unread`). If positive, `newsletter_queue` contains unread email IDs.

---

## 2. Parallel Subagent Dispatch Specs

Each content item is dispatched as an independent focused subagent using `invoke_subagent`.

### Common Subagent Dispatch Schema

```yaml
type: object
properties:
  skill: { type: string, description: "Target ingest skill relative path" }
  item_id: { type: string, description: "Unique identifier (MESSAGE_ID or TASK_ID)" }
  target_url: { type: string, optional: true, description: "Content URL" }
  delegate_list_id: { type: string, optional: true, description: "Google Task list ID" }
  suggestion_output_path: { type: string, description: "Staging path for subagent suggestion JSON" }
  report_directory: { type: string, description: "Target date-stamped report directory" }
required: ["skill", "item_id", "suggestion_output_path", "report_directory"]
```

### Prompt Templates by Queue Type

#### Newsletter (`ingest-newsletter`)
```
Follow the ingest-newsletter skill at .agents/skills/ingest-newsletter/SKILL.md.

MESSAGE_ID: <MESSAGE_ID>
SuggestionOutputPath: data/suggestions_pending/suggestion_newsletter_<MESSAGE_ID>.json
Report directory: reports/Newsletter_YYYY_MM_DD/

Skip Step 1 (batch discovery) — process only this single email.
Pass SuggestionOutputPath through to suggestion_log.md.
```

#### Threads (`ingest-threads`)
```
Follow the ingest-threads skill at .agents/skills/ingest-threads/SKILL.md.

THREADS_URL: <URL>
TASK_ID: <TASK_ID>
DELEGATE_LIST_ID: <DELEGATE_LIST_ID>
SuggestionOutputPath: data/suggestions_pending/suggestion_threads_<TASK_ID>.json
Report directory: reports/Threads_YYYY_MM_DD/

Pass SuggestionOutputPath through to suggestion_log.md.
```

#### Website (`ingest-website`)
```
Follow the ingest-website skill at .agents/skills/ingest-website/SKILL.md.

WEBSITE_URL: <URL>
TASK_ID: <TASK_ID>
DELEGATE_LIST_ID: <DELEGATE_LIST_ID>
SuggestionOutputPath: data/suggestions_pending/suggestion_website_<TASK_ID>.json
Report directory: reports/Website_YYYY_MM_DD/

Pass SuggestionOutputPath through to suggestion_log.md.
```

#### YouTube (`ingest-youtube`)
```
Follow the ingest-youtube skill at .agents/skills/ingest-youtube/SKILL.md.

YOUTUBE_URL: <URL>
TASK_ID: <TASK_ID>
DELEGATE_LIST_ID: <DELEGATE_LIST_ID>
SuggestionOutputPath: data/suggestions_pending/suggestion_youtube_<TASK_ID>.json
Report directory: reports/YouTube_YYYY_MM_DD/

Pass SuggestionOutputPath through to suggestion_log.md.
```

---

## 3. Final Summary Output Schema

Upon completion of all steps, format the final execution summary as follows:

```
Dispatched N items total (N newsletter(s), T Threads, W website(s), Y YouTube).
Completed: <success_count> | Failed: <failed_count> | Timed out: <timeout_count>

Newsletter(s): reports/Newsletter_YYYY_MM_DD/
Threads:
  ✅ @handle — topic → reports/Threads_YYYY_MM_DD/filename.md
  ⚠️ @handle — FAILED (reason)
Website(s):
  ✅ example.com — Article Title → reports/Website_YYYY_MM_DD/filename.md
  ⚠️ another.com — FAILED (reason)
YouTube:
  ✅ Video Title → reports/YouTube_YYYY_MM_DD/filename.md
  ⚠️ Another Video — FAILED (reason)
Skipped Z task(s) (no URL found).
Suggestions merged: <count> pending → data/suggestions_pending.md
Distillation complete. Suggestions reviewed.
```
