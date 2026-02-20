# bolta.list_recent_posts

**Version:** 2.0.0  
**Category:** Content Creation  
**Agent Types:** `content_creator`, `analytics`, `custom`  
**Roles Allowed:** All

---

## Purpose

Get the last N published posts for an account. Use this to avoid repetition and maintain content variety.

---

## When An Agent Uses This

**Content Creator:** "Before drafting, let me check what I posted recently to avoid repeating topics"  
**Analytics:** "Let me analyze recent performance to inform strategy"

---

## Parameters

```json
{
  "account_id": "string (UUID, required)",
  "limit": 10  // Default: 10, max: 50
}
```

---

## Returns

```json
{
  "success": true,
  "count": 10,
  "posts": [
    {
      "id": "uuid",
      "content": "Post content...",
      "platform": "linkedin",
      "published_at": "2026-02-20T09:00:00Z",
      "voice_profile_id": "uuid",
      "is_ai_generated": true,
      "metrics": {
        "likes": 47,
        "comments": 12,
        "shares": 8
      }
    }
  ],
  "account_platform": "linkedin"
}
```

---

## Hard Rules

- **MUST** return only published posts (status="Published")
- **MUST** order by `created_at` DESC (most recent first)
- **MUST** cap limit at 50 (prevent excessive queries)
