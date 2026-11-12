# The yes move: when it goes wrong

Read when an approve, reject or batch call refuses or comes back unclear. The order of calls: [review-yes-move.md](review-yes-move.md).

| Result | Say or do |
|-|-|
| stale review, alone or on one batch item | The post changed since it was read: its text, media, accounts or time. "This post changed since you looked. Here's the new version. Still yes?" Re-read the list and show text, account and time; approve only after a new yes. The rest of the batch stands. |
| review conflict | Someone already decided it. Say its status; stop. |
| `not_in_review` on a no | Never sent for review: [saying no](review-saying-no.md). |
| deletes stopped after 20 | The 5-minute limit per brand. Say how many went and ask before more. |
| `CLIENT_SIGNOFF_REQUIRED` | Client's yes first ([client approval](review-client-approval.md)). Stop. |
| `self_approval_not_allowed` | "Bolta needs someone else to approve posts you wrote here." Stop: no retry, no `publish-post`. |
| out of credits | Say `credits_needed` and `credits_remaining`; send them to bolta.ai/dashboard/settings/billing; approve again after. |
| billing unavailable | Credits couldn't be checked just now. Retry once shortly. |
| Library image still being made | Wait for the image, then approve again. |
| permission refusal | Say the reason plainly: your role can't approve, your plan doesn't include it, or this connection wasn't given that access. Stop after sending for review. |
| "Cannot approve post with status" | Not on the review list: send it first. |
| video not ready; Reddit needs a subreddit and title | Say what's missing; fix with `save-post` and `post_id` (Reddit: `platform_details`), then send it again. |
| timeout or unclear | `get-post` before any retry. |

Never "all done" when one failed.

## Always

- Follow the house rules in the Bolta skill.
- Read every time back from Bolta, never from memory.
