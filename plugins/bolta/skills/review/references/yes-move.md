# The yes move, in detail

Read before carrying out decisions.

## Order inside one reply

1. `submit-for-review` with every yes not yet on the review list, in one call. Read each result: a post "held back: needs a human edit" gets new text through `update-post` (text only, no status; that edit asks once), then is shown again, not approved now.
2. `approve-post` for each yes, the first in its own call: it may get the Bolta check.
3. Drops: `delete-post`, after the first approval, so its check covers them (a delete's own check covers only deletes).
4. Changes: `update-post` (new text, `status: "Draft"`), then `submit-for-review`.
5. `list-scheduled-posts` once, then the read-back ([read-back.md](read-back.md)).

## Times

| The user said | `schedule_mode` | Notes |
|-|-|-|
| nothing about time | `approve_only` | Drafts from here or Bolta land on the saved posting schedule, then learned good hours. |
| "best time" | `use_suggested_time` | Bolta's suggested time for that post. |
| a time, or an exact time shown in the list (a day is not a time) | `set_fixed_time` | `fixed_time` is workspace wall clock, no Z or offset: `2026-10-21T09:00:00`. Add `timezone` only when the user named a place. At least 2 minutes ahead; the refusal gives the earliest valid time. |

- Posts in a not-started campaign Claude wrote: propose one time per post inside the campaign's dates, show them with the list, then `set_fixed_time` on yes.
- Approve results carry no time. `list-scheduled-posts` does: send `start_date` and `end_date` in UTC ending in Z, a day wider than needed. Its times are UTC; show them in the workspace clock.

## Fingerprints

- Row read from the review list: pass its `content_fingerprint` as `expected_fingerprint`. Empty on old rows: leave it out.
- Sent for review in this same reply: leave it out. Bolta checks against what was just sent.
- Never reuse one from before a change.

## Reading the result

- Scheduled: read back the time.
- Approved or "Ready for Scheduling" with no time (usually typed by hand, or no connected account): say so. With an account and review mode off, ask for a time, then `schedule-post`. In review mode `schedule-post` sends it back to the review list, so use `update-post` with `status: "Draft"`, then submit and approve with `set_fixed_time`.
- `already_decided`: it was approved before; nothing changed.
- `warnings` (X length, Reddit): pass them on.
- Post now, check declined after the approval: the post stays scheduled at Bolta's time. Say the time; offer to pull it back (`fix`).

## When it goes wrong

| Result | Say or do |
|-|-|
| stale review (409) | "This post changed since you looked. Here's the new version. Still yes?" Re-read the review list for the current text and fingerprint; approve only after a new yes. |
| review conflict (409) | Someone already decided it. Say its status; stop. |
| permission refusal | Say the reason plainly: your role can't approve, your plan doesn't include it, or this connection wasn't given that access. Stop after sending for review. |
| "Cannot approve post with status" | Not on the review list: send it first. |
| video not ready; Reddit needs a subreddit and title | Say what's missing; fix with `update-post`, then send it again. |
| publishing blocked in review mode | "Review mode is on, so I can't post right now. Schedule it for 9:40 am instead?" |
| timeout or unclear | `get-post` before any retry. |

Several posts: report each one. Never "all done" when one failed.
