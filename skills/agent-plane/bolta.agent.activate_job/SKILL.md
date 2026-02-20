---
name: bolta.agent.activate_job
version: 2.0.0
description: Activate a paused job after preview and voice validation - the explicit trust moment where user says "yes, start posting"
category: agent
roles_allowed: [Editor, Admin]
agent_types: [custom]
safe_defaults:
  require_explicit_confirmation: true
  validate_prerequisites: true
tools_required:
  - bolta.get_job
  - bolta.update_job
  - bolta.get_voice_profile
  - bolta.get_account_info
inputs_schema:
  type: object
  required: [job_id, confirm_preview_reviewed, confirm_schedule_understood]
  properties:
    job_id: { type: string, description: "Job UUID to activate" }
    confirm_preview_reviewed: { type: boolean, description: "Explicit confirmation preview was reviewed" }
    confirm_schedule_understood: { type: boolean, description: "Explicit confirmation schedule is understood" }
    override_checks: { type: boolean, description: "Admin-only bypass for prerequisite checks" }
outputs_schema:
  type: object
  properties:
    job_id: { type: string }
    status: { type: string, enum: [active] }
    next_run: { type: string, description: "ISO timestamp of next scheduled run" }
organization: bolta.ai
author: Bolta Team
---

## Goal
Activate a paused job after preview and voice validation. This is the **explicit trust moment** where the user says "yes, start posting."

## Which Agents Use This
- **custom** (system/onboarding flows) — Used during agent hiring workflow after user reviews preview draft

## Hard Rules
1. MUST require explicit confirmation flags (confirm_preview_reviewed, confirm_schedule_understood)
2. MUST validate voice_profile_id exists (for content jobs)
3. MUST validate account_ids exist and have valid tokens
4. MUST show clear schedule summary before activation
5. MUST NOT activate without preview draft reviewed

## Steps

### 1. Validate prerequisites
- Check confirm_preview_reviewed == true
- Check confirm_schedule_understood == true
- `bolta.get_job(job_id)` → verify job exists and is in `paused` status

### 2. Validate dependencies (for content jobs)
- If job type is content creation:
  - Verify voice_profile_id exists: `bolta.get_voice_profile(voice_profile_id)`
  - Verify all account_ids exist and have valid tokens: `bolta.get_account_info(account_id)`
- If override_checks == true AND user is Admin: skip validation

### 3. Activate job
- `bolta.update_job(job_id, {status: "active"})`
- Calculate next_run based on schedule (cron expression or interval)
- Register job with Celery Beat scheduler

### 4. Return confirmation
- Return job_id, status ("active"), next_run timestamp

## Output
```json
{
  "job_id": "uuid",
  "status": "active",
  "next_run": "2026-02-21T09:00:00Z"
}
```

## Failure Handling
- If confirmation flags missing/false: fail with clear message
- If voice_profile_id invalid: fail with "Voice profile not found" (unless override_checks)
- If account token expired: fail with "Account disconnected, reconnect required" (unless override_checks)
- If job already active: return success (idempotent)

## Example Usage

### Scenario: Activate after preview approval
```json
{
  "job_id": "uuid",
  "confirm_preview_reviewed": true,
  "confirm_schedule_understood": true
}
```
**Result:** Job status → active, first run scheduled
