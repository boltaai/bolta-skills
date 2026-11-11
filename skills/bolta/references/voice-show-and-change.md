# Show the voice, change a rule, check a draft

Read when showing, changing or checking against the voice. Examples only.

## Showing the voice

> **Your voice** (Acme)
> For: owners of small design studios. Tone: direct, warm, plain.
> DO: open with a real number · name the problem first · end with one question
> DON'T: hard sell · hashtags mid-post · "game-changer"
> Recent: "We lost our biggest client in March..." (LinkedIn, Oct 6, 2,140 views)
> Bolta has learned from 12 of your yeses and edits.

- Tone: the tone words, never dial numbers.
- The 3 most specific DOs and DON'Ts, then "+5 more" if there are more.
- Recent: the 2 best published posts by real numbers, last 60 days. None: no line.
- The learning line: "Every yes and edit is saved, and your reasons for a no count too. After about 10 new ones, Bolta updates your DOs and DON'Ts overnight. See what changed in the Learning tab: bolta.ai/dashboard/knowledge-base?tab=memory". Count: `writing.feedback_count` (yeses and edits, not noes). At 0, say "Bolta hasn't learned from your decisions yet." first.
- `business.overview` missing: "Bolta has no description of Acme yet. Tell me what you do in two sentences and I'll add it." No record at all (`business_dna` missing): offer the site read.

## What you can't see

- Which rules Bolta added overnight: they look like typed ones. The Learning tab's version history shows them.
- When the next update runs: overnight, once about 10 new decisions build up, counted from the voice's last change (the user's own saves included); at most 2 new DOs and 2 DON'Ts.
- Edits teach because Bolta keeps its first version beside the user's. A single post saved with `create-post` over a pasted Bolta API key isn't Bolta's writing: nothing on it teaches ([brand-and-learning](voice-brand-and-learning.md)).

## "That's not me"

Name the gap in one line, then offer one rule:

> It reads more formal than your posts. Add a DO: "Write like you talk: short sentences, contractions"?

Unsure what's off? Ask once, with your guess.

## Changing a rule

Read the voice fresh first. One line per change:

> Adding to your DON'Ts: "No exclamation marks." The other 3 stay.
> Changing a DO: "Be data-driven" → "Open with a number when the post has one."

- Send the whole list: current rules plus or minus the change. A list built from scratch wipes the rest.
- Moving tone? Send all four dials (playful, professional, direct, thoughtful, 0-100). Mid-range dials change nothing: [brand-and-learning](voice-brand-and-learning.md).
- Each rule: one checkable sentence under 200 characters. Longer text is split into several rules.
- Clashes with an old rule? Show both, ask which stays.
- Several changes together: one save, one new version.
- Read back: "Saved to Acme's voice: 4 DON'Ts now." Name any difference.
- Undo means writing the old list back: keep the before in the conversation.

## Same change twice

> You've cut the hashtags twice. Add "No hashtags" to your DON'Ts so Bolta's drafts leave them out?

Add the learning line, once per conversation.

## Checking a draft

Judging a pasted or saved draft against the voice: [check a draft](voice-show-and-change-check.md).

## Always

- Follow the house rules in the Bolta skill.
- Never save a voice change the user hasn't seen as before and after.
