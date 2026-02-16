---
name: bolta.loop.from_template
version: 1.0.0
description: Create a recurring content loop from a template using a voice profile, then send all generated posts into Inbox Review as a bundle.
category: creator
roles_allowed: [Owner, Admin, Creator]
safe_defaults:
  always_route_to_review: true
tools_required:
  - bolta.get_workspace_policy
  - bolta.get_my_capabilities
  - bolta.get_voice_profile
  - bolta.render_template
  - bolta.create_loop
  - bolta.create_post
  - bolta.submit_for_review
inputs_schema:
  type: object
  required: [workspace_id, voice_profile_id, template_id]
  properties:
    workspace_id: { type: string }
    voice_profile_id: { type: string }
    template_id: { type: string }
    horizon_days: { type: number, default: 14 }
    cadence: { type: string, description: "e.g., daily|3x_week|weekdays" }
    account_ids: { type: array, items: { type: string } }
    topic_seeds: { type: array, items: { type: string } }
outputs_schema:
  type: object
  properties:
    loop_id: { type: string }
    post_ids: { type: array, items: { type: string } }
    review_bundle_id: { type: string }
    final_state: { type: string, enum: [pending_review] }
    warnings: { type: array, items: { type: string } }
---

## Goal
Turn a template into a real loop with multiple posts, all routed to review.

## Hard rules
- Always query workspace policy + capabilities.
- Always route to Inbox Review (pending review). Do not schedule or publish from this skill.

## Steps
1. Fetch policy + capabilities.
2. Create the loop shell:
   - `bolta.create_loop({workspace_id, voice_profile_id, template_id, horizon_days, cadence, account_ids})`
3. For each slot in the loop horizon:
   - Choose a topic seed (rotate through provided topic_seeds; if none, derive 5–10 from template theme).
   - Render template:
     - `bolta.render_template(template_id, {voice_profile_id, topic_seed, slot_index})`
   - Create draft post:
     - `bolta.create_post({workspace_id, voice_profile_id, account_ids, body, status: "draft", metadata: {loop_id, slot_index}})`
4. Submit as a single review bundle:
   - `bolta.submit_for_review({workspace_id, post_ids, note: "Loop generated from template"})`

## Output
Return loop_id, post_ids, review_bundle_id, final_state=pending_review.

## Failure handling
- If some posts fail creation, still submit the ones that succeeded.
- Add warnings listing failed slots.
