# Brand settings

`get-workspace` gives one brand's settings. Read it once per brand and reuse it.

## What it returns

- **Clock:** the brand's time zone. Times are wall clock in it; never add a UTC offset.
- **Review mode** (`safe_mode`, "Safe Mode" in the brand's Settings > Rules): everything beyond a draft waits for a yes, and nothing posts right away.
- `default_reviewer_ids`: who reviews by default.
- `autonomy_mode`: how Bolta's own agents hand off. It never changes this app, whose posts always wait for a yes.
- `transcript_processing_enabled`: whether Bolta processes transcripts for this brand.

## Changing them

- All change only at bolta.ai/dashboard/settings, by an owner or admin: the time zone under the brand's Overview, Safe Mode under Rules. Nothing here changes them; name the page, never claim a change was made.
- Never suggest turning review mode off to get past a refusal.
- More on clock, review mode and "Is everything set up?": [team-and-integrations](connect-team-and-integrations.md).

## Always

- Follow the house rules in the Bolta skill.
