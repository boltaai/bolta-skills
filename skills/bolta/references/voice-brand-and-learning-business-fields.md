# About your business, and how drafts use the voice

Read before editing about your business, reading a second site, calling `update-business-dna`, or explaining tone dials and example posts. Person voices and what Bolta learns: [voice-brand-and-learning](voice-brand-and-learning.md).

## Which record a voice reads

- `list-business-dna` first. A brand can hold several records. A voice reads the one it is linked to; an unlinked voice reads the brand's default. With several records and none the default, unlinked voices get no business facts: ask them to choose one in Brand > Business.
- `update-voice-profile` with `business_dna_id` points one voice at another record; an empty value unlinks it.
- Reading a second site: give a new `name` (such as "Acme shop site, Nov 2026") and send `set_as_default` false. With default arguments a read under a name already in use overwrites that record's tagline, colors, overview and rules, and makes it the default.
- No tool deletes a record or makes an existing one the default; both are in Bolta.

## Send only what changed

`update-business-dna` with `fields`: only the changed keys. Edit the record the voice in use reads. Show the before and after in one line first; it gets the same Bolta check as a voice change.

- **Basics:** `name`, `tagline`, `business_overview`, `website_url`, `brand_values`.
- **Image look:** `colors` (hex), `fonts`, `visual_aesthetics`, `logo_url`, `logo_placement` (bottom-right, top-left, center, subtle-background or none), `custom_image_instructions`, `tagline_on_images`.
- **Local details:** `city`, `neighborhood`, `service_area`, `years_in_business`, `owner_name`, `staff_names`.
- **Story:** `origin_story`, `community_involvement`, `testimonials` as `[{"name": "...", "quote": "..."}]`, real ones only.

Image fields steer images Bolta makes. Fonts and logo placement are guidance to the image model, not exact layout: never promise them.

Why it matters: routine and campaign drafts take their facts from this record. A thin overview gives generic drafts, however good the voice.

## How drafts use the voice

Routines, campaigns and single posts all write through a voice, so one rule change shapes all of them.

- Tone dials matter only past the middle: a tone quality shows up at 55 or above, formality at 25 or below or 75 or above, and pacing moderate adds nothing.
- Example posts are up to 3: drafts a person approved or edited for that voice come first, then the voice's accounts' own top posts.

## No description yet

`business_overview` missing: "Bolta has no description of Acme yet. Tell me what you do in two sentences and I'll add it." No record at all: offer to read their own site ([voice-setup-and-documents](voice-setup-and-documents.md)).
