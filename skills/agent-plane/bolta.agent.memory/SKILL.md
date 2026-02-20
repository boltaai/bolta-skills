# bolta.agent.memory

**Version:** 2.0.0  
**Category:** Agent Lifecycle  
**Agent Types:** All (foundational capability)  
**Roles Allowed:** All (agents use this for their own memory)

---

## Purpose

Store and retrieve information across job runs. This is how agents LEARN and improve over time.

Memory is what makes an agent a **team member** instead of a **script**. It accumulates context, preferences, and patterns that inform future decisions.

---

## When An Agent Uses This

**Content Creator reasoning:**
- "I should remember that Thursday posts get 2x engagement"
- "Last time I wrote about pricing, the reviewer flagged it — I'll avoid that pattern"
- "Audience prefers educational content over promotional 3:1"

**Reviewer reasoning:**
- "Content Creator tends to use 'leverage' — I need to watch for that"
- "When posts mention pricing, I should fact-check against current tiers"
- "User prefers punchy feedback over diplomatic suggestions"

**Analytics reasoning:**
- "LinkedIn threads outperform single posts, but only on Tuesdays"
- "Engagement drops 40% when we post >2x per day"
- "Best posting time shifts seasonally — track quarterly"

**Engagement reasoning:**
- "This user responded well to empathy last time — use that approach"
- "Question about Feature X comes up weekly — prepare standard response"
- "Escalation threshold: anything mentioning refunds → human immediately"

---

## What This Skill Does

Provides two core capabilities:

### 1. `bolta.remember` — Store Memory

Store a key-value pair in the AgentMemory table:

```
Agent thinks: "Thursday posts perform best"
→ remember(key="best_posting_day", value="Thursday - 2x avg engagement")
```

### 2. `bolta.recall` — Retrieve Memory

Retrieve stored memory by key or get all memories:

```
Agent thinks: "What did I learn about posting times?"
→ recall(key="best_posting_day")
→ Returns: "Thursday - 2x avg engagement"
```

---

## How It Works Differently Than V1

**V1 Approach:**
- No persistent memory across runs
- Each execution started fresh
- Templates couldn't learn or adapt
- Patterns had to be manually configured

**V2 Approach:**
- Memory persists across job runs
- Agents accumulate learnings over time
- Patterns emerge organically from experience
- System gets smarter without human intervention

**Example evolution:**

```
Week 1 (Content Creator):
- Drafts posts
- No memory yet
- Uses voice profile + recent posts for context

Week 4:
- Remembers: "educational > promotional 3:1"
- Remembers: "Thursday posts get 2x engagement"
- Remembers: "Threads work better than single posts on LinkedIn"
- Adapts strategy based on accumulated memory

Week 12:
- Remembers: 20+ patterns about what works
- Can explain WHY it made specific choices
- Strategies are data-informed, not template-driven
```

---

## Tools

### bolta.remember

**Purpose:** Store information in long-term memory

**Parameters:**

```json
{
  "key": "string (required)",    // Memory key (e.g., "best_posting_time")
  "value": "string (required)"   // What to remember
}
```

**Returns:**

```json
{
  "success": true,
  "message": "Remembered: best_posting_time",
  "action": "created" | "updated"
}
```

**Usage example:**

```
Content Creator after analyzing performance:
→ remember(
    key="audience_preference", 
    value="Educational content performs 3x better than promotional. Focus on how-to guides and case studies."
  )
```

---

### bolta.recall

**Purpose:** Retrieve information from long-term memory

**Parameters:**

```json
{
  "key": "string (optional)"  // If omitted, returns ALL memories
}
```

**Returns (single key):**

```json
{
  "success": true,
  "key": "audience_preference",
  "value": "Educational content performs 3x better than promotional...",
  "updated_at": "2026-02-15T14:30:00Z"
}
```

**Returns (all memories):**

```json
{
  "success": true,
  "count": 5,
  "memories": [
    {
      "key": "audience_preference",
      "value": "Educational content performs 3x better...",
      "updated_at": "2026-02-15T14:30:00Z"
    },
    {
      "key": "best_posting_time",
      "value": "9am EST on weekdays, avoid weekends",
      "updated_at": "2026-02-10T09:00:00Z"
    }
    // ... more memories
  ]
}
```

**Usage example:**

```
Content Creator before drafting:
→ recall()  // Get all memories
→ Reads: "audience_preference", "best_posting_time", "avoid_topics"
→ Uses this context to inform draft strategy
```

---

## Hard Rules

**MUST:**
- Scope memories to the agent instance (agent A's memory ≠ agent B's memory)
- Allow memory updates (same key = overwrite previous value)
- Track updated_at timestamp for each memory
- Return clear success/error responses

**MUST NOT:**
- Share memories across different agents (each agent has isolated memory)
- Delete memories automatically (only explicit deletion or workspace wipe)
- Limit memory storage (agents should be able to remember indefinitely)
- Block memory writes due to "too many memories"

**SHOULD:**
- Encourage agents to remember actionable insights, not raw data
- Store WHY something works, not just WHAT worked
- Update memories when new data contradicts old patterns
- Use descriptive keys (not "memory_1", "memory_2")

---

## Memory Categories (Recommended Keys)

Different agent types benefit from different memory patterns:

**Content Creator:**
- `audience_preference` — What content performs best
- `best_posting_time` — Optimal timing patterns
- `avoid_topics` — Topics that underperformed
- `successful_hooks` — Hook styles that work
- `platform_learnings` — Platform-specific patterns

**Reviewer:**
- `creator_patterns` — What Content Creator tends to do wrong
- `approval_criteria` — What makes content approve-worthy
- `brand_violations` — Common off-brand patterns to watch for
- `user_preferences` — How the human likes feedback delivered

**Analytics:**
- `performance_benchmarks` — Baseline metrics by platform
- `seasonal_patterns` — Quarterly/monthly trends
- `content_mix_optimal` — Ideal ratio of content types
- `audience_segments` — Key audience behavior patterns

**Engagement:**
- `response_templates` — What replies work for common questions
- `escalation_rules` — When to flag for human
- `user_sentiment_patterns` — How specific users engage
- `effective_de_escalation` — What works to calm complaints

---

## Cross-Agent Memory (Future)

Currently, each agent has isolated memory. Future enhancement:

**Shared workspace memory:**
- Analytics agent stores: "LinkedIn threads outperform single posts"
- Content Creator reads workspace memory and adapts strategy
- Memory attribution: which agent stored it, when, based on what data

**This enables emergent team intelligence** — insights from one agent inform others.

---

## Example: Content Creator Learning Over Time

**Job Run #1 (no memory):**
```
Agent drafts post about new feature
Uses voice profile + recent posts
No accumulated learnings yet
→ remember(key="first_run_topic", value="new_feature_launch")
```

**Job Run #5:**
```
Agent recalls memories
Sees: "Educational posts perform 3x better than promotional"
Decides: Frame new feature as educational (how to use it) vs. announcement
→ remember(key="feature_post_approach", value="Educational framing works better")
```

**Job Run #10:**
```
Agent recalls memories
Sees: "best_posting_time: Thursday 9am"
Sees: "audience_preference: Educational > promotional"
Sees: "successful_hooks: Use specific numbers"
Drafts: Educational post with data-driven hook, scheduled for Thursday
→ Performance exceeds baseline
→ remember(key="pattern_confirmed", value="Data hooks + educational + Thursday = high engagement")
```

**This is compounding intelligence.**

---

## Integration with Other Skills

**Used by:**
- `bolta.draft_post` — Content Creator recalls best practices before drafting
- `bolta.approve_post` — Reviewer recalls approval criteria
- `bolta.get_post_metrics` — Analytics stores performance patterns
- `bolta.reply_to_mention` — Engagement recalls successful response styles

**Enables:**
- Continuous improvement without human intervention
- Personalized strategies per agent instance
- Data-informed decision making
- Reduced reliance on hardcoded rules

---

## Metrics to Track

- **Memory usage growth** — How many memories per agent over time
- **Memory reference rate** — How often agents recall before acting
- **Memory update frequency** — How often memories get refined
- **Performance correlation** — Does more memory = better output?

---

## Error Handling

**Common scenarios:**

1. **Memory not found:**
   - Return `success: false` with clear error
   - Agent should handle gracefully (use defaults)

2. **Invalid key format:**
   - Validate key is non-empty string
   - Suggest descriptive key names

3. **Database write failure:**
   - Log error, return failure response
   - Agent can retry or continue without memory

---

## Notes

- Memory is **per-agent**, not per-workspace or per-job
- Memories persist **forever** (unless explicitly deleted or workspace wiped)
- Agents should remember **insights**, not raw data dumps
- Good memory: "Thursday posts get 2x engagement — schedule accordingly"
- Bad memory: "Post ID 12345 got 47 likes on 2026-02-15 at 9:03am"
- **The quality of memory determines the quality of learning**
