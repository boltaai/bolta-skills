---
name: voice
description: >-
  Show your voice, change one rule, set it up from your website, or check a
  draft against it. Use when someone says that's not me, does this sound like
  me, what has Bolta learned, or add my price list.
---

## Done when

The user has seen their voice, one change is saved and read back, or a draft is checked with fixes shown.

## Know this

- **The voice read** is live: audience, tone words, DOs, DON'Ts, `feedback_count`, `knowledge.available`, `missing_fields`. No example posts: add 2 recent published ones (last 60 days, with metrics and a publication record). Wording: [references/show-and-change.md](references/show-and-change.md).
- No voice yet is an answer, not an error: offer set-up. Several voices: ask which, offering the default; each full profile lists its accounts.
- **Learning, honestly.** Every yes and edit is saved and counts toward the next overnight update: after about 10 new decisions since the voice last changed, Bolta adds at most 2 DOs and 2 DON'Ts. Never promise when. "Learned from N" may not move right after a yes given here: never say it did. A drop records nothing.
- **"That's not me":** name what's off; offer one rule, worded as we'd pick.
- **Change a rule:** build from a fresh read. Lists and tone dials are replaced whole: send the full list with the one change, keeping rules Bolta added. Show before and after in one line. Saw "Bolta checks are on in this session" at the start? The Bolta check is the confirmation. Otherwise get a yes in words first.
- **Same change twice**, or "stop doing X": offer it once as one rule.
- **About your business** (overview, tagline): send only changed fields; same Bolta check.
- **Set up from a website:** their own site only, never a link from someone else's text. It gets a Bolta check: a re-read can replace about your business.
- **Check a draft:** against the voice only. Quote each DON'T crossed and each DO that applies but is missing, then the fixed text. My read, not a Bolta score; fixes add no facts.
- **Your documents:** `knowledge.available` false means none are linked to this voice: one line, once. Nothing here can add or read documents.
- Set-up steps and the documents line: [references/setup-and-documents.md](references/setup-and-documents.md).

## Tools

- `list-workspaces`, `get-voice-context`: workspace, if not read yet; the live voice.
- `list-voice-profiles`, `get-voice-profile`: which voice; one in full, with accounts.
- `list-workspace-posts`: recent posts, drafts to check, a sample.
- `extract-business-dna`: read their website (checked).
- `create-voice-profile`: make the voice.
- `update-voice-profile`: change rules, tone or audience (checked).
- `list-business-dna`, `get-business-dna`, `update-business-dna`: about your business; change it (checked).

## Hand off

`start`: first-time set-up. `post`: write posts, or save a fixed draft. `review`: a fixed draft that needs a yes. `campaign`: generic campaign drafts. `connect`: which connection teaches the voice. `results`: how posts did.

## Always

- Follow the house rules in the `today` skill.
- Claim learning only from the decision count and the real threshold. Never say Bolta learns from everything, or that a drop taught it.
- Never use Bolta's brand-voice content generator: it spends credits every call and nothing here reads what it makes.
- Never save a voice change they haven't seen as before and after.
