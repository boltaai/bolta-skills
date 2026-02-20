---
name: bolta.agent.configure
version: 2.0.0
description: Modify an existing agent's configuration including persona, model tier, enabled skills, and job settings
category: agent
roles_allowed: [Editor, Admin]
agent_types: [custom]
safe_defaults:
  require_job_pause_for_breaking_changes: true
tools_required:
  - bolta.get_agent
  - bolta.update_agent
  - bolta.list_jobs
  - bolta.update_job
inputs_schema:
  type: object
  required: [agent_id, updates]
  properties:
    agent_id: { type: string, description: "Agent UUID to configure" }
    updates: 
      type: object
      properties:
        persona: { type: string, description: "Personality and behavioral guidelines" }
        model: { type: string, enum: [claude-sonnet-4, claude-opus-4, claude-haiku-4], description: "Claude model tier" }
        enabled_skills: { type: array, items: { type: string }, description: "Skills this agent can use" }
        job_updates: 
          type: array
          items:
            type: object
            properties:
              job_id: { type: string }
              schedule: { type: object }
              run_instructions: { type: string }
outputs_schema:
  type: object
  properties:
    agent_id: { type: string }
    updated_fields: { type: array, items: { type: string } }
    warnings: { type: array, items: { type: string } }
organization: bolta.ai
author: Bolta Team
---

## Goal
Modify an existing agent's configuration to customize persona, model tier, enabled skills, and job settings after hiring.

## Which Agents Use This
- **custom** (system/configuration flows) — Used when users need to adjust agent behavior or settings post-hiring

## Hard Rules
1. MUST validate agent_id belongs to workspace
2. MUST preserve agent type (can't change content_creator → reviewer)
3. MUST validate enabled_skills against agent type permissions
4. MUST NOT allow breaking changes while jobs are active (require pause first)
5. Model tier changes require Admin role

## Steps

### 1. Validate agent and permissions
- `bolta.get_agent(agent_id)` → verify agent exists and belongs to workspace
- Check user role has permission to modify requested fields

### 2. Validate updates
- If updating persona: validate format and length
- If updating model: verify tier is valid for agent type
- If updating enabled_skills: validate each skill exists and is allowed for agent type
- If updating jobs: `bolta.list_jobs(agent_id)` → verify all job_ids belong to this agent

### 3. Check for breaking changes
- If jobs are currently active AND updates would break them:
  - Return error: "Pause jobs before making breaking changes"
  - Breaking changes: model tier downgrade, removing required skills
- Non-breaking changes can proceed even with active jobs

### 4. Apply updates
- `bolta.update_agent(agent_id, updates)`
- For each job_update:
  - `bolta.update_job(job_id, {schedule, run_instructions})`

### 5. Return confirmation
- List which fields were updated
- Include warnings if any (e.g., "Model tier downgrade may affect quality")

## Output
```json
{
  "agent_id": "uuid",
  "updated_fields": ["persona", "model", "enabled_skills"],
  "warnings": ["Model downgrade from Opus to Sonnet may reduce output quality"]
}
```

## Failure Handling
- If agent_id not found: fail with "Agent not found"
- If breaking changes attempted with active jobs: fail with "Pause jobs first"
- If invalid skill name provided: fail with "Skill 'xyz' not found or not allowed for this agent type"
- Partial updates allowed: if job_updates fail, agent updates still succeed (with warning)

## Example Usage

### Scenario 1: Adjust persona only
```json
{
  "agent_id": "uuid",
  "updates": {
    "persona": "More enthusiastic and emoji-heavy for social engagement"
  }
}
```
**Result:** Agent persona updated, no other changes

### Scenario 2: Upgrade model tier
```json
{
  "agent_id": "uuid",
  "updates": {
    "model": "claude-opus-4"
  }
}
```
**Result:** Agent now uses Opus (higher quality, higher cost)

### Scenario 3: Update job schedule
```json
{
  "agent_id": "uuid",
  "updates": {
    "job_updates": [
      {
        "job_id": "uuid",
        "schedule": {"cron": "0 9 * * 1,3,5"},
        "run_instructions": "Create 1 LinkedIn post about remote work best practices"
      }
    ]
  }
}
```
**Result:** Job now runs Monday, Wednesday, Friday at 9am with new instructions
