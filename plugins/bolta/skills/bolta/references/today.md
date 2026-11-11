# Today

Show a five-line summary of what needs you in Bolta: how many posts wait for your yes, what goes out this week, Bolta routines and campaigns running, anything ended or broken. Use when someone says what needs me, catch me up, or is vague about Bolta. Not for "what's waiting for me": that's review.

## Done when

Five lines or fewer on what needs the user (per brand), then one next step.

## Know this

- **Look once**, on the first Bolta ask: workspace, settings, accounts, voice; every playbook reuses them. Re-read after an error or a change.
- `get-voice-context` failing with "No voice profile" is an answer (no voice yet), not a fault. No accounts or no voice: hand to [start](start.md).
- **The summary** ([today-what-needs-me.md](today-what-needs-me.md)): read fresh, all at once. At most 5 lines (per brand), no empty ones; Running: each Bolta routine's next drafts (day, time), each campaign's week. Then the most urgent next step: one question only. Waiting = `total_team` + `total_recurring`; reply drafts (`total_hunter`) count apart. Never name Bolta's writer (`post_creator`).
- **Choose quietly.** One thing now: [post](post.md). "Every", "weekly", "keep posting", "each time X": [routine](routine.md). "Launch", "sale", "event", "for 3 weeks", "by Nov 3": [campaign](campaign.md). Unsure? Can they name the subject, the end, and want a verdict? Any no: [routine](routine.md). Still unclear? Ask once: "Should this keep going with no end, or is it about one thing that ends?"
- **Read Bolta's own state.** A Bolta routine's `display_state` and `pause_reason`, a draft's `expires_at`, a post's `reconnect_accounts`: show them, never re-derive them.
- Before the first reply, read [today-plain-words.md](today-plain-words.md): words to use and never say, how to show results.
- **The one next step**: the first that applies; the only question. In a scheduled run, the summary is the whole job; the next step is a suggestion.
  1. Something broke: fix that.
  2. Posts waiting: "Want to go through the 6 waiting?" ([review](review.md))
  3. A campaign ended: "Want the verdict on Spring sale?" ([campaign](campaign.md))
  4. Nothing going out this week: "What do you want to post about this week? I'll write the posts." ([post](post.md); skip if they said).
  5. No Bolta routine on: "Want Bolta to write 5 LinkedIn and X drafts every Monday at 8 am, about what Acme does? They wait for your yes, and it uses credits each run." ([routine](routine.md); name the networks they post on).

## Tools

- `list-workspaces`, `get-workspace`, `list-accounts`, `get-voice-context`: the look-once reads.
- `list-inbox-items`: what waits for a yes; finished reports (`source="report"`, `status="approved"`).
- `list-scheduled-posts` with `start_date`/`end_date` for the next 7 days; each row's `reconnect_accounts` names a disconnected account holding it up.
- `list-workspace-posts` with `status="failed"`: what didn't go out.
- `list-routines`: Bolta routines on, next drafts.
- `list-content-campaigns`: each campaign's week or end.
- `get-connect-link`: a reconnect link.
- `get-my-capabilities`: only after a refusal.

## Hand off

[start](start.md): set up, first week. [post](post.md): write now. [review](review.md): decide and schedule what's waiting. [routine](routine.md): anything every week, or changing one. [campaign](campaign.md): a launch, offer or event, and its verdict. [results](results.md): how it did. [voice](voice.md): "that's not me", what Bolta learned. [replies](replies.md): comments, conversations to join. [connect](connect.md): accounts, account groups, access. [fix](fix.md): undo, stop everything, nothing went out. [my-workflow](my-workflow.md): save this, run it on the app's own schedule.

## Always

- Follow the house rules in the Bolta skill.
- This playbook only reads.
