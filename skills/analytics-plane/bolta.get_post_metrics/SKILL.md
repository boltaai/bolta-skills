# bolta.get_post_metrics

**Version:** 2.0.0  
**Category:** Analytics  
**Agent Types:** `analytics`, `content_creator`, `custom`  
**Roles Allowed:** All

---

## Purpose

Retrieve performance metrics for published posts: likes, comments, shares, views, impressions, and engagement rate.

Analytics agents use this to identify patterns and make data-driven recommendations.

---

## When An Agent Uses This

**Analytics Agent reasoning:**
- "I need to identify which content types perform best"
- "Let me compare performance across platforms"
- "What posting times correlate with higher engagement?"

**Content Creator reasoning:**
- "Before drafting, let me see what worked last week"
- "Educational posts seem to perform better — let me confirm with data"

---

## Parameters

```json
{
  "account_id": "uuid (required)",
  "limit": 50,           // Number of posts to analyze
  "date_from": "2026-02-01",  // ISO date (optional)
  "date_to": "2026-02-20",    // ISO date (optional)
  "platform": "linkedin | twitter | instagram"  // Optional filter
}
```

---

## Returns

```json
{
  "success": true,
  "count": 25,
  "metrics": [
    {
      "post_id": "uuid",
      "content_preview": "First 100 chars...",
      "published_at": "2026-02-15T09:00:00Z",
      "platform": "linkedin",
      "likes": 47,
      "comments": 12,
      "shares": 8,
      "views": 2340,
      "impressions": 5670,
      "engagement_rate": 0.028,  // (likes+comments+shares)/impressions
      "ctr": 0.013  // clicks/impressions (if available)
    }
  ],
  "averages": {
    "likes": 35.2,
    "comments": 8.4,
    "engagement_rate": 0.022
  }
}
```

---

## Hard Rules

- **MUST** return only published posts (not drafts)
- **MUST** calculate engagement_rate consistently
- **MUST** filter by account_id + workspace (security)
- **SHOULD** include comparison to account averages
