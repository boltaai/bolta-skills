# Confidence scoring

How to score each section of the guideline so the user knows which claims are load-bearing and which are best guesses. Score before showing the guideline; every Low item also becomes an open question.

## Count independent evidence

Count distinct posts, distinct transcript passages and distinct documents. One post cross-posted to three platforms counts once. Quotes from one document count once however many you pull. Evidence the user gave in this conversation ("we never use exclamation marks") is a stated rule: record it as such, it needs no score.

## The three levels

**High**: proven by independent evidence.
- Two or more source types agree (for example human-written posts and a brand document), or
- ten or more distinct posts or transcript passages show the same pattern, and
- nothing contradicts it.

**Medium**: supported, not confirmed.
- One strong source or several weak ones, or
- three to nine posts or passages with a mostly consistent pattern, or
- minor contradictions that do not undermine the claim.

**Low**: inferred, sparse or contested.
- One weak source (one document, a handful of samples), or
- meaningful contradictions between sources, or
- reasoned rather than observed in the brand's own material.

## Which sources count for more

From most to least reliable. The first two are behavior; the rest are intent or hearsay.

1. **Human-written published posts**: `list-workspace-posts` rows with `content_origin` of `manual`. How the brand actually talks in public. Highest weight. A model that drafted over a plain API-key connection is also stamped `manual`: if the user says an assistant drafted posts that way, treat those as unknown origin.
2. **What the team refused**: `list-recurring-reviews` rows with status rejected, with a reason in `review_notes`. Strong for "We Are Not" rules; one rejection is Low, a pattern of three or more is Medium.
3. **The stored profile and Business DNA**: the brand's current Bolta configuration. It shows intent and what Bolta uses today, not proof of how people write. Its dos, don'ts and descriptors may be typed, learned by Bolta or extracted from a scrape, and you cannot tell which: treat as Medium unless posts confirm them.
4. **Brand documents** (decks, brand books, one-pagers): aspirational, may lag the real voice. Cap messaging claims at Medium until posts confirm.
5. **Transcripts** (sales calls, founder interviews): the truest unscripted voice, but noisy: several speakers, tangents, filler. Require a pattern across several passages before High. Strip personal data from excerpts.
6. **Website analysis** (`extract-business-dna` output or pages the user named): how the brand wants to sound, produced by a model from scraped text. Hypothesis tier.
7. **Posts written by Bolta or by an assistant** (`content_origin` of `ai_studio`, `social_agent`, `recurring_generator`, `onboarding`, `assistant`): they show what was shipped, not how the brand's people write. Never count `assistant` posts at all (circular). Count Bolta-written ones only as "approved and shipped", at Low.
8. **Pasted samples**: useful, unranked. Weight by volume and recency.

Posts with a blank `content_origin` (older posts) and `bulk_upload` posts are unknown origin: Medium at best.

## Section guidance

- **We Are / We Are Not**: High only when each attribute has behavioral confirmation (human-written posts or several transcript passages), not just a document asserting it.
- **Tone dials and matrix**: score each row independently. Social rows are often High (many posts); email, proposal or blog rows are often Medium or Low. Never blanket-score the matrix. A dial with no evidence is Low: say "default 50, not observed".
- **Terminology**: High when a term appears consistently across sources; Low for one-off use.
- **Messaging framework**: documents alone cap at Medium.
- **Dos and don'ts**: score each rule, or at least the group. A rule backed by a rejection reason or a pattern in posts is stronger than one asserted in a deck.
- **Performance claims** ("this phrasing performs"): only with metrics that have synced (posts older than about a day, `has_publication_record` true) and at least three posts. Otherwise say "present", not "proven".

## When posts are scarce

If there are few or no human-written posts, say so. Lean on documents, transcripts and the user's own statements, cap the aggregate at Medium, and recommend gathering more human-written posts before relying on the guideline. If Bolta wrote most of the posts, say so in the report; do not present Bolta's own phrasing as the brand's.

## Aggregate score

Weight the load-bearing sections (We Are / We Are Not, tone dials and matrix, terminology, dos and don'ts) more than the descriptive ones (personality, messaging).
- **High**: most weighted sections High, none Low on a load-bearing section.
- **Medium**: mixed; the core attributes are at least Medium.
- **Low**: core attributes are Low. Call the guideline provisional and recommend more signal before saving it to a profile.

## Open questions

Every Low item and every unresolved conflict becomes an open question with a recommended default, so the user can accept rather than deliberate. Resolving questions (user confirms or corrects) is how a Medium guideline becomes High; re-score after the user answers.
