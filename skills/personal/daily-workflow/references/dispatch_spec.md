# Daily Workflow Dispatch Specification & Schemas

This reference file defines the data schemas, dispatch prompt specs, and output specifications for the `daily-workflow` skill.

---

## 1. Task Queue Classification Schema

When discovering tasks from Google Tasks (`Delegate` list), classify each item based on URL patterns:

| Queue Enum | Matching Condition | Declarative Sub-Agent Persona |
|---|---|---|
| `threads_queue` | URL contains `threads.net` or `threads.com` | `threads_worker` |
| `youtube_queue` | URL contains `youtube.com` or `youtu.be` | `youtube_worker` |
| `website_queue` | Any other `http` / `https` URL | `website_worker` |
| `skip` | No URL found in task title, links, or notes | Log and skip item |

Newsletter count is checked via Gmail search (`label:newsletter is:unread`). If positive, `newsletter_queue` contains unread email IDs for `newsletter_worker`.

---

## 2. Declarative Subagent Dispatch Specs & Parameter Injection

Each content item is dispatched as an independent focused subagent using `invoke_subagent` referencing the persona by its logical **name** (path-free).

Personas are 100% static to maximize LLM prompt caching. All dynamic execution variables are injected into the subagent via the **First User Message**.

### Common Subagent Dispatch Schema

```yaml
type: object
properties:
  subagent: { type: string, description: "Declarative sub-agent persona name (e.g. newsletter_worker)" }
  item_id: { type: string, description: "Unique identifier (MESSAGE_ID or TASK_ID)" }
  target_url: { type: string, optional: true, description: "Content URL" }
  delegate_list_id: { type: string, optional: true, description: "Google Task list ID" }
  suggestion_output_path: { type: string, description: "Staging path for subagent suggestion JSON" }
  report_directory: { type: string, description: "Target date-stamped report directory" }
required: ["subagent", "item_id", "suggestion_output_path", "report_directory"]
```

### First User Message Parameter Templates

#### Newsletter (`newsletter_worker`)
```
MESSAGE_ID: <MESSAGE_ID>
SuggestionOutputPath: data/suggestions_pending/suggestion_newsletter_<MESSAGE_ID>.json
Report directory: reports/Newsletter_YYYY_MM_DD/

Skip Step 1 (batch discovery) — process only this single email.
Pass SuggestionOutputPath through to suggestion_log.md.
```

#### Threads (`threads_worker`)
```
THREADS_URL: <URL>
TASK_ID: <TASK_ID>
DELEGATE_LIST_ID: <DELEGATE_LIST_ID>
SuggestionOutputPath: data/suggestions_pending/suggestion_threads_<TASK_ID>.json
Report directory: reports/Threads_YYYY_MM_DD/

Pass SuggestionOutputPath through to suggestion_log.md.
```

#### Website (`website_worker`)
```
WEBSITE_URL: <URL>
TASK_ID: <TASK_ID>
DELEGATE_LIST_ID: <DELEGATE_LIST_ID>
SuggestionOutputPath: data/suggestions_pending/suggestion_website_<TASK_ID>.json
Report directory: reports/Website_YYYY_MM_DD/

Pass SuggestionOutputPath through to suggestion_log.md.
```

#### YouTube (`youtube_worker`)
```
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
