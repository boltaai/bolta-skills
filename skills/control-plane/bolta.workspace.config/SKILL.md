---
name: bolta.workspace.config
version: 2.0.0
description: View and update workspace-level configuration settings including Safe Mode, autonomy mode, and quotas
category: control
roles_allowed: [Admin]
agent_types: [custom]
safe_defaults:
  require_admin: true
tools_required: []
inputs_schema:
  type: object
  required: [workspace_id]
  properties:
    workspace_id: { type: string, description: "Workspace UUID" }
    action: { type: string, enum: [view, update], description: "View or update config", default: view }
    updates: 
      type: object
      properties:
        safe_mode: { type: boolean }
        autonomy_mode: { type: string, enum: [assisted, managed, autopilot, enterprise] }
        quotas: { type: object }
outputs_schema:
  type: object
  properties:
    success: { type: boolean }
    workspace_id: { type: string }
    config: { type: object }
    updated_fields: { type: array, items: { type: string } }
organization: bolta.ai
author: Bolta Team
---

## Goal
View and update workspace-level configuration settings to control safety guardrails, autonomy modes, and workspace policies.

## Which Agents Use This
- **custom** (system/admin flows) — Used during workspace setup or policy changes
- Typically invoked by Admin users, not agents

## Hard Rules
1. MUST require Admin role for any updates
2. MUST validate autonomy_mode transitions (can't skip levels)
3. MUST NOT allow disabling Safe Mode without explicit confirmation
4. Viewer role can only view config (no updates)

## Steps

### 1. Validate permissions
- Verify workspace_id exists
- For view: require workspace:read permission
- For update: require workspace:admin permission (Admin role only)

### 2. View config (action=view)
- Return current workspace configuration
- Show Safe Mode status, autonomy mode, quotas, policies

### 3. Update config (action=update)
- Validate each update field
- Apply updates to workspace config
- Return updated config and list of changed fields

### 4. Validate autonomy mode transitions
- Assisted → Managed (allowed)
- Managed → Autopilot (requires Safe Mode off confirmation)
- Cannot skip levels

## Output

**View config:**
```json
{
  "success": true,
  "workspace_id": "uuid",
  "config": {
    "safe_mode": true,
    "autonomy_mode": "managed",
    "quotas": {
      "daily_posts": 100,
      "hourly_api_requests": 1000
    },
    "policies": {
      "require_approval_for_schedule": true
    }
  }
}
```

**Update config:**
```json
{
  "success": true,
  "workspace_id": "uuid",
  "config": { ... },
  "updated_fields": ["safe_mode", "autonomy_mode"]
}
```

## Failure Handling
- If workspace_id not found: return error "Workspace not found"
- If not Admin role: return error "Admin permission required"
- If invalid autonomy_mode transition: return error with valid transitions

## Example Usage

### Scenario 1: View current config
```json
{
  "workspace_id": "uuid",
  "action": "view"
}
```
**Result:** Receive current workspace configuration

### Scenario 2: Update Safe Mode
```json
{
  "workspace_id": "uuid",
  "action": "update",
  "updates": {
    "safe_mode": false
  }
}
```
**Result:** Safe Mode disabled (requires Admin confirmation)
