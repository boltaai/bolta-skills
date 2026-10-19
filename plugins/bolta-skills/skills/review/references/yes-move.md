# The yes move, in detail

Read before carrying out decisions.

## Order inside one reply

1. `submit-for-review` for every yes not yet on the list, in one call. A post "held back: needs a human edit" gets new text through `update-post` (text only, no status; that edit asks once), then is shown again, not approved now.
2. Just sent some? `list-inbox-items` again for their `content_fingerprint`.
3. `approve-many-posts`, every yes in one call (25 at most; the rest in a second call). It gets the one Bolta check. If missing: `approve-post` each, the first in its own call.
4. `reject-post` for each no with a reason; `delete-post` for each drop. They pass once the approval's check did.
5. `list-scheduled-posts` once, then the read-back ([read-back.md](read-back.md)).

## Times

| The user said | `schedule_mode` | Notes |
|-|-|-|
| nothing about time | `approve_only` | Bolta picks from the saved posting schedule, then learned good hours. |
| "best time" | `use_suggested_time` | Bolta's suggested time for that post. |
| a time, or an exact time shown in the list (a day is not a time) | `set_fixed_time` | `fixed_time` is workspace wall clock, no Z or offset: `2026-10-21T09:00:00`. Add `timezone` only when the user named a place. At least 2 minutes ahead; the refusal gives the earliest valid time. |

- Posts in a not-started campaign Claude wrote: propose one time per post inside the campaign's dates, show them with the list, then `set_fixed_time` on yes.
- Approve results carry no time. `list-scheduled-posts` does: send `start_date` and `end_date` in UTC ending in Z, a day wider than needed. Its times are UTC; show them in the workspace clock.

## Fingerprints and roles

- `expected_fingerprint` is the row's `content_fingerprint`, read after any change; never reuse an old one. `approve-post` may leave it out when the row's is empty.
- Only owners and admins can approve or turn down. Others: send for review, say who can.
- Claude.ai chat runs no Bolta checks. Past 3 yeses, also offer bolta.ai/dashboard/hub.

## Reading the result

- Scheduled: read back the time.
- Approved or "Ready for Scheduling" with no time (typed by hand, or no connected account): say so. Account and review mode off: ask for a time, then `schedule-post`. In review mode that sends it back to the review list: `update-post` with `status: "Draft"`, submit, approve with `set_fixed_time`.
- `already_decided`: approved before; nothing changed. Repeating a batch is safe.
- `warnings` (X length, Reddit): pass them on.
- Post now, check declined after the approval: it stays scheduled at Bolta's time. Say the time; offer to pull it back (`fix`).

## When it goes wrong

| Result | Say or do |
|-|-|
| stale review (409), alone or on one batch item | "This post changed since you looked. Here's the new version. Still yes?" Re-read the list for the new text and fingerprint; approve only after a new yes. The rest stand. |
| review conflict (409) | Someone already decided it. Say its status; stop. |
| permission refusal | Say the reason plainly: your role can't approve, your plan doesn't include it, or this connection wasn't given that access. Stop after sending for review. |
| "Cannot approve post with status" | Not on the review list: send it first. |
| video not ready; Reddit needs a subreddit and title | Say what's missing; fix with `update-post`, then send it again. |
| timeout or unclear | `get-post` before any retry. |

Never "all done" when one failed.
