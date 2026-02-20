# bolta.reply_to_mention

**Version:** 2.0.0  
**Category:** Engagement  
**Agent Types:** `engagement`, `custom`  
**Roles Allowed:** All (creates drafts for approval)

---

## Purpose

Draft a reply to a mention, comment, or DM. Engagement agents use this to maintain community presence while staying on-brand.

---

## When An Agent Uses This

**Engagement Agent reasoning:**
- "This question is common — I can draft a helpful response"
- "This complaint needs de-escalation — I'll draft an empathetic reply"
- "This is a compliment — I'll draft a warm thank you"

---

## Parameters

```json
{
  "mention_id": "uuid (required)",
  "reply_text": "string (required)",
  "tone": "helpful | empathetic | professional",
  "escalate": false,  // If true, flag for human review
  "voice_profile_id": "uuid (optional)"
}
```

---

## Returns

```json
{
  "success": true,
  "draft_reply_id": "uuid",
  "status": "draft",
  "requires_approval": true,
  "escalated": false
}
```

---

## Hard Rules

- **MUST** match brand voice (use voice_profile_id)
- **MUST** create draft (not publish directly) unless role=editor+Safe Mode off
- **MUST** escalate sensitive topics (refunds, complaints, legal)
- **MUST NOT** use generic template responses
