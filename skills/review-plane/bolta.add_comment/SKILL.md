# bolta.add_comment

**Version:** 2.0.0  
**Category:** Review/QA  
**Agent Types:** `reviewer`, `custom`  
**Roles Allowed:** All (read-only comments)

---

## Purpose

Add a review comment to a draft without approving or rejecting. Used for suggestions, questions, or notes.

---

## When An Agent Uses This

**Reviewer Agent reasoning:**
- "I want to approve this, but with a suggestion"
- "I have a question for the creator"
- "I want to note something for the human reviewer"

---

## Parameters

```json
{
  "post_id": "string (UUID, required)",
  "comment": "string (required)",
  "comment_type": "suggestion | question | note | praise"
}
```

---

## Returns

```json
{
  "success": true,
  "comment_id": "uuid",
  "message": "Comment added to post."
}
```

---

## Hard Rules

- **MUST** attach comment to post
- **SHOULD** specify comment type for context
- **SHOULD** be specific and actionable
