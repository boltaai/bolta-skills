---
organization: bolta.ai
author: Max Fritzhand
---

## bolta.voice.learn_from_samples

Purpose:
Extract structured voice rules from past content.

When Used:
- User imports previous posts
- Upgrading from bootstrap voice
- Refining brand consistency

Inputs:
- post_text[] (array of strings)
- optional platform metadata

Behavior:
- Tone detection
- Sentence structure modeling
- Hook pattern extraction
- CTA pattern extraction
- Vocabulary frequency modeling
- Generate structured voice schema
- Compare against existing voice profile (if present)

Outputs:
- voice_profile_id (new or updated)
- delta_report (differences from previous voice)
- strength_score (voice consistency metric)

Notes:
This skill strengthens voice identity and should version
voice profiles rather than overwrite silently.
