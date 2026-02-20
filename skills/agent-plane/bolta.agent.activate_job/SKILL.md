# bolta.agent.activate_job

**Version:** 2.0.0  
**Category:** Agent Lifecycle  
**Agent Types:** `custom` (system)  
**Roles Allowed:** `admin`, `editor`

---

## Purpose

Activate a paused job after preview and voice validation. This is the **explicit trust moment** where the user says "yes, start posting."

---

## When Used

After hiring an agent:
1. Agent is created with jobs in `paused` status
2. User reviews preview draft
3. User adjusts voice profile if needed
4. User activates jobs (this skill)
5. Jobs start executing on schedule

---

## What This Does

1. Validates prerequisites (voice profile exists, accounts connected)
2. Updates Job status: `paused` → `active`
3. Calculates `next_run` based on schedule
4. Registers job with Celery Beat scheduler

---

## Parameters

```json
{
  "job_id": "uuid",
  "confirm_preview_reviewed": true,  // Explicit confirmation
  "confirm_schedule_understood": true,
  "override_checks": false  // Admin-only bypass
}
```

---

## Hard Rules

- **MUST** require explicit confirmation flags
- **MUST** validate voice_profile_id exists (for content jobs)
- **MUST** validate account_ids exist and have valid tokens
- **MUST** show clear schedule summary before activation
- **MUST NOT** activate without preview draft reviewed

---

## Integration

**After activation:**
- Job appears in active jobs list
- Celery Beat picks it up on next poll
- First run creates draft in Inbox
- User can pause/modify job anytime
