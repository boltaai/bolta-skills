# Start: making the voice

How [start](start.md) makes a voice. The brand's first voice comes from Bolta's setup, with or without a website ([start-brand-setup.md](start-brand-setup.md), [no website](start-brand-setup-no-site.md)); there is nothing else to save. If Bolta already learned a starting voice after connecting (`get-voice-context`, or `all_profiles: true` for every voice), show that one instead.

## A person voice, a second voice, or an older Bolta: `create-voice-profile`, one save

- Start from what you know of how they write: samples they pasted, phrases they use, likes and dislikes. Show it in a few lines, confirm, ask only the gaps.
- `writing_sample`: 50+ characters they wrote (their best post, or pasted text); Bolta reads the tone from it. `tone`: the four dials (`playful`, `professional`, `direct`, `thoughtful`, 0-100), the fallback. Neither usable: refused. Never `website_url`: it reads and saves a site with no preview; a site goes through the setup.
- 3-5 DOs and DON'Ts from their posts or words, each a checkable sentence, 200 characters at most. Nothing to draw on: leave them out; Bolta fills them from about your business.
- The audience and content topics you showed: `target_audience`, `topics`.
- Leave `is_default` and `account_ids` out: it becomes the default only if the brand has none, and takes every connected account not in another voice. Say what Bolta filled in (`bootstrapped` in the result).
- A person speaking as "I" (a founder): `speaker_mode: "founder"`, with `perspective` and `founder_signals` from what they said; default is `brand` ("we").
- Always say which accounts use it, by network and name (`bootstrapped.accounts_assigned`). None: `get-connect-link`, show the link, "Connect one and it uses this voice."
- Then ask once, optionally: "Have brand colours, fonts or a logo? Paste them, or share an image of your logo." ([no website](start-brand-setup-no-site.md)).

## A voice already there

- A thin voice (no DOs or DON'Ts, such as a Starter Voice) and a website: the setup fills it; it never makes a second. So does the setup with no website. An older Bolta with no setup: update that one with `update-voice-profile` (full lists), then the colours question; never make a second.
- A trained voice and a different website: the setup refuses (`voice_would_be_replaced`); ask before `replace_voice: true` ([start-brand-setup.md](start-brand-setup.md)).

## A DON'T after a drop

Add it with `update-voice-profile` after their yes. Send the current DON'Ts plus the new one: the list is replaced whole.

## Always

- Show what you'll save before saving it; make one brand voice, never a second.
