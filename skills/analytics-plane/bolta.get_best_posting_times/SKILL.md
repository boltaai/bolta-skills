# bolta.get_best_posting_times

**Version:** 2.0.0  
**Category:** Analytics  
**Agent Types:** `analytics`, `content_creator`, `custom`  
**Roles Allowed:** All

---

## Purpose

Analyze historical performance to recommend optimal posting schedule based on when YOUR specific audience is most engaged.

Not generic "best times" — data-driven recommendations for this account.

---

## When An Agent Uses This

**Analytics Agent reasoning:**
- "Let me analyze posting patterns vs. engagement to find optimal times"
- "Content Creator should know when to schedule for maximum reach"

**Content Creator reasoning:**
- "Before scheduling, let me check when posts perform best"
- "I remember Thursday was good — let me confirm the specific time"

---

## Parameters

```json
{
  "account_id": "uuid (required)",
  "platform": "linkedin | twitter | instagram",
  "analysis_period": "30d | 90d",  // How far back to analyze
  "min_posts_required": 10  // Need enough data for valid analysis
}
```

---

## Returns

```json
{
  "success": true,
  "account_id": "uuid",
  "platform": "linkedin",
  "analysis_period": "90d",
  "posts_analyzed": 47,
  "recommendations": [
    {
      "day": "Thursday",
      "time": "9:00 AM EST",
      "avg_engagement_rate": 0.038,
      "confidence": "high",  // Based on sample size
      "reason": "47% higher engagement than account average"
    },
    {
      "day": "Tuesday",
      "time": "2:00 PM EST",
      "avg_engagement_rate": 0.032,
      "confidence": "medium",
      "reason": "Consistent performance, lower variance"
    }
  ],
  "avoid_times": [
    {
      "day": "Sunday",
      "time": "morning",
      "reason": "62% lower engagement than average"
    }
  ],
  "summary": "Your audience engages most on weekday mornings (9-11am EST), especially Thursday. Avoid weekends."
}
```

---

## Hard Rules

- **MUST** require minimum post count for statistical validity
- **MUST** account for platform algorithms (LinkedIn ≠ Twitter patterns)
- **MUST** compare to account baseline (not platform averages)
- **SHOULD** indicate confidence level based on sample size
