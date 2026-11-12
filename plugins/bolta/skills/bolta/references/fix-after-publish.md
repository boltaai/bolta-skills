# Failed, late, partly out, or waiting on an account

Read with [fix-symptoms.md](fix-symptoms.md). One cause, one fix.

## Finding the posts

- `list-workspace-posts` takes any status, such as `partially_published`, `failed`, `processing`, `ready_for_scheduling`, `needs_revision`, `quality_blocked` or `expired`. A misspelled status returns an error listing the valid ones; it does not mean none exist.
- Everything that went out: read both `published` and `partially_published`.
- What a broken account blocks: `list-workspace-posts` with `account_ids` (from `list-accounts`): scheduled rows whose `reconnect_accounts` holds that account. `list-account-insights` gives `stale_since`, when its data stopped updating.

## Symptom, cause, fix

| They see | Why | Say or do |
|-|-|-|
| Failed, and its time is days ago | A post still unsent more than 2 days after its time turns Failed. `publish-post` refuses Failed posts. | Read it with `get-post`, then save its text as a new draft with `save-post`, no `post_id` ([post](post.md)). It needs a yes and a time again. |
| Partly out: one account failed | That account's send failed, or can't be confirmed (`outcome: "unknown"`). | Name the account and why. Unconfirmed: it may have gone out, so check the network first. Failed: in Bolta's Inbox, open it and press Retry; only the failed accounts resend, except a missing-media failure (see Instagram). Retry refused: a copy for that account alone ([post](post.md)). |
| Scheduled posts after a reconnect | Posts still Scheduled for that network go out at their time on their own. | Don't recreate them or ask for a new yes. If the brand has two handles on that network, confirm the destination with `get-post`. |
| Approved, no time, nothing connected | A post whose `awaiting_connection` is set waits for its account. Once it connects, it moves to Scheduled at its chosen time if still ahead, else the next free slot. | Give `get-connect-link`. Missing media, or a missing client yes, keeps it waiting. |
| An account shows `token_status` `ghost` | Added without connecting: Bolta writes for it but can't post. | Never offer a reconnect. The person connects it for the first time, then finishes in Bolta: [bolta.ai/dashboard/knowledge-base?tab=accounts](https://bolta.ai/dashboard/knowledge-base?tab=accounts). |
| Failed on X with a video | X takes images only. | Fix the media in Bolta, then Retry. Back on the review list instead? Fix it, then a new yes ([review](review.md)). |
| Failed on Instagram, text only | Instagram needs an image or video. | Retry refuses it, even after media is added. On the review list: add media, then a new yes. Else a new post with media (`save-post`, no `post_id`). |
| Failed on TikTok or YouTube | Both need a video. | Add a video, then Retry or a new yes. |
| Back on the review list after a yes | Review mode is on and the send failed; Bolta asks again. | Say the reason, fix it, then a new yes. |
| Late, around 17:45-18:15 UTC | Bolta's servers are busy then. | Say it in the workspace clock. Nothing to fix. |
| Out on the network, no results in Bolta | Bolta lost the link to the published post. | Say so. It can't be fixed here; the network's own numbers are the record. |

## Out of credits

Routine runs skipped, campaign parked: what comes back on its own and what to do is in [fix-after-publish-credits.md](fix-after-publish-credits.md).

## Always

- Follow the house rules in the Bolta skill.
- Never resend a partly published post to every account; it posts twice.
- Never call a post gone until a fresh list in the right status shows it.
