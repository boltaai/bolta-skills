---
name: bolta.get_post_metrics
version: 2.0.0
description: Retrieve performance metrics for published posts including likes, comments, shares, views, and engagement rate
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
    limit: { type: number, description: "Number of posts to analyze", default: 50 }
    date_from: { type: string, description: "ISO date (optional)" }
    date_to: { type: string, description: "ISO date (optional)" }
    platform: { type: string, enum: [linkedin, twitter, instagram], description: "Optional platform filter" }
outputs_schema:
  type: object
  properties:
    success: { type: boolean }
    count: { type: number }
    metrics: 
      type: array
      items:
        type: object
        properties:
          post_id: { type: string }
          content_preview: { type: string }
          published_at: { type: string }
          platform: { type: string }
          likes: { type: number }
          comments: { type: number }
          shares: { type: number }
          views: { type: number }
          impressions: { type: number }
          engagement_rate: { type: number }
organization: bolta.ai
author: Bolta Team
---

## Goal
Retrieve performance metrics for published posts to identify patterns and make data-driven content recommendations. Analytics agents use this to understand what works and what doesn't.

## Which Agents Use This
- **analytics** — Primary use case for performance analysis and reporting
- **content_creator** — Check what content types/topics performed best before drafting
- **custom** — Any agent needing historical performance context

## Hard Rules
1. MUST only return metrics for published posts (not drafts or scheduled)
2. SHOULD calculate engagement_rate consistently: (likes + comments + shares) / impressions
3. SHOULD include enough context to identify content patterns (preview, platform, timestamp)
4. Require valid account_id that belongs to workspace

## Steps

### 1. Validate input
- Verify account_id exists and belongs to workspace
- Validate date range if provided
- Apply limit (max 100 posts per request)

### 2. Query posts
- Fetch published posts for account_id within date range
- Filter by platform if specified
- Order by published_at desc

### 3. Fetch platform metrics
- For each post, query platform API for performance data
- Collect: likes, comments, shares, views, impressions
- Calculate engagement_rate

### 4. Return structured metrics
- Include post metadata (id, preview, published_at, platform)
- Include raw metrics (likes, comments, shares, views, impressions)
- Include calculated metrics (engagement_rate)

## Output
```json
{
  "success": true,
  "count": 25,
  "metrics": [
    {
      "post_id": "uuid",
      "content_preview": "🏠 5 remote work mistakes I made...",
      "published_at": "2026-02-15T09:00:00Z",
      "platform": "linkedin",
      "likes": 47,
      "comments": 12,
      "shares": 8,
      "views": 2340,
      "impressions": 8920,
      "engagement_rate": 0.0075
    }
  ]
}
```

## Failure Handling
- If account_id not found: return error "Account not found"
- If platform API fails: return cached/stale data with warning
- If no posts found in date range: return empty array with message

## Example Usage

### Scenario: Analytics agent analyzing recent performance
```json
{
  "account_id": "uuid",
  "limit": 50,
  "date_from": "2026-01-01",
  "platform": "linkedin"
}
```
**Result:** Receive metrics for last 50 LinkedIn posts since Jan 1 for pattern analysis
