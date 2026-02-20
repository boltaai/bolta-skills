# bolta.reject_post

**Version:** 2.0.0  
**Category:** Review/QA  
**Agent Types:** `reviewer`, `custom`  
**Roles Allowed:** `editor`, `admin`

---

## Purpose

Reject a draft post with specific feedback, sending it back for revision.

Reviewer agents use this to enforce brand standards and strategic fit.

---

## When An Agent Uses This

**Reviewer Agent reasoning:**
- "This violates voice profile (uses 'leverage' — forbidden)"
- "Posted about pricing yesterday — too repetitive"
- "CTA is weak — needs specificity"
- "I'll reject with specific suggestions"

---

## Parameters

```json
{
  "draft_id": "string (UUID, required)",
  "reason": "string (required)",  // WHY rejected (specific)
  "suggestions": "string (required)",  // WHAT to fix
  "severity": "minor | major | blocking"
}
```

---

## Returns

```json
{
  "success": true,
  "post_id": "uuid",
  "status": "Rejected",
  "message": "Post rejected. Feedback provided."
}
```

---

## Hard Rules

- **MUST** provide specific reason (not "needs improvement")
- **MUST** provide actionable suggestions
- **MUST** cite voice profile when applicable
- **SHOULD** be constructive, not just critical
