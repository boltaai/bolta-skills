---
name: bolta.get_mentions
version: 2.0.0
description: Fetch recent mentions, replies, and comments directed at the account for community engagement monitoring
category: engagement
roles_allowed: [Viewer, Creator, Editor, Admin]
agent_types: [engagement, custom]
safe_defaults: {}
tools_required:
  - platform_api_integration
inputs_schema:
  type: object
  required: [account_id]
  properties:
    account_id: { type: string, description: "Social account UUID" }
    since: { type: string, description: "ISO timestamp - fetch mentions since this time" }
    limit: { type: number, description: "Max mentions to return", default: 50 }
    filter: { type: string, enum: [all, unanswered, flagged], default: all }
outputs_schema:
  type: object
  properties:
    success: { type: boolean }
    count: { type: number }
    mentions: 
      type: array
      items:
        type: object
        properties:
          mention_id: { type: string }
          author: { type: string }
          content: { type: string }
          platform: { type: string }
          created_at: { type: string }
          sentiment: { type: string }
          has_response: { type: boolean }
          priority: { type: string }
organization: bolta.ai
author: Bolta Team
---

## Goal
Fetch recent mentions, replies, and comments directed at the account to monitor and respond to community interactions.

## Which Agents Use This
- **engagement** — Monitor for new mentions since last run, identify which need responses
- **moderator** — Check for complaints or urgent issues requiring human escalation
- **custom** — Any agent handling community engagement

## Hard Rules
1. MUST fetch mentions directed at the account (not general brand mentions)
2. SHOULD calculate sentiment and priority for triage
3. SHOULD flag has_response to avoid duplicate replies
4. Priority levels help agents decide what to respond to first

## Steps

### 1. Validate input
- Verify account_id exists and belongs to workspace
- Validate since timestamp if provided
- Apply limit (max 100)

### 2. Fetch mentions from platform
- Query platform API for mentions/replies/@mentions
- Filter by since timestamp
- Apply filter (all, unanswered, flagged)

### 3. Analyze mentions
- Determine sentiment (positive, neutral, negative)
- Calculate priority (normal, high, urgent) based on:
  - Sentiment (complaints = higher priority)
  - Keywords (refund, broken, help = urgent)
  - Author influence/follower count
- Check has_response

### 4. Return mentions array
- Include mention metadata, author, content, timestamps
- Include analysis (sentiment, priority, has_response)

## Output
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
      "sentiment": "neutral",
      "has_response": false,
      "priority": "high"
    }
  ]
}
```

## Failure Handling
- If account_id not found: return error "Account not found"
- If platform API fails: return cached mentions with warning
- If no mentions found: return empty array with count: 0

## Example Usage

### Scenario: Engagement agent checking for new mentions
```json
{
  "account_id": "uuid",
  "since": "2026-02-20T08:00:00Z",
  "filter": "unanswered"
}
```
**Result:** Receive list of unanswered mentions since 8am for response prioritization
