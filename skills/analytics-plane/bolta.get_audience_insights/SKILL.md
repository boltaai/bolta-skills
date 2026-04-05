---
name: bolta.get_audience_insights
version: 2.0.0
description: Retrieve audience demographics, behavior patterns, and engagement trends for data-driven content strategy
category: analytics
roles_allowed: [Viewer, Creator, Editor, Admin]
agent_types: [analytics, content_creator, custom]
safe_defaults: {}
tools_required:
  - platform_api_integration
inputs_schema:
  type: object
  required: [account_id]
  properties:
    account_id: { type: string, description: "Social account UUID" }
    insights_type: { type: string, enum: [demographics, behavior, content_preferences], description: "Type of insights to retrieve" }
    time_period: { type: string, enum: [7d, 30d, 90d], description: "Rolling time window for analysis" }
outputs_schema:
  type: object
  properties:
    success: { type: boolean }
    account_id: { type: string }
    time_period: { type: string }
    insights: 
      type: object
      properties:
        demographics: { type: object }
        behavior: { type: object }
        content_preferences: { type: object }
organization: bolta.ai
author: Bolta Team
---

## Goal
Retrieve audience demographics, behavior patterns, and engagement trends to help agents understand WHO they're creating content for and HOW that audience behaves.

## Which Agents Use This
- **analytics** — Primary use case for audience analysis and reporting
- **content_creator** — Check audience preferences before drafting content
- **custom** — Any agent needing audience context for decision-making

## Hard Rules
1. MUST aggregate over time period (not single snapshot)
2. MUST identify actionable patterns (not just raw counts)
3. SHOULD compare to platform benchmarks when available
4. Require valid account_id that belongs to workspace

## Steps

### 1. Validate input
- Verify account_id exists and belongs to workspace
- Validate time_period is supported

### 2. Query platform APIs
- Fetch follower demographics from platform (LinkedIn, Twitter, etc.)
- Fetch engagement behavior data
- Fetch content performance by type

### 3. Aggregate and analyze
- Calculate growth rates
- Identify peak activity times
- Determine content format preferences
- Extract actionable patterns

### 4. Return structured insights
- Demographics: follower count, growth rate, locations, industries
- Behavior: peak activity times, session duration, engagement by day
- Content preferences: top formats, topics, optimal post length

## Output
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
      "top_industries": ["Technology", "Marketing", "SaaS"]
    },
    "behavior": {
      "peak_activity_times": ["9am-11am EST", "2pm-4pm EST"],
      "engagement_by_day": {
        "thursday": 0.038,
        "sunday": 0.012
      }
    },
    "content_preferences": {
      "top_formats": ["thread", "single_post", "carousel"],
      "top_topics": ["remote work", "productivity", "team collaboration"],
      "avg_engagement_by_length": {
        "short": 0.021,
        "medium": 0.028,
        "long": 0.034
      }
    }
  }
}
```

## Failure Handling
- If account_id not found: return error "Account not found"
- If platform API fails: return cached data with warning
- If insufficient data for time_period: suggest longer period

## Example Usage

### Scenario: Analytics agent analyzing audience
```json
{
  "account_id": "uuid",
  "insights_type": "demographics",
  "time_period": "30d"
}
```
**Result:** Receive demographic breakdown for strategy planning
