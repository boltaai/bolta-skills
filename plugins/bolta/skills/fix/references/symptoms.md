# Why nothing went out

Read when something didn't go out or get written. The first row that fits is the answer: one cause, one fix.

## Where the reason is

- **Accounts:** `token_status` other than `valid` means disconnected, the cause of most failed sends.
- **The review list:** `total_team` (drafts from you, Bolta routines and campaigns) and `total_recurring` (older repeating posts) are workspace-wide.
- **One post:** `status` first. `metadata.failure.errors` holds each network's reason (`friendly`) and fix (`action`). `metadata.partial` lists the accounts it missed (`unpublished`); `outcome: "unknown"` may have gone out, so check the network. `quality_block` says why it was held back. Otherwise a `failure_routed` entry in `activity_history`. Nothing saved: say so, then check the account.
- **Scheduled times** are UTC: ask a day wider, dates ending in `Z`.

## Symptom, cause, fix

| They see | Why | Say or do |
|-|-|-|
| Nothing went out, but drafts exist | Waiting for your yes, or never sent for review; Bolta posts neither. | Say how many; `review`. |
| Its time passed minutes ago | Sending, or waiting for a retry (up to 2 days). | Look in 15 minutes. |
| Didn't go out, because... | Usually a disconnected account. The reason and fix are on the post, per network. | Say it. Reconnect (`connect`), then a new yes (`review`). |
| Went out on 2 of 3 accounts | One account failed, or can't be confirmed. | Name it and why. Never resend to all (it posts twice); a copy for that account: `post`. |
| Back on the review list after a yes | Review mode is on and the send failed; Bolta asks again. | Say the reason, fix it, then a new yes. |
| Held back: needs a human edit | Bolta's quality check stopped it; the reasons are on the post. | New text only, never a status: `review`. |
| Approved, but no time | Usually no connected account, or typed by hand. | Give it a time: `review`. |
| Gone from the review list | Expired: 30 days past its time, or untouched, with no decision. It never posts. | Offer it as a new draft (`post`). |
| A Bolta routine wrote nothing | Off, blocked, no schedule, an unchanged page, or a skipped slot with no reason saved. | Read it and its runs (`routine`). |
| A campaign wrote nothing | Not started, paused, needs accounts, writer paused, week done, window closed, or an error. | Read its phase, last error, outcome (`campaign`). |
| Late, around 17:45-18:15 UTC | Bolta's servers are busy then. | Say it in the workspace clock. Nothing to fix. |
| Not in the recently deleted list | Deleted in the Bolta dashboard (final), over 7 days ago, or in another workspace. | It can't come back. Have the text? `post` saves it again. |
| Every save blocked; the hook error names Git Bash | Windows without Git Bash: the checks can't run. | "Install Git for Windows (git-scm.com/downloads/win), then restart Claude." |

## Traps

- A time sent while taking a post back stays on it: send the status alone.
- Due now (`queued`) posts aren't among scheduled posts: look for them too. One already sending can't be stopped.
- After taking posts back, list again and report each; never "all done" when one failed.
- A deleted `job` is an older Bolta automation; it comes back without the conversations it watched.
- A declined Bolta check means not done; never reach it another way.
