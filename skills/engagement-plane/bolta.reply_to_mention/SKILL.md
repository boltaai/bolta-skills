---
name: bolta.reply_to_mention
version: 2.0.0
description: Draft a reply to a mention, comment, or DM while maintaining brand voice and community presence
category: engagement
roles_allowed: [Viewer, Creator, Editor, Admin]
agent_types: [engagement, custom]
safe_defaults:
  always_draft_for_approval: true
  escalate_sensitive_topics: true
tools_required:
  - bolta.get_voice_profile
  - bolta.create_reply_draft
inputs_schema:
  type: object
  required: [mention_id, reply_text]
  properties:
    mention_id: { type: string, description: "Mention UUID to reply to" }
    reply_text: { type: string, description: "Draft reply content" }
    tone: { type: string, enum: [helpful, empathetic, professional], description: "Reply tone" }
    escalate: { type: boolean, description: "Flag for human review", default: false }
    voice_profile_id: { type: string, description: "Voice profile to match" }
outputs_schema:
  type: object
  properties:
    success: { type: boolean }
    draft_reply_id: { type: string }
    status: { type: string, enum: [draft] }
    requires_approval: { type: boolean }
    escalated: { type: boolean }
organization: bolta.ai
author: Bolta Team
---

## Goal
Draft a reply to a mention, comment, or DM while staying on-brand and maintaining community presence.

## Which Agents Use This
- **engagement** — Respond to common questions, compliments, and community interactions
- **moderator** — De-escalate complaints with empathetic responses
- **custom** — Any agent handling community engagement

## Hard Rules
1. MUST match brand voice (use voice_profile_id)
2. MUST create draft (not publish directly) unless role=editor AND Safe Mode off
3. MUST escalate sensitive topics (refunds, complaints, legal, billing)
4. MUST NOT use generic template responses
5. Tone should match context (complaint = empathetic, question = helpful, compliment = warm)

## Steps

### 1. Validate input
- Verify mention_id exists
- Verify reply_text is non-empty
- Load voice_profile if provided

### 2. Check for sensitive topics
- If content mentions: refund, billing, legal, broken, angry, lawsuit
  - Set escalate=true automatically
  - Flag for human review

### 3. Create reply draft
- Create draft reply linked to mention
- Apply voice profile for brand consistency
- Apply tone (helpful, empathetic, professional)
- Mark requires_approval=true

### 4. Return draft confirmation
- Return draft_reply_id, status, escalated flag

## Output
```json
{
  "success": true,
  "draft_reply_id": "uuid",
  "status": "draft",
  "requires_approval": true,
  "escalated": false
}
```

## Failure Handling
- If mention_id not found: return error "Mention not found"
- If reply_text empty: return error "Reply text required"
- If voice_profile_id invalid: use workspace default voice

## Example Usage

### Scenario 1: Helpful response to question
```json
{
  "mention_id": "uuid",
  "reply_text": "Hi! You can reset your password from Settings → Security. Let me know if you need help!",
  "tone": "helpful",
  "voice_profile_id": "uuid"
}
```
**Result:** Draft reply created for approval

### Scenario 2: Escalate complaint
```json
{
  "mention_id": "uuid",
  "reply_text": "We're sorry to hear about your experience. Our team is looking into this.",
  "tone": "empathetic",
  "escalate": true
}
```
**Result:** Draft reply created AND flagged for human review (complaint escalation)
