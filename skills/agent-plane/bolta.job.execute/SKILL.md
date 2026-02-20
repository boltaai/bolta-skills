---
name: bolta.job.execute
version: 2.0.0
description: Documentation of V2 execution engine - how jobs fire and agents reason through tasks (NOT a callable tool)
category: agent
type: documentation
roles_allowed: []
agent_types: []
tools_required: []
inputs_schema:
  type: object
  description: "This is system documentation, not a callable skill"
  properties: {}
outputs_schema:
  type: object
  description: "This is system documentation, not a callable skill"
  properties: {}
organization: bolta.ai
author: Bolta Team
---

## Goal
Document how the V2 execution engine works — the core system that powers agentic job execution. This is **not a skill agents call**, but documentation for developers and users.

## What Is Job Execution?

A **Job** connects:
- An **Agent** (who does the work)
- A **Voice Profile** (how they sound)
- **Account(s)** (where they post)
- A **Schedule** (when they run)
- **Run Instructions** (what they should do)

When a job fires:
1. Loads agent's context (persona, memory, voice profile)
2. Builds system prompt with all relevant context
3. Sends task brief to Claude Messages API
4. Agent reasons and chooses tools
5. Execution loop runs until agent completes or hits max turns
6. Output is stored (draft posts, analytics reports, etc.)

## Job Model Structure

```python
class Job:
    agent = ForeignKey(Agent)           # Which agent executes this
    name = CharField()                  # Human-readable job name
    voice_profile_id = UUIDField()      # Voice to use
    account_ids = JSONField()           # Social accounts to target
    schedule = JSONField()              # Cron expression
    trigger = CharField()               # "scheduled" | "manual" | "event"
    status = CharField()                # "active" | "paused" | "failed"
    run_instructions = TextField()      # Natural language task brief
```

**Key insight:** `run_instructions` is a BRIEF, not a script. The agent reads it and decides its own path.

## Execution Engine Flow

### 1. Scheduled Job (Most Common)

```
Celery Beat (every 60s)
  → Query: Jobs WHERE status='active' AND next_run <= now()
  → For each due job: Create Run object, spawn Celery task

Worker picks up task:
  → Acquire Postgres advisory lock (prevent concurrent posts to same account)
  → Load agent, job, voice profile, account
  → Build initial message with task brief
  → Call execute_claude(agent, messages, mode="job")

Agent reasoning loop:
  → Read task brief
  → Recall memory
  → Call tools (get_voice_profile, list_recent_posts, draft_post, etc.)
  → Return output

Run completes:
  → Update Run (status, tokens, cost, trace)
  → Release lock
  → Update Job (last_run, next_run)
  → Draft appears in Inbox
```

### 2. System Prompt Builder

System prompt structure:
```
[Base Template for Agent Type]
  → Type-specific behavioral guidelines

[Persona]
  → User-editable personality

[Memory]
  → What agent has learned over time

[Runtime Context]
  → Current task brief
  → Available tools
```

**This context makes the agent intelligent.**

### 3. Tool Filtering (Defense in Depth)

1. **By agent type:**
   - Content Creator → draft_post, get_voice_profile, list_recent_posts
   - Reviewer → approve_post, reject_post, add_comment
   - Analytics → get_post_metrics, get_audience_insights

2. **By agent role:**
   - Creator role → can draft, can't approve
   - Editor role → can draft, can approve
   - Admin role → full access

3. **Runtime validation:**
   - Tool execution checks role again
   - Logs all tool calls
   - Returns clear success/error responses

## What Agents Decide vs. What System Enforces

### Agents Decide:
- Which tools to call and in what order
- How to interpret the task brief
- What content to create
- Whether to iterate or finish
- What to remember for next time

### System Enforces:
- Tool access (type + role filtering)
- Max iterations (prevent infinite loops)
- Safe Mode (approval gates)
- Role permissions
- Workspace quotas

**The balance:** Agent has creative freedom within safety constraints.

## Run Trace Structure

```json
{
  "run_id": "uuid",
  "status": "completed",
  "total_tokens": 4523,
  "cost_usd": 0.087,
  "trace": [
    {
      "turn": 1,
      "thinking": "I need to check recent posts first...",
      "tool_calls": [
        {"tool": "bolta.list_recent_posts", "input": {...}, "output": {...}},
        {"tool": "bolta.get_voice_profile", "input": {...}, "output": {...}}
      ]
    },
    {
      "turn": 2,
      "thinking": "Now I'll draft the post...",
      "tool_calls": [
        {"tool": "bolta.draft_post", "input": {...}, "output": {...}}
      ]
    }
  ]
}
```

This shows how the agent reasoned, which tools it chose, and in what order — essential for debugging.

## V1 vs V2 Comparison

| Aspect | V1 (RecurringTemplates) | V2 (Job Execution) |
|--------|-------------------------|---------------------|
| Execution | Template fill → post | Agent reasoning → tools → output |
| Flexibility | Fixed pipeline | Agent chooses path |
| Learning | Static template | Memory accumulation |
| Adaptation | Manual template edits | Agents adapt based on performance |
| Intelligence | Regex-level | LLM reasoning |

## Notes

- The execution engine is **thin by design** — intelligence lives in prompts, not code
- Jobs are **creative briefs**, not scripts
- Agents **choose their own paths** — same brief, different executions over time
- Memory makes agents **improve without human intervention**
- Tool access is **filtered defensively** at multiple layers
- Traces provide **full observability** into agent decision-making
