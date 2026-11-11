# Saying no, sending back, dropping many

Read before turning a post down, when a "no" lands on a draft nobody sent for review, when someone wants changes made instead of a no, or before deleting more than a few. Back to [review](review.md).

## A no with a reason

- `reject-post(post_id, reason, categories)`. `reason`: the user's own words, what is wrong (not what to do instead), up to 2000 characters. It can't be added later, so ask first when they gave none: "What's off with 2? Too salesy, too long, wrong tone, something else?"
- `categories`: only codes that truly fit; an unknown code refuses the whole call. Plain word to code:
  - tone: too_casual, too_formal, wrong_tone, off_brand
  - length and shape: too_long, too_short, wrong_format, platform_mismatch
  - facts and words: factual_error, spelling_grammar, wrong_emoji, wrong_hashtag
  - the ask: missing_cta, wrong_cta, too_salesy
  - substance: not_engaging, off_topic, repetitive, no_substance
  - anything else: other
- The post is kept as Rejected, never deleted, scheduled or posted. In a campaign it stays in the campaign and counts as turned down.
- Only owners and admins can turn a post down, the same as a yes ([yes move](review-yes-move.md)).
- Repeating it is safe: `already_decided`, and the first reason stands. Already approved: someone decided it; say its status and stop.

## A draft nobody sent for review

`reject-post` answers "not waiting for review" (`not_in_review`) and changes nothing. Pick by what the user wants:

- They gave a reason, so Bolta should learn: `submit-for-review` with that post, then `reject-post` with their words. Say "I put it on the review list and turned it down, so Bolta keeps your reason."
- They just don't want it: `delete-post`. Say that a drop records no reason.

## What a no teaches

A reason teaches the voice only on posts Bolta counts as its own writing: drafts from a Bolta routine, a campaign, a voice batch, Bolta's chat, and posts saved here while signed in to Bolta. On a post saved with `save-post` over a pasted Bolta API key, or typed by hand in Bolta, the reason stays on the post and the voice learns nothing. Never say it taught Bolta then. Same reason twice: the DON'T offer in [read-back](review-read-back.md).

## "Send it back for changes"

Nothing here sends a post back for changes: `reject-post` is a hard no that can't be reopened for edits. Offer one of two:

- You make the change: `save-post` with `post_id` and the new `content`, show it (a Draft needs `submit-for-review`; a waiting post keeps waiting), then the yes move with the result's `content_fingerprint`.
- A teammate reworks it: "Open it from Approvals in Bolta and leave your notes there for them: bolta.ai/dashboard/approvals."

A client asks for changes with their own button ([client approval](review-client-approval.md)). Reworking a post a teammate or client sent back: [more decisions](review-more-decisions.md).

## In Bolta instead

No `reject-post` on this app: "Tap the X (Dismiss) on that post at bolta.ai/dashboard/approvals and give your reason." On an older recurring row the button reads Reject. It is greyed out while the client decides and hidden on expired rows.

## Dropping many

`delete-post` stops after 20 deletes in 5 minutes per brand. Past that Bolta refuses the rest: stop, say how many were removed and how many are left, and ask before going on. Never loop until it passes.

## Always

- Follow the house rules in the Bolta skill.
- Never use `reject-post` to ask for edits, or `delete-post` to stand in for a no that has a reason.
- Never say Bolta learned from a no unless the post was Bolta's own writing.
