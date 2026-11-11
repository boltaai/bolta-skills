# Why nothing happened

Read when a campaign seems stuck or nothing went out. One fresh `get-content-campaign` answers most of it: the phase, the last error, the outcome.

## 1. The phase: `schedule_status.state`

- `draft`: not started. Start it, unless it's one I wrote (then it never starts; see [review](review.md)).
- `paused`: paused. Resume it (one Bolta check). If its only account was removed, set one first.
- `scheduled` with `next_generation_at`: next drafts then, in the workspace clock. Wait, or press "Generate now" on the campaign page to write them early (uses credits).
- `scheduled` with no `next_generation_at`: armed but never started. Start it.
- `generating`: writing this week's drafts. Wait a few minutes.
- `needs_accounts`: needs accounts. Set them ([targets.md](campaign-targets.md)) or pick them on the campaign page. With a `starts_on` it restarts by itself; without one, press "Generate again".
- `needs_review`: waiting for you (`posts_to_review`). Hand to [review](review.md).
- `posting`: posting. Nothing to do.
- `done`: finished. Give the verdict ([verdict.md](campaign-verdict.md)).
- `active` and nothing else: on, nothing due yet. Run the checks below.

## 2. On, but not writing? Check in this order

- **On?** Only an on campaign writes. Not started or paused: start or resume it (the phase lines above).
- **A start date?** No `starts_on`: no weekly schedule. It writes once when started; "Generate again" writes more.
- **Usable accounts?** None picked, or all disconnected: needs accounts. Adding one (targets.md, or the campaign page) restarts a dated campaign; no second start.
- **Bolta's writer paused?** `blocked` is set: Bolta won't write until its writer is resumed on the dashboard.
- **This week already written?** `last_generated_on` (a week start) is this week or later: look at its drafts.
- **Window closed?** `window_closed` true: nothing more comes. Start a new campaign.
- **The last error:** `schedule_status.last_error.message` is already a plain sentence. Say it as given.
  - With `retry_at`: Bolta tries again by itself then. Say the time; don't press anything.
  - No `retry_at` (a failed run): press "Generate again" at bolta.ai/dashboard/campaigns/<id>. It uses credits.
  - `code` is `insufficient_credits`: relay its "N left, M needed" text. Bolta checks again by itself; after a top-up, "Generate now" on the campaign page tries at once.

## 3. Nothing went out?

Read `results.outcome` and `results.outcome_reason`: [why-nothing-outcome.md](campaign-why-nothing-outcome.md) says what each one means and what to say.

## Worth knowing

- "Nothing went out" is nearly always waiting for your yes.
- A campaign I wrote shows `nothing_approved`: its drafts were never sent for review. Say they're still drafts, then [review](review.md).
- A full calendar proves nothing: it shows what exists, not what went out.
- Drafts landing late around 17:45-18:15 UTC (say it in the workspace clock): Bolta's servers were busy, not a problem with the campaign.
