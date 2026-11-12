# Start: a brand with no website, and its colours

Read with [start-brand-setup.md](start-brand-setup.md) once they said there is no website, or after any setup that left colours, fonts and logo empty.

## Without a website

They said there is none: Bolta's same setup, from their words.

1. **Preview** the findings and their notes as a brand (positioning, products, writing rules, topics, a sample post), in their words: products by the names they gave, no descriptions or benefits they didn't say, no spelling or region guessed. Assumptions as statements, one question: "Save this?".
2. **On their yes:** `extract-business-dna` with `setup: true` and no `url`, plus `notes` (their words about the business; `notes` or `writing_samples` is required), `writing_samples`, `audience`, `goals`, `products`, `favorite_creators`: only what they said or shared. It makes the business record from their words, the voice (a thin Starter Voice is filled, never a second), and assigns the accounts.
3. **Follow it** with `check: true` until done, then show what it made, the two scores and `setup.dashboard_url`. `setup.without_website` lists what a site would add: say it in a line and that sharing the site later only fills gaps; never ask again. Then the colours question below, in the same reply.

An older Bolta that refuses a setup with no `url`: `create-voice-profile` from the same words ([start-making-voice.md](start-making-voice.md)).

## Colours, fonts and logo

A brand set up with no website has none. After it's saved, ask once, optionally: "Have brand colours, fonts or a logo? Paste them, or share an image of your logo."

- Hex codes or font names they paste: saved as given with `update-business-dna` `fields` (`colors` as hex strings, `fonts`, `visual_aesthetics`, `logo_url`) on the brand's record (`setup.business_dna`, or `list-business-dna`).
- From a logo image, colours are an estimate: "Looks like #1F3A5F and #F2B705, right?" Save only after a yes. Never guess fonts from an image.
- Nothing given: leave it blank; they can add it on the Brand page or by sharing their website later. Never invent visuals.

## Always

- Never invent a colour, a font, a logo or a fact; ask once, then leave it.
