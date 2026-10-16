# Brand voice guideline: output template

Fill every section from the evidence. Attribute each claim to a source, score it per confidence-scoring.md, and say "not observed" rather than padding. The guideline is rule-based: Bolta stores rules, not example posts. Section 12 maps it to profile fields.

## 1. Metadata
- **Brand name:**
- **Workspace:** name (id)
- **Niche and audience:** primary, secondary
- **Date and version:**
- **Sources used:** counts by type (human-written posts, Bolta-written posts, reviews, documents, transcripts, website analysis, stored profile and DNA)
- **Aggregate confidence:** High, Medium or Low (see confidence-scoring.md)

## 2. Summary
Three to five sentences: how the brand sounds in one breath, who it talks to, and the one thing a writer must get right. A new writer should be able to apply it immediately.

## 3. We Are / We Are Not
The constants of the voice. At least four rows; each attribute is paired with the line it must not cross.

| We Are | We Are Not |
|-|-|
| Direct | Blunt or cold |
| Proof-driven | Hype-driven |
| Confident | Arrogant |
| Plain-spoken | Dumbed down |

For each "We Are" attribute add: **Definition** (what it means for this brand), **Evidence** (the quoted post or source, with count), **Confidence**, **In practice** (one do, one don't).

## 4. Personality
Three to five adjectives and a one-line "if the brand were a person" sketch, each grounded in evidence.

## 5. Messaging framework
- **Core value proposition:** one sentence.
- **Pillars:** two to four recurring themes.
- **Proof points:** facts, numbers or outcomes the brand leans on. Only ones found in its own material.

## 6. Tone dials and tone by context
Voice is the constant personality; tone is what flexes. Dials, 0 to 100:

| Dial | Value | Evidence |
|-|-|-|
| playful | | |
| professional | | |
| direct | | |
| thoughtful | | |

Then at least three contexts, each rated on formality, energy and technical depth, with a one-line note:

| Context | Formality | Energy | Technical depth | Notes |
|-|-|-|-|-|
| LinkedIn post | Medium | High | Low | Lead with the outcome; one call to action. |
| X or short form | Low | High | Low | One idea per post; dry humor fine. |
| Email | Medium | Medium | Low | Short; no hype. |
| Blog or long form | Medium | Medium | High | Teach; show the work. |

## 7. Terminology
| Class | Terms |
|-|-|
| Must use | exact brand and product terms |
| Preferred | favored word over the alternative |
| Avoid | soft-banned words |
| Never | hard-banned: hype clichés, competitor framing |

## 8. Language that works and to avoid
- **Works:** phrasings, sentence shapes and openers the brand uses well, quoted from real posts (personal data removed).
- **Avoid:** clichés, filler and constructions that read off-brand.

## 9. Before and after
At least two pairs: an off-brand draft and an on-brand rewrite, with one line on what changed and why. Mark these as illustrations you wrote, not brand posts.

## 10. Confidence
| Section | Confidence | Basis |
|-|-|-|
| We Are / We Are Not | High | 40 human-written posts and a brand book agree |
| Tone matrix | Medium | strong for social, thin for email |
| Terminology | High | consistent across sources |
| Messaging | Medium | deck only, no behavioral confirmation |

## 11. Open questions
Grouped High, Medium, Low by how much they block confident writing. Each carries a recommendation the user can accept as is.
- Q: ... Recommendation: ...

Also list **Conflicts** (sources that disagree, both readings) and **Gaps** (attributes with thin or no evidence), and **Sources** with type, recency, volume and what each contributed. Strip names, emails and handles from quoted material.

## 12. Bolta profile mapping
What will be written to the profile if the user approves. Show exact values.

| Profile field | Value from this guideline | Set on |
|-|-|-|
| `tone` | all four dials | create or update |
| `tone_of_voice` | three to six descriptors | create or update |
| `target_audience` | one sentence | create or update |
| `dos` | We Are plus must-use and preferred terms, as imperatives of 200 characters or fewer | create or update (full merged list) |
| `donts` | We Are Not plus avoid and never terms, same limits | create or update (full merged list) |
| `content_size`, `pacing`, `speaker_mode` | from the matrix and speaker choice | create or update |
| `custom_rules` | structural, formatting and per-platform flexes | create only; on an existing profile give the text to paste in the dashboard |
| Business DNA fields | tagline, overview, colors | `update-business-dna` |

```json
{
  "tone": {"playful": 25, "professional": 70, "direct": 80, "thoughtful": 60},
  "tone_of_voice": ["direct", "proof-driven", "plain-spoken"],
  "target_audience": "Platform-engineering leads at mid-size companies who distrust hype.",
  "dos": ["Open with a concrete number when the post has one", "Say 'platform', not 'tool'"],
  "donts": ["Never use 'thrilled to announce'", "No hype adjectives such as game-changing"]
}
```

For a refresh, the `dos` and `donts` shown are merged with the profile's existing entries and the diff is shown before anything is sent.
