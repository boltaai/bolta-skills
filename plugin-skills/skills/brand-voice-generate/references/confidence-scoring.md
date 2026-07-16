# Confidence Scoring Methodology

How `brand-voice-generate` assigns confidence to each section of the guideline, so the brand
knows which claims are load-bearing and which are best-guesses awaiting confirmation.

## Why score confidence
A guideline synthesized from strong evidence should be trusted and used as-is. One synthesized
from thin evidence should be used cautiously and its gaps surfaced as open questions. Confidence
scoring makes that distinction explicit and drives which items become open questions.

## The three levels

**High** — the attribute is proven by multiple independent sources, or by a large volume of
consistent behavioral evidence.
- Backed by 2+ source types that agree (e.g. Business DNA + published posts), OR
- 10+ published posts / transcript passages showing the same pattern consistently, AND
- No contradicting evidence.

**Medium** — supported but not confirmed.
- One strong source, or several weak ones, OR
- A moderate sample (3-9 posts/passages) with mostly-consistent signal, OR
- Minor contradictions that don't undermine the core claim.

**Low** — inferred, sparse, or contested.
- A single weak source (one document, a handful of samples), OR
- Meaningful contradictions between sources, OR
- Inferred by reasoning rather than observed in the brand's own material.
Every Low item should also appear in Open Questions with a recommended default.

## Evidence reliability (which sources count for more)
From most to least reliable:
1. **Business DNA / Voice Profiles** — brand-owned, explicit, authoritative.
2. **Published posts** (`list-workspace-posts status=Published`) — behavioral: how the brand
   actually talks in public. Primary evidence, not a footnote.
3. **Brand documents** — decks, brand books, one-pagers (aspirational; may lag actual voice).
4. **Transcripts** — sales calls, interviews (truest unscripted voice, but noisy and PII-heavy).
5. **Pasted samples** — useful but unranked; weight by volume and recency.

## Section-level guidance
- **We Are / We Are Not:** High only if each attribute has behavioral confirmation (posts or
  transcripts), not just a document asserting it.
- **Tone matrix:** score each context row independently — social rows are often High (lots of
  posts) while email/proposal rows are Medium/Low (little evidence). Never blanket-score the matrix.
- **Terminology:** High when a term appears consistently across sources; Low for one-off usage.
- **Messaging framework:** documents alone → cap at Medium until behavioral evidence confirms.

## Transcript-primary handling
When transcripts are the main evidence (little/no published content), treat them as behavioral
signal but discount for noise: multiple speakers, off-brand tangents, and verbal filler. Require
a pattern to recur across several passages before scoring it High. Strip PII from any excerpt
carried into the guideline.

## Published-posts-as-behavioral-evidence
Bolta's advantage: the brand's published posts live in the workspace. Treat them as first-class
behavioral evidence — they show real, shipped voice, not aspiration. Volume and consistency of
posts is the single strongest path to a High-confidence guideline.

## Aggregate score
Compute a weighted average across sections, weighting the load-bearing sections (We Are / We
Are Not, tone matrix, terminology) more than descriptive ones (personality, messaging).
- **Aggregate High:** most weighted sections High, none Low on a load-bearing section.
- **Aggregate Medium:** mixed; at least the core attributes are Medium+.
- **Aggregate Low:** core attributes are Low → tell the user the guideline is provisional and
  recommend gathering more signal (more posts, a transcript) before relying on it.

## Relationship to open questions
Every Low-confidence item and every unresolved conflict becomes an Open Question — and each
open question ships WITH a recommended default so the brand can accept, not just deliberate.
Resolving open questions (user confirms or corrects) is how a Medium guideline becomes High.
