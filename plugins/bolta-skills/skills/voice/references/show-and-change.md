# Showing the voice, changing a rule, checking a draft

Read when showing, changing or checking against the voice. Examples only.

## Showing the voice

> **Your voice** (Acme)
> For: owners of small design studios. Tone: direct, warm, plain.
> DO: open with a real number · name the problem first · end with one question
> DON'T: hard sell · hashtags mid-post · "game-changer"
> Recent: "We lost our biggest client in March..." (LinkedIn, Oct 6, 2,140 views)
> Bolta has learned from 12 of your decisions.

- Tone: the tone words, never dial numbers.
- The 3 most specific DOs and DON'Ts, then "+5 more" if there are more.
- Recent: the 2 best published posts by real numbers, last 60 days. None: no line.
- The learning line: "Every yes and edit is saved. After about 10 new ones, Bolta updates your DOs and DON'Ts overnight." At 0 decisions, end with "Bolta hasn't learned from your decisions yet." and the learning line.
- `business.overview` missing: "Bolta has no description of Acme yet. Tell me what you do in two sentences and I'll add it." No record at all (`business_dna` missing): offer the site read.

## What Claude can't see

- Which rules Bolta added overnight. They look like typed ones.
- When the next update runs. The 10 count from the voice's last change, the user's own included.
- Edits teach because Bolta keeps its first version beside the user's. Over a plain API-key connection there is no first version, so edits don't teach (`connect`).

## "That's not me"

Name the gap in one line, then offer one rule:

> It reads more formal than your posts. Add a DO: "Write like you talk: short sentences, contractions"?

Unsure what's off? Ask once, with our guess.

## Changing a rule

Read the voice fresh first. One line per change:

> Adding to your DON'Ts: "No exclamation marks." The other 3 stay.
> Changing a DO: "Be data-driven" → "Open with a number when the post has one."

- Send the whole list: current rules plus or minus the change. A list built from scratch wipes the rest.
- Moving tone? Send all four dials (playful, professional, direct, thoughtful, 0-100).
- Each rule: one checkable sentence under 200 characters. Longer text is split into several rules.
- Clashes with an old rule? Show both; ask which stays.
- Several changes named together: one save, one Bolta check.
- Read back: "Saved to Acme's voice: 4 DON'Ts now." Say if anything differs.
- Undo means writing the old list back: keep the before in the conversation.

## Same change twice

> You've cut the hashtags twice. Add "No hashtags" to your DON'Ts so Bolta's drafts leave them out?

Add the learning line, once per conversation.

## Checking a draft

Pasted, or a saved draft from the post list. Judge against the voice only.

> **Close to your voice.** 1 DON'T crossed, 1 DO missing.
> - "A game-changer for studios" crosses DON'T: "game-changer".
> - DO "open with a real number" fits here; it opens with a question.
> - Unchecked claim: "3x more leads". Is that real?
>
> Fixed: "<full new text>"

- Verdict: on voice, close, or off voice. No score.
- Quote every finding. A rule that doesn't fit this piece isn't missing.
- A fix keeps the meaning and adds no facts, numbers, quotes or stories.
- Next: a saved draft goes to `post` to save the fix; one waiting for a yes, to `review`.
- Several drafts: one line each (verdict, worst problem), details for the worst.
