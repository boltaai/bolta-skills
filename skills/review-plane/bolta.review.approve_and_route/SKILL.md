---
name: bolta.review.approve_and_route
version: 2.0.0
description: V2 - Approve inbox posts and route to Approved→Scheduled based on workspace governance. Handles bulk approvals with flexible scheduling.
category: review
roles_allowed: [Editor, Admin]
agent_types: [reviewer, custom]
tools_required:
  - bolta.get_workspace_policy
  - bolta.get_my_capabilities
  - bolta.get_inbox_item
  - bolta.approve_post
  - bolta.schedule_post
  - bolta.update_post
  - bolta.add_comment
inputs_schema:
  type: object
  required: [workspace_id, post_ids]
  properties:
    workspace_id: { type: string }
    agent_id: { type: string, description: "V2 - Agent executing approval (optional, for audit)" }
    post_ids: { type: array, items: { type: string }, description: "Posts to approve (can be bulk)" }
    schedule_mode: { type: string, enum: [approve_only, use_suggested_time, set_fixed_time, use_agent_memory], default: "approve_only" }
    fixed_time: { type: string, description: "ISO timestamp if schedule_mode is set_fixed_time" }
    schedule_times: { type: array, items: { type: string }, description: "Per-post schedule times (length must match post_ids)" }
outputs_schema:
  type: object
  properties:
    approved_ids: { type: array, items: { type: string } }
    scheduled_ids: { type: array, items: { type: string } }
    failed: { type: array, items: { type: object } }
    final_states: { type: object, description: "post_id → final_state map" }
organization: bolta.ai
author: Max Fritzhand
---

## Goal
Move posts from Inbox → Approved, optionally → Scheduled, based on workspace governance and scheduling preferences.

## V2 Changes
- **State machine:** `Inbox → Approved → Scheduled → Published`
- **Safe Mode enforcement (workspace-level):**
  - Safe Mode ON → approval required before scheduling (this skill's purpose)
  - Safe Mode OFF + Editor/Admin → can schedule directly (bypassed this skill in autopilot)
- **Bulk approvals** — can approve many posts at once
- **Flexible scheduling** — approve-only, use suggested times, fixed time, or agent-learned times
- **Agent memory integration** — can use learned optimal posting times

## When This Skill Is Called
- **Manual trigger** — Human clicks "Approve" or "Approve & Schedule" in Bolta inbox
- **Reviewer agent** — After `bolta.inbox.triage`, agent may call this for auto-approvals (with human confirmation)
- **Bulk operations** — Select 10 posts → "Approve All"

## Policy Rules
1. **Must have Editor or Admin role** (only these roles can approve)
2. **Scheduling requires additional permission:**
   - If Safe Mode ON: scheduling is separate action after approval
   - If Safe Mode OFF: approval can include scheduling in one step
3. **Never publish directly** — this skill routes to `approved` or `scheduled`, NOT `published`
4. **Respect per-post metadata:**
   - If post has `suggested_time` in metadata, use it (unless overridden)
   - If post has `do_not_schedule` flag, skip scheduling even if requested

## Steps

1. **Check policy & capabilities:**
   - `bolta.get_workspace_policy(workspace_id)` → extract `safe_mode`
   - `bolta.get_my_capabilities(workspace_id)` → verify `review:approve` and `posts:schedule`
   - If missing `review:approve`: fail immediately (unauthorized)

2. **Load post metadata:**
   - For each `post_id`:
     - `bolta.get_inbox_item(post_id)` → fetch post content, current state, suggested_time, metadata
     - Verify state is `inbox` (can't approve what's not in inbox)
     - Extract `suggested_time` from metadata if present

3. **Approve posts (state transition: Inbox → Approved):**
   - For each post_id:
     - `bolta.approve_post(post_id)`
       - On success: post transitions to `approved` state
       - Add to `approved_ids`
       - If agent_id provided: add comment `bolta.add_comment(post_id, "Approved by {agent.name}")`
     - On failure (permission denied, invalid state):
       - Add to `failed` array with reason
       - Continue with remaining posts

4. **Route to Scheduled (if requested):**
   
   **If schedule_mode == "approve_only":**
   - Stop here. Posts remain in `approved` state.
   - Human can schedule them later manually.
   - `final_states[post_id] = "approved"`
   
   **If schedule_mode == "use_suggested_time":**
   - For each approved post:
     - If post has `suggested_time` in metadata:
       - Validate time (must be future, > now + 5 minutes)
       - `bolta.schedule_post(post_id, suggested_time)`
       - On success: add to `scheduled_ids`, `final_states[post_id] = "scheduled"`
       - On failure: add to `failed`, post remains `approved`
     - Else (no suggested_time):
       - Add warning: "No suggested_time, post remains approved"
       - `final_states[post_id] = "approved"`
   
   **If schedule_mode == "set_fixed_time":**
   - Requires `fixed_time` parameter
   - For each approved post:
     - `bolta.schedule_post(post_id, fixed_time)`
     - On success: add to `scheduled_ids`
     - On failure: add to `failed`, post remains `approved`
   
   **If schedule_mode == "use_agent_memory":**
   - Requires `agent_id`
   - `bolta.recall(agent_id, "best_posting_times")` → get learned optimal times
   - For each approved post (index i):
     - Pick schedule time from agent memory (e.g., "Monday 9am", "Wednesday 2pm")
     - `bolta.schedule_post(post_id, calculated_time)`
     - On success: add to `scheduled_ids`
     - On failure: add to `failed`, post remains `approved`
   
   **If schedule_times array provided:**
   - Must match length of `post_ids`
   - For each post (index i):
     - `bolta.schedule_post(post_ids[i], schedule_times[i])`
     - On success: add to `scheduled_ids`
     - On failure: add to `failed`, post remains `approved`

5. **Handle scheduling failures gracefully:**
   - If platform API fails (Twitter down, account disconnected):
     - Post remains in `approved` state
     - Add to `failed` with specific error
     - Don't revert approval (human can retry scheduling later)
   - If schedule time invalid (past, too soon):
     - Add to `failed` with validation error
     - Post remains `approved`

6. **Update agent memory (if agent context):**
   - If `agent_id` provided:
     - `bolta.remember(agent_id, "last_approval_batch_size", post_ids.length)`
     - `bolta.remember(agent_id, "approval_success_rate", success_count / total_count)`
     - If scheduling used: `bolta.remember(agent_id, "scheduled_times_used", schedule_times)`

## Output
```json
{
  "approved_ids": ["uuid1", "uuid2", "uuid3"],
  "scheduled_ids": ["uuid1", "uuid2"],
  "failed": [
    {
      "post_id": "uuid3",
      "reason": "Platform API error: Twitter rate limit exceeded",
      "recoverable": true
    }
  ],
  "final_states": {
    "uuid1": "scheduled",
    "uuid2": "scheduled",
    "uuid3": "approved"
  }
}
```

## Failure Handling
- **Partial approval failure:** If some posts fail to approve, continue with others
- **Partial scheduling failure:** If some fail to schedule, others still succeed
- **Never revert approvals:** Once approved, post stays approved even if scheduling fails
- **Bulk operation resilience:** One failure doesn't block the batch

## Agent Types That Use This Skill
- **reviewer** — Primary use case (human-guided approvals or auto-approvals after triage)
- **custom** — User-defined agents with approval permissions

## Example Use Cases

**Scenario 1: Human Manual Approval (No Scheduling)**
```json
{
  "workspace_id": "uuid",
  "post_ids": ["uuid1", "uuid2", "uuid3"],
  "schedule_mode": "approve_only"
}
```
Result: 3 posts → `approved` state, human schedules them later

**Scenario 2: Bulk Approve & Schedule with Suggested Times**
```json
{
  "workspace_id": "uuid",
  "post_ids": ["uuid1", "uuid2", "uuid3"],
  "schedule_mode": "use_suggested_time"
}
```
Result: 3 posts approved → scheduled using each post's suggested_time metadata

**Scenario 3: Reviewer Agent Auto-Approval (After Triage)**
- Reviewer agent runs `bolta.inbox.triage`
- Identifies 8 posts as "ready to approve" (high confidence)
- Calls this skill with those 8 post_ids + `schedule_mode: use_agent_memory`
- Agent uses learned optimal posting times
- 8 posts → approved → scheduled
- Human reviews retrospectively

**Scenario 4: Agency Bulk Scheduling**
- Agency approves 20 client posts
- Wants them all to go out at 10am tomorrow
- `schedule_mode: set_fixed_time`, `fixed_time: "2026-02-21T10:00:00Z"`
- 20 posts → approved → scheduled for same time

**Scenario 5: Partial Failure Recovery**
- Approve 5 posts, schedule 5
- 2 scheduling calls fail (Twitter API down)
- Output: 5 approved, 3 scheduled, 2 failed (but still approved)
- Human can retry scheduling the 2 later when Twitter is back
