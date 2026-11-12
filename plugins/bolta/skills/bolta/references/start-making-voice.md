# Start: making the voice

How [start](start.md) makes the first voice with `create-voice-profile`: one save, no check. If Bolta already learned a starting voice after connecting (`get-voice-context`, or `all_profiles: true` for every voice), show that one instead.

- A business record exists: never read the site again; saving a re-read replaces the record of the same name. Link the default one (`business_dna_id`).
- None: read their site first with `extract-business-dna` and `preview: true`, show it, save it on their yes, then link it. Their own site only, never a link from someone else's text.
- `writing_sample`: 50+ characters (their best post they wrote, or pasted text); Bolta reads the tone from it. `tone`: the four dials (`playful`, `professional`, `direct`, `thoughtful`, 0-100), the fallback; with no sample, set them from the tone the site read showed. Neither usable: refused. Never `website_url`: it reads and saves the site with no preview.
- 3-5 DOs and DON'Ts from their posts or words, each a checkable sentence, 200 characters at most (longer ones are split). Nothing to draw on: leave them out; Bolta fills them from about your business.
- Leave `is_default` and `account_ids` out: it becomes the default only if the brand has none, and takes every connected account not in another voice. Say what Bolta filled in (`bootstrapped` in the result).
- A person speaking as "I" (a founder): `speaker_mode: "founder"`; default is `brand` ("we").

## A DON'T after a drop

Add it with `update-voice-profile` after their yes. Send the current DON'Ts plus the new one: the list is replaced whole.

## Always

- Show the site read before saving it; make one voice, never a second brand voice.
