---
name: bolta.list_recent_posts
version: 2.0.0
description: Get the last N published posts for an account to avoid repetition and maintain content variety
category: content
roles_allowed: [Viewer, Creator, Editor, Admin]
agent_types: [content_creator, analytics, custom]
safe_defaults:
  default_limit: 10
  max_limit: 50
tools_required: []
inputs_schema:
  type: object
  required: [account_id]
  properties:
    account_id: { type: string, description: "Social account UUID" }
    limit: { type: number, description: "Number of posts to retrieve (default 10, max 50)", default: 10 }
outputs_schema:
  type: object
  properties:
    success: { type: boolean }
    count: { type: number }
    posts: 
      type: array
      items:
        type: object
        properties:
          id: { type: string }
          content: { type: string }
          platform: { type: string }
          published_at: { type: string }
          voice_profile_id: { type: string }
          is_ai_generated: { type: boolean }
          metrics: { type: object }
organization: bolta.ai
author: Bolta Team
---

## Goal
Get the last N published posts for an account. Use this to avoid repetition and maintain content variety.

## Which Agents Use This
- **content_creator** — Check what was posted recently to avoid repeating topics
- **analytics** — Analyze recent performance to inform strategy
- **reviewer** — Verify new content is different from recent posts
- All content-related agents benefit from recent post context

## Hard Rules
1. MUST only return published posts (not drafts or scheduled)
2. MUST order by published_at descending (most recent first)
3. MUST respect limit parameter (max 50 posts)
4. SHOULD include metrics if available

## Steps

### 1. Validate input
- Verify account_id exists and belongs to workspace
- Validate limit (default 10, max 50)

### 2. Query recent posts
- Fetch published posts for account_id
- Order by published_at desc
- Apply limit

### 3. Include post metadata
- Post content (full text)
- Platform, published timestamp
- Voice profile used
- Whether AI-generated
- Basic metrics if available

### 4. Return posts array
- Return count and posts array

## Output
```json
{
  "success": true,
  "count": 10,
  "posts": [
    {
      "id": "uuid",
      "content": "🏠 5 remote work mistakes I made...",
      "platform": "linkedin",
      "published_at": "2026-02-20T09:00:00Z",
      "voice_profile_id": "uuid",
      "is_ai_generated": true,
      "metrics": {
        "likes": 47,
        "comments": 12,
        "shares": 8,
        "engagement_rate": 0.028
      }
    }
  ]
}
```

## Failure Handling
- If account_id not found: return error "Account not found"
- If no published posts: return empty array with count: 0

## Example Usage

### Scenario: Content creator checking recent posts before drafting
```json
{
  "account_id": "uuid",
  "limit": 10
}
```
**Result:** Receive last 10 published posts to avoid topic repetition and maintain variety
