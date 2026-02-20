---
name: bolta.get_voice_profile
version: 2.0.0
description: Retrieve voice profile details including tone, style, vocabulary, dos/donts to understand brand voice before creating content
category: content
roles_allowed: [Viewer, Creator, Editor, Admin]
agent_types: [content_creator, reviewer, engagement, custom]
safe_defaults: {}
tools_required: []
inputs_schema:
  type: object
  required: [voice_profile_id]
  properties:
    voice_profile_id: { type: string, description: "Voice profile UUID" }
outputs_schema:
  type: object
  properties:
    success: { type: boolean }
    voice_profile_id: { type: string }
    name: { type: string }
    description: { type: string }
    tone: { type: object }
    dos: { type: array, items: { type: string } }
    donts: { type: array, items: { type: string } }
    vocabulary: { type: object }
    examples: { type: array, items: { type: object } }
organization: bolta.ai
author: Bolta Team
---

## Goal
Retrieve voice profile details (tone, style, vocabulary, dos/donts, examples) to understand the brand voice before creating content. This is a **foundational context tool** for maintaining brand consistency.

## Which Agents Use This
- **content_creator** — Load exact tone and style before drafting
- **reviewer** — Use as reference to validate drafts against
- **engagement** — Match brand voice in replies
- All content-related agents need voice profile for consistency

## Hard Rules
1. MUST validate voice_profile_id exists and belongs to workspace
2. SHOULD include tone settings, dos/donts, vocabulary rules, and examples
3. Cache voice profiles for performance (updates are infrequent)

## Steps

### 1. Validate voice profile access
- Verify voice_profile_id exists
- Verify voice_profile belongs to workspace

### 2. Load voice profile
- Query VoiceProfile model
- Include all tone settings, rules, vocabulary, examples

### 3. Return structured voice data
- Tone settings (playful, professional, direct, thoughtful)
- Dos and donts
- Vocabulary preferences
- Example posts demonstrating the voice

## Output
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
  "donts": ["No corporate jargon", "Avoid 'leverage'", "No passive voice"],
  "vocabulary": {
    "prefer": ["use", "build", "ship", "create"],
    "avoid": ["leverage", "utilize", "synergy", "optimize"]
  },
  "examples": [
    {
      "text": "We built this in 2 weeks. You can too.",
      "explanation": "Direct, specific, outcome-focused"
    }
  ]
}
```

## Failure Handling
- If voice_profile_id not found: return error "Voice profile not found"
- If voice_profile not in workspace: return error "Access denied"

## Example Usage

### Scenario: Content creator loading voice before drafting
```json
{
  "voice_profile_id": "uuid"
}
```
**Result:** Receive complete voice profile to match tone, style, and vocabulary in content
