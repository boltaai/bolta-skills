---
name: bolta.get_best_posting_times
version: 2.0.0
description: Analyze historical performance to recommend optimal posting schedule based on when YOUR specific audience is most engaged
category: analytics
roles_allowed: [Viewer, Creator, Editor, Admin]
agent_types: [analytics, content_creator, custom]
safe_defaults:
  min_posts_required: 10
tools_required:
  - bolta.get_post_metrics
inputs_schema:
  type: object
  required: [account_id]
  properties:
    account_id: { type: string, description: "Social account UUID" }
    platform: { type: string, enum: [linkedin, twitter, instagram], description: "Target platform" }
    analysis_period: { type: string, enum: [30d, 90d], description: "How far back to analyze" }
    min_posts_required: { type: number, description: "Minimum posts needed for valid analysis", default: 10 }
outputs_schema:
  type: object
  properties:
    success: { type: boolean }
    account_id: { type: string }
    posts_analyzed: { type: number }
    recommendations: 
      type: array
      items:
        type: object
        properties:
          day: { type: string }
          time: { type: string }
          avg_engagement_rate: { type: number }
          confidence: { type: string }
          reason: { type: string }
organization: bolta.ai
author: Bolta Team
---

## Goal
Analyze historical performance to recommend optimal posting schedule based on when YOUR specific audience is most engaged. Not generic "best times" — data-driven recommendations for this account.

## Which Agents Use This
- **analytics** — Primary use case for schedule optimization analysis
- **content_creator** — Check best times before scheduling posts
- **custom** — Any agent needing timing optimization for content

## Hard Rules
1. MUST analyze actual account performance (not generic platform averages)
2. MUST require minimum sample size (default 10 posts) for valid recommendations
3. SHOULD indicate confidence level based on sample size
4. SHOULD explain WHY each time is recommended (e.g., "47% higher engagement")

## Steps

### 1. Validate input
- Verify account_id exists and belongs to workspace
- Check if enough posts exist for analysis_period

### 2. Fetch historical performance
- `bolta.get_post_metrics(account_id, analysis_period)`
- Extract published_at timestamp and engagement metrics for each post

### 3. Analyze patterns
- Group posts by day of week and time of day
- Calculate avg engagement rate for each time slot
- Identify statistically significant patterns
- Compare to account baseline

### 4. Generate recommendations
- Rank time slots by performance
- Calculate confidence based on sample size
- Explain why each time performs well
- Return top 3-5 recommendations

## Output
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
      "confidence": "high",
      "reason": "47% higher engagement than account average"
    },
    {
      "day": "Tuesday",
      "time": "2:00 PM EST",
      "avg_engagement_rate": 0.032,
      "confidence": "medium",
      "reason": "32% higher, but only 8 posts in this slot"
    }
  ]
}
```

## Failure Handling
- If < min_posts_required: return error "Need at least 10 posts for analysis"
- If account_id not found: return error "Account not found"
- If platform API fails: return error with suggestion to retry

## Example Usage

### Scenario: Content creator checking best time before scheduling
```json
{
  "account_id": "uuid",
  "platform": "linkedin",
  "analysis_period": "90d"
}
```
**Result:** Receive data-driven schedule recommendations for optimal engagement
