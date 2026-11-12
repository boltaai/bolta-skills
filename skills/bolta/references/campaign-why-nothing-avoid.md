# Why most empty campaigns are empty, and how to avoid it

Read before starting a campaign, and when one made no posts at all. In Bolta, most campaigns that never made a post were **saved and never started**, or started with nothing to post to. Bad drafts are the rare cause; when people do decide campaign drafts, they mostly say yes. The next most common loss is drafts nobody decides.

## The causes, most common first

1. **Never started.** Creating, the planner's save and a duplicate all leave it not started (`status` draft). Only `activate` makes Bolta write. Fix: show the plan, ask "Start it?", activate, read `status` back.
2. **No accounts.** It switches on, then waits at `needs_accounts`. Fix: `update-content-campaign` with `account_ids`; a dated campaign restarts by itself.
3. **No strategy.** A blank strategy with a mix or Content defaults reaches the writer with no angle; those drafts get sent back far more often. Fix: always send `strategy_key`.
4. **Sources never read.** Web-made and duplicated campaigns start with sources unread, so the writer works from the notes alone. Fix: `analyze-content-campaign-source` for each source not `ready`.
5. **Start date in the past.** Weeks already over are skipped. A 1-week campaign started late can have nothing left (`window_closed`). Fix: move `starts_on` forward before starting.
6. **Formats the networks can't take.** A blog with no WordPress site, text for Instagram or TikTok, a carousel for X: written, then refused or held ([settings-formats.md](campaign-settings-formats.md)).
7. **Billing.** No paid plan ("Your plan doesn't include campaigns yet"), or `insufficient_credits` in `schedule_status.last_error`: Bolta rechecks by itself after a top-up.
8. **Nobody decided.** Drafts wait for a yes, then expire 30 days after their planned time. Too many a week is the usual reason: size to what the user decides in one sitting.
9. **Video without its video.** A video draft that came back with no video can't go out and usually expires.

## Before every start: the check

Read `get-content-campaign` and say any miss in one line:

- `strategy_key` set; `theme` is the real subject.
- `starts_on` today or later, the event in the last week; `ends_on` within 4 weeks.
- `account_ids` not empty (unless the brand has nothing connected).
- Every `context_sources` row `ready`, or its failure said.
- `resolved_content_mix` fits the accounts' networks.
- Weekly drafts from all running routines and campaigns, plus this one, still fit one sitting.

## A campaign that made nothing: the diagnosis

1. `list-content-campaigns`, then a fresh `get-content-campaign` for the one meant.
2. `status` draft: never started. Run the check, then ask to start it.
3. Active: read `schedule_status.state` and `last_error` ([why-nothing.md](campaign-why-nothing.md)).
4. Finished: `results.outcome_reason` ([why-nothing-outcome.md](campaign-why-nothing-outcome.md)).
5. Its dates have passed: a not-started one gets a new `starts_on` (`update-content-campaign`) before starting. A finished one can't start again: offer a new campaign with the same brief, the fixes and a future start.

Worked example: [campaign-made-nothing](../examples/campaign-made-nothing.json).

## Always

- Never call a campaign running until `status` reads active and it has accounts.
- Say the cause from what was read, never a guess.
- Follow the house rules in the Bolta skill.
