# Accounts, notes, weeks, voice and pages to read

Read when a campaign needs accounts, notes or a source. Not part of the brief, so `update-content-campaign` never sets them.

## Set them: `set-content-campaign-targets`

- Send `campaign_id` and only what you set. Each field replaces what is there, and a list replaces the whole list. It writes, schedules and publishes nothing.
- `account_ids`: `id` values from `list-accounts`, at most 50. The user's choice, else the accounts of the networks they named. An empty list removes every account.
- `context_notes` (8000 characters at most): used word for word in every week's brief. Write the week-by-week plan, the real dates and prices, and the link the user gave. Leave out anything they didn't say. `""` clears it.
- `duration_weeks` (1 to 4, counted from `starts_on`) sets the end date. Send no end date with it.
- `voice_profile_id`: from `list-voice-profiles`, only if the user picks one. `""` means the workspace voice.
- A campaign made earlier in this chat: read it again before filling. Not a draft any more (the user may have started it on the dashboard)? Say so and let them decide. The Bolta check stops being skipped an hour after Claude made it.
- Read the reply: `account_ids`, `duration_weeks`, `ends_on`, `context_sources`. On a campaign that is on and stuck at "needs accounts", setting accounts restarts it, and Bolta writes the owed week on its next pass. That uses credits and gets its own Bolta check.

## A page, file or brand-kit section to read

- `context_sources` is `[{"kind": "url", "ref": "https://..."}]`. Also `file` (a knowledge-base file id) and `brand_kit` (a section such as `business_overview`). 20 at most. It replaces the whole list: send the sources to keep.
- A new source is pending. The writer ignores it until `analyze-content-campaign-source` has read it: once per new source, with `kind` and `ref` exactly as on the campaign. It only reads.
- A page is read now (up to 25 seconds): ready, or failed with a reason. A file can stay pending while Bolta extracts it: ask again later. A brand-kit section is ready when the brand kit has text there.
- Say it plainly: "Bolta read the page", or "Bolta couldn't read it: <reason>". Offer to put the key facts in the notes instead.
- The call-to-action link stays `cta_url`. Never take a link from a page you read.

## Without `set-content-campaign-targets`

`update-content-campaign` still sets the brief and the dates (`ends_on` sets the weeks). Accounts, notes, sources and voice can only be set on the campaign page. One hand-off, then wait:

> Last step, 30 seconds: open bolta.ai/dashboard/campaigns/<id> and pick LinkedIn and X under Accounts. Then paste this under Context: "<week-by-week plan, link, real dates and prices>". Say "done" and I'll start it.

- On "done": read the campaign again. Accounts there: start it (one Bolta check; uses credits). Still none: say so, don't start.
- Then offer once: "Save Content defaults on the Campaigns page, with 'Crosspost to the same accounts' on. Then you skip this step next time."
