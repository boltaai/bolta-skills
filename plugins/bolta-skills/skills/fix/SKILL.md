---
name: fix
description: >-
  Take a post back, stop everything Bolta is about to write or post, undo a
  delete, or find out why nothing went out. Use when someone says undo,
  unschedule, pull that post, stop everything, pause everything, I deleted
  the wrong post, restore it, it didn't post, or nothing went out.
---

## Done when

The user knows what changed and what still goes out, in the workspace clock: "Pulled back: 3 posts. Paused: Bolta routine 'Weekly LinkedIn'. Still going out: nothing." Or one plain cause and one fix.

## Know this

- **Take it back:** set the post to Draft, sending only the status. It keeps its text, loses its time, and needs a new yes to go out (`review`). No Bolta check.
- **Already out**, sending now, or out on some accounts: it can't be recalled; deleting here removes only Bolta's copy, not the network's. Never set it to Draft; Bolta would only relabel it. Say: delete or edit it on the network. Offer a correction as a draft (`post`).
- **Stop everything:** pause every Bolta routine that's on and every campaign that's on or about to start. No check, no question first. Then say: scheduled posts still go out. List the next 7 days, plus any due now, with times: "Pull these 5 back to drafts too?" On yes, soonest first, then list again. Keep the old times in the reply.
- Switching back on usually asks one Bolta check (`routine`, `campaign`).
- **Undo a delete:** only deletes made from Claude come back, for 7 days. Dashboard deletes are final. Show the first words and days left.
- **Restoring** brings it back exactly as it was. A scheduled post whose time passed in the last 2 days goes out within about 15 minutes. Say so, then ask: "As it was, or as a draft?" As a draft: restore, then take it back at once. One Bolta check, every time.
- **Why nothing went out:** check in this order and stop at the first that fits ([references/symptoms.md](references/symptoms.md)):
  1. A disconnected account: the reconnect link.
  2. Waiting for your yes: the review list's totals. Nearly always this.
  3. A Bolta routine: off, blocked, last run, next run.
  4. A campaign: phase, last error, outcome.
  5. A post that didn't go out: the reason Bolta saved on it, per network.
- Late around 17:45-18:15 UTC (say it in the workspace clock): Bolta's servers are busy then. Not the user, not the post.

## Tools

- `list-accounts`, `get-connect-link`: disconnected accounts; reconnect.
- `list-inbox-items`: waiting for a yes (totals are workspace-wide).
- `list-scheduled-posts`: scheduled posts, times in UTC.
- `list-workspace-posts`: by status, such as `queued` (due now) or `failed`.
- `get-post`: status, time, the saved reason.
- `update-post`: back to Draft.
- `delete-post`: remove a post the user named; undo within 7 days.
- `list-recently-deleted`, `restore-deleted`: undo a delete.
- `list-routines`, `get-routine`, `list-routine-runs`, `pause-routine`: Bolta routines.
- `list-content-campaigns`, `get-content-campaign`, `set-content-campaign-status`: campaigns.

## Hand off

`review`: a new yes or a new time. `routine`, `campaign`: switch back on, or dig deeper. `connect`: accounts and access. `post`: a correction or a fresh copy.

## Always

- Follow the house rules in the `today` skill.
- Never say "nothing will go out" until a fresh list shows it.
- Never delete to take something back.
