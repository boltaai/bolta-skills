---
name: bolta.week.plan
version: 1.0.0
description: Generate a 7-day content calendar draft using voice profile + optional templates, then route posts to Draft or Pending Review depending on Safe Mode.
category: creator
roles_allowed: [Owner, Admin, Creator]
safe_defaults:
  never_publish: true
  never_schedule_unless_explicit: true
tools_required:
  - bolta.get_workspace_policy
  - bolta.get_my_capabilities
  - bolta.get_voice_profile
  - bolta.list_templates
  - bolta.render_template
  - bolta.create_post
  - bolta.submit_for_review
inputs_schema:
  type: object
  required: [workspace_id, voice_profile_id]
  properties:
    workspace_id: { type: string }
    voice_profile_id: { type: string }
    account_ids: { type: array, items: { type: string } }
    templates: { type: array, items: { type: string }, description: "template_ids; optional" }
    weekly_theme: { type: string }
    requested_action: { type: string, enum: [draft_only, send_to_review] }
outputs_schema:
  type: object
  properties:
    post_ids: { type: array, items: { type: string } }
    calendar: { type: array, items: { type: object } }
    final_state: { type: string, enum: [draft, pending_review] }
---

## Goal
Produce a sensible 7-day plan: variety + cadence + voice consistency.

## Rules
- If Safe Mode ON: route to pending_review regardless of requested_action.
- If templates not provided: pick from workspace templates (list) by matching weekly_theme.

## Steps
1. Fetch policy + capabilities + voice.
2. Build 7 slots (Day 1..7). Each slot includes:
   - goal (teach / story / proof / CTA / engagement)
   - hook style (question / contrarian / list / mini-story)
   - short topic
3. For each slot:
   - If template available for slot goal: render it.
   - Else: write in voice based on slot plan.
   - Create post in draft.
4. Routing:
   - If Safe Mode ON or requested_action == send_to_review: submit all post_ids as a bundle.
   - Else leave as drafts.

## Output
Return post_ids + a simple calendar array (day, goal, topic, post_id).
