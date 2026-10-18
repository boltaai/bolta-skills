# Campaign and Bolta routine results

Read for one campaign's results, comparing campaigns, or a Bolta routine. Finishing a campaign: hand to `campaign`. Bolta works these numbers out on every read, so read again each time; never reuse earlier numbers.

## A campaign: `get-content-campaign`

Say it in this order.

1. **The outcome line**, from `results.outcome`:
   - `no_results_yet`: early. Nothing out yet.
   - `in_progress`: going out, more to come.
   - `published`: finished, and posts went out.
   - `published_nothing`: finished, and nothing went out. Give the reason (below).
2. **How it ran:** `results.total_posts` made, then `pending_review` (waiting for your yes), `draft` (still drafts), `rejected`, `deleted` (dropped), `quality_blocked` (held back: needs a human edit), `scheduled` and `publishing` (not sent yet), `failed`. `results.runs` says how often Bolta wrote and how often that failed; `schedule_status.last_error.message` is already a plain sentence.
3. **Where it went out:** `results.published` counts posts live on at least one account. `results.by_platform` gives went out, failed and pending per network. `results.partially_published`: "went out on 2 of 3 accounts". `published_unverified` counts as out, with no per-account record behind it.
4. **The decision rate:** undecided is `pending_review` plus `draft`; decided is the rest of `total_posts`. "You decided 10 of 12."
5. **Engagement**, only from `results.engagement`. `measurable_posts` above `measured_posts` means some aren't measured yet. To name the best post, match the campaign's post ids against published posts read with metrics.

**When nothing went out**, `results.outcome_reason` names the first thing that stopped it:
- `no_accounts_connected`: nothing could go out.
- `runs_failed`: every time Bolta tried to write, it failed. Say the last error.
- `not_started`: it never started.
- `nothing_generated`: Bolta ran but wrote no drafts.
- `quality_blocked`: drafts were held back and need a human edit.
- `publishing_failed`: every send failed, usually a disconnected account.
- `awaiting_approval`: waiting for your yes. The usual answer.
- `nothing_approved`: drafts were seen and none got a yes. Also shown for drafts I wrote that were never sent for review.
- `not_sent_yet`: approved; their times haven't come.
- `unknown`: Bolta can't tell. Look at the posts.

**Its posts:** `list-content-campaign-posts` returns every post, oldest first. It ignores `status` and `limit`, so filter yourself. `has_pending_review: true` means waiting for a yes.

**A campaign I wrote** stays "not started" on the dashboard. Its results still count its posts. Give the read and leave the status alone.

## Comparing campaigns

- Few went out: say where it stopped, not that the strategy failed.
- First run of a strategy: too early to drop it. The first run had the thinnest context.
- Two campaigns teach something only if they differ in one thing, ideally the strategy.

## A Bolta routine: `get-routine`, `list-routine-runs`

- `performance_summary` covers every run since it began, not the user's window: `runs`, `runs_failed`, `artifacts_created` (drafts made), `artifacts_approved` (got a yes), `artifacts_published` (went out), `artifacts_rejected` (got a no), `artifacts_awaiting_review` (waiting for your yes).
- Decision rate: approved plus rejected, out of drafts made. Dropped drafts leave the count.
- `list-routine-runs` gives up to 50 runs, newest first, each with a status and `artifacts`: `created`, `awaiting_you`, `scheduled`, `published`, `failed`.
- In a run, `failed` drafts got a no, lapsed or were dropped: not errors. A run marked failed with "No drafts from this run were approved" means none got a yes. Say that, not "it broke".
- Counts are per post. A post out on only some accounts may show as scheduled. If "went out" looks low, check the posts.
- Engagement per Bolta routine isn't readable from here. One line, one link: its page at bolta.ai/dashboard/routines/<id> shows it.
- No run when one was due: `routine`. Drafts waiting now: `review`.
