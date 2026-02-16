---
organization: bolta.ai
author: Max Fritzhand
---

## bolta.voice.validate

Purpose:
Evaluate content against a Voice Profile.

When Used:
- Before submitting for review
- Before scheduling
- During Autopilot execution
- During review workflows

Inputs:
- voice_profile_id
- content_text (string)

Behavior:
- Compare tone alignment
- Validate structure rules
- Detect vocabulary drift
- Score hook and CTA consistency

Outputs:
- compliance_score (0–100)
- deviation_report
- suggested_rewrite (optional)

Notes:
This skill does not modify content automatically unless explicitly requested.
It provides a compliance layer.
