# bolta.get_mentions

**Version:** 2.0.0  
**Category:** Engagement  
**Agent Types:** `engagement`, `custom`  
**Roles Allowed:** All

---

## Purpose

Fetch recent mentions, replies, and comments directed at the account. Used by engagement agents to monitor and respond to community interactions.

---

## When An Agent Uses This

**Engagement Agent reasoning:**
- "Let me check for new mentions since my last run"
- "I need to identify which mentions need responses"
- "Are there any complaints or urgent issues?"

---

## Parameters

```json
{
  "account_id": "uuid (required)",
  "since": "2026-02-20T08:00:00Z",  // ISO timestamp (optional)
  "limit": 50,
  "filter": "all | unanswered | flagged"
}
```

---

## Returns

```json
{
  "success": true,
  "count": 12,
  "mentions": [
    {
      "mention_id": "uuid",
      "author": "@username",
      "content": "Hey @brand, how do I reset my password?",
      "platform": "twitter",
      "created_at": "2026-02-20T09:15:00Z",
      "sentiment": "neutral | positive | negative",
      "has_response": false,
      "priority": "normal | high | urgent"
    }
  ]
}
```

---

## Hard Rules

- **MUST** mark mentions as "seen" after retrieval
- **MUST** include sentiment analysis (for triage)
- **SHOULD** flag urgent/negative mentions for immediate attention
