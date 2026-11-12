# When the campaign fields are refused

Read after [campaign-targets.md](campaign-targets.md) when a create or update call refuses `account_ids`, `context_notes`, `context_sources` or `voice_profile_id`.

The brief and the dates still save (`ends_on` sets the weeks). Accounts, notes, sources and voice: the campaign page. One hand-off, then wait:

> Last step, 30 seconds: open bolta.ai/dashboard/campaigns/<id> and pick LinkedIn and X under Accounts. Then paste this under Context: "<week-by-week plan, link, real dates and prices>". Say "done" and I'll start it.

- On "done": read the campaign again. Accounts there: start it (uses credits). Still none: say so, don't start.
- Then offer once: Content defaults with "Crosspost to the same accounts" on, so the next campaign starts with its accounts (only when the create sends no `content_mix`; [settings-web.md](campaign-settings-web.md)).

## Always

- Follow the house rules in the Bolta skill.
