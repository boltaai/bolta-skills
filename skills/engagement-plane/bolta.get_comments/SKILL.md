---
name: bolta.get_comments
version: 2.0.0
description: Fetch comments on posts to monitor conversations and identify response opportunities or policy violations
category: engagement
roles_allowed: [Viewer, Creator, Editor, Admin]
agent_types: [engagement, moderator, custom]
safe_defaults: {}
tools_required:
  - platform_api_integration
inputs_schema:
  type: object
  properties:
    post_id: { type: string, description: "Specific post UUID (optional)" }
    account_id: { type: string, description: "All recent posts for account (optional)" }
    since: { type: string, description: "ISO timestamp - fetch comments since this time" }
    filter: { type: string, enum: [all, unanswered, flagged, spam_suspected], default: all }
outputs_schema:
  type: object
  properties:
    success: { type: boolean }
    count: { type: number }
    comments: 
      type: array
      items:
        type: object
        properties:
          comment_id: { type: string }
          post_id: { type: string }
          author: { type: string }
          content: { type: string }
          created_at: { type: string }
          sentiment: { type: string }
          spam_score: { type: number }
          has_response: { type: boolean }
organization: bolta.ai
author: Bolta Team
---

## Goal
Fetch comments on specific posts or across recent posts to monitor conversations, identify response opportunities, and detect policy violations.

## Which Agents Use This
- **engagement** — Monitor for questions to answer, compliments to acknowledge
- **moderator** — Scan for spam, harassment, or policy violations
- **custom** — Any agent needing comment monitoring

## Hard Rules
1. MUST provide either post_id OR account_id (not neither)
2. SHOULD calculate spam_score and sentiment for each comment
3. SHOULD flag has_response to avoid duplicate replies
4. Filter options help agents prioritize (unanswered, flagged, spam_suspected)

## Steps

### 1. Validate input
- Verify post_id OR account_id provided
- Validate since timestamp if provided

### 2. Fetch comments
- If post_id: fetch comments for that post
- If account_id: fetch comments across recent posts
- Apply since filter
- Apply filter (unanswered, flagged, spam_suspected)

### 3. Analyze comments
- Calculate spam_score (0-1, low = genuine, high = spam)
- Determine sentiment (positive, neutral, negative)
- Check has_response (did we already reply?)

### 4. Return comments array
- Include comment metadata, author, content, timestamps
- Include analysis (sentiment, spam_score, has_response)

## Output
```json
{
  "success": true,
  "count": 18,
  "comments": [
    {
      "comment_id": "uuid",
      "post_id": "uuid",
      "author": "@username",
      "content": "Great post! How does this compare to X?",
      "created_at": "2026-02-20T10:30:00Z",
      "sentiment": "positive",
      "spam_score": 0.02,
      "has_response": false
    }
  ]
}
```

## Failure Handling
- If post_id and account_id both missing: return error "Provide post_id or account_id"
- If post_id not found: return error "Post not found"
- If platform API fails: return cached comments with warning

## Example Usage

### Scenario: Engagement agent checking unanswered questions
```json
{
  "account_id": "uuid",
  "since": "2026-02-20T08:00:00Z",
  "filter": "unanswered"
}
```
**Result:** Receive list of unanswered comments since 8am for response drafting
