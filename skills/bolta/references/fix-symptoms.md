# Why nothing went out

Read when something didn't go out or get written. The first row that fits is the answer: one cause, one fix. Failed, partly out, back on the review list after a yes, late, waiting on an account, or out of credits: [fix-after-publish.md](fix-after-publish.md).

## Where the reason is

- **Accounts:** `token_status` other than `valid` or `ghost` means disconnected, the cause of most failed sends. `ghost` means added without connecting: never a reconnect ([fix-after-publish.md](fix-after-publish.md)).
- **The review list:** `total_team` (drafts from you, Bolta routines and campaigns) and `total_recurring` (drafts from older automations) are workspace-wide.
- **One post:** `status` first. `metadata.failure.errors` holds each network's reason (`friendly`) and fix (`action`). `metadata.partial` lists the accounts it missed (`unpublished`); `outcome: "unknown"` may have gone out, so check the network. `quality_block` says why it was held back. Otherwise a `failure_routed` entry in `activity_history`. Nothing saved: say so, then check the account.
- **Scheduled times** are UTC: ask a day wider, dates ending in `Z`.

## Symptom, cause, fix

| They see | Why | Say or do |
|-|-|-|
| Nothing went out, but drafts exist | Waiting for your yes, or never sent for review; Bolta posts neither. | Say how many; [review](review.md). |
| Its time passed minutes ago | Sending, or waiting for a retry (up to 2 days). | Look in 15 minutes. |
| Didn't go out, because... | Usually a disconnected account. The reason and fix are on the post, per network. | Say it. Reconnect ([connect](connect.md)); [fix-after-publish.md](fix-after-publish.md) says what comes back on its own. |
| Went out on 2 of 3 accounts | One account failed, or can't be confirmed (`outcome: "unknown"`). | Name it and why; check the network if unconfirmed. Never resend to all (it posts twice): [fix-after-publish.md](fix-after-publish.md). |
| Held back: needs a human edit | Bolta's quality check stopped it; the reasons are on the post. | New text only, never a status: [review](review.md). |
| Approved, but no time | Typed by hand, or waiting for an account ([fix-after-publish.md](fix-after-publish.md)). | Give it a time: [review](review.md). |
| Gone from the review list | Expired: 30 days past its time, or untouched, with no decision. It never posts on its own. Confirm with `list-workspace-posts` status `expired`. | It can be restored in Bolta at [bolta.ai/dashboard/approvals](https://bolta.ai/dashboard/approvals) ("Expired without a decision"); it gets a new time when approved. Or a new draft here ([post](post.md)). Never try to set it back to Draft: `save-post` `unschedule` works only on a Scheduled post. |
| A Bolta routine wrote nothing | Off, blocked, no schedule, an unchanged page, out of credits, or a skipped slot, whose reason can't be read from here. | Read it and its runs ([routine](routine.md)). |
| A campaign wrote nothing | Not started, paused, needs accounts, out of credits, writer paused, week done, window closed, or an error. | Read its phase, last error, outcome ([campaign](campaign.md)). |
| Not in the recently deleted list | Deleted in the Bolta dashboard (final), over 7 days ago, or in another workspace. | It can't come back. Have the text? [post](post.md) saves it again. |
| Every save blocked; the hook error names Git Bash | Windows without Git Bash: the checks can't run. | "Install Git for Windows (git-scm.com/downloads/win), then restart this app." |

## Traps

Taking posts back, queued posts, deleted jobs, declined checks: [fix-symptoms-traps.md](fix-symptoms-traps.md).

## Always

- Follow the house rules in the Bolta skill.
