# Bolta Agentic Skills Pack v1

Bolta is a **policy-aware creative workflow runtime**.

This Skills Pack transforms Bolta from a scheduling tool into an
**agent-native content operating system** — where agents generate,
route, review, and automate content safely inside governed workspaces.

Agents act.  
Bolta enforces.  
Humans retain control.

---

# 🧠 Primary Agentic Workflows

Bolta supports three foundational paradigms.

Everything else builds on these.

---

## Workflow A — Loop Builder → Inbox Review (Client-Run)

**Purpose**  
Generate structured content loops using Brand Voice + Templates,
then route all outputs into Inbox Review.

**What Happens**
- Agent builds a multi-post batch (7–14+ posts)
- Posts are generated in Brand Voice
- Posts are grouped into a review bundle
- Routing follows workspace policy automatically

**Policy Enforcement**
- Safe Mode ON → always Pending Review  
- Safe Mode OFF → defaults to review unless explicitly allowed  
- Role must include content creation capability  

**Skills Used**
- `bolta.loop.from_template`
- `bolta.draft.post`
- `bolta.submit_for_review`

This is the default safe creative workflow.

---

## Workflow B — Cron Agent → Recurring Job (Autopilot)

**Purpose**  
Run scheduled content generation automatically.

**What Happens**
- Agent runs on cron (local or hosted)
- Generates posts on cadence
- Either routes to review or schedules directly

**Hard Constraints**
- Safe Mode must be respected
- Scheduling requires explicit permission
- Role capabilities are enforced server-side

**Skills Used**
- `bolta.cron.generate_to_review`
- `bolta.cron.generate_and_schedule`

This is the automation layer.

---

## Workflow C — Agent as Teammate (RBAC Model)

**Purpose**  
Agents operate as first-class principals inside workspaces.

Agents:
- Have explicit roles (Creator / Viewer / Admin)
- Have scoped API keys
- Cannot bypass workspace policy
- Are logged in audit trails

All enforcement happens server-side.

**Skills Used**
- `bolta.team.create_agent_teammate`
- `bolta.team.rotate_key`
- `bolta.policy.explain`
- `bolta.audit.export_activity`

This is the governance layer.

---

# 🏛 Bolta Agentic Architecture

Bolta is divided into four planes. Skills orchestrate workflows; the backend enforces identity, permissions, and routing.

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
- Resources (voices, templates, posts, loops, accounts)

### Role → Capabilities
Roles determine what a principal can do.
- Owner / Admin / Creator / Viewer
- Capabilities map to actions (create, submit, approve, schedule, publish)

### Policy Gate
A centralized decision layer used by every entrypoint (UI, API, MCP tools):
- `authorize(principal, workspace, action, resource) -> allow/deny (+reason)`
- `resolve_route(policy, action, requested_state) -> final_state`

---
# 0️⃣ Voice Plane 

Voice is a first-class primitive in Bolta.

Before content can be generated, a workspace must have an active Voice Profile.
Voice Profiles define tone, structure, vocabulary bias, and stylistic rules
that agents must follow.

These skills initialize, validate, and evolve voice over time.

**Rule**

Before executing any Content Plane skill:

if no active voice_profile:
    require bolta.voice.bootstrap

Voice is a hard dependency for content generation.


## 1️⃣ Content Plane
Creates and shapes content.

**Responsibilities**
- Voice application (tone, style rules)
- Template rendering
- Draft generation
- Loop creation (structured batches)

**Primary primitives**
- Voice Profiles
- Templates
- Draft Posts
- Loops

**Typical states**
- `draft`

---

## 2️⃣ Review Plane
Controls human oversight and safe routing.

**Responsibilities**
- Inbox Review queue
- Bundling posts for review
- Approvals and edits
- Safe Mode enforcement

**Primary primitives**
- Review Items / Bundles
- Review Status transitions

**Typical states**
- `pending_review`
- `approved`
- `needs_edits`

**Rule**
- If Safe Mode is ON, content must pass through this plane before schedule/publish.

---

## 3️⃣ Automation Plane
Runs recurring workflows and conditional scheduling.

**Responsibilities**
- Cron-triggered generation (client-run or hosted later)
- Scheduling posts (only if allowed)
- Retry logic + idempotency keys
- Backoff + failure routing to review

**Primary primitives**
- Job Runs
- Generation Tasks
- Scheduling Requests

**Typical states**
- `scheduled`
- `failed -> pending_review`

---

## 4️⃣ Control Plane
Governance, identity, security, and observability.

**Responsibilities**
- Principals (humans + agents)
- Workspace memberships
- Role assignment
- API keys (scoped)
- Audit logs
- Policy configuration

**Primary primitives**
- Principals
- Memberships
- Policies
- Keys
- Audit Events

---

## State Machine (Simplified)

- `draft`
  -> `pending_review` (submit_for_review OR Safe Mode routing)
  -> `approved` (admin approval)
  -> `scheduled` (if allowed)
  -> `published`

Failure routing:
- schedule/publish denied or fails -> `pending_review` with warning (preferred)
- hard failures -> `draft` + error metadata

---

# 🔧 Core Tool Surface

All skills rely on a consistent, policy-aware tool layer:

- `bolta.get_workspace_policy`
- `bolta.get_my_capabilities`
- `bolta.get_voice_profile`
- `bolta.list_templates`
- `bolta.render_template`
- `bolta.create_post`
- `bolta.create_loop`
- `bolta.submit_for_review`
- `bolta.list_inbox_items`
- `bolta.update_post`
- `bolta.approve_post`
- `bolta.schedule_post`
- `bolta.publish_post`
- `bolta.create_agent_principal`
- `bolta.rotate_api_key`
- `bolta.export_audit_log`

Every skill must:

1. Query workspace policy  
2. Query effective capabilities  
3. Respect Safe Mode  
4. Never bypass server authorization  


# 🚀 Autonomy Levels

Bolta scales from assisted generation to fully autonomous runtime. These levels describe how customers typically adopt Bolta over time.

## Assisted Mode
- Draft generation
- Loop creation
- Weekly planning
- Human approval required

## Managed Automation
- Inbox triage
- Review digest
- Controlled approval routing
- Optional conditional scheduling

## Autopilot
- Cron-based generation
- Conditional scheduling
- Policy-aware automation

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

This is how autonomous content becomes safe, scalable, and enterprise-ready.
