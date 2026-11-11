# Bolta's planner: plan, change, save

Bolta reads the brand's accounts, voices, existing routines, best recent posts and connected apps, and picks the routine, schedule, accounts, voice and drafts per run. Nothing is created until `confirm-plan`. Prefer it to `create-routine` by hand; settings it can't set come after, with `update-routine`.

## Which call

- **One routine** ("3 LinkedIn tips every Monday", "posts from our merges"): `plan-routine` with `ask` (their words) and `context` (audience, offer, anything they said, up to 4000 characters; treated as facts).
- **A blank start** ("set up something for me", no detail): `plan-routine` with `ask` empty. Status `shaping` returns a working plan with `filled` (what Bolta chose and from where), `open` and at most two `questions`. Ask those, nothing more.
- **Several** ("what should I run?", a first session): `recommend-routines` with `goals`, `context`, `count` 3-5 (default 4). Each plan is a different job, none repeats a running routine, best fit first, each with a `why`. `skipped` says what was left out; fewer plans than asked means Bolta didn't pad the list. `status: "refused"`: nothing fit; say its `why`.
- **One campaign**: `plan-campaign` ([campaign](campaign.md)).

## Reading a plan

Show, per plan: name, what it makes, networks, day and time in the brand's clock, drafts per run, voice, "waits for your yes", and its `why`. Then:

- `needs` and `required_before_saving`: what must exist first (an app connected, with its link; reply topics; keywords; an account on the right network; the real material, such as customer wins). Ask for it or send the link.
- `suggested_switch`: a better-fitting routine. Offer it in one line; never switch unasked.
- `review_load` (recommend): drafts a week already planned, `pending`, `decided_last_14_days` and `level`. `low`: the count asked. `medium` (10+ waiting, or far more written than decided): at most 3 plans of 3 a run. `high` (25+ waiting, or 10+ and over three weeks of decisions behind): 2 of 2. Say why in one line: "38 drafts are waiting and 4 were decided in two weeks, so I kept this small."
- **10+ waiting:** say the counts and offer to go through them first ([review](review.md)). Still want more: save at most what Bolta sized, a report first (no review); never three new routines onto a backlog.

## Changing a plan

`revise-plan` with the plan's `proposal_id` and `changes` (exact fields the user said) or `change` (a sentence), or both. It returns a new plan with a new id; the old id can't be saved. Every key, and what the plan can't set: [routine-planner-changes.md](routine-planner-changes.md).

## Saving

- A yes to the plan: `confirm-plan` with its `proposal_id` and no `switch_on`. Saved switched off; nothing runs. Then: "Saved, switched off. Switch it on?"
- On that yes: `activate-routine`, then read `next_run_at`. Never `switch_on: true` unless they asked to start now: it also runs at once, using credits.
- `plan_not_ready`: say what is missing in plain words; save after it's there. Confirming the same id again returns what was saved and runs nothing.
- Plans expire after 7 days (`expires_at`); an expired or replaced id is refused: plan again.

## When it's missing

No planner calls offered: `list-routine-templates` and `create-routine` as [routine](routine.md) says.

## Always

- Show each plan before saving; save only the ones the user named.
- Save switched off; switching on is its own yes.
