---
name: bolta.draft.post
version: 2.0.0
description: Create a single draft post using a workspace voice profile and optional template. Routes to Inbox or schedules based on workspace policy and actor role.
category: content
roles_allowed: [Viewer, Creator, Editor, Admin]
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
inputs_schema:
  type: object
  required: [workspace_id, voice_profile_id, prompt]
  properties:
    workspace_id: { type: string }
    agent_id: { type: string, description: "Agent executing this skill (optional, V2)" }
    voice_profile_id: { type: string }
    prompt: { type: string }
    template_id: { type: string }
    account_ids: { type: array, items: { type: string } }
    requested_action: { type: string, enum: [draft_only, send_to_inbox, schedule, publish] }
    suggested_time: { type: string, description: "ISO timestamp; only used if schedule allowed" }
    job_id: { type: string, description: "Job ID if executed as part of a job (V2)" }
outputs_schema:
  type: object
  properties:
    post_id: { type: string }
    final_state: { type: string, enum: [draft, inbox, approved, scheduled, published] }
    inbox_item_id: { type: string }
    notes_for_reviewer: { type: string }
    warnings: { type: array, items: { type: string } }
organization: bolta.ai
author: Max Fritzhand
---

## Goal
Create one post in the user's Brand Voice, optionally using a template, and route it safely through the V2 state machine.

## Which Agent Types Use This
- **content_creator** — Primary use case (generates posts as part of jobs)
- **custom** — User-defined agents with content creation enabled

## Hard Rules
1. Always call `bolta.get_workspace_policy` + `bolta.get_my_capabilities` first.
2. **Safe Mode enforcement (workspace-level):**
   - If Safe Mode ON: ALL content goes to Inbox for approval, regardless of role
   - If Safe Mode OFF: Creator/Viewer still route to Inbox; Editor/Admin can schedule directly
3. If actor role does not include the required capability for an action (schedule/publish), MUST NOT attempt it.
4. If `requested_action` is omitted: default to `send_to_inbox` (if Safe Mode ON or role is Creator/Viewer), otherwise `draft_only`.
5. Never publish directly without explicit approval.
6. Never schedule unless capability includes `posts:schedule`.

## Steps

### 1. Check policy & capabilities
- `bolta.get_workspace_policy(workspace_id)` → extract `safe_mode` (boolean)
- `bolta.get_my_capabilities(workspace_id)` → check role capabilities

### 2. Load context for consistency
- `bolta.get_voice_profile(voice_profile_id)` → tone, style rules, banned phrases
- `bolta.list_recent_posts(account_ids, limit=5)` → avoid repetition, maintain consistency
- If `agent_id` provided: `bolta.recall(agent_id, "content_preferences")` → retrieve agent memory

### 3. Generate content
- **If template_id provided:**
  - `bolta.list_templates(workspace_id)` (if needed for validation)
  - `bolta.render_template(template_id, {prompt, voice_profile_id, context})`
  - Use rendered text as the post body
- **Else:**
  - Generate body using voice profile constraints
  - Apply tone, structure, vocabulary bias from voice
  - Check recent posts to avoid repetition

### 4. Create the draft
- `bolta.draft_post({workspace_id, voice_profile_id, account_ids, content: body, status: "draft"})`
- Returns `post_id`

### 5. Route based on governance
- **If Safe Mode ON OR role is Creator/Viewer:**
  - Route to Inbox: post transitions to `inbox` state
  - `inbox_item_id` created automatically by system
  - `final_state = inbox`

- **If Safe Mode OFF AND role is Editor/Admin:**
  - `requested_action == draft_only` → leave in `draft`
  - `requested_action == send_to_inbox` → route to `inbox`
  - `requested_action == schedule` → `bolta.schedule_post(post_id, suggested_time)` → `final_state = scheduled`
  - `requested_action == publish` → `bolta.publish_post(post_id)` → `final_state = published`

### 6. Store learnings (if agent context)
- If successful and `agent_id` provided:
  - `bolta.remember(agent_id, "last_successful_hook_style", hook_type_used)`
  - Update agent memory with what worked

## Output
Return:
```json
{
  "post_id": "uuid",
  "final_state": "inbox",
  "inbox_item_id": "uuid",
  "notes_for_reviewer": "AI draft ready for review",
  "warnings": []
}
```

## Failure Handling
- If any tool call returns unauthorized/forbidden: downgrade to `inbox` (if possible) or leave in `draft`.
- Never retry publish/schedule more than once.
- On failure, create inbox item with error context for human review.
- Log to Run record if executed as part of a Job.

## V2 Agent Context

**When agents use this skill:**

**Content Creator reasoning:**
> "I need to draft a post about our new feature. First, let me check the voice profile to match tone. Then I'll review recent posts to avoid repetition. I see we posted about pricing yesterday, so I'll focus on product benefits instead."

**Key differences from V1:**
- V1: Template fill → post
- V2: Agent reasons about context → chooses tools → drafts content → learns from feedback

**Example execution trace:**
```
Turn 1: get_voice_profile() → "Direct, specific, no jargon"
Turn 2: list_recent_posts() → 2 about pricing (avoid)
Turn 3: recall() → "Educational > promotional 3:1"
Turn 4: draft_post() → Created with educational angle
Turn 5: remember() → Store "educational_format_used"
```

## Example Usage

### Scenario 1: Job Execution (Safe Mode ON)
```json
{
  "workspace_id": "uuid",
  "agent_id": "uuid",
  "job_id": "uuid",
  "voice_profile_id": "uuid",
  "account_ids": ["twitter-uuid"],
  "prompt": "Write a post about our new feature launch",
  "requested_action": "send_to_inbox"
}
```
**Result:** Post created → routed to Inbox → awaits approval → then scheduled/published

### Scenario 2: Manual Draft (Safe Mode OFF, Editor role)
```json
{
  "workspace_id": "uuid",
  "voice_profile_id": "uuid",
  "account_ids": ["linkedin-uuid"],
  "prompt": "Share our hiring announcement",
  "requested_action": "schedule",
  "suggested_time": "2026-02-21T09:00:00Z"
}
```
**Result:** Post created → immediately scheduled for 9am tomorrow (bypasses inbox)
