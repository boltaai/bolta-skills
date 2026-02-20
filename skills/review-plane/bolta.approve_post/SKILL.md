# bolta.approve_post

**Version:** 2.0.0  
**Category:** Review/QA  
**Agent Types:** `reviewer`, `custom`  
**Roles Allowed:** `editor`, `admin`

---

## Purpose

Approve a draft post, moving it from Inbox to Approved status, ready for scheduling or publishing.

This is the **quality gate** — only approved content moves forward.

---

## When An Agent Uses This

**Reviewer Agent reasoning:**
- "I've validated this draft against the voice profile"
- "Brand compliance checks passed"
- "Strategic timing is appropriate"
- "This is ready to publish — I'll approve it"

---

## Parameters

```json
{
  "draft_id": "string (UUID, required)",
  "notes": "string (optional)",  // Feedback for creator or human
  "approve_with_changes": false,  // Approve despite minor suggested tweaks
  "schedule_time": "ISO timestamp (optional)"  // If scheduling immediately
}
```

---

## Returns

```json
{
  "success": true,
  "post_id": "uuid",
  "status": "Approved",
  "message": "Post approved. Ready for scheduling."
}
```

---

## Hard Rules

- **MUST** validate role (editor/admin only)
- **MUST** change status: Draft → Approved
- **MUST** record approver (agent or human)
- **SHOULD** include approval reasoning in notes
