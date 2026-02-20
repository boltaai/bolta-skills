# bolta.get_voice_profile

**Version:** 2.0.0  
**Category:** Content Creation  
**Agent Types:** All  
**Roles Allowed:** All

---

## Purpose

Retrieve voice profile details (tone, style, vocabulary, dos/donts, examples) to understand the brand voice before creating content.

This is a **foundational context tool** — agents use it to load the canonical brand voice reference.

---

## When An Agent Uses This

**Content Creator:** "Before drafting, I need to know the exact tone and style"  
**Reviewer:** "I need the voice profile as the reference to validate drafts against"  
**Engagement:** "I need to match brand voice in replies"

---

## Parameters

```json
{
  "voice_profile_id": "string (UUID, required)"
}
```

---

## Returns

```json
{
  "success": true,
  "voice_profile_id": "uuid",
  "name": "Bolta Brand Voice",
  "description": "Bold, founder-led voice...",
  "tone": {
    "playful": 3,
    "professional": 7,
    "direct": 9,
    "thoughtful": 6
  },
  "dos": ["Lead with outcomes", "Use short sentences", "Be specific"],
  "donts": ["No jargon", "Avoid hedging", "No vague promises"],
  "brand_persona": "...",
  "speaker_mode": "brand",
  "products": [...],
  "business_dna": {...}
}
```

See `/skills/voice-plane/bolta.voice.bootstrap/SKILL.md` for full structure.

---

## Hard Rules

- **MUST** validate voice_profile_id belongs to workspace
- **MUST** return comprehensive voice data (not just name)
- **SHOULD** include related business DNA if linked
