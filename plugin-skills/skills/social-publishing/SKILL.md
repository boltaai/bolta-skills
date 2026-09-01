---
name: social-publishing
description: >
  Write, schedule and publish the brand's own social content — one post or many,
  one platform or several. Use this skill when the user asks to "write a post",
  "draft something about X", "schedule this for Tuesday", "post this to LinkedIn
  and X", "put together this week's posts", or "publish that now". Covers voice
  loading, per-platform tailoring, the review queue, scheduling and verification.
  For replying to other people's posts use reddit-engagement or
  cross-platform-engagement; for replies to comments on our own posts use
  social-inbox; for WordPress long-form use `create-wordpress-blog-post`.
---

# Social Publishing

Turn an idea into content that lands on the right accounts at the right time, in
the brand's voice, through the approval path the workspace actually requires.

## When to use
Anything where Bolta is the author. The default outcome is a **Draft** — never
publish or schedule unless the user asked for it.

## Tools this skill uses
| Tool | Why |
|-|-|
| `list-workspaces` | Resolve `workspace_id` once. |
| `list-accounts` | Account UUIDs for `account_ids`. |
| `list-buckets` | Named account groups — "post to my founder bucket". |
| `get-voice-context` | Load tone, do/don't rules and exemplars before writing. |
| `get-business-dna` | Deeper product/audience grounding when the topic needs facts. |
| `create-post` | Save the draft. Omit `requested_action` to keep it a Draft. |
| `bulk-create-posts` / `bulk-create-status` | Many posts in one pipeline; poll the status. |
| `update-post` | Revise before scheduling. |
| `get-post-platform-details` / `update-post-platform-details` | Per-platform options (Threads polls, Reddit flair, YouTube/TikTok/Pinterest fields). |
| `submit-for-review` | Route into the review queue when Safe Mode is on or a human should sign off. |
| `schedule-post` | Schedule at a wall-clock time. |
| `publish-post` | Publish immediately (admin/owner; blocked under Safe Mode). |
| `get-post` | Verify what actually landed. |
| `list-scheduled-posts` | Show the calendar; avoid stacking posts on one slot. |
| `get-connect-link` | Hand the user a connect URL when nothing is connected. |

## Prerequisites
- `workspace_id` via `list-workspaces`; auth is automatic, never ask for a key.
- At least one connected account. If none, `get-connect-link` and stop.
- Publishing immediately needs owner/admin and is refused under Safe Mode — use
  `submit-for-review` instead and say why.

## Workflow

### 1. Resolve workspace, accounts, voice
`list-workspaces` → `list-accounts` → `get-voice-context`. If the user named a
bucket, `list-buckets` and expand it to account ids.

Load the voice **before** writing, not after. Retrofitting a draft into a voice
produces the "sounds like AI wearing a costume" result.

### 2. Decide the shape
- One post, one platform → `create-post`.
- One idea, several platforms → write per-platform variants rather than the same
  text everywhere. A LinkedIn post pasted into X reads as a cross-post, because
  it is one.
- Several posts (a week, a campaign) → `bulk-create-posts`, then poll
  `bulk-create-status` until it settles.

### 3. Write
Write in the loaded voice. One idea per post. Concretely:
- No thought-leadership cadence, no rhetorical-question-then-answer.
- No fabricated statistics, quotes or customer stories. If you do not have the
  number, write the post without it.
- Respect platform length: X 280, Bluesky 300, Threads 500.
- Hashtags only where the platform's culture uses them; never on Bluesky, X or
  Reddit replies.

### 4. Save as a draft
`create-post(workspace_id, content, account_ids, ...)` with no
`requested_action`. Show the user what you saved and where it will go.

### 5. Per-platform options (when relevant)
`update-post-platform-details(post_id, platform, ...)` — Threads polls, Reddit
subreddit and flair, YouTube privacy, Pinterest board, TikTok settings. Read the
current values with `get-post-platform-details` first rather than overwriting.

### 6. Route it correctly
- **Draft only** (default) — stop here and tell the user it is waiting.
- **Review** — `submit-for-review(workspace_id, post_ids, note)`. This is the
  right path under Safe Mode and whenever someone else signs off.
- **Schedule** — `schedule-post(workspace_id, post_id, time=...)`. Send the time
  as wall clock; it resolves to the workspace's timezone. **Never send a UTC
  offset and never convert the user's stated time yourself** — that is how posts
  go out hours late.
- **Publish now** — `publish-post(workspace_id, post_id)`. Confirm explicitly
  first. This is public and irreversible.

### 7. Check the calendar
Before scheduling several, `list-scheduled-posts(workspace_id)` so you do not
stack three posts on one morning or collide with something already queued.

### 8. Verify
`get-post(post_id)` after scheduling or publishing. Report the actual state,
target accounts and time. If publish failed on one platform of several, say
which — a partial publish reported as a success is worse than a failure.

## Definition of done
- The user knows exactly what was saved, where it will go, and when.
- Nothing was published or scheduled that they did not ask for.
- Scheduled times were echoed back in their own timezone for confirmation.
- Multi-platform posts have per-platform text, not one string copied across.

## Failure handling
- No connected accounts → `get-connect-link`, stop.
- Safe Mode blocks `publish-post` → `submit-for-review` and explain the setting;
  do not try to work around it.
- Permission error → `get-my-capabilities`, name the missing role, do not retry.
- Scheduling rejected for an offset-bearing time → resend as naive wall clock
  plus an explicit `timezone` if the user named one.
- `bulk-create-status` still running → wait and poll; do not re-issue the bulk
  create, which would duplicate the batch.
- Quota / plan errors → report the limit plainly and stop. Do not retry a
  quota refusal; the answer will not change until the plan or the period does.

## Save this as a routine
For recurring content — "a post every Monday", "three drafts a week":
1. `list-routine-templates()` → e.g. `weekly_social_posts`.
2. `create-routine(...)` with a schedule and
   `output_config={artifact_type: "post", count: N}`.
3. `activate-routine(...)`.

Scheduled runs produce drafts into the review queue by default. Ask whether the
user wants to approve each batch or let workspace autonomy handle it — and never
set `approval_policy: "auto"` without them saying so.
