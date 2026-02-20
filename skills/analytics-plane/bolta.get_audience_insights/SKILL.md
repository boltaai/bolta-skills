# bolta.get_audience_insights

**Version:** 2.0.0  
**Category:** Analytics  
**Agent Types:** `analytics`, `custom`  
**Roles Allowed:** All

---

## Purpose

Retrieve audience demographics, behavior patterns, and engagement trends.

Helps agents understand WHO they're creating content for and HOW that audience behaves.

---

## When An Agent Uses This

**Analytics Agent reasoning:**
- "I need to understand our audience composition"
- "What topics resonate most with our followers?"
- "When is our audience most active?"

**Content Creator reasoning:**
- "Let me check if my audience is B2B or B2C"
- "What content format does my audience prefer?"

---

## Parameters

```json
{
  "account_id": "uuid (required)",
  "insights_type": "demographics | behavior | content_preferences",
  "time_period": "7d | 30d | 90d"  // Rolling window
}
```

---

## Returns

```json
{
  "success": true,
  "account_id": "uuid",
  "time_period": "30d",
  "insights": {
    "demographics": {
      "follower_count": 12450,
      "growth_rate_30d": 0.08,
      "top_locations": ["United States", "United Kingdom", "Canada"],
      "top_industries": ["Technology", "Marketing", "SaaS"],
      "avg_follower_size": "1k-10k"  // How big is typical follower
    },
    "behavior": {
      "peak_activity_times": ["9am-11am EST", "2pm-4pm EST"],
      "avg_session_duration": "3m 42s",
      "engagement_by_day": {
        "monday": 0.024,
        "thursday": 0.038,  // Highest
        "sunday": 0.012     // Lowest
      }
    },
    "content_preferences": {
      "top_formats": ["thread", "single_post", "carousel"],
      "top_topics": ["remote work", "productivity", "team collaboration"],
      "avg_engagement_by_length": {
        "short": 0.021,
        "medium": 0.028,
        "long": 0.034  // Longer content performs better
      }
    }
  }
}
```

---

## Hard Rules

- **MUST** aggregate over time period (not single snapshot)
- **MUST** identify actionable patterns (not just raw counts)
- **SHOULD** compare to platform benchmarks when available
