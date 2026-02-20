# Bolta Agentic Skills Pack v2

Bolta is a **policy-aware creative workflow runtime**.

This Skills Pack transforms Bolta from a scheduling tool into an
**agent-native content operating system** — where agents generate,
route, review, and automate content safely inside governed workspaces.

Agents act.  
Bolta enforces.  
Humans retain control.

---

## What's New in V2

**V2 introduces agentic job execution:**
- Jobs replace RecurringTemplates (agents reason about tasks instead of filling templates)
- Agent memory and learning (agents improve over time)
- Agent hiring flow (marketplace-driven onboarding)
- @Mention review workflow (feedback loops)
- Enhanced business context (products, audience DNA, performance data)

**Core philosophy:** Skills are capabilities that agents choose based on reasoning, not pipeline steps.

Different agents use the same skills differently based on their role and context.

---

## Agent Types

V2 introduces specialized agent types with different mindsets:

| Agent Type | Mindset | Primary Skills |
|------------|---------|----------------|
| **Content Creator** | Creative, audience-focused | `draft_post`, `get_voice_profile`, `list_recent_posts` |
| **Reviewer** | Critical, brand-protective | `approve_post`, `reject_post`, `inbox.triage` |
| **Analytics** | Data-driven, insight-focused | `get_post_metrics`, `get_audience_insights` |
| **Engagement** | Social, community-focused | `get_mentions`, `reply_to_mention` |
| **Moderator** | Protective, fair | `get_comments`, moderation tools |
| **Custom** | User-defined | All tools (requires explicit configuration) |

---

# 🧠 Primary Agentic Workflows

Bolta supports five foundational workflows.

---

## Workflow A — Agent Job → Inbox Review

**Purpose**  
Agents generate content using jobs (not templates), then route to Inbox Review.

**What Happens**
- Agent receives job brief (natural language instructions)
- Agent reasons about task and chooses tools
- Agent drafts content in Brand Voice
- Content automatically routes to Inbox for human review
- Routing follows workspace policy automatically

**Policy Enforcement**
- Safe Mode ON → always routes to Inbox Review  
- Safe Mode OFF → defaults to Inbox unless role is Editor/Admin  
- Role capabilities enforced server-side

**Skills Used**
- `bolta.draft.post`
- `bolta.get_voice_profile`
- `bolta.list_recent_posts`
- `bolta.agent.memory` (remember/recall)

**V2 Enhancement:** Agents learn from feedback and adapt drafts over time.

---

## Workflow B — Scheduled Job → Recurring Automation

**Purpose**  
Run scheduled content generation automatically.

**What Happens**
- Job fires on schedule (cron, event trigger, or manual)
- Agent loads context (voice, memory, business DNA)
- Agent generates content
- Either routes to review or schedules directly (based on policy)

**Hard Constraints**
- Safe Mode must be respected
- Scheduling requires explicit permission
- Role capabilities enforced server-side

**Skills Used**
- `bolta.job.execute`
- `bolta.draft.post`
- `bolta.get_voice_profile`

**V2 Enhancement:** Jobs use agent reasoning instead of template fills.

---

## Workflow C — Inbox Triage + Review

**Purpose**  
Human or agent reviews pending content before approval/scheduling.

**What Happens**
- Drafts accumulate in Inbox
- Reviewer (human or agent) triages items
- Items approved/rejected with feedback
- Approved items scheduled or published

**Skills Used**
- `bolta.inbox.triage`
- `bolta.review.approve_and_route`
- `bolta.reject_post`
- `bolta.add_comment`

**V2 Enhancement:** Reviewer agents can auto-triage with confidence scores.

---

## Workflow D — Agent Hiring Flow (New in V2)

**Purpose**  
Onboard agents as teammates from marketplace presets.

**What Happens**
- User selects agent preset (e.g., "The Hype Man")
- Agent configuration loads (persona, model tier, skills)
- Agent generates preview draft
- User reviews preview and activates agent
- Agent jobs become active

**Skills Used**
- `bolta.agent.hire`
- `bolta.agent.configure`
- `bolta.agent.activate_job`

---

## Workflow E — @Mention Review (New in V2)

**Purpose**  
Capture feedback on live posts to improve future content.

**What Happens**
- User mentions agent on published post (@AgentName)
- Mention captured as feedback signal
- Agent stores learning in memory
- Future drafts incorporate feedback

**Skills Used**
- `bolta.agent.mention` (read-only)
- `bolta.agent.memory` (remember)

---

# 🏛 Bolta Agentic Architecture

Bolta is divided into skill planes. Skills orchestrate workflows; the backend enforces identity, permissions, and routing.

## Core Concepts

### Principal
A first-class actor in the system.
- `type`: `human` | `agent`
- Owns API keys / auth tokens
- Produces auditable actions

### Workspace
The governance boundary.
- Policies (Safe Mode, Inbox Direct Scheduling, etc.)
- Memberships (principals + roles)
- Resources (voices, templates, posts, jobs, accounts)

### Role → Capabilities
Roles determine what a principal can do.
- Viewer / Creator / Editor / Admin
- Capabilities map to actions (create, submit, approve, schedule, publish)

### Policy Gate
A centralized decision layer used by every entrypoint (UI, API, MCP tools):
- `authorize(principal, workspace, action, resource) -> allow/deny (+reason)`
- `resolve_route(policy, action, requested_state) -> final_state`

---

## State Machine

```
draft
  → inbox (submit_for_review OR Safe Mode routing)
  → approved (Editor/Admin approval)
  → scheduled (if allowed)
  → published
```

**Failure routing:**
- schedule/publish denied or fails → `inbox` with warning (preferred)
- hard failures → `draft` + error metadata

**V2 Note:** State names updated (`pending_review` → `inbox` in V2 codebase, but conceptually identical).

---

## 0️⃣ Voice Plane

Voice is a first-class primitive in Bolta.

Before content can be generated, a workspace must have an active Voice Profile.
Voice Profiles define tone, structure, vocabulary bias, and stylistic rules
that agents must follow.

**Rule:** Before executing any Content Plane skill, if no active voice_profile, require `bolta.voice.bootstrap`.

Voice is a hard dependency for content generation.

**Skills:**
- `bolta.voice.bootstrap` — Create comprehensive voice profile
- `bolta.voice.learn_from_samples` — Refine voice from existing content

---

## 1️⃣ Content Plane

Creates and shapes content.

**Responsibilities:**
- Voice application (tone, style rules)
- Template rendering (V1 compatibility)
- Draft generation
- Job execution (V2)

**Primary primitives:**
- Voice Profiles
- Templates (deprecated in V2, use jobs)
- Draft Posts
- Jobs (V2)

**Typical states:**
- `draft`
- `inbox` (V2)

**Skills:**
- `bolta.draft.post` — Create draft post in brand voice
- `bolta.get_voice_profile` — Load voice details
- `bolta.list_recent_posts` — Check recent content
- `bolta.get_business_context` — Load products, audience, brand DNA (V2)
- `bolta.week.plan` — Content calendar planning (V2)

---

## 2️⃣ Review Plane

Controls human oversight and safe routing.

**Responsibilities:**
- Inbox Review queue
- Bundling posts for review
- Approvals and edits
- Safe Mode enforcement

**Primary primitives:**
- Inbox Items
- Review Bundles
- Review Status transitions

**Typical states:**
- `inbox`
- `approved`
- `needs_edits`

**Rule:** If Safe Mode is ON, content must pass through this plane before schedule/publish.

**Skills:**
- `bolta.inbox.triage` — Inbox management and prioritization (V2)
- `bolta.review.approve_and_route` — Approve and schedule
- `bolta.reject_post` — Reject with feedback
- `bolta.add_comment` — Add review notes

---

## 3️⃣ Automation Plane

Runs recurring workflows and conditional scheduling.

**Responsibilities:**
- Job-triggered generation (V2)
- Cron-triggered generation (V1 compatibility)
- Scheduling posts (only if allowed)
- Retry logic + idempotency keys
- Backoff + failure routing to review

**Primary primitives:**
- Jobs (V2)
- Job Runs (V2)
- Generation Tasks
- Scheduling Requests

**Typical states:**
- `scheduled`
- `failed → inbox`

**Skills:**
- `bolta.job.execute` — V2 job execution engine (documentation)
- `bolta.cron.generate_and_schedule` — Cron-based automation (V1 compatibility)
- ~~`bolta.loop.from_template`~~ — **DEPRECATED** (V1 legacy, see DEPRECATED.md)

---

## 4️⃣ Agent Plane (New in V2)

Agent lifecycle, orchestration, and memory.

**Responsibilities:**
- Agent hiring and configuration
- Agent memory (cross-run learning)
- @Mention feedback loops
- Job activation

**Primary primitives:**
- Agent Teammates
- Agent Memory
- Agent Jobs
- Mentions

**Skills:**
- `bolta.agent.hire` — Conversational agent onboarding
- `bolta.agent.configure` — Modify agent settings
- `bolta.agent.activate_job` — Activate paused jobs
- `bolta.agent.memory` — remember/recall for learning
- `bolta.agent.mention` — @mention handling (read-only)

---

## 5️⃣ Analytics Plane (New in V2)

Performance tracking, audience insights, data-driven recommendations.

**Skills:**
- `bolta.get_post_metrics` — Post performance data
- `bolta.get_audience_insights` — Demographics, behavior patterns
- `bolta.get_best_posting_times` — Optimal schedule based on YOUR data

---

## 6️⃣ Engagement Plane (New in V2)

Community management, mentions, replies, moderation.

**Skills:**
- `bolta.get_mentions` — Fetch mentions and replies
- `bolta.reply_to_mention` — Draft replies in brand voice
- `bolta.get_comments` — Fetch comments for moderation

---

## 7️⃣ Control Plane

Governance, identity, security, and observability.

**Responsibilities:**
- Principals (humans + agents)
- Workspace memberships
- Role assignment
- API keys (scoped)
- Audit logs
- Policy configuration

**Primary primitives:**
- Principals
- Memberships
- Policies
- Keys
- Audit Events

**Skills:**
- `bolta.workspace.config` — Workspace settings
- `bolta.policy.explain` — Explain workspace policies
- `bolta.audit.export_activity` — Export activity logs
- `bolta.team.create_agent_teammate` — Create agent (V2)

---

# 🔧 Core Tool Surface

All skills rely on a consistent, policy-aware tool layer:

**Policy & Capabilities:**
- `bolta.get_workspace_policy`
- `bolta.get_my_capabilities`

**Voice & Context:**
- `bolta.get_voice_profile`
- `bolta.get_business_context` (V2)
- `bolta.list_templates`
- `bolta.render_template`

**Content Operations:**
- `bolta.draft_post` (V2, replaces `create_post`)
- `bolta.create_loop` (V1 compatibility)
- `bolta.list_recent_posts` (V2)

**Review Operations:**
- `bolta.inbox.triage` (V2)
- `bolta.approve_post`
- `bolta.reject_post`
- `bolta.add_comment` (V2)
- `bolta.schedule_post`
- `bolta.publish_post`

**Agent Operations (V2):**
- `bolta.agent.hire`
- `bolta.agent.configure`
- `bolta.agent.activate_job`
- `bolta.agent.memory` (remember/recall)

**Control Plane:**
- `bolta.team.create_agent_teammate`
- `bolta.workspace.config`
- `bolta.policy.explain`
- `bolta.audit.export_activity`

Every skill must:

1. Query workspace policy  
2. Query effective capabilities  
3. Respect Safe Mode  
4. Never bypass server authorization  

---

# 🚀 Autonomy Levels

Bolta scales from assisted generation to fully autonomous runtime. These levels describe how customers typically adopt Bolta over time.

## Assisted Mode
- Draft generation
- Job creation (V2)
- Weekly planning
- Human approval required

## Managed Automation
- Inbox triage
- Review digest
- Controlled approval routing
- Optional conditional scheduling

## Autopilot
- Job-based generation (V2)
- Conditional scheduling
- Policy-aware automation
- Agent learning from feedback

## Governance & Enterprise
- Agent management
- Key rotation
- Workspace policy controls
- Audit exports
- Activity filtering

---

# 🎯 Design Philosophy

Bolta is not:
- An API wrapper  
- A content generator  
- A basic scheduler  

Bolta is:
A **policy-aware agent runtime for creative systems**.

Agents generate.  
Policies govern.  
Humans approve.  

**V2 Addition:**
Skills are capabilities agents choose based on reasoning, not pipeline steps.
The same skill serves different purposes depending on the agent's role and context.

This is how autonomous content becomes safe, scalable, and enterprise-ready.

---

# 📦 Skill Documentation Structure

Each skill includes:

## 1. SKILL.md — Comprehensive Documentation

**Required sections:**
- **YAML frontmatter** (name, version, description, category, roles_allowed, inputs_schema, outputs_schema)
- **Goal** — What the skill does (1-2 sentences)
- **Steps** — Numbered workflow
- **Hard rules** — Must/must not constraints
- **Failure handling** — What happens when things go wrong
- **Output** — Return format

**V2 additions (optional):**
- **Which agent types use this** — Brief context
- **Example usage** — Real-world scenarios

## 2. schema.json — Claude Messages API Tool Definition

- **name** — Matches server-side tool definition
- **description** — How agents understand the tool
- **input_schema** — Parameters with descriptions
- **required** — Mandatory fields

## 3. handler.example.py — Optional Reference Implementation

Shows how the tool connects to data (not always included).

---

# 🔄 Migration from V1

If you're using RecurringTemplates (V1 loops):

1. **Read:** `skills/automation-plane/bolta.loop.from_template/DEPRECATED.md`
2. **For each template:**
   - Create Content Creator agent via `bolta.agent.hire`
   - Create Job with natural language instructions (not template variables)
   - Bind voice_profile_id, account_ids
   - Activate job via `bolta.agent.activate_job`
3. **Optional:** Delete old template
4. **Observe improvement:** V2 agents adapt and improve over time

**V1 skills still work** for backward compatibility, but V2 jobs are recommended.

---

# 📚 For Developers

## Adding a New Skill

1. **Choose the right plane** (content, review, agent, analytics, etc.)
2. **Create directory:** `skills/{plane}/bolta.skill_name/`
3. **Write SKILL.md:**
   - Start with YAML frontmatter
   - Write concrete steps (numbered)
   - Add hard rules and failure handling
   - Optionally add V2 agent context (brief)
4. **Write schema.json** — Match server-side tool definition
5. **Implement handler** — Add to server tool registry
6. **Update this README** — Add to plane documentation

## Testing Skills

Use the Bolta API or MCP server to test skills in context:

```bash
# Create test agent
curl -X POST /api/v1/agents \
  -d '{"type": "content_creator", "name": "Test Agent"}'

# Create test job
curl -X POST /api/v1/jobs \
  -d '{"agent_id": "...", "run_instructions": "Test task"}'

# Trigger execution
curl -X POST /api/v1/jobs/{job_id}/run
```

---

# 📚 For Users

## Getting Started

1. **Create workspace** and connect social accounts
2. **Set up voice profile** via `bolta.voice.bootstrap`
3. **Hire an agent** from the marketplace (optional, V2 feature)
4. **Create drafts** via `bolta.draft.post` or job execution
5. **Review in Inbox** and approve/reject with feedback
6. **Schedule or publish** approved content
7. **Watch agents improve** as they learn from feedback (V2)

## Quick Start (V1 Compatibility)

```bash
# Draft a post
bolta.draft.post({
  workspace_id: "...",
  voice_profile_id: "...",
  prompt: "Write about our new feature"
})

# Review and approve
bolta.review.approve_and_route({
  workspace_id: "...",
  post_ids: ["..."],
  schedule_mode: "use_suggested_time"
})
```

---

**This is what policy-aware agentic automation looks like.**

Agents act. Bolta enforces. Humans retain control.

Welcome to Bolta Skills Pack V2. 🚀
