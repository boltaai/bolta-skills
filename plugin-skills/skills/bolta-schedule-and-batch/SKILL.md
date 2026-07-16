---
name: bolta-schedule-and-batch
description: >
  Schedule Bolta posts for a future time and create posts in bulk. Use this skill when the user
  asks to "schedule this post", "schedule a week of content", "post every day next week", "queue
  these up", "create 10 posts", "batch create posts", or "make a bunch of drafts at once". Covers
  both scheduling a single post (new or existing Draft) and firing off a bulk-create job with
  progress tracking. For a single one-off Draft use bolta-draft-post.
---

# Bolta — Schedule & Batch

Two related jobs: put a post on the calendar at a specific time, and create many posts in one
bulk operation. Both hinge on **unambiguous times** — always confirm the workspace timezone or
use explicit ISO 8601 offsets.

## When to use
- The user wants a post to go out at a future time (scheduling).
- The user wants several posts created at once (batch/bulk).

## Tools this skill uses
| Tool | Why |
|-|-|
| `list-workspaces` | Resolve `workspace_id` if unknown — start here. |
| `list-accounts` | Get account UUIDs for `account_ids` in each post. |
| `create-post` | Create + schedule in one call (`requested_action: schedule` + `scheduled_time`). |
| `schedule-post` | Schedule an **existing** Draft (`post_id` + `time`). |
| `list-scheduled-posts` | Verify what is actually queued. |
| `bulk-create-posts` | Create many posts at once; returns a `task_id`. |
| `bulk-create-status` | Poll the bulk job by `task_id` until done. |

Full contract: `../../references/bolta-tools.md`.

## Prerequisites
- `workspace_id` — resolve once via `list-workspaces`, reuse.
- Account UUIDs from `list-accounts` for every post.
- A clear timezone. If the user says "9am Tuesday", confirm the intended zone (or the workspace
  default) and convert to an explicit ISO 8601 string with offset before scheduling.

## Workflow A — Schedule a post

### 1. Resolve workspace + accounts
`list-workspaces` → `workspace_id`; `list-accounts` → `account_ids`.

### 2. Nail down the time
Convert the requested time to ISO 8601 with an explicit offset (e.g. `2026-07-20T09:00:00-04:00`).
If the zone is unclear, ask before proceeding — a wrong zone posts at the wrong hour.

### 3. Schedule
- **New content:** `create-post` with `requested_action: "schedule"` and `scheduled_time` set to
  the ISO string, plus `content` and `account_ids`.
- **Existing Draft:** `schedule-post` with `workspace_id`, `post_id`, and `time` (ISO 8601).

### 4. Verify
Call `list-scheduled-posts(workspace_id)` and confirm the post appears at the expected time.
Report the scheduled time back in the user's terms.

## Workflow B — Batch create

### 1. Resolve workspace + accounts
Same as above; every post object needs its `account_ids`.

### 2. Build the posts array
Assemble `posts` — an array of post objects (each with `content`, `account_ids`, and optionally
`scheduled_time` / `requested_action` / `media` / `poll`). Default each to Draft unless the user
asked to schedule; if scheduling a series, space the ISO times out and keep the timezone
consistent across all of them.

### 3. Kick off the bulk job
Call `bulk-create-posts(workspace_id, posts)`. It returns a `task_id` — it does not create the
posts synchronously.

### 4. Poll to completion
Call `bulk-create-status(task_id)` and re-poll until the job reports done. Do not assume success
from the initial call.

### 5. Summarize
Report per-item results from the status response — how many created, any failures, and previews.
Offer to fix or retry any failed items.

## Failure handling
- Ambiguous timezone → stop and confirm; never guess the offset.
- `scheduled_time` in the past → reject and ask for a future time.
- Scheduling an existing Draft that isn't found → re-list to get the right `post_id`.
- Bulk job with partial failures → surface exactly which items failed and why; offer to re-run just those.
- Permission error → report the missing role/scope (creator+ to create; editor for bulk ops).

## Example
User: "Schedule a post for 9am next Tuesday and also batch-create 5 drafts."
1. `list-workspaces` → workspace_id; `list-accounts` → account_ids.
2. Confirm zone → `2026-07-21T09:00:00-04:00`.
3. `create-post(..., requested_action="schedule", scheduled_time="2026-07-21T09:00:00-04:00")`.
4. `list-scheduled-posts(workspace_id)` → confirm it's queued.
5. `bulk-create-posts(workspace_id, posts=[...5 objects...])` → `task_id`.
6. Poll `bulk-create-status(task_id)` until done → "5 Drafts created, 1 scheduled for Tue 9am."
