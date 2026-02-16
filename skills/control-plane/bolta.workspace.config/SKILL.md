# SKILL: bolta.workspace.config

Display name: Workspace Configuration
Slug: bolta-workspace-config
Version: 1.0.0
Category: control
Plane: control
Organization: bolta.ai
Author: Max Fritzhand

---

## Purpose

**View and update workspace-level configuration settings.**

This control plane skill allows administrators to:
- View current workspace settings (Safe Mode, autonomy mode, quotas)
- Update workspace policies
- Configure safety guardrails
- Manage workspace-level permissions

**When to Use:**
- Configuring workspace policies
- Enabling/disabling Safe Mode
- Changing autonomy modes
- Adjusting quota limits
- Troubleshooting policy issues

**When NOT to Use:**
- User-level settings → Use account settings
- Agent-specific config → Use agent management skills
- Post creation → Use content plane skills

---

## Required Environment Variables

```yaml
BOLTA_API_KEY:
  required: true
  description: Bolta API key with admin permissions

BOLTA_WORKSPACE_ID:
  required: true
  description: Workspace UUID to configure
```

---

## Permissions

**Required:**
- `workspace:admin` - Full workspace administration access

**Roles Allowed:** Owner, Admin only

---

## Input Schema

```yaml
type: object
required:
  - workspace_id

properties:
  workspace_id:
    type: string
    format: uuid
    description: Workspace to configure

  action:
    type: string
    enum: [view, update]
    default: view
    description: View current config or update settings

  # Update parameters (only if action=update)
  safe_mode:
    type: boolean
    description: Enable/disable Safe Mode

  autonomy_mode:
    type: string
    enum: [assisted, managed, autopilot, governance]
    description: Agent autonomy level

  max_posts_per_day:
    type: integer
    minimum: 1
    maximum: 10000
    description: Daily post quota limit

  max_api_requests_per_hour:
    type: integer
    minimum: 1
    maximum: 100000
    description: Hourly API request limit
```

---

## Output Schema

```yaml
type: object
properties:
  workspace_id:
    type: string
    description: Workspace UUID

  name:
    type: string
    description: Workspace name

  safe_mode:
    type: boolean
    description: Safe Mode status

  autonomy_mode:
    type: string
    description: Current autonomy mode

  max_posts_per_day:
    type: integer
    description: Daily post quota (null = default 100)

  max_api_requests_per_hour:
    type: integer
    description: Hourly API quota (null = default 1000)

  updated:
    type: boolean
    description: True if settings were changed

  previous_values:
    type: object
    description: Settings before update (if action=update)
```

---

## Usage Examples

### Example 1: View Current Configuration

**Request:**
```json
{
  "workspace_id": "550e8400-e29b-41d4-a716-446655440000",
  "action": "view"
}
```

**Response:**
```json
{
  "workspace_id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "My Workspace",
  "safe_mode": true,
  "autonomy_mode": "managed",
  "max_posts_per_day": 100,
  "max_api_requests_per_hour": 1000
}
```

### Example 2: Enable Safe Mode

**Request:**
```json
{
  "workspace_id": "550e8400-e29b-41d4-a716-446655440000",
  "action": "update",
  "safe_mode": true
}
```

**Response:**
```json
{
  "workspace_id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "My Workspace",
  "safe_mode": true,
  "updated": true,
  "previous_values": {
    "safe_mode": false
  }
}
```

### Example 3: Change to Autopilot Mode

**Request:**
```json
{
  "workspace_id": "550e8400-e29b-41d4-a716-446655440000",
  "action": "update",
  "autonomy_mode": "autopilot",
  "safe_mode": false
}
```

**Response:**
```json
{
  "workspace_id": "550e8400-e29b-41d4-a716-446655440000",
  "autonomy_mode": "autopilot",
  "safe_mode": false,
  "updated": true,
  "previous_values": {
    "autonomy_mode": "managed",
    "safe_mode": true
  },
  "warnings": [
    "Autopilot mode enabled: posts will be scheduled without human review",
    "Ensure quotas are configured and monitoring is active"
  ]
}
```

### Example 4: Increase Quotas

**Request:**
```json
{
  "workspace_id": "550e8400-e29b-41d4-a716-446655440000",
  "action": "update",
  "max_posts_per_day": 200,
  "max_api_requests_per_hour": 2000
}
```

**Response:**
```json
{
  "workspace_id": "550e8400-e29b-41d4-a716-446655440000",
  "max_posts_per_day": 200,
  "max_api_requests_per_hour": 2000,
  "updated": true,
  "previous_values": {
    "max_posts_per_day": 100,
    "max_api_requests_per_hour": 1000
  }
}
```

---

## See Also

- `bolta.quota.status` - View current quota usage
- `bolta.policy.explain` - Understand policy decisions
- `bolta.audit.export_activity` - Export audit logs

**Documentation:**
- [autonomy-modes.md](../../../docs/autonomy-modes.md)
- [safe-mode.md](../../../docs/safe-mode.md)
- [quotas.md](../../../docs/quotas.md)

---

## Support

- GitHub: https://github.com/boltaai/bolta-skills/issues
- Email: support@bolta.ai
