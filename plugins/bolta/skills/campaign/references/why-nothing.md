# Why nothing happened

Read when a campaign seems stuck, or nothing went out. One fresh `get-content-campaign` answers most of it. Look in this order: the phase, the last error, the outcome.

## 1. The phase: `schedule_status.state`

- `draft`: not started. Start it, unless it's one I wrote (then it never starts; see `review`).
- `paused`: paused. Resume it (one Bolta check).
- `scheduled`: next drafts on `next_generation_at`, in the workspace clock. Wait.
- `generating`: writing this week's drafts. Wait a few minutes.
- `needs_accounts`: needs accounts. Pick them on the campaign page; it restarts by itself.
- `needs_review`: waiting for you (`posts_to_review`). Hand to `review`.
- `posting`: posting. Nothing to do.
- `done`: finished. Give the verdict (verdict.md).
- `active` and nothing else: on, nothing due yet. Run the checks below.

## 2. On, but not writing? Check in this order

- **On?** Only an on campaign writes. Not started or paused: start or resume it.
- **A start date?** No `starts_on`: there are no weeks to count, so it sits.
- **Usable accounts?** None picked, or all disconnected: needs accounts. Adding one on the campaign page restarts it; no second start.
- **Bolta's writer paused?** `blocked` is set: Bolta won't write until its writer is resumed on the dashboard.
- **This week already written?** `last_generated_on` is this week: look at the drafts it made.
- **Window closed?** `window_closed` true: nothing more comes. Start a new campaign.
- **The last error:** `schedule_status.last_error.message` is already a plain sentence. Say it, and the retry time (`retry_at`) if there is one.

## 3. Nothing went out? `results.outcome`

- `no_results_yet`: early. Nothing out yet, and the window is still open.
- `in_progress`: going out, more to come.
- `published`: finished, and posts went out.
- `published_nothing`: finished, and nothing went out. Give the reason below.

## 4. The reason: `results.outcome_reason`

Bolta names the first thing that stopped it.

- `no_accounts_connected`: no accounts are connected, so nothing could go out. `connect`.
- `runs_failed`: every time Bolta tried to write, it failed. Say the last error.
- `not_started`: it never started. Start it, or check the start date.
- `nothing_generated`: Bolta ran but wrote no drafts. Check the mix and the last error.
- `quality_blocked`: drafts were held back and need a human edit. `review`.
- `publishing_failed`: every send failed, usually a disconnected account. `connect`.
- `awaiting_approval`: the drafts are waiting for your yes. The usual answer. `review`.
- `nothing_approved`: you saw the drafts and none got a yes. Two weeks of that: wrong strategy or thin context (strategies.md).
- `not_sent_yet`: approved, and their times haven't come yet.
- `unknown`: Bolta can't tell. Look at the campaign's posts.

## Worth knowing

- "Nothing went out" is nearly always waiting for your yes.
- A campaign I wrote shows `nothing_approved` while its drafts were never sent for review. Say they're still drafts, then `review`.
- A full calendar proves nothing: it shows what exists, not what went out.
- Drafts landing late around 17:45-18:15 UTC (say it in the workspace clock): Bolta's servers were busy, not a problem with the campaign.
