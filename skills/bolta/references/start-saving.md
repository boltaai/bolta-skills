# Start: saving what they picked, then switching on

Read with [start](start.md) when the user answers the proposal. A yes to set up is a yes to save; switching on is its own yes.

## In short

- "Set up 1 and 2" is a yes to save, not to switch on. Save each now, switched off (`confirm-plan` with no `switch_on`, or `create-routine` with no `activate-routine`), then ask "Switch both on?" Never ask before saving.
- On "switch them on": `activate-routine` each, then read `next_run_at` back. Never `switch_on: true`: it also runs at once and spends credits.

## The order on their yes

1. **Optional brand and voice:** only if they agreed to its preview: `extract-business-dna` with `setup: true`, the same `url` and their words, then `check: true` until done ([start-brand-setup.md](start-brand-setup.md)). That yes covers the record and voice; never make a second voice. No website: [no-site setup](start-brand-setup-no-site.md). Skip this step for a routine-only yes.
2. **If setup ran:** show what it made, the two scores and `setup.dashboard_url`.
3. **Accounts:** name selected usable accounts. None connected: compatible drafts can start without one; offer `get-connect-link` for publishing. Required source, history and company-page bindings still apply.
4. **Routines:** save each one they picked, switched off. Never one they didn't pick.
5. **One question:** "Saved, switched off: Weekly coffee tips, Friday roundup. Switch both on?"

## Saving with Bolta's planner

- `confirm-plan` with that plan's `proposal_id` and no `switch_on`.
  - `switch_on` default false: a routine is saved switched off, a campaign as a draft; nothing runs.
  - `switch_on: true` saves, switches on and starts the first run at once, which uses credits. Never send it here: switch on with `activate-routine` instead, which waits for the schedule.
- Each plan has its own id; save them one by one.
- A change first ("Tuesdays instead", "only 2"): `revise-plan` with their words as `change`. It returns a new id; the old id can no longer be saved.
- Refused as `plan_not_ready`: the plan still needs something (a connection, reply topics). Say what, in plain words; save the others.
- Confirming the same id twice returns what was saved and runs nothing.

## Saving without the planner

`create-routine` as [routine](routine.md) says, with `approval_policy: "review_every_artifact"` (ask me first) and no `activate-routine`. Accounts not connected yet: bind them once connected ([routine-settings.md](routine-settings.md)); say so.

## Switching on

- Only on "switch them on" or the like: `activate-routine` for each, then read `next_run_at` from the result and say it in the brand's clock: "On. First drafts Tue Nov 17, 8:00 am (Sydney)." Never work the time out yourself.
- Switching on is not running. Never run a routine now in the first session: a run uses credits and the schedule will bring the first drafts.
- A campaign plan saved by `confirm-plan` is a draft, not started. Starting it is its own yes ([campaign](campaign.md)).
- No voice yet: offer setup if useful, without blocking a compatible draft routine. Real founder events and customer outcomes still need supplied evidence.

## Stopping early

They pick nothing, or stop after saving: say the state as it is. "Saved, switched off: Weekly coffee tips. Nothing is running. Say 'switch it on' when you're ready."

## Always

- Save only what they picked; switch on only after its own yes.
- Read the first-drafts time back from Bolta; never promise to check in later.
