# Voice constant, tone flexes

The model behind writing and checking in a brand's voice. **Voice** is who the brand is and does not change. **Tone** is how
that voice adapts to a situation and changes constantly. Hold the first fixed and move the second, and copy stays
recognizably the brand on every channel while still fitting the moment.

## Voice versus tone

| | Voice | Tone |
|-|-|-|
| What it is | The brand's fixed personality | Situational adjustment of it |
| Changes? | Never | With every context |
| Where it lives in Bolta | `writing.dos`, `writing.donts`, `writing.tone_of_voice`, `writing.persona`, `voice_profile.speaker_mode` | `writing.tone` dials, `writing.formality`, `writing.pacing`, `writing.content_size`, `platforms.<platform>` |
| Example | "Direct and proof-led" | Warmer in a support reply, tighter on X |

A brand that is direct and proof-led is direct and proof-led in a launch post, an apology and a proposal. What flexes is the
register: formality, pacing, length and how much jargon, not the identity.

## Reading the profile as voice and tone

- Voice constants: every `dont` is a boundary; every `do` is a habit; `tone_of_voice` descriptors (for example "confident",
  "approachable") name the character. Crossing a `dont` is the most serious failure, worse than under-expressing a `do`.
- Tone settings: the four dials in `writing.tone` (playful, professional, direct, thoughtful, each 0 to 100) are the
  profile's baseline register. `formality` (0 to 100) and `pacing` (slow, moderate, fast, concise) refine it. The
  platform's own settings in `platforms.<platform>` then adjust emoji, hashtags, length and call to action.
- Bolta has no stored table of contexts, no "we are / we are not" pairs and no terminology list. If the user pasted a
  guideline that has them, use it for those and name it as the source. Otherwise pair each descriptor with the nearest `dont`
  yourself and say that you did.

## Three register dials for flexing

When the profile does not say how to adjust for a context, flex along these three, and never at the cost of a `do` or `dont`.
The profile wins whenever it speaks: a platform setting or `custom_rules` beats this table.

| Dial | Low | Medium | High |
|-|-|-|-|
| Formality | Contractions, casual, first-name energy | Professional but human, contractions fine, no slang | Precise, structured, no contractions |
| Energy | Calm, measured, matter-of-fact | Engaged, warm, forward-moving | Punchy, urgent, specific, without hype |
| Technical depth | Plain language, outcome-focused | Domain terms explained in context | Full vocabulary, expert reader assumed |

Starting points by context (a default, not a rule):

| Context | Formality | Energy | Technical depth |
|-|-|-|-|
| LinkedIn post | Medium | Medium to high | Low to medium |
| X or short-form | Low | High | Low |
| Cold email | Medium | Medium | Low |
| Support reply | Low | Medium | Low to medium |
| Proposal or deck | High | Medium | High |
| Blog or long-form | Medium | Medium | Medium to high |

Map them to the profile rather than overriding it: if `formality` is 80, even the X row stays formal-leaning and you
lower energy and length instead. If `use_emojis` is false, no row brings emoji back.

## Applying voice and tone together

1. Lock the voice first: the `donts`, the `dos` that apply, the descriptors, the speaker mode (we or I).
2. Pick the context: platform settings if present, otherwise the nearest row above. Set the three dials.
3. Write with both. Every sentence carries the voice; the register follows the dials.
4. Check boundaries: nothing crosses a `dont`; emoji, length and language rules hold.
5. Check: rules honored, register fits, no boundary crossed. That is on-brand by the profile, and no more than that.

Illustration of the split, with placeholders instead of invented facts: a direct, proof-led brand announcing a milestone on
LinkedIn keeps the proof first ("[the number], and what it let us do: [the concrete result]") with medium formality and
steady energy. On X the same two habits survive in fewer words with lower formality. The voice held; only the register moved.

## Common mistakes

- **Flexing voice instead of tone.** Making the brand "more casual" by dropping a `do`. Keep the habit, lower the formality.
- **Ignoring the boundary column.** "Confident" copy that reads arrogant. Check the `donts` explicitly, line by line.
- **One tone everywhere.** The LinkedIn register in a support reply or a proposal. Match the context.
- **Hype smuggled in as energy.** High energy is not hype. Raise urgency with verbs and specifics, not with "game-changing",
  "thrilled" or "revolutionary", unless the profile allows them.
- **Inventing proof to sound proof-led.** A proof-led voice needs real numbers from the user. If you have none, write the
  claim without a figure or leave a bracketed placeholder, and tell the user.
- **Terminology drift under tone pressure.** A casual context is no licence to break a ban in the profile or the guideline.
- **Treating dial values as targets.** A `playful` of 40 does not ask for jokes. Flag only clear mismatches.
