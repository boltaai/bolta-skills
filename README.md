# Bolta Skills Pack — V2 Agentic Architecture

**Version:** 2.0.0  
**Philosophy:** [V2-AGENTIC-PHILOSOPHY.md](https://github.com/bolta-ai/Bolta-Server/blob/main/docs/V2-AGENTIC-PHILOSOPHY.md)  
**Status:** Production-ready

---

## What This Is

This is the **capability library** for Bolta V2's agentic automation platform.

Skills are not pipelines. Skills are **capabilities** that agents choose to use based on their reasoning about the task.

Different agents use the same skills differently. A Content Creator and a Reviewer both use `bolta.get_voice_profile`, but for different purposes:
- **Creator:** "What tone should I match?"
- **Reviewer:** "Does this draft match our canonical voice?"

**The agent's mindset determines how the tool serves them.**

---

## Core Philosophy

### Tools Are Hands, Reasoning Is the Product

> "Most 'AI-powered' products are Perplexity wrappers. Bolta V2 is different. The agent reasoning IS the product."

**Not this:**
```
Template loop → fill variables → post
```

**This:**
```
Agent receives brief → considers context → chooses tools → reasons about approach → delivers output
```

**Same brief, different executions over time** — the agent adapts based on memory and performance data.

---

## How Agents Use Skills

### Agent Types Have Different Mindsets

| Agent Type | Mindset | Primary Skills Used |
|------------|---------|---------------------|
| **Content Creator** | Creative, audience-focused | `draft_post`, `get_voice_profile`, `list_recent_posts` |
| **Reviewer** | Critical, brand-protective | `approve_post`, `reject_post`, `get_voice_profile` |
| **Analytics** | Data-driven, insight-focused | `get_post_metrics`, `get_audience_insights`, `get_best_posting_times` |
| **Engagement** | Social, de-escalation | `get_mentions`, `reply_to_mention`, `get_comments` |
| **Moderator** | Protective, fair | `get_comments`, moderation tools |
| **Acquisition** | Strategic, personalized | Lead scoring, outreach tools |
| **Custom** | User-defined | All tools (requires explicit configuration) |

### Example: Same Skill, Different Usage

**Skill:** `bolta.list_recent_posts`

**Content Creator uses it:**
- **Goal:** Avoid repetition
- **Reasoning:** "What did I post recently? I shouldn't repeat the same topic 3 days in a row."
- **Action:** Checks last 10 posts, sees 2 about pricing, decides to write about product features instead

**Analytics uses it:**
- **Goal:** Performance analysis
- **Reasoning:** "Which content types performed best? I need to recommend strategy adjustments."
- **Action:** Fetches last 50 posts with metrics, identifies patterns, stores findings in memory

**Reviewer uses it:**
- **Goal:** Strategic fit check
- **Reasoning:** "Is this draft timing appropriate given our recent content calendar?"
- **Action:** Checks last week's posts, sees we posted about pricing yesterday, flags draft as "too soon"

**Same tool. Three completely different use cases. The agent's mindset determines HOW the tool serves them.**

---

## Skill Planes (Capability Categories)

### agent-plane/ — Agent Lifecycle & Orchestration
**Purpose:** Hiring, configuring, and managing AI agents as team members

- **bolta.agent.hire** — Conversational agent onboarding from marketplace presets
- **bolta.agent.configure** — Modify agent persona, model tier, enabled skills
- **bolta.agent.activate_job** — Activate paused jobs after preview validation
- **bolta.agent.memory** — `remember` and `recall` for cross-run learning
- **bolta.agent.mention** — @mention handling (read-only feedback mode)
- **bolta.job.execute** — Documentation of the V2 execution engine

**Used by:** System/onboarding flows, all agent types (memory)

---

### content-plane/ — Content Creation Tools
**Purpose:** Drafting, voice matching, context gathering for content generation

- **bolta.draft_post** — Create draft post in brand voice for Inbox review
- **bolta.get_voice_profile** — Load voice details (tone, style, dos/donts)
- **bolta.list_recent_posts** — Check recent content to avoid repetition
- **bolta.get_business_context** — Load products, audience, brand DNA
- **bolta.get_account_info** — Social account details and token status
- **bolta.week.plan** — Content calendar planning (multi-post strategy)

**Used by:** Content Creator, Reviewer (for voice reference)

---

### review-plane/ — Review/QA Tools
**Purpose:** Quality gates, approval workflows, feedback loops

- **bolta.approve_post** — Approve draft (Draft → Approved)
- **bolta.reject_post** — Reject with specific feedback
- **bolta.add_comment** — Add review notes without approve/reject
- **bolta.inbox.triage** — Inbox management and prioritization
- **bolta.review.digest** — Review summary and activity log

**Used by:** Reviewer agents, human reviewers

---

### analytics-plane/ — Analytics Tools
**Purpose:** Performance tracking, audience insights, data-driven recommendations

- **bolta.get_post_metrics** — Post performance data (likes, shares, engagement rate)
- **bolta.get_audience_insights** — Demographics, behavior patterns, preferences
- **bolta.get_best_posting_times** — Optimal schedule based on YOUR data

**Used by:** Analytics agents, Content Creators (for informed strategy)

---

### engagement-plane/ — Engagement Tools
**Purpose:** Community management, mentions, replies, moderation

- **bolta.get_mentions** — Fetch mentions and replies directed at account
- **bolta.reply_to_mention** — Draft replies in brand voice
- **bolta.get_comments** — Fetch comments for response or moderation

**Used by:** Engagement agents, Moderator agents

---

### voice-plane/ — Voice Profile Tools
**Purpose:** Voice creation, learning, validation

- **bolta.voice.bootstrap** — Create comprehensive voice profile
- **bolta.voice.learn_from_samples** — Refine voice from existing content

**Used by:** Onboarding flows, voice management

---

### control-plane/ — Workspace Management
**Purpose:** Governance, policy, audit, team management

- **bolta.workspace.config** — Workspace settings and preferences
- **bolta.policy.explain** — Explain workspace policies and rules
- **bolta.audit.export_activity** — Export activity logs for compliance
- **bolta.team.create_agent_teammate** — Create new agent (V2-aware)

**Used by:** Admin users, system flows

---

### automation-plane/ — ⚠️ Partial Deprecation
**Purpose:** V1 legacy automation (migrating to job execution)

- ~~**bolta.loop.from_template**~~ — **DEPRECATED** (see `DEPRECATED.md`)
- **bolta.cron.generate_and_schedule** — Cron-based job execution (updated for V2)
- **bolta.cron.generate_to_review** — Cron → draft → Inbox flow

**Migration path:** Use Job execution instead of RecurringTemplates

---

## Skill Documentation Structure

Each skill includes:

### 1. SKILL.md — Comprehensive Documentation

- **What it does** (capability, not pipeline step)
- **Which agent types use it**
- **When an agent might choose this skill**
- **Parameters and return format**
- **Examples of agentic usage** (agent reasoning about when to use it)
- **Hard rules** (must/must not)

### 2. schema.json — Claude Messages API Tool Definition

- **name** — Matches exactly what `agents/tools.py` defines
- **description** — How agents understand the tool
- **input_schema** — Parameters with descriptions
- **required** — Which fields are mandatory

**Critical:** Schema MUST match server-side tool definitions in `Bolta-Server/agents/tools.py`

### 3. handler.example.py — Optional Reference Implementation

Shows how the tool connects to data (not always included).

---

## How Jobs Execute (High-Level)

```
1. Job fires (scheduled, manual, or event-triggered)
   ↓
2. Execution engine loads agent context:
   - Persona (agent personality + behavioral guidelines)
   - Memory (what the agent has learned)
   - Voice profile (brand voice reference)
   - Business DNA (products, audience, positioning)
   ↓
3. Agent receives task brief (natural language, not template)
   ↓
4. Agent reasons about task:
   - "What context do I need?"
   - "What approach makes sense?"
   - "What did I learn from previous runs?"
   ↓
5. Agent chooses tools:
   - get_voice_profile()
   - list_recent_posts()
   - recall("audience_preference")
   - draft_post(...)
   ↓
6. Agent iterates until complete or max turns
   ↓
7. Output delivered (draft in Inbox, report, etc.)
   ↓
8. Run logged (tokens, cost, trace)
```

**Key insight:** The agent chooses its own path. Same brief can result in different tool sequences based on context.

---

## Example: Content Creator Workflow

**Job:** "Create 3 LinkedIn posts about remote work best practices"

**Agent reasoning:**

```
Turn 1 (Context gathering):
Agent: "I need to understand the brand voice and recent content first."
→ Calls: get_voice_profile(voice_profile_id)
→ Calls: list_recent_posts(account_id, limit=10)
→ Calls: recall()  // Check what I've learned

Turn 2 (Analysis):
Agent: "Voice profile says: direct, specific, no jargon. Recent posts: 
2 about pricing (skip that topic). Memory says: educational > promotional 3:1.
Audience prefers how-to content with specific numbers."

Turn 3 (Drafting):
Agent: "I'll create an educational post with a numbered list and specific data."
→ Calls: draft_post(
    content="🏠 5 remote work mistakes...",
    platform="linkedin",
    account_id="...",
    voice_profile_id="...",
    notes="Educational format (performs 3x better). Used numbered list..."
  )

Turn 4 (Completion):
Agent: "Task complete. Draft created with ID abc-123. Ready for review."
→ Stores memory: remember(key="recent_topic", value="remote work mistakes")
```

**Result:** Draft in Inbox, human reviews, approves, schedules.

---

## Key Differences from V1

| Aspect | V1 (RecurringTemplates) | V2 (Agentic Jobs) |
|--------|-------------------------|-------------------|
| **Execution** | Template fill → post | Agent reasoning → tools → output |
| **Flexibility** | Fixed pipeline | Agent chooses path |
| **Learning** | Static template | Memory accumulation |
| **Context** | Template variables | Full business DNA + voice + memory |
| **Adaptation** | Manual edits | Agents adapt based on performance |
| **Intelligence** | None (regex-level) | Claude reasoning (LLM-level) |
| **Output** | Predictable, repetitive | Adaptive, context-aware |

---

## The Moat: Why This Is Defensible

Competitors can copy:
- The Messages API integration ✅
- The skill definitions ✅
- The UI ✅

Competitors **cannot** copy:
- Your voice profile after 260 feedback iterations ❌
- Your agent's accumulated memory (6 months of learned patterns) ❌
- Your business DNA (products, positioning, audience insights) ❌
- Your cross-agent coordination patterns (how your team learned to work together) ❌

**The longer you use Bolta, the smarter your agents get.**

And critically: **It's not one agent getting smarter — it's the SYSTEM getting smarter.**

Content Creator learns audience preferences → stores in memory  
Analytics agent identifies best posting times → stores in memory  
Content Creator reads Analytics' memory → adapts strategy  
Reviewer enforces new standards based on what works

**This is emergent team intelligence. Competitors can't replicate that with a signup form.**

---

## For Developers

### Adding a New Skill

1. **Choose the right plane** (content, review, analytics, etc.)
2. **Create directory:** `skills/{plane}/bolta.skill_name/`
3. **Write SKILL.md** — Focus on WHEN an agent uses this, not just WHAT it does
4. **Write schema.json** — Match format in `Bolta-Server/agents/tools.py`
5. **Implement handler** — Add to `agents/tools.py` tool registry
6. **Update this README** — Add to plane documentation
7. **Test with agent** — Does the agent choose it appropriately?

### Testing Skills

```bash
# Create test agent
curl -X POST /api/agents \
  -d '{"type": "content_creator", "name": "Test Agent"}'

# Create test job
curl -X POST /api/jobs \
  -d '{"agent_id": "...", "run_instructions": "Test task"}'

# Trigger execution
curl -X POST /api/jobs/{job_id}/run

# Check Run trace
curl /api/runs/{run_id}/trace
```

---

## For Users

### Getting Started

1. **Hire an agent** from the marketplace (e.g., "The Hype Man")
2. **Set up voice profile** (`bolta.voice.bootstrap`)
3. **Connect social accounts**
4. **Review preview draft** the agent generates
5. **Activate jobs** when ready
6. **Monitor Inbox** for agent-created drafts
7. **Approve/reject** with feedback
8. **Watch agents improve** as they learn from performance data

### Agent + Skill Pairing

- **Need content?** → Hire Content Creator → Uses content-plane skills
- **Need QA?** → Hire Reviewer → Uses review-plane skills
- **Need insights?** → Hire Analytics → Uses analytics-plane skills
- **Need community mgmt?** → Hire Engagement → Uses engagement-plane skills

**You can hire multiple agents** — they coordinate as a team.

---

## Migration from V1

If you're using RecurringTemplates (V1 loops):

1. **Read:** `skills/content-plane/bolta.loop.from_template/DEPRECATED.md`
2. **For each template:**
   - Create Content Creator agent
   - Create Job with natural language instructions (not template)
   - Bind voice_profile_id, account_ids
   - Activate job
3. **Delete old template**
4. **Observe improvement:** V2 agents will outperform static templates within 2 weeks

---

## Philosophy in Practice

### Skills Are Capabilities

Don't think: "This skill does X, then Y, then Z."

Think: "This skill gives the agent the ability to X. The agent decides when to use it."

### Agents Are Team Members

Don't think: "I configured this automation."

Think: "I hired this agent. It's learning how to help me."

### Reasoning Is the Product

Don't think: "Is this feature AI-powered?"

Think: "Does the AI reason about the task, or just execute a script?"

**If there's no reasoning, it's not agentic.**

---

## Links

- **Philosophy:** [V2-AGENTIC-PHILOSOPHY.md](https://github.com/bolta-ai/Bolta-Server/blob/main/docs/V2-AGENTIC-PHILOSOPHY.md)
- **Execution Engine:** `bolta.job.execute` documentation
- **Server Implementation:** [Bolta-Server/agents/](https://github.com/bolta-ai/Bolta-Server/tree/main/agents)
- **Changelog:** [CHANGELOG.md](./CHANGELOG.md)

---

**This is what "truly agentic" means.**

Tools are hands. Reasoning is the product. Agents are team members.

Welcome to Bolta V2. 🚀
