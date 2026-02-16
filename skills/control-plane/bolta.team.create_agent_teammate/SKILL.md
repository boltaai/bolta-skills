---
name: bolta.team.create_agent_teammate
version: 1.0.0
description: Create an agent identity (service account) inside a workspace and issue an API key with least privilege.
category: ops
roles_allowed: [Owner, Admin]
tools_required:
  - bolta.get_my_capabilities
  - bolta.create_agent_principal
inputs_schema:
  type: object
  required: [workspace_id, agent_name]
  properties:
    workspace_id: { type: string }
    agent_name: { type: string }
    role: { type: string, enum: [Creator, Viewer, Admin], default: Creator }
    key_label: { type: string }
outputs_schema:
  type: object
  properties:
    agent_id: { type: string }
    role: { type: string }
    api_key_preview: { type: string }
    allowed_actions: { type: array, items: { type: string } }
---

## Rules
- Default role is Creator.
- Never create an Admin agent unless explicitly requested.

## Steps
1. Verify capability includes `team:manage` (or equivalent).
2. Create agent principal:
   - `bolta.create_agent_principal({workspace_id, name: agent_name, role, key_label})`
3. Return agent_id, role, key preview, allowed actions.

## Output
Return created agent identity + capabilities summary.
