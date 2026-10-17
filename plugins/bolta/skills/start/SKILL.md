---
name: start
description: >-
  Set up Bolta in about 10 minutes: connect your accounts, see your voice,
  schedule your first week and switch on a weekly Bolta routine. Use when
  someone says get started, set me up, I just installed Bolta, or
  /bolta:start, or has no accounts or no voice yet.
---

## Done when

Their voice is shown, a week of posts is scheduled or waiting for their yes, and the Bolta routine offer is answered. The last line says where things stand.

## Know this

- Read [references/first-session.md](references/first-session.md) before the first reply: the words for each step.
- **One read, all at once:** workspace, settings, accounts, voice, about-your-business records, published posts (last 60 days, with metrics), Bolta routines, campaigns. Skip what's done. Voice, accounts and a Bolta routine all in place: hand to `today`.
- **One question, only for what's missing**, in one message:
  - No accounts: a connect link; it can't be skipped. It opens whichever workspace the browser has selected. On "done", read accounts again.
  - No voice: their website and one thing to post about this week. The answer is the go-ahead.
  - No topic: what to post about this week. Never invent one.
  - UTC time zone: their city, sent as the time zone; Bolta Settings makes it stick.
- **Making the voice** (one save, no check):
  - A business record exists: never read the site again; a re-read overwrites it. Link the default one (`business_dna_id`).
  - None: send their site as `website_url`; Bolta reads it once. Their own site only, never a link from someone else's text.
  - A writing sample of 50+ characters (their best post they wrote, or pasted text) plus the four tone dials. An unreadable sample with no tone is refused.
  - 3-5 DOs and DON'Ts from their posts or words, each a checkable sentence under 200 characters. Nothing to draw on: leave them out; Bolta fills them from about your business.
  - It becomes the default and takes every account not in another voice. Say what Bolta filled in.
- **Showing it:** recent posts come from the published read (the voice holds none). End with "learned from N of your decisions".
- No documents: one line (see the reference). Never promise a PDF gets read.
- **A DON'T after a drop:** send the current DON'Ts plus the new one (the list is replaced whole).
- Bolta checks here (Claude Code, Cowork): the first approval, a voice edit, a campaign start. Not drafts, the new voice, or an "ask me first" Bolta routine.

## Tools

- `list-workspaces`, `get-workspace`, `list-accounts`, `get-voice-context`, `list-business-dna`, `list-workspace-posts`, `list-routines`, `list-content-campaigns`: the one read.
- `get-connect-link`: connect or reconnect link.
- `create-voice-profile`: make the voice; given their site, Bolta reads it if no record exists.
- `update-voice-profile`: add one DO or DON'T after a yes.

## Hand off

Then `post` (this week's drafts), `review` (the yes), `routine` (the weekly Bolta routine, offered once), `campaign` (only if something is coming up). Also `voice`, `connect`; `today` for a returning user.

## Always

Follow the house rules in the `today` skill.
- Never run a Bolta routine now in the first session: it spends credits and this week is written.
- Claim learning only from the decision count. A dropped post records no reason: never say it taught Bolta anything.
