# bolta.agent.configure

**Version:** 2.0.0  
**Category:** Agent Lifecycle  
**Agent Types:** `custom` (system)  
**Roles Allowed:** `admin`, `editor`

---

## Purpose

Modify an existing agent's configuration: persona, model tier, enabled skills, and job settings.

This is how users customize hired agents to match their specific needs.

---

## When Used

- User wants to adjust agent personality after hiring
- User needs to change model tier (Sonnet ↔ Opus) for quality/cost tradeoffs
- User wants to enable/disable specific skills
- User needs to update job schedules or instructions

---

## What This Does

Updates Agent model fields:
- `persona` — Personality and behavioral guidelines
- `model` — Claude model tier (sonnet/opus/haiku)
- `enabled_skills` — Which tools the agent can use
- Jobs associated with agent (schedule, run_instructions)

---

## Parameters

```json
{
  "agent_id": "uuid",
  "updates": {
    "persona": "string (optional)",
    "model": "claude-sonnet-4" | "claude-opus-4" | "claude-haiku-4",
    "enabled_skills": ["skill.name.1", "skill.name.2"],
    "job_updates": [
      {
        "job_id": "uuid",
        "schedule": {"cron": "0 9 * * 1,3,5"},
        "run_instructions": "Updated task brief"
      }
    ]
  }
}
```

---

## Hard Rules

- **MUST** validate agent_id belongs to workspace
- **MUST** preserve agent type (can't change content_creator → reviewer)
- **MUST** validate enabled_skills against agent type permissions
- **MUST NOT** allow breaking changes while jobs are active (pause first)

---

## Integration

**Before:** `bolta.agent.hire` creates agent
**After:** User can activate jobs with `bolta.agent.activate_job`
