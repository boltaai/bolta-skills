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
bulk operation. Both hinge on **sending the user's wall-clock time as-is** — the server
interprets it in the workspace timezone.

## When to use
- The user wants a post to go out at a future time (scheduling).
- The user wants several posts created at once (batch/bulk).

## Tools this skill uses
| Tool | Why |
|-|-|
| `list-workspaces` | Resolve `workspace_id` if unknown — start here. |
| `list-accounts` | Get account UUIDs for `account_ids` in each post. |
| `create-post` | Create + schedule in one call (`requested_action: schedule` + `scheduled_time`). |
| `schedule-post` | Schedule an **existing** Draft (`post_id` + `time`). Requires admin or owner role. |
| `list-scheduled-posts` | Verify what is actually queued. |
| `bulk-create-posts` | Create many posts at once; returns a `task_id`. |
| `bulk-create-status` | One-shot status check for a bulk job by `task_id`. |

## Prerequisites
- `workspace_id` — resolve once via `list-workspaces`, reuse. Auth is automatic via the Bolta
  connector's OAuth grant — never ask for an API key. Default new content to Draft; confirm
  before publish/delete.
- Account UUIDs from `list-accounts` for every post.

## Time format — get this right
All scheduling fields (`scheduled_time`, `time`) take the **naive local wall-clock time the
user asked for** — no UTC offset, no trailing `Z`. The server interprets it in the workspace
timezone. Do NOT convert to your own locale or append an offset: any offset-bearing value
without a named zone is rejected.

- User says "9am Tuesday" → send `2026-07-21T09:00:00`. Nothing else.
- User names a zone out loud ("9am Pacific") → send `2026-07-21T09:00:00` **plus** the
  separate `timezone` param with the IANA name (`timezone: "America/Los_Angeles"`). That is
  the only case where `timezone` belongs in the call.
- Never send `2026-07-21T09:00:00-04:00` or `...T13:00:00Z` — both 400.

## Workflow A — Schedule a post

### 1. Resolve workspace + accounts
`list-workspaces` → `workspace_id`; `list-accounts` → `account_ids`.

### 2. Nail down the time
Take the user's stated time literally as a naive string (see Time format above). Only ask a
clarifying question if the *day or hour* is ambiguous — the zone is the workspace default
unless the user named one.

### 3. Schedule
- **New content:** `create-post` with `requested_action: "schedule"` and `scheduled_time` set to
  the naive wall-clock string, plus `content` and `account_ids` (or `social_buckets` with bucket IDs from `list-buckets` to hit a whole account group).
- **Existing Draft:** `schedule-post` with `workspace_id`, `post_id`, and `time` (naive
  wall-clock). Add `timezone` only if the user named a zone.

### 4. Verify
Call `list-scheduled-posts(workspace_id)` and confirm the post appears at the expected time.
Report the scheduled time back in the user's terms.

**Safe Mode:** if the workspace has Safe Mode on, scheduling is rerouted — the post lands in
Pending Approval instead of the schedule queue (and `publish-post` is blocked outright; use
`submit-for-review`). A post showing as pending review after a schedule call is that reroute
working, **not a failure** — tell the user it's awaiting approval and where to approve it.

## Workflow B — Batch create

### 1. Resolve workspace + accounts
Same as above; every post object needs its `account_ids`.

### 2. Build the posts array
Assemble `posts` — each item takes the same flat keys as `create-post`: `content`,
`account_ids` (or `social_buckets`), and optionally `media`. To schedule an item, set
**`status: "Scheduled"`** with a `scheduled_time` (required when Scheduled, naive wall-clock);
otherwise omit both and it lands as a Draft. There is **no per-item `requested_action`** —
that param is single-create-only and is silently ignored here, leaving posts as Drafts with
no error. If scheduling a series, space the naive times out; the workspace timezone applies
to all of them.

### 3. Kick off the bulk job
Call `bulk-create-posts(workspace_id, posts)`. It returns a `task_id` — it does not create the
posts synchronously.

### 4. Check status — once
The result card polls the bulk job itself and lists every post when the work lands — do
**not** re-poll `bulk-create-status` in a loop or restate the copy. If you need the outcome
programmatically (e.g. to report failures), call `bulk-create-status(task_id)` once after a
reasonable pause, not repeatedly.

### 5. Summarize
Report per-item results — how many created, any failures, and previews. Offer to fix or retry
any failed items. Safe Mode applies per item exactly as in Workflow A: scheduled items may
land in Pending Approval — report that as a reroute, not a failure.

## Failure handling
- Time rejected for carrying an offset → re-read what the user actually said and resend those
  digits naive; do not convert the rejected value.
- `scheduled_time` in the past → reject and ask for a future time.
- Scheduling an existing Draft that isn't found → re-list to get the right `post_id`.
- Bulk job with partial failures → surface exactly which items failed and why; offer to re-run just those.
- Permission error → report the missing role (workspace roles are owner/admin/creator/viewer;
  `schedule-post` needs admin or owner).

## Example
User: "Schedule a post for 9am next Tuesday and also batch-create 5 drafts."
1. `list-workspaces` → workspace_id; `list-accounts` → account_ids.
2. `create-post(..., requested_action="schedule", scheduled_time="2026-07-21T09:00:00")` — no
   offset, no `timezone` (user named no zone).
3. `list-scheduled-posts(workspace_id)` → confirm it's queued (or rerouted to Pending Approval
   under Safe Mode — say so).
4. `bulk-create-posts(workspace_id, posts=[...5 draft objects...])` → `task_id`; the card
   tracks completion → "5 Drafts created, 1 scheduled for Tue 9am."
