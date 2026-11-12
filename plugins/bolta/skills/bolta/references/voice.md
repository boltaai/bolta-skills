# Voice

Show your voice, change one rule, set it up, check a draft against it, or write a batch in it. Every routine and campaign draft is written in it. Use for: that's not me, does this sound like me, what has Bolta learned, add my price list.

## Done when

The user has seen their voice, one change is saved and read back, a draft is checked with fixes shown, or a voice batch is saved as drafts.

## Know this

- **The voice read** is live: audience, tone words, DOs, DON'Ts, `feedback_count`, `knowledge.available`, `missing_fields`. No example posts: add 2 recent published ones (last 60 days, `has_publication_record` true). Wording: [show-and-change](voice-show-and-change.md).
- No voice yet: offer set-up. Several voices: ask which, offering the default.
- **Learning:** every yes, edit and no on Bolta's drafts and posts from this app is saved toward an overnight update: after about 10 new decisions since the voice last changed, Bolta adds at most 2 DOs and 2 DON'Ts. `feedback_count` can lag: never say it moved. A drop records nothing. Details: [references/brand-and-learning.md](voice-brand-and-learning.md).
- **"That's not me":** name what's off; offer one rule.
- **Change a rule:** build from a fresh read. Lists and tone dials are replaced whole: send the full list with the one change, keeping rules Bolta added. Show before and after in one line. With Bolta checks on, the check confirms; else a yes in words.
- **Same change twice**, or "stop doing X": offer one rule, once.
- **Soft rules or settings** ("no emojis", "write in Spanish"), what only a new voice can set, moving an account to another voice: [references/rules-or-settings.md](voice-rules-or-settings.md).
- **About your business** (overview, tagline): send only changed fields; same Bolta check. Which record a voice reads: [references/brand-and-learning.md](voice-brand-and-learning.md).
- **Make or update a voice** ("make my voice", "a voice for our founder"): first show what you know of how they write (pasted samples, phrases, likes), confirm, ask only the gaps. The brand's voice: Bolta's setup, preview first, with a site ([brand setup](start-brand-setup.md)) or without (no `url`: [no website](start-brand-setup-no-site.md)). A person's voice: [setup](voice-setup-and-documents.md). No account: the reply opens with the connect link and why ([start](start.md)).
- **Check a draft:** against the voice only: each DON'T crossed, each DO missing, then the fixed text. My read, not a Bolta score: [check](voice-show-and-change-check.md).
- **A voice batch:** `voice-generate`, 1 credit per post written; it makes no images. Say the cost, get a yes: [references/batch.md](voice-batch.md). One post: you write it, free.
- **Your documents:** nothing here can add or read them; the one line to say: [documents](voice-setup-and-documents-files.md).

## Tools

- `list-workspaces`, `get-voice-context`: workspace; the live voice; `all_profiles`: every voice.
- `get-voice-profile`: one in full, with accounts.
- `list-workspace-posts`: recent posts, drafts to check, a sample.
- `extract-business-dna`: set up from their website (checked).
- `create-voice-profile`: a person's or second voice.
- `update-voice-profile`: change rules, tone or audience (checked).
- `list-business-dna` (`dna_id`), `update-business-dna`: about your business; change it (checked).
- `voice-generate`, `bulk-create-status`, `bulk-create-posts`: a voice batch; its result; saving leftovers.

## Hand off

[start](start.md): first-time set-up. [post](post.md): write posts. [review](review.md): a fixed draft that needs a yes. [routine](routine.md): a routine in this voice or another. [campaign](campaign.md): campaign drafts, or one in another voice. [replies](replies.md), [results](results.md). [connect](connect.md): which connection teaches the voice.

## Always

- Follow the house rules in the Bolta skill.
- Claim learning only from what Bolta actually counts. Never say Bolta learns from everything, that a drop taught it, or when it will change.
- Never run `voice-generate` before saying its credit cost and getting a yes.
- Never save a voice change they haven't seen as before and after.
