# Brand settings

Each `list-workspaces` row is one brand's full settings. Read it once per brand and reuse it.

## What it returns

- **Clock:** the brand's time zone. Times are wall clock in it; never add a UTC offset.
- **Review mode** (`safe_mode`, "Safe Mode" in the brand's Settings > Rules): everything beyond a draft waits for a yes, and nothing posts right away.
- `default_reviewer_ids`: who reviews by default.
- `autonomy_mode` (Default automation level): at auto or aggressive, routines, campaigns and jobs that follow the brand publish without review. Posts made through this connection still wait for a yes.
- `approval`: in plain words, whether work publishes without review there, with its `updated_at`.
- `connection_automation_permission` (`granted`, `not_granted`, `not_asked`): whether this connection may loosen approval or automation there.
- `connection_turned_off`: what an owner or admin turned off for this connection on that brand. Don't try those tools there; say it was turned off for this connection and can be turned back on in Bolta: Settings > API > AI app connections.
- `transcript_processing_enabled`: whether Bolta processes transcripts for this brand.

## Changing them

- The time zone changes only at bolta.ai/dashboard/settings, by an owner or admin, under the brand's Overview. Name the page; never claim a change was made.
- Safe Mode and the Default automation level: in Bolta (Settings > Rules > Approvals), or here with `set-brand-approval`, on the user's words only ([brand approval](connect-brand-approval.md)).
- Never suggest turning review mode off to get past a refusal.
- More on clock, review mode and "Is everything set up?": [team-and-integrations](connect-team-and-integrations.md).

## Always

- Follow the house rules in the Bolta skill.
