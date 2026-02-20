# bolta.job.execute

**Version:** 2.0.0  
**Category:** Agent Lifecycle (Documentation)  
**Type:** System Documentation (Not a Callable Tool)

---

## Purpose

This is NOT a skill agents call directly. It's **documentation of how the V2 execution engine works** — the core system that powers agentic job execution.

Understanding this helps:
- Developers implement job execution correctly
- Users understand what happens when a job fires
- Agent designers understand the execution model

---

## What Is Job Execution?

In Bolta V2, a **Job** is a task binding that connects:
- An **Agent** (who does the work)
- A **Voice Profile** (how they sound)
- **Account(s)** (where they post)
- A **Schedule** (when they run)
- **Run Instructions** (what they should do)

When a job fires, the execution engine:
1. Loads the agent's context (persona, memory, voice profile)
2. Builds a system prompt with all relevant context
3. Sends the task brief to Claude Messages API
4. Agent reasons about the task and chooses tools
5. Execution loop runs until agent completes or hits max turns
6. Output is stored (draft posts, analytics reports, etc.)

---

## Architecture Components

### 1. Job Model

```python
class Job(models.Model):
    agent = ForeignKey(Agent)           # Which agent executes this
    name = CharField()                  # Human-readable job name
    voice_profile_id = UUIDField()      # Voice to use (required for content)
    account_ids = JSONField()           # Social accounts to target
    schedule = JSONField()              # Cron expression or event trigger
    trigger = CharField()               # "scheduled" | "manual" | "event"
    status = CharField()                # "active" | "paused" | "failed"
    run_instructions = TextField()      # Natural language task brief
```

**Key insight:** `run_instructions` is a BRIEF, not a script. The agent reads it and decides its own path.

---

### 2. Execution Engine (`execute_claude`)

**Core function signature:**

```python
def execute_claude(agent, messages, mode="job") -> dict:
    """
    Run the agent's reasoning loop with tool access.
    
    Args:
        agent: Agent model instance
        messages: List of message dicts for Claude API
        mode: "job" | "chat" | "mention"
    
    Returns:
        {
            "success": bool,
            "output": str,
            "tool_calls": int,
            "total_tokens": int,
            "cost_usd": float,
            "trace": [...],
        }
    """
```

**How it works:**

```python
# 1. Build system prompt (THE MAGIC)
system_prompt = build_system_prompt(agent, mode)
# Includes: persona + business DNA + voice profile + memory + task brief

# 2. Get tools for this agent
tools = get_tools_for_agent(agent, mode)
# Filtered by agent type + role (defense in depth)

# 3. Run Claude Messages API loop
for turn in range(max_turns):
    response = claude.messages.create(
        model=agent.model,
        system=system_prompt,
        tools=tools,
        messages=messages,
    )
    
    # If agent finished, return output
    if response.stop_reason == "end_turn":
        return extract_output(messages)
    
    # If agent used tools, execute them
    if response.stop_reason == "tool_use":
        results = [execute_tool_safe(block) for block in response.content]
        messages.append({"role": "user", "content": results})
        continue
    
    # Max turns exceeded
    return {"error": "max_turns_exceeded"}
```

**The orchestrator is ~50 lines. The intelligence is in:**
- System prompt construction
- Tool filtering and execution
- Context injection

---

### 3. System Prompt Builder

**Structure:**

```
[Base Template for Agent Type]
  → Type-specific behavioral guidelines
  → What the agent should/shouldn't do

[Persona]
  → User-editable personality
  → Tone, style, approach

[Memory]
  → What the agent has learned over time
  → Cross-run accumulated insights

[Runtime Context]
  → Current task brief
  → Mode-specific instructions
  → Available tool list
```

**Example for Content Creator:**

```
You are a Content Creator agent for Acme Corp.

## Your Role
Create compelling social media content that resonates...

## YOUR PERSONALITY
Bold, trend-aware, audience-obsessed. You use data hooks...

## WHAT YOU REMEMBER
- audience_preference: Educational content performs 3x better
- best_posting_time: Thursday 9am EST
- successful_hooks: Lead with specific numbers

## CURRENT TASK
Create 3 LinkedIn posts about remote work best practices.
Voice Profile ID: 284de8cd-6344-4c8c-8c4d-6da61b97e807
```

**This context makes the agent intelligent.**

---

### 4. Tool Execution

**Tool filtering (defense in depth):**

1. **By agent type:**
   - Content Creator → `draft_post`, `get_voice_profile`, `list_recent_posts`
   - Reviewer → `approve_post`, `reject_post`, `add_comment`
   - Analytics → `get_post_metrics`, `get_audience_insights`

2. **By agent role:**
   - `creator` role → can draft, can't approve
   - `editor` role → can draft, can approve
   - `admin` role → full access

3. **Runtime validation:**
   - Tool execution checks role again (defense in depth)
   - Logs all tool calls
   - Returns clear success/error responses

**Tool safety:**

```python
def execute_tool_safe(tool_name, tool_input, agent):
    # Role check
    if tool_name in ROLE_GATED_TOOLS:
        if agent.role not in ROLE_GATED_TOOLS[tool_name]:
            return {"error": "Permission denied"}
    
    # Execute with error handling
    try:
        result = _get_tool_handler(tool_name)(tool_input, agent)
        return result
    except Exception as e:
        logger.error(f"Tool error: {e}")
        return {"error": str(e)}
```

---

## Job Execution Flow

### Scheduled Job (Most Common)

```
1. Celery Beat runs every 60s
   → Queries: Jobs WHERE status='active' AND next_run <= now()

2. For each due job:
   → Create Run object (status='running')
   → Spawn Celery task: execute_job_run.delay(job_id, run_id, account_id)

3. Worker picks up task:
   → Acquires Postgres advisory lock (prevent concurrent posts to same account)
   → Loads agent, job, voice profile, account
   → Builds initial message with task brief
   → Calls execute_claude(agent, messages, mode="job")

4. Agent reasoning loop:
   → Reads task brief: "Create 3 LinkedIn posts about remote work"
   → Recalls memory: "Educational > promotional, Thursday is best"
   → Calls tools:
     - get_voice_profile(voice_profile_id)
     - list_recent_posts(account_id, limit=10)
     - draft_post(content, platform, account_id, voice_profile_id)
   → Returns output

5. Run completes:
   → Update Run (status='completed', tokens, cost, trace)
   → Release advisory lock
   → Update Job (last_run, next_run, run_count)

6. Draft appears in Inbox
   → Human reviews
   → Approves or rejects
   → If approved → scheduled → published
```

---

### Manual Job

```
User triggers job manually via UI
→ Same flow as scheduled, but trigger="manual"
→ Runs immediately, doesn't update next_run
```

---

### Event-Triggered Job

```
Event fires (new mention, new follower, etc.)
→ Job.trigger = "event"
→ Event payload passed to agent as context
→ Same execution flow
```

---

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
- Role permissions (creator can't publish directly)
- Workspace quotas (token limits, run limits)

**The balance:** Agent has creative freedom within safety constraints.

---

## Cost Tracking

**Token-based pricing:**

```python
# After execution:
run.input_tokens = sum([turn.input_tokens for turn in trace])
run.output_tokens = sum([turn.output_tokens for turn in trace])
run.total_tokens = run.input_tokens + run.output_tokens

# Cost calculation (example for Claude Sonnet):
input_cost_per_million = 3.00   # $3/M input tokens
output_cost_per_million = 15.00  # $15/M output tokens

run.cost_usd = (
    (run.input_tokens / 1_000_000) * input_cost_per_million +
    (run.output_tokens / 1_000_000) * output_cost_per_million
)
```

**Workspace quota enforcement:**

```python
if workspace.total_cost_this_month > workspace.quota_limit:
    pause_all_jobs(workspace)
    notify_admin("Quota exceeded")
```

---

## Debugging Job Execution

**Run trace structure:**

```json
{
  "run_id": "uuid",
  "agent_id": "uuid",
  "job_id": "uuid",
  "status": "completed",
  "started_at": "2026-02-20T14:30:00Z",
  "completed_at": "2026-02-20T14:30:45Z",
  "total_tokens": 4523,
  "cost_usd": 0.087,
  "trace": [
    {
      "turn": 1,
      "role": "assistant",
      "thinking": "I need to check recent posts and voice profile first...",
      "tool_calls": [
        {"tool": "bolta.list_recent_posts", "input": {...}, "output": {...}},
        {"tool": "bolta.get_voice_profile", "input": {...}, "output": {...}}
      ]
    },
    {
      "turn": 2,
      "role": "assistant",
      "thinking": "Now I'll draft the post...",
      "tool_calls": [
        {"tool": "bolta.draft_post", "input": {...}, "output": {...}}
      ]
    },
    {
      "turn": 3,
      "role": "assistant",
      "content": "Task completed. Draft created with ID abc-123.",
      "stop_reason": "end_turn"
    }
  ]
}
```

**This trace shows:**
- How the agent reasoned
- Which tools it chose
- In what order
- What it decided at each step

**Essential for debugging and improving prompts.**

---

## Key Differences from V1 RecurringTemplates

| Aspect | V1 (RecurringTemplates) | V2 (Job Execution) |
|--------|-------------------------|---------------------|
| **Execution** | Template fill → post | Agent reasoning → tools → output |
| **Flexibility** | Fixed pipeline | Agent chooses path |
| **Learning** | Static template | Memory accumulation |
| **Context** | Template variables | Full business DNA + voice + memory |
| **Adaptation** | Manual template edits | Agents adapt based on performance |
| **Intelligence** | None (regex-level) | Claude reasoning (LLM-level) |

---

## Notes

- The execution engine is **thin by design** — intelligence lives in prompts, not code
- Jobs are **creative briefs**, not scripts to execute
- Agents **choose their own paths** — same brief, different executions over time
- Memory makes agents **improve without human intervention**
- Tool access is **filtered defensively** at multiple layers
- Traces provide **full observability** into agent decision-making

**This is what "truly agentic" means.**
