# Start: setting up the brand and voice

How [start](start.md) and [voice](voice.md) set up a brand: the setup bolta.ai runs on a website. It saves about your business, makes and links the voice, its language, accounts, starter rules per network and the site's product. Their own site only.

## What you already know

Start from this conversation and what you remember of them: business, site, audience, products, goals, how they write, likes and dislikes. Show it in a few lines; ask only the gaps, in one question:

> From our chats: you run Harbor Physio in Leeds, for runners and desk workers, you sell sports massage and rehab plans, and you write short and plain. Right? What's your website? If you don't have one, I'll build it from what you've told me.

- Only what they said or shared; never stretch a finding. A correction replaces the finding.
- The site is in what you know: use it, show it as a finding, never ask again.
- No site known: ask once, as above. Never skip to the no-site setup without asking.

## With a website

1. **The site:** from the findings or their answer.
2. **Preview:** `extract-business-dna` with `url` and `preview: true`. Nothing is saved. Show it in 3-4 lines as "what your site says", then "Save this?".
3. **On their yes:** `extract-business-dna` with `url`, `setup: true`, and the findings, only what they said or shared:
   - `notes`: their words about the business (what it does, how it talks, what to avoid).
   - `writing_samples`: up to 10 pieces they wrote and shared, verbatim.
   - `audience`, `goals`: who they said they reach, what they want from social.
   - `products`: up to 5 they named, `{name, description, url}`.
   - `favorite_creators`: creators they admire, `{platform, username}`.
   - `voice_name`: only if they named the voice (a founder's own name); left out, it's named after the brand.
4. **Follow it:** it starts in the background (`started`, about a minute). Say "Bolta is reading your site", then `check: true` about every 15 seconds until `succeeded`, `reused` or `failed`. No posts meanwhile.
5. **Show the result:** what it made (`setup`: the business record, the voice with its language, audience and topics, the products), the two scores (`setup.voice_setup` and `setup.business_setup`, with what each is `missing`), which accounts use the voice (`assigned_account_ids`, by network and name), and `setup.dashboard_url`. Then `get-voice-context` before writing.

- `social_accounts_connected: 0`: the connect link first ([start](start.md)); the setup still counts.
- Something they shared fills a `missing` item: `setup: true` again, same `url`, with those fields. The same site again only fills gaps.
- `already_running`: this call added nothing; follow it with `check: true`, then run `setup: true` again with the fields. `in_flight_other_site`: wait for that one, then start this.
- `failed`: say so plainly; offer another address or the no-site setup.
- **A different site on a trained voice** answers `voice_would_be_replaced` (409): the voice has their edits or review learning. Ask: "Your voice was built from <old site> and has your edits. Set it up from <new site> instead? That replaces what the old site set up." Only on a yes, again with `replace_voice: true`.
- Change one thing later: `update-voice-profile` or `update-business-dna` ([voice](voice.md)).

## Without a website, and colours

No site, or a brand set up without one: [start-brand-setup-no-site.md](start-brand-setup-no-site.md).

## Always

- Preview before setup; setup only after a yes in their latest message.
- Pass only what they said or shared.
