---
name: bolta.team.rotate_key
version: 1.0.0
description: Rotate or revoke an existing API key for a human or agent principal, issuing a replacement key.
category: ops
roles_allowed: [Owner, Admin]
tools_required:
  - bolta.get_my_capabilities
  - bolta.rotate_api_key
inputs_schema:
  type: object
  required: [workspace_id, api_key_id]
  properties:
    workspace_id: { type: string }
    api_key_id: { type: string }
    action: { type: string, enum: [rotate, revoke], default: rotate }
    new_label: { type: string }
outputs_schema:
  type: object
  properties:
    result: { type: string, enum: [rotated, revoked] }
    new_api_key_preview: { type: string }
organization: bolta.ai
author: Max Fritzhand
---

## Steps
1. Check capability: `team:manage_keys`.
2. Call:
   - `bolta.rotate_api_key({workspace_id, api_key_id, action, new_label})`
3. Output result.

## Safety
- If revoke is requested, confirm no automation depends on it (if you can detect), otherwise warn in output.
