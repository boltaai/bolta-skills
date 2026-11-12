# The yes move, in detail

Read before carrying out decisions. Times: [review-times.md](review-times.md). Library posts, send-backs: [review-more-decisions.md](review-more-decisions.md). Credits: [review-credits.md](review-credits.md).

## Order inside one reply

1. `submit-for-review` for every yes not yet on the list, in one call. `note`: a short factual note for reviewers, never invented urgency; it can't pick a reviewer. A post "held back: needs a human edit", or a quality refusal (it carries `how_to_fix`), gets new text via `save-post` with `post_id` and `content` (that edit asks once), then is shown again, not approved now.
2. Just sent some? `list-inbox-items` again for their `content_fingerprint`.
3. `approve-many-posts`, every yes in one call (25 at most; the rest in a second call). It gets the one Bolta check. One post is one item.
4. `reject-post` for each no with a reason; `delete-post` for each drop. They pass once the approval's check did.
5. Read back ([read-back.md](review-read-back.md)). Each `approve-many-posts` item gives `scheduled` and, when set, `scheduled_time` (UTC) and `credits_charged`. After a batch, read back once with `list-workspace-posts` and those posts' `account_ids`, the scheduled queue (UTC `start_date`/`end_date` ending in Z, a day wider). Its times are UTC; show them in the brand clock.

## Times

| The user said | `schedule_mode` | Notes |
|-|-|-|
| nothing about time | `approve_only` | Bolta picks from the saved posting schedule, then learned good hours. |
| "best time" | `use_suggested_time` | Bolta's suggested time for that post. |
| a time, or an exact time shown in the list (a day is not a time) | `set_fixed_time` | `fixed_time` is brand wall clock, no Z or offset: `2026-10-21T09:00:00`. `timezone` only when the user named a place. At least 2 minutes ahead; a refusal gives the earliest valid time. |

- A not-started campaign you wrote: propose a time per post inside its dates, show them, then `set_fixed_time` on yes.

## Fingerprints, roles, notes

- `expected_fingerprint`: the row's `content_fingerprint`, read after any change; never reuse an old one. A legacy recurring row has none: send its `review_id` (the row's `id`) instead of `post_id` and `expected_fingerprint`. Any other row with an empty one can't be approved here: read the list again; still empty, it is approved in Bolta (bolta.ai/dashboard/approvals).
- Here, `approve-many-posts` and `reject-post` follow Bolta's rule: owners and admins any post; creators Bolta's drafts and posts naming them reviewer; a per-person setting can give or take it away; viewers never. Own post, review mode and client sign-off still apply. More: [people and roles](connect-people-and-roles.md). Refused: give Bolta's sentence, send for review, say who can.
- `comments` on an approval: an optional note kept on the review trail, and for AI drafts fed to Bolta's learning. Use the user's words only.
- No checks plugin, no Bolta checks. Past 3 yeses, also offer bolta.ai/dashboard/approvals.

## Reading the result

Scheduled, "Ready for Scheduling", `already_decided`, `warnings`: [review-yes-move-result.md](review-yes-move-result.md).

## When it goes wrong

Every refusal and what to say: [review-yes-move-errors.md](review-yes-move-errors.md). Never "all done" when one failed.

## Always

- Follow the house rules in the Bolta skill.
- Read every time back from Bolta, never from memory.
