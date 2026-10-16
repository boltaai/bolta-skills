# Times, statuses, Safe Mode and read-backs

Read this when a time is involved, when a post is in a status you did not expect, or when a call is refused.

## Time rules

1. Send the wall-clock time the user said, as a naive ISO string, in the workspace timezone: "9am Tuesday" is `2026-10-20T09:00:00`. Nothing else. This applies to `approve-post` `fixed_time`, `schedule-post` `time`, `update-post` `scheduled_time` and bulk items. A Draft never carries a time (see "Why a Draft has no time" below).
2. Never send a trailing `Z` or an offset, never convert to or from UTC, never use your own clock or locale. The Bolta connector rejects an offset that arrives without `timezone`. If a time is rejected, re-read what the user typed and resend those digits. Do not "correct" the rejected value: converting it just sends the same error back.
3. If the user names a zone out loud ("9am Pacific"), send the same digits plus `timezone="America/Los_Angeles"` (an IANA name). Only then does `timezone` belong in the call. It wins over the workspace timezone.
4. Resolve "next Tuesday" or "tomorrow" from today's date and show the full date back. Ask only when the day or hour is ambiguous.
5. Echo every time as "Tue 20 Oct, 9:00 AM, Sydney (workspace timezone)", using the `timezone` from `get-workspace`. If that timezone is "UTC", which is the default, and the user named none, ask once which timezone they mean.
6. Lead time: `approve-post` with `set_fixed_time` refuses a time less than 2 minutes ahead (`schedule_time_too_soon`, with `earliest_valid_time`). `schedule-post` needs a future time. Bulk items with a past or unreadable time are dropped into `rejected`.
7. A local time that does not exist or happens twice on a daylight-saving changeover day is resolved by the server without telling you. If the user's time falls in that hour, say so and ask for another.
8. Publishing happens within a few minutes of the time, not on the second, and can be later when the queue is busy. Never promise a to-the-minute time.

## Why a Draft has no time

`create-post` and bulk items treat a `scheduled_time` with no `status` or `requested_action` as "schedule this". For an OAuth connection that sends the post straight to Pending Approval, not to the Draft you promised. Keep the time in the conversation and apply it at approval with `set_fixed_time`.

## Reading times back

- Reads return UTC. Convert to the workspace timezone before you compare or echo a time. Do not show the user a UTC time as if it were theirs.
- Date filters on reads (`start_date`, `end_date`) are interpreted as UTC. This is the one place you convert: turn the user's local window into UTC with a `Z`.
- `list-scheduled-posts` lists only posts whose status is Scheduled: it will not show Pending Approval, Approved or Ready for Scheduling. `limit` goes to 200 with `page`; `pagination.has_next` says more exist.
- `list-workspace-posts` caps `limit` at 100 and returns `has_more`. `status` accepts `draft`, `scheduled`, `pending_approval`, `published`, `failed` and any exact status label; an unknown one is an error listing the valid ones.
- `approve-post` returns `status`, `scheduled` and `warnings` but not the time. Always read it back.

## Statuses and what you may do

| Status | Meaning | Tools that apply |
|-|-|-|
| Draft | Saved, waiting | `update-post`, `submit-for-review`. `schedule-post` and `publish-post` are refused for an OAuth connection |
| Pending Approval | In the review queue | `approve-post`. `submit-for-review` is refused. An edit makes `approve-post` return `stale_review` |
| Needs Revision | A reviewer sent it back | Edit with `update-post`, then `submit-for-review` |
| Ready for Scheduling | Approved, no time yet (or no account yet) | `schedule-post` unless Safe Mode is on; `publish-post` unless Safe Mode is on |
| Approved | Approved | Same as Ready for Scheduling |
| Scheduled | Waiting for its time | `publish-post` (goes now, replaces the time). `schedule-post` is refused here. To move it use `update-post` `scheduled_time` |
| Queued, Processing | Being published | Nothing. Never publish again. Report anything Processing for over 15 minutes |
| Published | Went out on at least one platform | `get-post`. Per-account results are not visible |
| Partially Published | Some accounts failed | Do not republish: the accounts that succeeded would get a duplicate. Tell the user, name what you can see, point to Bolta |
| Failed | Nothing went out | There is no retry tool. After the cause is fixed and the user agrees, `update-post(post_id, status="Draft")` and run the ladder again |
| Quality Blocked | A text check refused it | `get-post` shows `quality_block.message`. Rewrite with `update-post`; it re-checks and returns the post to Draft |
| Rejected, Expired | Not publishable | Copy the text into a new Draft if the user wants it |

## Safe Mode (`get-workspace` `safe_mode` true)

| Call | Safe Mode off | Safe Mode on |
|-|-|-|
| `create-post` as Draft | Draft | Draft |
| `approve-post` with `set_fixed_time` | Scheduled at that time | Scheduled at that time |
| `approve-post` with `approve_only` | Scheduled at a slot the server picks | Same: the slot is chosen even under Safe Mode |
| `schedule-post` on an approved post | Scheduled | Sent back to Pending Approval; the time is not applied |
| `publish-post` | Queued | Refused |

So under Safe Mode the only way to a time the user chose is `approve-post` with `set_fixed_time`. Safe Mode exists so that someone reviews before anything goes out. The server accepts the connected user's own approval, but if the user says a teammate must review, stop at Pending Approval.

## The automatic slot

`approve_only` and `use_suggested_time` on a post Claude wrote always end up Scheduled at a slot the server picks (at least 1 hour ahead; with a saved posting schedule, the next free slot in it; otherwise at least 4 hours from other posts and 9:00 to 18:00 on weekdays in the audience timezone, which is the workspace timezone when none is set). The user's time is discarded. Use these modes only when the user wants Bolta to pick the time, and then read the time back and show it. A batch approved this way spreads over days.

## Moving, pausing and cancelling

- Move a Scheduled post: `update-post(post_id, scheduled_time=...)` with the exact time the user just stated, then read back. This keeps the approval.
- Take a post out of the schedule: `update-post(post_id, status="Draft")`. That clears the time and removes it from the queue; the text stays. Read back with `get-post` and confirm the status is Draft.
- Deleting is not a cancel. See the undo-and-recovery skill.

## Refusals you will see

| Message contains | Meaning | Do |
|-|-|-|
| "Approval required: an assistant may only schedule" | The post is not approved yet | Follow the ladder |
| "Immediate publishing is disabled when Safe Mode is ON" | Safe Mode | Sequence for Safe Mode in SKILL.md |
| "Cannot approve post with status" | Not in the review queue | `get-post`; submit it first if it is a Draft |
| `stale_review` (409) | The post changed after review began | Sequence for changing a post in SKILL.md |
| `schedule_time_too_soon` | Under 2 minutes ahead | Ask for a later time |
| "Scheduled time must be in the future" | Past time | Ask again |
| `no_connected_account`, `no_account_selected`, `accounts_need_reconnect` | No usable account | `list-accounts`, then `get-connect-link` |
| `REDDIT_REQUIREMENTS`, `FACEBOOK_MIXED_MEDIA_UNSUPPORTED`, `FACEBOOK_MULTIPLE_VIDEOS_UNSUPPORTED` | Platform rule | See platform-fields.md and media.md |
| `OUTPUT_TRUNCATED`, `PART_MARKER_LEAK`, `GENERATED_PAYLOAD` | The text looks cut off or carries scaffolding | Fix the text with `update-post`, send it back through Draft |
| "Monthly quota exceeded" | Plan limit | Report it and stop; do not retry |
| "Invalid API key", "API key expired", "API key inactive" | The connection is dead | Tell the user to reconnect the Bolta connector; do not retry |
