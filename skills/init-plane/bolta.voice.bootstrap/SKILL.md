---
organization: bolta.ai
author: Max Fritzhand
---

## bolta.voice.bootstrap

Purpose:
Create a default Voice Profile for a new workspace.

When Used:
- First-time onboarding
- No active voice profile exists
- Level 0 activation

Inputs:
- topic_focus (string)
- audience_type (string)
- tone_preference (enum: professional, casual, bold, analytical, etc.)
- example_sentences (optional array of strings)

Behavior:
- Generate tone rules
- Generate formatting preferences
- Generate hook and CTA patterns
- Generate vocabulary bias
- Create structured voice schema
- Store as `default_voice_profile`
- Mark status = provisional

Outputs:
- voice_profile_id
- summary_of_voice
- confidence_score

Notes:
This skill must be run before any content-generation skill
if no active voice profile exists.
