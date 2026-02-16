---
name: bolta.policy.explain
version: 1.0.0
description: Explain workspace policy and the caller's effective capabilities (what actions are allowed) in plain language.
category: ops
roles_allowed: [Owner, Admin, Creator, Viewer]
tools_required:
  - bolta.get_workspace_policy
  - bolta.get_my_capabilities
inputs_schema:
  type: object
  required: [workspace_id]
  properties:
    workspace_id: { type: string }
outputs_schema:
  type: object
  properties:
    safe_mode: { type: boolean }
    inbox_direct_scheduling: { type: boolean }
    capabilities: { type: array, items: { type: string } }
    allowed_actions_summary: { type: string }
    forbidden_actions_summary: { type: string }
---

## Steps
1. Fetch policy.
2. Fetch effective capabilities for this principal.
3. Produce:
   - Allowed: create drafts, submit review, schedule, publish, approve, manage team, etc.
   - Forbidden: anything missing.

## Output
Return policy flags + capability list + short summaries.
