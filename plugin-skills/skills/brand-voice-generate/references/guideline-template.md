# Bolta Brand Voice Guideline — Output Template

The structure `brand-voice-generate` fills in. Every section must be present and populated.
Fill from the discovery report; attribute every claim to evidence; assign confidence per
`confidence-scoring.md`. The final section — **voice-generate parameter mapping** — is what
makes the guideline operational inside Bolta, so it is required, not optional.

---

## 1. Metadata
- **Brand / business name:** (from Business DNA)
- **Workspace:** `workspace_id`
- **Niche / industry:** (from Business DNA)
- **Audience:** primary + secondary
- **Date generated / version:**
- **Sources used:** count by type (DNA, Voice Profiles, published posts, documents, transcripts)
- **Aggregate confidence:** High / Medium / Low (weighted — see §11)

## 2. Executive Summary
3-5 sentences: how the brand sounds in one breath, who it talks to, and the single most
important thing a writer must get right. Written so a new agent could apply it immediately.

## 3. We Are / We Are Not
The voice constants. Minimum 4 rows. Each "We Are" attribute is paired with the boundary it
must never cross.

| We Are | We Are Not | 
|-|-|
| Direct | Blunt / cold |
| Proof-driven | Hype-driven |
| Confident | Arrogant |
| Plain-spoken | Dumbed-down |

### Attribute detail
For each "We Are" attribute:
- **Definition** — what it means for this brand specifically.
- **Evidence** — the source(s) that prove it (e.g. "12 published LinkedIn posts lead with a metric").
- **Confidence** — High / Medium / Low.
- **In practice** — one do and one don't.

## 4. Brand Personality
3-5 adjectives + a one-line "if the brand were a person" sketch. Ground each in evidence.

## 5. Messaging Framework
- **Core value proposition** — one sentence.
- **Messaging pillars** — 2-4 recurring themes the brand returns to.
- **Proof points** — the facts/numbers/outcomes the brand leans on.

## 6. Tone-by-Context Matrix
Voice is the brand's constant personality — the We Are / We Are Not attributes that never
change. Tone is what flexes by context along three dimensions: formality, energy, and technical
depth. Minimum 3 contexts; score each on all three dimensions.

| Context | Formality | Energy | Technical depth | Notes |
|-|-|-|-|-|
| LinkedIn post | Medium | High | Low | Lead with outcome; one CTA. |
| X / short-form | Low | High | Low | Punchy; dry humor OK. |
| Cold email | Medium | Medium | Low | Respectful; no hype; short. |
| Proposal / deck | High | Medium | High | Rigorous; proof-heavy. |
| Blog / long-form | Medium | Medium | High | Teach; show the work. |

## 7. Terminology
| Class | Terms |
|-|-|
| Must-use | (exact brand terms, product names) |
| Preferred | (favored word → over alternative) |
| Avoid | (soft-banned words) |
| Never | (hard-banned — hype clichés, competitor framing, etc.) |

## 8. Language That Works / To Avoid
- **Works:** phrasings, sentence shapes, openers the brand uses well (with real examples).
- **To avoid:** clichés, filler, and constructions that read off-brand.

## 9. Content Examples
At least two before/after pairs showing the voice applied — off-brand draft → on-brand rewrite,
with a one-line note on what changed and why.

## 10. Confidence Scores
| Section | Confidence | Basis |
|-|-|-|
| We Are / We Are Not | High | 40 published posts + DNA |
| Tone matrix | Medium | Strong for social, thin for email |
| Terminology | High | Consistent across all sources |
| Messaging | Medium | Deck only, no behavioral confirmation |

## 11. Open Questions
Each grouped by priority AND carrying a recommended default the brand can accept as-is.

- **High** (blocks confident generation):
  - Q: … — **Recommendation:** …
- **Medium** (affects some contexts):
  - Q: … — **Recommendation:** …
- **Low** (nice-to-resolve):
  - Q: … — **Recommendation:** …

## 12. Sources Appendix
Every source with type, reliability weight, recency, volume, and what it contributed. Redact
PII (names, emails, phone numbers) from any transcript excerpts quoted.

---

## 13. voice-generate parameter mapping (Bolta operational layer)

The guideline is only useful once it drives Bolta's writer. Map it onto `voice-generate`
parameters as a copy-ready block. This is what `brand-voice-enforce` and every agent consume.

| voice-generate param | Filled from | Example |
|-|-|-|
| `tone` | Dominant register from We-Are + default tone-matrix row | `"direct, proof-driven, plain-spoken"` |
| `dos` | We-Are attributes + must-use/preferred terminology, as imperatives | `["lead with a concrete metric","say 'platform' not 'tool'","show the work behind claims"]` |
| `donts` | We-Are-Not boundaries + avoid/never terminology | `["no 'thrilled to announce'","no hype adjectives (game-changing, revolutionary)","never dumb it down"]` |
| `custom_rules` | Structural / formatting / tone-flex rules that don't fit dos/donts | `"One CTA per post. On X, one idea per post; dry humor OK. In email keep under 120 words."` |
| `context` | Positioning + audience summary from Business DNA | `"DevOps SaaS for platform-engineering leads at mid-market companies; buyers are technical and skeptical of hype."` |
| `business_name` | Business DNA name | `"Acme Platform"` |
| `niche` | Business DNA industry | `"DevOps / platform engineering"` |

**Rendered block (ready to paste into a `voice-generate` call):**

```json
{
  "tone": "direct, proof-driven, plain-spoken",
  "dos": ["lead with a concrete metric", "say 'platform' not 'tool'", "show the work behind claims"],
  "donts": ["no 'thrilled to announce'", "no hype adjectives", "never dumb it down"],
  "custom_rules": "One CTA per post. On X, one idea per post; dry humor OK. Email under 120 words.",
  "context": "DevOps SaaS for platform-engineering leads; technical, hype-skeptical buyers.",
  "business_name": "Acme Platform",
  "niche": "DevOps / platform engineering"
}
```

> These params also flow through to every autonomous agent that writes for this workspace, so
> the same voice governs ad-hoc drafts and the agent workforce. **Persist it natively too**:
> `create-voice-profile` / `update-voice-profile` write the guideline back as a Bolta Voice
> Profile, `extract-business-dna` seeds Business DNA from the brand's site, and
> `update-business-dna` edits DNA fields in place (safe partial merge) — all live on the
> exposed MCP surface. The mapping above stays the inline enforcement mechanism for one-off
> generation.
