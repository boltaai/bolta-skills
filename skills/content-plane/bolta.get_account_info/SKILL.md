---
name: bolta.get_account_info
version: 2.0.0
description: Get social account details including platform, handle, status, and token validity
category: content
roles_allowed: [Viewer, Creator, Editor, Admin]
agent_types: [content_creator, reviewer, analytics, engagement, custom]
safe_defaults: {}
tools_required: []
inputs_schema:
  type: object
  required: [account_id]
  properties:
    account_id: { type: string, description: "Social account UUID" }
outputs_schema:
  type: object
  properties:
    success: { type: boolean }
    account_id: { type: string }
    platform: { type: string }
    username: { type: string }
    handle: { type: string }
    display_name: { type: string }
    token_status: { type: string }
    is_active: { type: boolean }
organization: bolta.ai
author: Bolta Team
---

## Goal
Get social account details to verify platform, handle, and token validity before posting or engaging.

## Which Agents Use This
- **content_creator** — Verify which platform they're posting to
- **engagement** — Check token status before replying
- **analytics** — Validate accounts before fetching metrics
- All agent types that interact with social accounts

## Hard Rules
1. MUST validate account belongs to workspace
2. MUST return current token_status (valid/expired/revoked)
3. SHOULD cache account details for performance

## Steps

### 1. Validate account access
- Verify account_id belongs to workspace

### 2. Fetch account details
- Query Account model for metadata
- Check OAuth token status

### 3. Return account info
- Platform, username, handle, display_name
- Token status and is_active flag

## Output
```json
{
  "success": true,
  "account_id": "uuid",
  "platform": "linkedin",
  "username": "acmecorp",
  "handle": "@acmecorp",
  "display_name": "Acme Corp",
  "token_status": "valid",
  "is_active": true
}
```

## Failure Handling
- If account_id not found: return error "Account not found"
- If account not in workspace: return error "Access denied"

## Example Usage

### Scenario: Content creator verifying account before posting
```json
{
  "account_id": "uuid"
}
```
**Result:** Receive account details including platform and token status
