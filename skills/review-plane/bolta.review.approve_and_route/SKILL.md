---
name: bolta.review.approve_and_route
version: 1.0.0
description: Approve pending review posts and route them to scheduled or back to draft based on workspace policy and per-post settings.
category: review
roles_allowed: [Owner, Admin]
tools_required:
  - bolta.get_workspace_policy
  - bolta.get_my_capabilities
  - bolta.approve_post
  - bolta.schedule_post
  - bolta.update_post
inputs_schema:
  type: object
  required: [workspace_id, post_ids]
  properties:
    workspace_id: { type: string }
    post_ids: { type: array, items: { type: string } }
    schedule_mode: { type: string, enum: [use_suggested_time, set_fixed_time, approve_only], default: approve_only }
    fixed_time: { type: string }
outputs_schema:
  type: object
  properties:
    approved_ids: { type: array, items: { type: string } }
    scheduled_ids: { type: array, items: { type: string } }
    failed: { type: array, items: { type: object } }
organization: bolta.ai
author: Max Fritzhand
---

## Hard rules
- Must have `review:approve` capability.
- Scheduling only if capability includes `posts:schedule`.
- If Inbox Direct Scheduling is OFF, do not auto-schedule unless schedule_mode explicitly requests it.

## Steps
1. Fetch policy + capabilities.
2. For each post_id:
   - Approve: `bolta.approve_post({post_id})`
   - If schedule_mode == approve_only: stop.
   - Else schedule if allowed:
     - If use_suggested_time: call schedule with post's suggested time if present; otherwise skip with warning.
     - If set_fixed_time: schedule using fixed_time.
3. If scheduling not allowed, keep approved but unscheduled and record failure reason.

## Output
Return approved_ids, scheduled_ids, failed[].
