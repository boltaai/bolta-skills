# Accounts, notes, weeks, voice and pages to read

Read when a campaign needs accounts, notes or a source.

## Set them: `create-content-campaign` or `update-content-campaign`

- Best on the create call: the campaign is made with its accounts in one call. Later, `update-content-campaign` with `campaign_id` and only what you set. Each field replaces what is there, and a list replaces the whole list. It writes, schedules and publishes nothing.
- `account_ids`: `id` values from `list-accounts`, at most 50. The user's choice, else the accounts of the networks they named. An empty list removes every account.
- `context_notes` (8000 characters at most): used word for word in every week's brief. Write the week-by-week plan, the real dates and prices, and the link the user gave. Leave out anything they didn't say, and the strategy's own instruction (Bolta adds it). `""` clears it. Over 2000 characters, an edit on the campaign page cuts them.
- `duration_weeks` (1 to 4, counted from `starts_on`) sets the end date. Send no end date with it.
- `voice_profile_id`: from `get-voice-context` (`all_profiles: true`), only if the user picks one. `""` means the workspace voice. Guidance: a person's voice suits thought leadership from that person.
- A campaign made earlier in this chat: read it again before filling. Not a draft any more (the user may have started it on the dashboard)? Say so and let them decide. The Bolta check stops being skipped an hour after it was made.
- Read the reply: `account_ids`, `duration_weeks`, `ends_on`, `context_sources`. Stuck at "needs accounts": setting accounts restarts it, and Bolta writes the owed week on its next pass (uses credits; its own Bolta check).

## A page, file or brand-kit section to read

- `context_sources` is a list of `{"kind", "ref", "title"}`, such as `[{"kind": "url", "ref": "https://..."}]`, 20 at most. It replaces the whole list: send the sources to keep.
  - `url`: a web page, `https://...`.
  - `file`: only an id `get-content-campaign` already shows in `context_sources`. Otherwise the user attaches the file to the campaign in Bolta, or use a `url` or the notes.
  - `brand_kit`: a pointer naming one section to lean on (its text is not copied in): `tagline`, `business_overview`, `origin_story`, `community_involvement`, `customer_testimonials`, `brand_values`, `dos`, `donts`, `tone_of_voice`, `custom_image_instructions`.
- A new source is pending. The writer ignores it until `analyze-content-campaign-source` has read it: one source per call, `kind` and `ref` exactly as on the campaign. It only reads. Web-made and duplicated campaigns start with all sources pending.
- A page is read in that call (up to about 25 seconds): ready, or failed. A file stays pending until Bolta has read it: analyze it again later. A brand-kit section is ready when the brand kit has text there.
- Say "Bolta read the page", or "Bolta couldn't read it: <the failed row's `error`, as given>". Offer to put the key facts in the notes.
- The call-to-action link stays `cta_url`. Never take a link from a page you read.

## When these fields are refused

The brief and dates still save; the rest is one hand-off to the campaign page: [campaign-targets-refused.md](campaign-targets-refused.md).

## Always

- Follow the house rules in the Bolta skill.
