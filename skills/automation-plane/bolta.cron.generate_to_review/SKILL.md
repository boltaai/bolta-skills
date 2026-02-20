---
name: bolta.cron.generate_to_review
version: 2.0.0
description: V2 Job execution skill - Agent generates N posts per run, routes to Inbox for review. Called by Celery job runner. Replaces RecurringTemplate logic.
category: automation
roles_allowed: [Creator, Editor, Admin]
agent_types: [content_creator, custom]
safe_defaults:
  always_route_to_inbox: true
tools_required:
  - bolta.get_workspace_policy
  - bolta.get_my_capabilities
  - bolta.get_voice_profile
  - bolta.list_templates
  - bolta.render_template
  - bolta.draft_post
  - bolta.list_recent_posts
  - bolta.get_account_info
  - bolta.remember
  - bolta.recall
inputs_schema:
  type: object
  required: [workspace_id, agent_id, job_id, voice_profile_id, account_ids]
  properties:
    workspace_id: { type: string }
    agent_id: { type: string, description: "V2 - Agent executing this job" }
    job_id: { type: string, description: "V2 - Job ID for this run" }
    run_id: { type: string, description: "V2 - Run ID for audit logging" }
    voice_profile_id: { type: string }
    account_ids: { type: array, items: { type: string } }
    template_id: { type: string, description: "Optional template to use" }
    n_posts: { type: number, default: 3, description: "Number of posts to generate per run" }
    topic_seeds: { type: array, items: { type: string }, description: "Optional topic hints" }
    run_instructions: { type: string, description: "Job-specific override instructions" }
    client_tag: { type: string, description: "V2 - Agency client tag for organization" }
outputs_schema:
  type: object
  properties:
    run_id: { type: string }
    post_ids: { type: array, items: { type: string } }
    inbox_item_id: { type: string }
    final_state: { type: string, enum: [inbox] }
    warnings: { type: array, items: { type: string } }
    tokens_used: { type: object, properties: { prompt: { type: number }, completion: { type: number } } }
organization: bolta.ai
author: Max Fritzhand
---

## Goal
Execute a scheduled job run: generate N posts using Brand Voice, route to Inbox for human review.

## V2 Changes
- **This is THE core job execution skill** — called by Celery job runner for scheduled jobs
- **Replaces RecurringTemplate logic** — jobs are now Agent-owned with this skill as the execution engine
- **Agent memory integration** — recalls top topics, hook styles, posting times
- **Per-account advisory locks** — caller (Celery) handles locking to prevent duplicate posts
- **Run logging** — tokens tracked, cost computed, stored in Run record
- **Always routes to Inbox** — this skill never schedules directly (use `bolta.cron.generate_and_schedule` for that)

## When This Skill Is Called
- **Trigger:** Celery Beat detects `Job.next_run_at <= now` and `Job.status == active`
- **Caller:** `execute_job_run(job_id, run_id, account_id)` Celery task
- **Context:** Agent's full persona + memory + voice profile injected into system prompt
- **Tool access:** Filtered by agent type (content_creator gets content tools only)

## Policy Rules
1. **Always route to Inbox** — this is the "safe automation" skill
2. **Respect voice soft-delete** — if voice_profile_id is soft-deleted, fail gracefully and pause job
3. **Idempotency** — if run_id already exists with status=completed, skip execution
4. **Max retries** — if this run fails, Celery retries up to Job.max_retries (default 2)
5. **Escalation on failure** — after max retries, create inbox item with error context for human

## Steps

1. **Pre-flight checks:**
   - `bolta.get_workspace_policy(workspace_id)` → extract `safe_mode` (informational; this skill always routes to inbox)
   - `bolta.get_my_capabilities(workspace_id)` → verify agent has content creation capability
   - `bolta.get_voice_profile(voice_profile_id)` → verify voice exists and is active
     - If soft-deleted: fail with error "Voice profile deleted, job paused" → pause job
   - Verify all `account_ids` exist and are connected:
     - `bolta.get_account_info(account_id)` for each account
     - If any account disconnected: fail with error "Account disconnected" → pause job

2. **Load agent memory for context:**
   - `bolta.recall(agent_id, "top_performing_topics")` → prioritize proven topics
   - `bolta.recall(agent_id, "preferred_hook_style")` → use successful hooks
   - `bolta.recall(agent_id, "audience_timezone")` → context for timing references
   - `bolta.recall(agent_id, "recent_failures")` → avoid repeating mistakes

3. **Load recent posts for consistency:**
   - `bolta.list_recent_posts(account_ids, limit=10)` → avoid repetition
   - Extract: topics covered, hook styles used, engagement levels (if available)

4. **Generate N posts:**
   - For each of `n_posts` (default 3):
     
     **If `template_id` provided:**
     - `bolta.render_template(template_id, {topic_seed, voice_profile_id, agent_memory})`
     - Use rendered content
     
     **Else if `topic_seeds` provided:**
     - Pick next seed from array
     - Generate post using voice profile + seed + agent memory
     
     **Else (no template, no seeds):**
     - Generate topic based on:
       - Agent memory (top performing topics)
       - Voice profile (brand focus areas)
       - Recent posts (avoid repetition, maintain variety)
       - `run_instructions` (job-specific guidance)
     
     **Apply `run_instructions` if provided:**
     - Job-level override instructions (e.g., "Focus on product features. 3 posts per run. Instagram carousel format.")
     - This overrides default agent behavior for this specific job
     
     **Create draft:**
     - `bolta.draft_post({workspace_id, voice_profile_id, account_ids: [account_id], content, status: "draft"})`
     - Tag with `run_id`, `job_id`, `client_tag` in metadata
     - Collect `post_id`

5. **Route to Inbox:**
   - All generated posts transition to `inbox` state as a batch
   - System creates single `inbox_item_id` for the bundle
   - Inbox item tagged with:
     - `agent_id` (who created it)
     - `job_id` (which job)
     - `run_id` (this execution)
     - `client_tag` (for agency filtering)
   - `final_state = inbox`

6. **Update agent memory:**
   - `bolta.remember(agent_id, "last_successful_run", ISO_timestamp)`
   - `bolta.remember(agent_id, "last_run_topics", topics_used)`
   - If any posts generated unusually well (future enhancement): store successful patterns

7. **Return execution summary:**
   - `run_id` (for audit trail)
   - `post_ids` (array of created drafts)
   - `inbox_item_id` (bundle ID for review queue)
   - `final_state` (always "inbox")
   - `warnings` (any non-fatal issues: missing topics, template fallback, etc.)
   - `tokens_used` ({ prompt, completion }) — for cost tracking

## Output
```json
{
  "run_id": "uuid",
  "post_ids": ["uuid1", "uuid2", "uuid3"],
  "inbox_item_id": "bundle-uuid",
  "final_state": "inbox",
  "warnings": [],
  "tokens_used": {
    "prompt": 1234,
    "completion": 567
  }
}
```

## Failure Handling

**Voice profile deleted:**
- Fail immediately with clear error message
- Pause job (set `Job.status = paused`, `Job.error_message = "Voice profile deleted"`)
- Create inbox item with warning for human: "Job X paused - voice profile missing"

**Account disconnected:**
- Fail immediately with clear error message
- Pause job temporarily
- Create inbox item with reconnection instructions

**Template rendering fails:**
- Fall back to voice-based generation without template
- Add warning to output
- Continue execution

**Individual post creation fails:**
- Continue with remaining posts (don't fail entire run)
- Add warning to output
- If 0 posts succeed, mark run as failed

**Max retries exceeded:**
- After `Job.max_retries` failures, create inbox item with:
  - Full error context
  - Last N run error messages
  - Suggested fixes (reconnect account, restore voice, etc.)
  - Job remains paused until human intervention

## Idempotency
- Check at start: if `run_id` exists with `status=completed`, return cached output
- If `run_id` exists with `status=failed`, allow retry (Celery handles this)

## Advisory Lock Context
- **Caller (Celery) acquires Postgres advisory lock** per account before invoking this skill
- Lock ID: `hash(account_id)`
- Lock mode: non-blocking (`pg_try_advisory_lock`)
- If lock not acquired: Celery requeues job for +30s later
- This skill assumes lock is held — focuses on content generation, not concurrency

## Agent Types That Use This Skill
- **content_creator** — Primary use case (scheduled content generation)
- **custom** — User-defined agents with automation enabled

## Example Job Configuration
```json
{
  "id": "job-uuid",
  "agent_id": "hype-man-uuid",
  "name": "Daily Twitter Posts",
  "voice_profile_id": "bolta-voice-uuid",
  "account_ids": ["twitter-uuid"],
  "schedule": {"cron": "0 9 * * 1-5"},
  "trigger": "scheduled",
  "status": "active",
  "n_posts": 3,
  "client_tag": "Acme Corp",
  "run_instructions": "Focus on product launches and founder stories. Keep it punchy and conversational."
}
```

When Celery fires this job at 9am on weekdays:
1. Creates Run record (status=running)
2. Acquires lock on twitter-uuid account
3. Calls this skill with job config + agent context
4. Skill generates 3 posts → routes to inbox
5. Run record updated (status=completed, tokens logged)
6. Lock released
