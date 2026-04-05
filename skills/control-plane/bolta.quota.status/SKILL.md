---
name: bolta.quota.status
version: 2.0.0
description: View current quota usage and limits for a workspace including post count, API requests, and reset timers
category: control
roles_allowed: [Viewer, Creator, Editor, Admin]
agent_types: [analytics, custom]
safe_defaults: {}
tools_required: []
inputs_schema:
  type: object
  required: [workspace_id]
  properties:
    workspace_id: { type: string, description: "Workspace UUID" }
outputs_schema:
  type: object
  properties:
    success: { type: boolean }
    daily_posts: { type: object }
    hourly_api_requests: { type: object }
    percentage_used: { type: number }
    time_until_reset: { type: string }
organization: bolta.ai
author: Bolta Team
---

## Goal
View current quota usage and limits for a workspace to monitor usage, check if approaching limits, and plan content schedules.

## Which Agents Use This
- **analytics** — Monitor quota usage as part of workspace health reporting
- **custom** — Any agent that needs to check quota status before executing tasks
- Humans use this to troubleshoot quota exceeded errors

## Hard Rules
1. MUST show current usage vs limits
2. MUST show time until quota reset
3. SHOULD show percentage usage for quick visual assessment
4. Require workspace:read permission

## Steps

### 1. Validate workspace access
- Verify workspace_id exists
- Verify user has workspace:read permission

### 2. Query quota usage
- Fetch daily post count (used/limit)
- Fetch hourly API request count (used/limit)
- Calculate remaining quota
- Calculate percentage used

### 3. Calculate reset time
- Determine time until daily reset (midnight UTC)
- Determine time until hourly reset (top of next hour)

### 4. Return quota status
- Usage counts, limits, remaining
- Percentage used
- Time until reset

## Output
```json
{
  "success": true,
  "daily_posts": {
    "used": 47,
    "limit": 100,
    "remaining": 53,
    "resets_in": "4h 23m"
  },
  "hourly_api_requests": {
    "used": 234,
    "limit": 1000,
    "remaining": 766,
    "resets_in": "23m"
  },
  "percentage_used": {
    "posts": 0.47,
    "api": 0.234
  }
}
```

## Failure Handling
- If workspace_id not found: return error "Workspace not found"
- If no permission: return error "Access denied"

## Example Usage

### Scenario: Analytics agent checking quota before bulk job
```json
{
  "workspace_id": "uuid"
}
```
**Result:** Receive current quota status to determine if bulk job can proceed
