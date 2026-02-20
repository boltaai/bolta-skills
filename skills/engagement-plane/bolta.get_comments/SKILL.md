# bolta.get_comments

**Version:** 2.0.0  
**Category:** Engagement  
**Agent Types:** `engagement`, `moderator`, `custom`  
**Roles Allowed:** All

---

## Purpose

Fetch comments on a specific post or across recent posts. Used by engagement/moderation agents to monitor conversations and identify response opportunities or policy violations.

---

## When An Agent Uses This

**Engagement Agent reasoning:**
- "Let me check comments on our latest post"
- "Are there questions I can answer?"

**Moderator Agent reasoning:**
- "I need to scan for spam or harassment"
- "Are there policy violations?"

---

## Parameters

```json
{
  "post_id": "uuid (optional)",  // Specific post
  "account_id": "uuid (optional)",  // All recent posts
  "since": "2026-02-20T08:00:00Z",
  "filter": "all | unanswered | flagged | spam_suspected"
}
```

---

## Returns

```json
{
  "success": true,
  "count": 18,
  "comments": [
    {
      "comment_id": "uuid",
      "post_id": "uuid",
      "author": "@username",
      "content": "Great post! How does this compare to X?",
      "created_at": "2026-02-20T10:30:00Z",
      "sentiment": "positive",
      "spam_score": 0.02,  // Low = likely genuine
      "has_response": false
    }
  ]
}
```

---

## Hard Rules

- **MUST** include spam scoring
- **MUST** flag policy violations (harassment, hate speech)
- **SHOULD** prioritize comments with questions
