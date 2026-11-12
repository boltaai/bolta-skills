# Fix

Take a post back, stop everything Bolta is about to write or post, undo a delete, or find out why nothing went out. Use for: undo, unschedule, pull that post, stop or pause everything, I deleted the wrong post, restore it, it didn't post.

## Done when

The user knows what changed and what still goes out, in the workspace clock: "Pulled back: 3 posts. Paused: Bolta routine 'Weekly LinkedIn'. Still going out: nothing." Or one plain cause and one fix.

## Know this

- **Take it back:** `save-post` with `post_id` and `unschedule: true`, nothing else. It keeps its text, loses its time (`was_scheduled_for` in the result is the time it no longer goes out at), and needs a new yes to go out ([review](review.md)). No Bolta check.
- **Already out**, sending now, or out on some accounts: it can't be recalled; deleting here removes only Bolta's copy, not the network's. Never try to take it back; `unschedule` works only on a Scheduled post. Say: delete or edit it on the network. Offer a correction as a draft ([post](post.md)).
- **Stop everything:** pause every Bolta routine that's on and every campaign that's on or about to start. No check, no question first. Then say: scheduled posts still go out. List the next 7 days, plus any due now (those can no longer be pulled back), with times: "Pull these 5 back to drafts too?" On yes, soonest first, then list again. Keep the old times in the reply.
- Switching back on usually asks one Bolta check ([routine](routine.md), [campaign](campaign.md)).
- **Undo a delete or restore a post:** read [undo a delete](fix-undo-delete.md) first.
- **Why nothing went out:** check in this order and stop at the first that fits ([references/symptoms.md](fix-symptoms.md)):
  1. A disconnected account: the reconnect link.
  2. Waiting for your yes: the review list's totals. Nearly always this.
  3. A Bolta routine: off, blocked, last run, next run.
  4. A campaign: phase, last error, outcome.
  5. A post that didn't go out: the reason Bolta saved on it, per network.
- **Failed, partly out, waiting on an account, or out of credits:** [fix-after-publish.md](fix-after-publish.md).
- Late around 17:45-18:15 UTC (say it in the workspace clock): Bolta's servers are busy then. Not the user, not the post.

## Tools

- `list-accounts`, `get-connect-link`: disconnected accounts; reconnect.
- `list-inbox-items`: waiting for a yes (totals are workspace-wide).
- `list-workspace-posts` with `account_ids` (from `list-accounts`): the scheduled queue on those accounts, times in UTC.
- `list-workspace-posts`: by status, such as `queued` (due now), `failed` or `partially_published`.
- `get-post`: status, time, the saved reason.
- `save-post`: a fresh copy of a Failed post (no `post_id`); back to Draft (`post_id`, `unschedule: true`).
- `delete-post`: remove a post the user named; undo within 7 days; at most 20 per 5 minutes.
- `list-recently-deleted`, `restore-deleted`: undo a delete.
- `list-routines`, `get-routine`, `list-routine-runs`, `pause-routine`: Bolta routines.
- `list-content-campaigns`, `get-content-campaign`, `set-content-campaign-status`: campaigns.

## Hand off

[review](review.md): a new yes or a new time. [routine](routine.md), [campaign](campaign.md): switch back on, or dig deeper. [connect](connect.md): accounts and access. [post](post.md): a correction or a fresh copy.

## Always

- Follow the house rules in the Bolta skill.
- Never say "nothing will go out" until a fresh list shows it.
- Never delete to take something back.
