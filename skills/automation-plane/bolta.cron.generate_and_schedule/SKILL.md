---
name: bolta.cron.generate_and_schedule
version: 2.0.0
description: V2 Job execution skill with direct scheduling - Agent generates N posts and schedules them ONLY if Safe Mode OFF AND agent is Editor/Admin. Otherwise routes to Inbox.
category: automation
roles_allowed: [Editor, Admin]
agent_types: [content_creator, custom]
safe_defaults:
  respect_safe_mode: true
  downgrade_to_review_on_deny: true
tools_required:
  - bolta.get_workspace_policy
  - bolta.get_my_capabilities
  - bolta.get_voice_profile
  - bolta.list_templates
  - bolta.render_template
  - bolta.draft_post
  - bolta.schedule_post
  - bolta.list_recent_posts
  - bolta.get_account_info
  - bolta.remember
  - bolta.recall
inputs_schema:
  type: object
  required: [workspace_id, agent_id, job_id, voice_profile_id, account_ids]
  properties:
    workspace_id: { type: string }
    agent_id: { type: string, description: "V2 - Agent executing this job (must have Editor/Admin role)" }
    job_id: { type: string, description: "V2 - Job ID for this run" }
    run_id: { type: string, description: "V2 - Run ID for audit logging" }
    voice_profile_id: { type: string }
    account_ids: { type: array, items: { type: string } }
    template_id: { type: string, description: "Optional template to use" }
    n_posts: { type: number, default: 3 }
    schedule_times: { type: array, items: { type: string }, description: "ISO timestamps; length >= n_posts preferred" }
    topic_seeds: { type: array, items: { type: string } }
    run_instructions: { type: string, description: "Job-specific override instructions" }
    client_tag: { type: string, description: "V2 - Agency client tag" }
outputs_schema:
  type: object
  properties:
    run_id: { type: string }
    scheduled_post_ids: { type: array, items: { type: string } }
    inbox_post_ids: { type: array, items: { type: string } }
    inbox_item_id: { type: string, description: "If any posts routed to inbox" }
    final_state: { type: string, enum: [scheduled, inbox, mixed] }
    warnings: { type: array, items: { type: string } }
    tokens_used: { type: object }
organization: bolta.ai
author: Max Fritzhand
---

## Goal
Execute a scheduled job run: generate N posts and schedule them directly (autopilot mode) — BUT only if governance allows. Falls back to Inbox if not permitted.

## V2 Changes
- **Direct scheduling capability** — for trusted agents when Safe Mode OFF
- **Workspace-level Safe Mode enforcement** — if ON, downgrades to inbox routing
- **Role-gated** — only Editor/Admin agents can use this skill
- **Graceful degradation** — if scheduling denied, routes to inbox instead of failing
- **Same agent memory integration** as `bolta.cron.generate_to_review`

## When to Use This Skill vs `bolta.cron.generate_to_review`

| Skill | Use When | Routing |
|---|---|---|
| `bolta.cron.generate_to_review` | Safe automation (always human review) | Always → Inbox |
| `bolta.cron.generate_and_schedule` | Autopilot (trusted agents, proven performance) | → Scheduled (if allowed) OR → Inbox (if not) |

## Governance Decision Tree

```
Can this agent schedule directly?
├─ Is Safe Mode ON?
│  └─ YES → route to Inbox (Safe Mode overrides everything)
│  └─ NO → check role
│     ├─ Is agent role Editor or Admin?
│     │  └─ YES → schedule directly ✅
│     │  └─ NO → route to Inbox (Creator/Viewer always need approval)
```

## Policy Rules
1. **Safe Mode ON → always route to Inbox** (regardless of agent role)
2. **Safe Mode OFF + Editor/Admin role → schedule directly**
3. **Safe Mode OFF + Creator/Viewer role → route to Inbox**
4. **Scheduling requires valid schedule_times** — if missing or malformed, route to Inbox
5. **Voice soft-delete → pause job immediately**
6. **Account disconnected → pause job immediately**

## Steps

1. **Pre-flight checks (same as generate_to_review):**
   - `bolta.get_workspace_policy(workspace_id)` → extract `safe_mode`
   - `bolta.get_my_capabilities(workspace_id)` → verify scheduling capability
   - `bolta.get_voice_profile(voice_profile_id)` → verify active
   - `bolta.get_account_info(account_id)` → verify connected
   - If voice deleted or account disconnected: fail and pause job

2. **Determine execution mode:**
   ```
   if safe_mode == true:
     execution_mode = "inbox"
     reason = "Safe Mode ON"
   else if agent.role in ["editor", "admin"]:
     execution_mode = "schedule"
   else:
     execution_mode = "inbox"
     reason = "Agent role requires approval"
   ```

3. **Load agent memory for context (same as generate_to_review):**
   - `bolta.recall(agent_id, "top_performing_topics")`
   - `bolta.recall(agent_id, "preferred_hook_style")`
   - `bolta.recall(agent_id, "best_posting_times")` → use if schedule_times not provided

4. **Load recent posts:**
   - `bolta.list_recent_posts(account_ids, limit=10)` → avoid repetition

5. **Generate N posts (same logic as generate_to_review):**
   - For each of `n_posts`:
     - Render template OR generate from voice + memory
     - Apply `run_instructions` if provided
     - `bolta.draft_post(...)` → collect `post_id`

6. **Route based on execution mode:**

   **If execution_mode == "schedule":**
   - For each post (index i):
     - Get schedule time:
       - If `schedule_times[i]` provided → use it
       - Else if agent memory has `best_posting_times` → use learned time
       - Else → add warning, fall back to inbox for this post
     
     - Validate schedule time:
       - Must be future timestamp (> now + 5 minutes)
       - If invalid → add warning, route this post to inbox
     
     - `bolta.schedule_post(post_id, schedule_time)`
       - On success → add to `scheduled_post_ids`
       - On failure (API error, platform issue) → add to `inbox_post_ids` + warning
   
   - If ALL posts scheduled successfully:
     - `final_state = "scheduled"`
   - If SOME scheduled, SOME to inbox:
     - `final_state = "mixed"`
     - Create inbox_item for the failed ones
   - If NONE scheduled (all failed):
     - `final_state = "inbox"`
     - Create single inbox_item for all posts

   **If execution_mode == "inbox":**
   - All posts transition to `inbox` state
   - Create `inbox_item_id` for the bundle
   - `final_state = "inbox"`
   - Add `reason` to warnings (why downgraded: Safe Mode ON, role insufficient, etc.)

7. **Update agent memory:**
   - `bolta.remember(agent_id, "last_scheduled_run", ISO_timestamp)`
   - If execution_mode == "schedule":
     - `bolta.remember(agent_id, "scheduled_times_used", schedule_times)` → learn optimal times
   - If any posts failed to schedule:
     - `bolta.remember(agent_id, "recent_failures", failure_reasons)` → avoid repeating

8. **Return execution summary:**
   - `run_id`
   - `scheduled_post_ids` (posts that were scheduled)
   - `inbox_post_ids` (posts that were routed to inbox)
   - `inbox_item_id` (if any posts went to inbox)
   - `final_state` (scheduled | inbox | mixed)
   - `warnings` (downgrade reasons, scheduling failures, etc.)
   - `tokens_used`

## Output Examples

### Success (all scheduled)
```json
{
  "run_id": "uuid",
  "scheduled_post_ids": ["uuid1", "uuid2", "uuid3"],
  "inbox_post_ids": [],
  "inbox_item_id": null,
  "final_state": "scheduled",
  "warnings": [],
  "tokens_used": { "prompt": 1234, "completion": 567 }
}
```

### Downgraded (Safe Mode ON)
```json
{
  "run_id": "uuid",
  "scheduled_post_ids": [],
  "inbox_post_ids": ["uuid1", "uuid2", "uuid3"],
  "inbox_item_id": "bundle-uuid",
  "final_state": "inbox",
  "warnings": [
    "Downgraded to inbox: Safe Mode ON (workspace-level governance)"
  ],
  "tokens_used": { "prompt": 1234, "completion": 567 }
}
```

### Mixed (partial failure)
```json
{
  "run_id": "uuid",
  "scheduled_post_ids": ["uuid1", "uuid2"],
  "inbox_post_ids": ["uuid3"],
  "inbox_item_id": "bundle-uuid",
  "final_state": "mixed",
  "warnings": [
    "Post 3: schedule_time missing, routed to inbox"
  ],
  "tokens_used": { "prompt": 1234, "completion": 567 }
}
```

## Failure Handling

**Same as `bolta.cron.generate_to_review`:**
- Voice deleted → pause job
- Account disconnected → pause job
- Template rendering fails → fall back to voice generation
- Max retries exceeded → create inbox item with error context

**Additional (scheduling-specific):**
- Invalid schedule_time → route that post to inbox, continue with others
- Platform API scheduling fails → route to inbox, add warning
- Missing schedule_times → route to inbox with suggestion to add times or use memory

## When to Use This Skill (User Guidance)

**Use `bolta.cron.generate_to_review` when:**
- First setting up automation (test before trusting)
- High-sensitivity brands (every post needs eyes)
- New voice profiles (not proven yet)
- Experimental content strategies

**Use `bolta.cron.generate_and_schedule` when:**
- Agent proven reliable (reviewed 50+ posts, 95%+ approval rate)
- Safe Mode OFF (workspace decision)
- Editor/Admin role agents (trusted with scheduling)
- High-volume automation (24/7 content flow)
- Agency autopilot mode (30+ clients, can't manually review everything)

**Migration path:**
1. Start with `generate_to_review` (Safe Mode ON)
2. Review agent output for 1-2 weeks
3. If quality high: turn Safe Mode OFF, switch job to `generate_and_schedule`
4. Monitor audit logs; revert if quality drops

## Agent Types That Use This Skill
- **content_creator** — Primary use case (autopilot content generation)
- **custom** — User-defined agents with full automation enabled

## Example Job Configuration
```json
{
  "id": "job-uuid",
  "agent_id": "trusted-creator-uuid",
  "name": "Daily LinkedIn Autopilot",
  "voice_profile_id": "bolta-voice-uuid",
  "account_ids": ["linkedin-uuid"],
  "schedule": {"cron": "0 10 * * 1-5"},
  "trigger": "scheduled",
  "status": "active",
  "n_posts": 1,
  "schedule_times": ["10:00"],
  "client_tag": "Acme Corp",
  "run_instructions": "Professional thought-leadership posts. Balance education vs promotion 70/30."
}
```

When Celery fires this job at 10am on weekdays:
1. Checks Safe Mode (OFF) + agent role (Editor) → execution_mode = "schedule"
2. Generates 1 post using voice + memory
3. Schedules for 10:00am same day
4. Post goes live at 10:00am without human intervention
5. Human reviews retrospectively via audit logs
