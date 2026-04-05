---
name: bolta.week.plan
version: 2.0.0
description: Generate a 7-day content calendar draft using voice profile + optional templates. V2 - Agent-aware, routes via workspace Safe Mode governance.
category: creator
roles_allowed: [Viewer, Creator, Editor, Admin]
agent_types: [content_creator, custom]
safe_defaults:
  never_publish: true
  never_schedule_unless_explicit: true
tools_required:
  - bolta.get_workspace_policy
  - bolta.get_my_capabilities
  - bolta.get_voice_profile
  - bolta.list_templates
  - bolta.render_template
  - bolta.draft_post
  - bolta.list_recent_posts
  - bolta.remember
  - bolta.recall
inputs_schema:
  type: object
  required: [workspace_id, voice_profile_id]
  properties:
    workspace_id: { type: string }
    agent_id: { type: string, description: "V2 - Agent executing this skill" }
    voice_profile_id: { type: string }
    account_ids: { type: array, items: { type: string } }
    templates: { type: array, items: { type: string }, description: "template_ids; optional" }
    weekly_theme: { type: string }
    requested_action: { type: string, enum: [draft_only, send_to_inbox] }
    job_id: { type: string, description: "V2 - Job ID if executed as part of a job" }
outputs_schema:
  type: object
  properties:
    post_ids: { type: array, items: { type: string } }
    calendar: { type: array, items: { type: object } }
    final_state: { type: string, enum: [draft, inbox] }
    inbox_item_id: { type: string }
organization: bolta.ai
author: Max Fritzhand
---

## Goal
Produce a sensible 7-day plan: variety + cadence + voice consistency.

## V2 Changes
- **Agent-aware execution:** Uses agent memory to recall what content styles performed best
- **State machine updated:** `Draft → Inbox` (V2 terminology, no more "pending_review")
- **Safe Mode is workspace-level only**
- **Agent memory integration:** Stores and recalls top-performing topics, hook styles, posting times

## Policy Rules
1. **Safe Mode enforcement (workspace-level):**
   - If Safe Mode ON: route all posts to Inbox regardless of role
   - If Safe Mode OFF: Creator/Viewer still route to Inbox; Editor/Admin can leave as drafts
2. If templates not provided: pick from workspace templates by matching weekly_theme
3. Ensure variety across 7 days (don't repeat same hook style 3 days in a row)

## Steps

1. **Check policy & capabilities:**
   - `bolta.get_workspace_policy(workspace_id)` → extract `safe_mode`
   - `bolta.get_my_capabilities(workspace_id)` → check role capabilities
   - `bolta.get_voice_profile(voice_profile_id)` → tone, style rules

2. **Load agent memory (if agent context):**
   - If `agent_id` provided:
     - `bolta.recall(agent_id, "top_performing_topics")` → prioritize proven topics
     - `bolta.recall(agent_id, "best_posting_times")` → suggest optimal times
     - `bolta.recall(agent_id, "preferred_hook_style")` → use successful hooks

3. **Load recent context:**
   - `bolta.list_recent_posts(account_ids, limit=14)` → avoid repetition from last 2 weeks

4. **Build 7-day plan:**
   - Create 7 slots (Day 1..7). Each slot includes:
     - **Goal:** teach | story | proof | CTA | engagement | thought-leadership
     - **Hook style:** question | contrarian | list | mini-story | stat | quote
     - **Topic:** short description
     - **Optimal time:** based on agent memory or default (9am, varies by day)
   
   - **Variety rules:**
     - Don't repeat same goal type 2 days in a row
     - Don't repeat same hook style 3 days in a row
     - Balance educational vs promotional (70/30 split)

5. **Generate posts for each slot:**
   - If `templates` provided and match slot goal: 
     - `bolta.render_template(template_id, {topic, hook_style, voice_profile_id})`
   - Else if workspace templates available:
     - `bolta.list_templates(workspace_id)` → pick template matching slot goal
   - Else:
     - Generate from scratch using voice profile + slot plan
   
   - For each post:
     - `bolta.draft_post({workspace_id, voice_profile_id, account_ids, content, status: "draft"})`
     - Collect `post_id`

6. **Route based on governance:**
   - If Safe Mode ON OR role is Creator/Viewer OR `requested_action == send_to_inbox`:
     - All posts transition to `inbox` state as a batch
     - System creates single `inbox_item_id` for the bundle (7 posts grouped)
     - `final_state = inbox`
   - Else:
     - Leave posts in `draft` state
     - `final_state = draft`

7. **Store learnings (if agent context):**
   - If successful and `agent_id` provided:
     - `bolta.remember(agent_id, "last_weekly_plan_theme", weekly_theme)`
     - `bolta.remember(agent_id, "content_variety_ratio", goal_distribution)`

## Output
Return:
- `post_ids` (array of UUIDs, one per day)
- `calendar` (array of objects with: day, goal, topic, hook_style, post_id, suggested_time)
- `final_state` (draft | inbox)
- `inbox_item_id` (if routed to inbox as bundle)

## Example Calendar Output
```json
{
  "post_ids": ["uuid1", "uuid2", ...],
  "calendar": [
    {
      "day": 1,
      "goal": "teach",
      "topic": "How to write viral hooks",
      "hook_style": "question",
      "post_id": "uuid1",
      "suggested_time": "2026-02-21T09:00:00Z"
    },
    {
      "day": 2,
      "goal": "story",
      "topic": "How we 10x'd engagement in 30 days",
      "hook_style": "mini-story",
      "post_id": "uuid2",
      "suggested_time": "2026-02-22T10:00:00Z"
    },
    ...
  ],
  "final_state": "inbox",
  "inbox_item_id": "bundle-uuid"
}
```

## Failure Handling
- If template rendering fails: fall back to voice-based generation
- If any post creation fails: continue with others, note failures in warnings
- If routing fails: leave all posts in draft state with error context

## Agent Types That Use This Skill
- **content_creator** — Primary use case (weekly planning as part of content strategy)
- **custom** — User-defined agents with content planning enabled
