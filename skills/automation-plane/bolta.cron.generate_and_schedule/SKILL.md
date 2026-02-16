---
name: bolta.cron.generate_and_schedule
version: 1.0.0
description: Cron generator that can schedule posts ONLY if Safe Mode is OFF AND the principal has scheduling permission; otherwise routes to review.
category: automation
roles_allowed: [Owner, Admin]
tools_required:
  - bolta.get_workspace_policy
  - bolta.get_my_capabilities
  - bolta.render_template
  - bolta.create_post
  - bolta.schedule_post
  - bolta.submit_for_review
inputs_schema:
  type: object
  required: [workspace_id, voice_profile_id, template_id]
  properties:
    workspace_id: { type: string }
    voice_profile_id: { type: string }
    template_id: { type: string }
    n_posts: { type: number, default: 3 }
    account_ids: { type: array, items: { type: string } }
    schedule_times: { type: array, items: { type: string }, description: "ISO timestamps; length >= n_posts preferred" }
outputs_schema:
  type: object
  properties:
    job_run_id: { type: string }
    scheduled_ids: { type: array, items: { type: string } }
    review_routed_ids: { type: array, items: { type: string } }
    warnings: { type: array, items: { type: string } }
---

## Hard rules
- If Safe Mode ON: do not schedule. Route to review.
- If missing `posts:schedule`: do not schedule. Route to review.

## Steps
1. Fetch policy + capabilities.
2. Create drafts.
3. If allowed to schedule:
   - For each post, schedule using schedule_times[i] if provided; else add warning and route to review.
4. If not allowed:
   - Bundle and submit to review.

## Output
scheduled_ids, review_routed_ids, warnings.
