---
name: bolta.audit.export_activity
version: 1.0.0
description: Export audit/activity events for a workspace (agent + human actions) for debugging and compliance.
category: ops
roles_allowed: [Owner, Admin]
tools_required:
  - bolta.export_audit_log
inputs_schema:
  type: object
  required: [workspace_id]
  properties:
    workspace_id: { type: string }
    start_time: { type: string }
    end_time: { type: string }
    actor_filter: { type: string, description: "optional principal_id" }
outputs_schema:
  type: object
  properties:
    events: { type: array, items: { type: object } }
    summary: { type: string }
organization: bolta.ai
author: Max Fritzhand
---

## Steps
1. Call `bolta.export_audit_log({workspace_id, start_time, end_time, actor_filter})`
2. Summarize:
   - top actions
   - failures
   - suspicious patterns (many denied attempts, repeated schedule calls)

## Output
Return events + a short summary.
