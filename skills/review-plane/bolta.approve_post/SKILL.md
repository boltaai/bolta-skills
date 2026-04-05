---
name: bolta.approve_post
version: 2.0.0
description: Approve a draft post, moving it from Inbox to Approved status, ready for scheduling or publishing
category: review
roles_allowed: [Editor, Admin]
agent_types: [reviewer, custom]
safe_defaults:
  require_editor_role: true
tools_required:
  - bolta.update_post
inputs_schema:
  type: object
  required: [draft_id]
  properties:
    draft_id: { type: string, description: "Draft post UUID to approve" }
    notes: { type: string, description: "Feedback for creator or human (optional)" }
    approve_with_changes: { type: boolean, description: "Approve despite minor suggested tweaks", default: false }
    schedule_time: { type: string, description: "ISO timestamp if scheduling immediately (optional)" }
outputs_schema:
  type: object
  properties:
    success: { type: boolean }
    post_id: { type: string }
    status: { type: string, enum: [Approved, Scheduled] }
    message: { type: string }
organization: bolta.ai
author: Bolta Team
---

## Goal
Approve a draft post, moving it from Inbox to Approved status. This is the **quality gate** — only approved content moves forward.

## Which Agents Use This
- **reviewer** — Validate drafts against voice profile, brand compliance, and strategy
- **custom** — Any agent with review permissions
- Requires Editor or Admin role

## Hard Rules
1. MUST validate role (Editor/Admin only)
2. MUST change status: Draft → Approved (or Scheduled if schedule_time provided)
3. MUST record approver (agent or human)
4. SHOULD include approval reasoning in notes
5. MUST NOT approve posts that violate voice profile or brand guidelines

## Steps

### 1. Validate permissions
- Verify user/agent has Editor or Admin role
- Verify draft_id exists and is in reviewable state

### 2. Validate draft quality
- Check against voice profile (if reviewer agent)
- Verify brand compliance
- Confirm strategic fit

### 3. Approve post
- Update post status: Draft → Approved
- Record approver (agent_id or user_id)
- Add approval notes if provided
- Timestamp approval

### 4. Schedule if requested
- If schedule_time provided:
  - Validate time is future
  - Update post status: Approved → Scheduled
  - Set scheduled_time

### 5. Return confirmation
- Return post_id, new status, confirmation message

## Output
```json
{
  "success": true,
  "post_id": "uuid",
  "status": "Approved",
  "message": "Post approved. Ready for scheduling."
}
```

## Failure Handling
- If not Editor/Admin role: return error "Permission denied - Editor role required"
- If draft_id not found: return error "Draft not found"
- If schedule_time invalid (past): return error "Schedule time must be in future"

## Example Usage

### Scenario 1: Reviewer agent approving draft
```json
{
  "draft_id": "uuid",
  "notes": "Voice profile match verified. Strategic timing appropriate. Approved."
}
```
**Result:** Post moved to Approved status, ready for scheduling

### Scenario 2: Approve and schedule immediately
```json
{
  "draft_id": "uuid",
  "notes": "Great content, scheduling for optimal time.",
  "schedule_time": "2026-02-21T09:00:00Z"
}
```
**Result:** Post approved AND scheduled for 9am tomorrow
