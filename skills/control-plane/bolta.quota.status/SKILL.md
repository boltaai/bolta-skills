# SKILL: bolta.quota.status

Display name: Quota Status
Slug: bolta-quota-status
Version: 1.0.0
Category: control
Plane: control
Organization: bolta.ai
Author: Max Fritzhand

---

## Purpose

**View current quota usage and limits for a workspace.**

This monitoring skill shows:
- Daily post count (used/limit/remaining)
- Hourly API request count (used/limit/remaining)
- Percentage usage
- Time until quota reset

**When to Use:**
- Monitoring quota usage
- Checking if approaching limits
- Troubleshooting quota exceeded errors
- Planning content schedules

---

## Required Environment Variables

```yaml
BOLTA_API_KEY:
  required: true
  description: Bolta API key

BOLTA_WORKSPACE_ID:
  required: true
  description: Workspace UUID
```

---

## Permissions

**Required:**
- `workspace:read` - View workspace information

**Roles Allowed:** All roles (owner, admin, editor, creator, reviewer, viewer)

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
    description: Workspace to check quota for
```

---

## Output Schema

```yaml
type: object
properties:
  workspace_id:
    type: string
    description: Workspace UUID

  daily_posts:
    type: object
    properties:
      limit:
        type: integer
        description: Maximum posts per day
      used:
        type: integer
        description: Posts created today
      remaining:
        type: integer
        description: Posts remaining today
      percentage:
        type: number
        description: Usage percentage (0-100)

  hourly_api_requests:
    type: object
    properties:
      limit:
        type: integer
        description: Maximum API requests per hour
      used:
        type: integer
        description: Requests made this hour
      remaining:
        type: integer
        description: Requests remaining this hour
      percentage:
        type: number
        description: Usage percentage (0-100)

  date:
    type: string
    format: date
    description: Current date (UTC)

  quota_resets_at:
    type: string
    format: date-time
    description: When daily quota resets (UTC midnight)

  warnings:
    type: array
    items:
      type: string
    description: Warnings if approaching/exceeding limits
```

---

## Usage Examples

### Example 1: Normal Usage (47%)

**Request:**
```json
{
  "workspace_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Response:**
```json
{
  "workspace_id": "550e8400-e29b-41d4-a716-446655440000",
  "daily_posts": {
    "limit": 100,
    "used": 47,
    "remaining": 53,
    "percentage": 47.0
  },
  "hourly_api_requests": {
    "limit": 1000,
    "used": 234,
    "remaining": 766,
    "percentage": 23.4
  },
  "date": "2024-03-15",
  "quota_resets_at": "2024-03-16T00:00:00Z",
  "warnings": []
}
```

### Example 2: Approaching Limit (85%)

**Response:**
```json
{
  "daily_posts": {
    "limit": 100,
    "used": 85,
    "remaining": 15,
    "percentage": 85.0
  },
  "warnings": [
    "Approaching daily quota limit: 85/100 posts used (85%)"
  ]
}
```

### Example 3: Quota Exceeded

**Response:**
```json
{
  "daily_posts": {
    "limit": 100,
    "used": 100,
    "remaining": 0,
    "percentage": 100.0
  },
  "warnings": [
    "Daily post quota exceeded: 100/100 posts used",
    "No more posts can be created until 2024-03-16T00:00:00Z",
    "Contact admin to increase quota limit or wait for reset"
  ],
  "quota_resets_at": "2024-03-16T00:00:00Z"
}
```

---

## Integration with Other Skills

**Use with:**
- `bolta.workspace.config` - Increase quotas if needed
- `bolta.draft.post` - Check before creating posts
- `bolta.loop.from_template` - Verify quota before bulk operations

---

## See Also

**Documentation:**
- [quotas.md](../../../docs/quotas.md) - Complete quota guide

**Related Skills:**
- `bolta.workspace.config` - Adjust quota limits
- `bolta.audit.export_activity` - View quota usage history

---

## Support

- GitHub: https://github.com/boltaai/bolta-skills/issues
- Email: support@bolta.ai
