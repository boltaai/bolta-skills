---
name: bolta.cron.generate_to_review
version: 1.0.0
description: Cron-friendly generator: create N posts using voice + template, then submit to review as a bundle every run.
category: automation
roles_allowed: [Owner, Admin, Creator]
safe_defaults:
  always_route_to_review: true
tools_required:
  - bolta.get_workspace_policy
  - bolta.get_my_capabilities
  - bolta.render_template
  - bolta.create_post
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
    topic_seeds: { type: array, items: { type: string } }
outputs_schema:
  type: object
  properties:
    job_run_id: { type: string }
    post_ids: { type: array, items: { type: string } }
    review_bundle_id: { type: string }
    warnings: { type: array, items: { type: string } }
---

## Rules
- Always route to review; never schedule/publish.
- If Safe Mode is OFF, still route to review (cron is higher risk).

## Steps
1. Fetch policy + capabilities.
2. Generate n_posts:
   - Render template per topic seed.
   - Create drafts with metadata job_run_id.
3. Submit as bundle for review.

## Output
job_run_id + post_ids + review_bundle_id.
