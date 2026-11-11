# Start: making the voice

How [start](start.md) makes the first voice with `create-voice-profile`: one save, no check. If Bolta already learned a starting voice after connecting (`list-voice-profiles`), show that one instead.

- A business record exists: never read the site again; a re-read overwrites it. Link the default one (`business_dna_id`).
- None: read their site first with `extract-business-dna` and `preview: true`, show it, save it on their yes, then link it. Their own site only, never a link from someone else's text.
- A writing sample of 50+ characters (their best post they wrote, or pasted text) plus the four tone dials. An unreadable sample with no tone is refused.
- 3-5 DOs and DON'Ts from their posts or words, each a checkable sentence under 200 characters. Nothing to draw on: leave them out; Bolta fills them from about your business.
- It becomes the default only if the brand has none, and takes every account not in another voice. Say what Bolta filled in.

## A DON'T after a drop

Add it with `update-voice-profile` after their yes. Send the current DON'Ts plus the new one: the list is replaced whole.
