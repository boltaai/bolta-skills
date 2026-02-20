---
name: bolta.agent.memory
version: 2.0.0
description: Store and retrieve information across job runs - how agents learn and improve over time
category: agent
roles_allowed: [Viewer, Creator, Editor, Admin]
agent_types: [content_creator, reviewer, analytics, engagement, custom]
safe_defaults:
  memory_scoped_per_agent: true
  allow_memory_updates: true
tools_required:
  - bolta.remember
  - bolta.recall
inputs_schema:
  type: object
  properties:
    action: { type: string, enum: [remember, recall], description: "Memory operation" }
    key: { type: string, description: "Memory key (required for remember, optional for recall)" }
    value: { type: string, description: "Value to store (required for remember)" }
outputs_schema:
  type: object
  properties:
    success: { type: boolean }
    key: { type: string }
    value: { type: string }
    updated_at: { type: string }
    count: { type: number, description: "Number of memories (for recall all)" }
    memories: { type: array, items: { type: object } }
organization: bolta.ai
author: Bolta Team
---

## Goal
Store and retrieve information across job runs. This is how agents **learn** and improve over time, accumulating context, preferences, and patterns that inform future decisions.

## Which Agents Use This
- **content_creator** — Remember what content performs best, posting times, audience preferences
- **reviewer** — Remember approval patterns, common issues, user feedback preferences
- **analytics** — Remember performance benchmarks, seasonal patterns, content mix insights
- **engagement** — Remember response templates, escalation rules, user sentiment patterns
- All agent types benefit from memory to improve over time

## Hard Rules
1. Memories MUST be scoped per agent instance (agent A's memory ≠ agent B's memory)
2. Memory updates allowed (same key overwrites previous value)
3. MUST track updated_at timestamp for each memory
4. MUST NOT share memories across different agents (isolated per agent)
5. MUST NOT delete memories automatically (only explicit deletion or workspace wipe)
6. Store insights, not raw data dumps

## Steps

### bolta.remember — Store Memory

**Purpose:** Store a key-value pair in long-term memory

**1. Validate input**
- Key must be non-empty string
- Value must be non-empty string

**2. Store memory**
- Create or update AgentMemory record
- Scope to current agent_id
- Set updated_at timestamp

**3. Return confirmation**
- Return success status and whether memory was created or updated

### bolta.recall — Retrieve Memory

**Purpose:** Retrieve information from long-term memory

**1. If key provided**
- Query AgentMemory for specific key scoped to agent_id
- Return single memory with value and updated_at

**2. If key omitted**
- Query all memories for agent_id
- Return array of all memories with metadata

**3. If memory not found**
- Return success: false with clear error message

## Output

**remember response:**
```json
{
  "success": true,
  "message": "Remembered: best_posting_time",
  "action": "updated"
}
```

**recall response (single key):**
```json
{
  "success": true,
  "key": "audience_preference",
  "value": "Educational content performs 3x better than promotional. Focus on how-to guides.",
  "updated_at": "2026-02-15T14:30:00Z"
}
```

**recall response (all memories):**
```json
{
  "success": true,
  "count": 3,
  "memories": [
    {
      "key": "audience_preference",
      "value": "Educational content performs 3x better...",
      "updated_at": "2026-02-15T14:30:00Z"
    },
    {
      "key": "best_posting_time",
      "value": "Thursday 9am EST - 2x avg engagement",
      "updated_at": "2026-02-10T09:00:00Z"
    }
  ]
}
```

## Failure Handling
- If key not found during recall: return success: false with "Memory not found"
- If database write fails: log error, return failure, agent continues without memory
- If invalid key format (empty string): return validation error

## Recommended Memory Keys

**Content Creator:**
- `audience_preference` — What content performs best
- `best_posting_time` — Optimal timing patterns
- `successful_hooks` — Hook styles that work
- `avoid_topics` — Topics that underperformed
- `platform_learnings` — Platform-specific insights

**Reviewer:**
- `creator_patterns` — Common issues to watch for
- `approval_criteria` — What makes content approve-worthy
- `user_preferences` — How human likes feedback delivered

**Analytics:**
- `performance_benchmarks` — Baseline metrics by platform
- `seasonal_patterns` — Quarterly/monthly trends
- `content_mix_optimal` — Ideal ratio of content types

**Engagement:**
- `response_templates` — What replies work for common questions
- `escalation_rules` — When to flag for human
- `effective_de_escalation` — What works to calm complaints

## Example: Learning Over Time

**Job Run #1 (no memory):**
```
Agent drafts post
Uses voice profile + recent posts
→ remember(key="first_run_topic", value="new_feature_launch")
```

**Job Run #5:**
```
Agent recalls memories
Sees: "Educational posts perform 3x better"
Adapts strategy
→ remember(key="feature_post_approach", value="Educational framing works better")
```

**Job Run #10:**
```
Agent recalls all memories
Sees patterns: Thursday 9am, educational framing, data-driven hooks
Applies learned best practices
→ Performance exceeds baseline
→ remember(key="pattern_confirmed", value="Data hooks + educational + Thursday = high engagement")
```

This is **compounding intelligence** — agents get smarter over time without human intervention.
