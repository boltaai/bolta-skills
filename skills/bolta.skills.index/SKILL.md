# SKILL: bolta.skills.index

Display name: Bolta Skills Registry
Slug: bolta-skills-registry
Version: 0.4.0
Tags: registry,catalog,bootstrap,workspace,index,discovery
Organization: bolta.ai
Author: Max Fritzhand
Type: registry
Executes: false

## Purpose

**The canonical registry and orchestration layer for all Bolta skills.**

This skill serves as the single source of truth for skill discovery, installation recommendations, and workspace-aware capability bootstrapping. It does not execute content operations directly — instead, it provides intelligent routing to the appropriate skills based on:

- **Workspace policy** (Safe Mode, autonomy mode, quotas)
- **Principal identity** (user role, agent permissions)
- **Operational context** (what you're trying to accomplish)

**Key Responsibilities:**
1. **Discovery** - Index all available skills with metadata
2. **Recommendation** - Suggest install sets based on workspace policy and role
3. **Orchestration** - Guide multi-skill workflows
4. **Compatibility** - Enforce skill compatibility with workspace settings
5. **Bootstrapping** - Help new workspaces get started quickly

**When to Use:**
- Setting up a new workspace ("What skills should I install?")
- Discovering available capabilities ("What can Bolta do?")
- Troubleshooting skill compatibility ("Why can't I use this skill?")
- Planning multi-step workflows ("Which skills do I need?")

## Source

https://github.com/boltaai/bolta-skills

## Architecture: The Five Planes

Skills are organized into **planes** — logical groupings that separate concerns and enable modular capability composition.

### Voice Plane
**Purpose:** Brand voice creation, evolution, and validation

Voice is the foundation of all content operations. These skills help establish, refine, and maintain consistent brand voice across all generated content.

**Core Principle:** Voice should be learned from examples, validated against real content, and evolved over time.

**Skills:**
- `bolta.voice.bootstrap` - Interactive voice profile creation from scratch
- `bolta.voice.learn_from_samples` - Extract voice patterns from existing content
- `bolta.voice.evolve` - Refine voice based on approved posts
- `bolta.voice.validate` - Score content against voice profile (0-100)

**Typical Flow:**
1. Bootstrap initial voice profile
2. Learn from sample content
3. Validate generated content
4. Evolve voice as brand matures

---

### Content Plane
**Purpose:** Content creation, planning, and scheduling

The execution layer for post creation. These skills transform ideas into scheduled social media posts.

**Core Principle:** Content should be intentional, planned, and aligned with voice.

**Skills:**
- `bolta.draft.post` - Create a single post in Draft status
- `bolta.loop.from_template` - Generate multiple posts from a template
- `bolta.week.plan` - Plan a week's worth of content with scheduling
- `bolta.content.repurpose` - Transform long-form content into social posts
- `bolta.content.thread_builder` - Create multi-post threads (Twitter, LinkedIn)

**Output:** Draft or Scheduled posts (subject to Safe Mode routing)

---

### Review Plane
**Purpose:** Human-in-the-loop review and approval workflows

Enables teams to review, approve, and refine agent-generated content before publishing.

**Core Principle:** Autonomy with oversight — agents generate, humans decide.

**Skills:**
- `bolta.inbox.triage` - Organize pending posts by priority/topic
- `bolta.review.digest` - Daily summary of posts awaiting review
- `bolta.review.approve_and_route` - Bulk approve + schedule posts
- `bolta.review.suggest_edits` - AI-powered improvement suggestions
- `bolta.review.compliance_check` - Flag posts for policy violations

**Typical Flow:**
1. Agent creates posts → Pending Approval
2. `review.digest` sends daily summary
3. Human reviews via `inbox.triage`
4. Bulk approve via `approve_and_route`

---

### Automation Plane
**Purpose:** Scheduled, recurring, and autonomous content generation

The autonomy layer. These skills enable hands-off content operations with guardrails.

**Core Principle:** Predictable automation with quota enforcement and safety nets.

**Skills:**
- `bolta.cron.generate_to_review` - Daily content generation → Pending Approval
- `bolta.cron.generate_and_schedule` - Autonomous scheduling (requires Safe Mode OFF)
- `bolta.recurring.from_template` - Recurring posts (daily tips, weekly roundups)
- `bolta.auto.respond_to_trending` - Auto-generate posts from trending topics
- `bolta.auto.content_gap_fill` - Detect scheduling gaps and auto-fill

**Safety Guardrails:**
- Quota enforcement (max posts/day, max API requests/hour)
- Job run tracking (observability for all executions)
- Autonomy mode compatibility checks
- Safe Mode routing (autopilot incompatible with Safe Mode ON)

---

### Control Plane
**Purpose:** Workspace governance, policy, and audit

The management layer for teams, permissions, security, and compliance.

**Core Principle:** Visibility and control for workspace administrators.

**Skills:**
- `bolta.team.create_agent_teammate` - Provision agent principals with specific roles
- `bolta.team.rotate_key` - Rotate API keys for security
- `bolta.policy.explain` - Explain authorization decisions ("Why was this blocked?")
- `bolta.audit.export_activity` - Export audit logs (PostActivity, JobRuns)
- `bolta.quota.status` - View current quota usage (daily posts, hourly API calls)
- `bolta.workspace.config` - View/update autonomy mode, Safe Mode, quotas

**Typical Use Cases:**
- Onboarding new team members (human or agent)
- Investigating authorization failures
- Compliance reporting (SOC2, GDPR data exports)
- Quota monitoring and adjustment

---

## Full Skill Index

### Voice Plane Skills

#### bolta.voice.bootstrap
**Path:** `skills/voice-plane/bolta.voice.bootstrap/SKILL.md`
**Purpose:** Interactive voice profile creation wizard
**Inputs:** Brand name, industry, target audience
**Outputs:** Complete VoiceProfile (tone, dos, don'ts, constraints)
**Permissions:** `voice:write`
**Safe Mode:** Compatible
**Typical Duration:** 5-10 minutes (interactive)

#### bolta.voice.learn_from_samples
**Path:** `skills/voice-plane/bolta.voice.learn_from_samples/SKILL.md`
**Purpose:** Extract voice patterns from existing content
**Inputs:** URLs or text samples (3-10 examples)
**Outputs:** Voice profile draft with auto-detected patterns
**Permissions:** `voice:write`
**Safe Mode:** Compatible
**Typical Duration:** 2-3 minutes

#### bolta.voice.evolve
**Path:** `skills/voice-plane/bolta.voice.evolve/SKILL.md`
**Purpose:** Refine voice based on approved posts
**Inputs:** Date range for approved posts
**Outputs:** Updated VoiceProfile (version incremented)
**Permissions:** `voice:write`, `posts:read`
**Safe Mode:** Compatible
**Typical Duration:** 1-2 minutes
**Note:** Creates new VoiceProfileVersion snapshot

#### bolta.voice.validate
**Path:** `skills/voice-plane/bolta.voice.validate/SKILL.md`
**Purpose:** Score content against voice profile
**Inputs:** Post ID or content text
**Outputs:** Compliance score (0-100), deviation report
**Permissions:** `voice:read`, `posts:read`
**Safe Mode:** Compatible
**Typical Duration:** < 30 seconds

---

### Content Plane Skills

#### bolta.draft.post
**Path:** `skills/content-plane/bolta.draft.post/SKILL.md`
**Purpose:** Create a single post in Draft status
**Inputs:** Topic, platform(s), optional voice profile ID
**Outputs:** Post ID (Draft status)
**Permissions:** `posts:write`
**Safe Mode:** Always routes to Draft
**Autonomy Mode:** Respects assisted/managed routing
**Quota Impact:** +1 to daily post count
**Typical Duration:** 30-60 seconds

#### bolta.loop.from_template
**Path:** `skills/content-plane/bolta.loop.from_template/SKILL.md`
**Purpose:** Generate multiple posts from a template
**Inputs:** Template ID, count (1-50), variation parameters
**Outputs:** Array of Post IDs
**Permissions:** `posts:write`, `templates:read`
**Safe Mode:** Routes all posts to Draft
**Quota Impact:** +N to daily post count (checked before execution)
**Typical Duration:** 1-3 minutes (depends on count)
**Note:** Uses JobRun tracking for observability

#### bolta.week.plan
**Path:** `skills/content-plane/bolta.week.plan/SKILL.md`
**Purpose:** Plan a week's content with scheduling
**Inputs:** Start date, posting frequency, themes
**Outputs:** 7-day content calendar with scheduled posts
**Permissions:** `posts:write`, `posts:schedule`
**Safe Mode:** Routes to Pending Approval if ON
**Autonomy Mode:** Respects managed/autopilot routing
**Quota Impact:** +5-15 to daily post count (spread across week)
**Typical Duration:** 3-5 minutes

#### bolta.content.repurpose
**Path:** `skills/content-plane/bolta.content.repurpose/SKILL.md`
**Purpose:** Transform long-form content into social posts
**Inputs:** Blog URL or full text, target platforms
**Outputs:** Multiple platform-specific posts
**Permissions:** `posts:write`
**Safe Mode:** Routes to Draft
**Typical Duration:** 2-4 minutes

#### bolta.content.thread_builder
**Path:** `skills/content-plane/bolta.content.thread_builder/SKILL.md`
**Purpose:** Create multi-post threads
**Inputs:** Topic, thread length (2-10 posts), platform
**Outputs:** Linked post sequence
**Permissions:** `posts:write`
**Safe Mode:** Routes to Draft
**Typical Duration:** 1-2 minutes

---

### Review Plane Skills

#### bolta.inbox.triage
**Path:** `skills/review-plane/bolta.inbox.triage/SKILL.md`
**Purpose:** Organize pending posts by priority
**Inputs:** Optional filters (platform, date range)
**Outputs:** Categorized list of posts awaiting review
**Permissions:** `posts:read`, `posts:review`
**Safe Mode:** N/A (read-only)
**Typical Duration:** < 10 seconds

#### bolta.review.digest
**Path:** `skills/review-plane/bolta.review.digest/SKILL.md`
**Purpose:** Daily summary of posts awaiting review
**Inputs:** None (workspace context)
**Outputs:** Formatted summary with quick approve links
**Permissions:** `posts:read`, `posts:review`
**Safe Mode:** N/A (read-only)
**Typical Duration:** < 5 seconds
**Note:** Designed for cron execution (daily 9am)

#### bolta.review.approve_and_route
**Path:** `skills/review-plane/bolta.review.approve_and_route/SKILL.md`
**Purpose:** Bulk approve and schedule posts
**Inputs:** Post IDs or filter criteria
**Outputs:** Updated post statuses
**Permissions:** `posts:write`, `posts:approve`, `posts:schedule`
**Safe Mode:** N/A (human override)
**Typical Duration:** < 30 seconds
**Note:** Bypasses Safe Mode (human decision)

#### bolta.review.suggest_edits
**Path:** `skills/review-plane/bolta.review.suggest_edits/SKILL.md`
**Purpose:** AI-powered improvement suggestions
**Inputs:** Post ID
**Outputs:** Suggested edits with rationale
**Permissions:** `posts:read`, `voice:read`
**Safe Mode:** N/A (read-only)
**Typical Duration:** < 30 seconds

#### bolta.review.compliance_check
**Path:** `skills/review-plane/bolta.review.compliance_check/SKILL.md`
**Purpose:** Flag posts for policy violations
**Inputs:** Post ID or bulk filter
**Outputs:** Compliance report with severity flags
**Permissions:** `posts:read`, `policies:read`
**Safe Mode:** N/A (read-only)
**Typical Duration:** < 10 seconds

---

### Automation Plane Skills

#### bolta.cron.generate_to_review
**Path:** `skills/automation-plane/bolta.cron.generate_to_review/SKILL.md`
**Purpose:** Daily content generation → Pending Approval
**Inputs:** None (uses workspace settings)
**Outputs:** Posts in Pending Approval status
**Permissions:** `posts:write`, `cron:execute`
**Safe Mode:** Compatible (routes to Pending Approval)
**Autonomy Mode:** Recommended for managed/governance
**Quota Impact:** +3-10 posts/day (configurable)
**Typical Duration:** 2-5 minutes
**Execution:** Daily cron (configurable time)

#### bolta.cron.generate_and_schedule
**Path:** `skills/automation-plane/bolta.cron.generate_and_schedule/SKILL.md`
**Purpose:** Autonomous scheduling (no human review)
**Inputs:** None (uses workspace settings)
**Outputs:** Posts in Scheduled status
**Permissions:** `posts:write`, `posts:schedule`, `cron:execute`
**Safe Mode:** **INCOMPATIBLE** (requires Safe Mode OFF)
**Autonomy Mode:** **REQUIRES autopilot**
**Quota Impact:** +5-15 posts/day (configurable)
**Typical Duration:** 3-7 minutes
**Execution:** Daily cron (configurable time)
**Warning:** Bypasses human review — use with caution

#### bolta.recurring.from_template
**Path:** `skills/automation-plane/bolta.recurring.from_template/SKILL.md`
**Purpose:** Recurring posts (daily tips, weekly roundups)
**Inputs:** Template ID, recurrence pattern (daily/weekly/monthly)
**Outputs:** RecurringPostReview record + scheduled posts
**Permissions:** `posts:write`, `templates:read`
**Safe Mode:** Respects routing
**Quota Impact:** +N posts per recurrence
**Typical Duration:** 1-2 minutes (setup)

#### bolta.auto.respond_to_trending
**Path:** `skills/automation-plane/bolta.auto.respond_to_trending/SKILL.md`
**Purpose:** Auto-generate posts from trending topics
**Inputs:** Trending topic sources (Twitter, Google Trends)
**Outputs:** Posts related to current trends
**Permissions:** `posts:write`, `integrations:read`
**Safe Mode:** Routes to Pending Approval
**Quota Impact:** +1-5 posts/day
**Typical Duration:** 2-3 minutes

#### bolta.auto.content_gap_fill
**Path:** `skills/automation-plane/bolta.auto.content_gap_fill/SKILL.md`
**Purpose:** Detect scheduling gaps and auto-fill
**Inputs:** Date range to analyze
**Outputs:** Posts to fill detected gaps
**Permissions:** `posts:write`, `posts:read`
**Safe Mode:** Routes to Pending Approval
**Quota Impact:** Variable (based on gaps detected)
**Typical Duration:** 3-5 minutes

---

### Control Plane Skills

#### bolta.team.create_agent_teammate
**Path:** `skills/control-plane/bolta.team.create_agent_teammate/SKILL.md`
**Purpose:** Provision agent principals with roles
**Inputs:** Agent name, role (creator/editor/reviewer), permissions
**Outputs:** AgentPrincipal record + API key
**Permissions:** `workspace:admin`, `agents:create`
**Safe Mode:** N/A (admin operation)
**Role Required:** Owner or Admin
**Typical Duration:** < 30 seconds

#### bolta.team.rotate_key
**Path:** `skills/control-plane/bolta.team.rotate_key/SKILL.md`
**Purpose:** Rotate API keys for security
**Inputs:** API key ID or agent ID
**Outputs:** New API key (old key revoked)
**Permissions:** `workspace:admin`, `agents:manage`
**Safe Mode:** N/A (admin operation)
**Role Required:** Owner or Admin
**Typical Duration:** < 10 seconds
**Note:** Old key immediately invalidated

#### bolta.policy.explain
**Path:** `skills/control-plane/bolta.policy.explain/SKILL.md`
**Purpose:** Explain authorization decisions
**Inputs:** Action attempt (e.g., "Why can't I publish?")
**Outputs:** Policy analysis with specific blockers
**Permissions:** None (informational)
**Safe Mode:** N/A (read-only)
**Typical Duration:** < 5 seconds
**Use Case:** Troubleshooting "Access Denied" errors

#### bolta.audit.export_activity
**Path:** `skills/control-plane/bolta.audit.export_activity/SKILL.md`
**Purpose:** Export audit logs
**Inputs:** Date range, filters (principal, action type, denied actions)
**Outputs:** CSV or JSON export of PostActivity records
**Permissions:** `workspace:admin`, `audit:read`
**Safe Mode:** N/A (admin operation)
**Role Required:** Owner or Admin
**Typical Duration:** < 30 seconds
**Use Case:** Compliance reporting, SOC2 audits

#### bolta.quota.status
**Path:** `skills/control-plane/bolta.quota.status/SKILL.md`
**Purpose:** View current quota usage
**Inputs:** None (workspace context)
**Outputs:** Daily post count, hourly API usage, limits, percentage
**Permissions:** `workspace:read`
**Safe Mode:** N/A (read-only)
**Typical Duration:** < 5 seconds

#### bolta.workspace.config
**Path:** `skills/control-plane/bolta.workspace.config/SKILL.md`
**Purpose:** View/update workspace settings
**Inputs:** Settings to update (autonomy_mode, safe_mode, quotas)
**Outputs:** Updated workspace configuration
**Permissions:** `workspace:admin`
**Safe Mode:** N/A (admin operation)
**Role Required:** Owner or Admin
**Typical Duration:** < 10 seconds
**Warning:** Changing autonomy mode affects all agent operations

---

## Recommended Install Sets

Install sets are curated skill bundles tailored to specific autonomy modes and use cases.

### Assisted Mode Install Set
**Autonomy Level:** Low (maximum human control)
**Safe Mode:** Must be ON
**Use Case:** New users, high-stakes brands, learning Bolta

**Skills:**
- `bolta.voice.bootstrap` - Set up initial voice profile
- `bolta.draft.post` - Create individual posts (always Draft)
- `bolta.loop.from_template` - Scale content creation safely
- `bolta.week.plan` - Plan content calendar

**Rationale:**
Assisted mode prioritizes learning and control. All content goes to Draft for manual review before scheduling. Ideal for:
- Teams new to AI content generation
- Brands with strict compliance requirements
- Users who want to learn Bolta patterns before automating

**Expected Workflow:**
1. Bootstrap voice profile
2. Create posts in Draft (manually or via templates)
3. Human reviews and schedules each post
4. Graduate to Managed when comfortable

---

### Managed Mode Install Set
**Autonomy Level:** Medium (guided automation with oversight)
**Safe Mode:** ON (recommended) or OFF
**Use Case:** Established users, moderate volume, review workflows

**Skills:**
- All Assisted skills +
- `bolta.inbox.triage` - Organize posts for review
- `bolta.review.digest` - Daily review summaries
- `bolta.review.approve_and_route` - Bulk approval workflow
- `bolta.voice.validate` - Quality scoring
- `bolta.cron.generate_to_review` - Daily automated generation

**Rationale:**
Managed mode balances efficiency with oversight. Agent generates content autonomously, but humans approve before publishing. Ideal for:
- Teams with 1-2 reviewers
- Brands publishing 3-10 posts/day
- Users who trust the voice profile

**Expected Workflow:**
1. Agent generates posts overnight (via cron) → Pending Approval
2. Daily digest arrives at 9am
3. Reviewer triages inbox, validates voice compliance
4. Bulk approve/schedule approved posts
5. Refine voice profile based on patterns

---

### Autopilot Mode Install Set
**Autonomy Level:** High (hands-off automation)
**Safe Mode:** Must be OFF (incompatible)
**Use Case:** High volume, trusted voice, minimal oversight

**Skills:**
- All Managed skills +
- `bolta.cron.generate_and_schedule` - Autonomous scheduling
- `bolta.auto.respond_to_trending` - Trend-based posting
- `bolta.auto.content_gap_fill` - Auto-fill scheduling gaps
- `bolta.recurring.from_template` - Recurring post automation
- `bolta.quota.status` - Monitor quota usage

**Rationale:**
Autopilot mode maximizes efficiency for high-volume operations. Agent schedules directly without human approval. Ideal for:
- Established brands with proven voice profiles
- High-frequency posting (10+ posts/day)
- Teams with minimal manual review capacity

**Expected Workflow:**
1. Agent generates and schedules posts automatically
2. Quota enforcement prevents runaway generation
3. Periodic voice validation checks (weekly)
4. Human reviews published analytics, adjusts strategy

**Warning:**
Autopilot bypasses human review. Only use with:
- Well-tested voice profiles (version 5+)
- Quota limits configured (max 20 posts/day recommended)
- Regular validation spot-checks (review 10% of published posts)

---

### Governance Mode Install Set
**Autonomy Level:** N/A (control & audit focused)
**Safe Mode:** N/A
**Use Case:** Admins, compliance teams, workspace management

**Skills:**
- `bolta.policy.explain` - Authorization troubleshooting
- `bolta.audit.export_activity` - Compliance exports
- `bolta.team.create_agent_teammate` - Agent provisioning
- `bolta.team.rotate_key` - Security operations
- `bolta.workspace.config` - Workspace administration
- `bolta.quota.status` - Usage monitoring
- `bolta.voice.validate` - Quality auditing

**Rationale:**
Governance mode is not an autonomy level — it's a control plane install set for administrators. Ideal for:
- Workspace owners managing teams
- Compliance officers conducting audits
- Security teams rotating keys
- Admins troubleshooting authorization issues

**Expected Workflow:**
1. Onboard new team members (human or agent)
2. Configure workspace policies (Safe Mode, autonomy, quotas)
3. Monitor quota usage and adjust limits
4. Export audit logs for compliance reporting
5. Rotate API keys on schedule (e.g., quarterly)
6. Investigate authorization failures via policy.explain

---

## Decision Matrix: Skill Recommendations

This matrix determines which skills to recommend based on workspace context.

### Input Variables
1. **Safe Mode** (ON/OFF)
2. **Autonomy Mode** (assisted/managed/autopilot/governance)
3. **User Role** (owner/admin/editor/creator/reviewer/viewer)
4. **Agent Permissions** (if principal is agent)
5. **Workspace Quotas** (daily post limit, hourly API limit)
6. **Voice Profile Status** (exists, version number)

### Decision Rules

#### Rule 1: Voice Bootstrapping (First-Time Setup)
```
IF voice_profile_count == 0:
  RECOMMEND: bolta.voice.bootstrap (HIGH PRIORITY)
  RATIONALE: Cannot create content without voice profile
```

#### Rule 2: Safe Mode + Autopilot Incompatibility
```
IF safe_mode == ON AND autonomy_mode == "autopilot":
  ERROR: Incompatible configuration
  RECOMMEND: Either disable Safe Mode OR switch to "managed"
  RATIONALE: Autopilot bypasses review; contradicts Safe Mode intent
```

#### Rule 3: Agent Permission Gating
```
IF principal_type == "agent":
  IF agent.permissions NOT IN required_permissions:
    EXCLUDE: Skills requiring missing permissions
    RECOMMEND: bolta.policy.explain to understand blockers
```

#### Rule 4: Role-Based Filtering
```
IF role IN ["viewer", "reviewer"]:
  EXCLUDE: All write operations (posts:write, voice:write)
  INCLUDE: Read-only skills (audit.export, policy.explain)

IF role IN ["creator", "editor"]:
  INCLUDE: Content plane skills
  EXCLUDE: Control plane skills (team.*, workspace.config)

IF role IN ["admin", "owner"]:
  INCLUDE: All skills (no restrictions)
```

#### Rule 5: Quota-Based Warnings
```
IF daily_posts_used >= (daily_post_limit * 0.8):
  WARN: "Approaching daily quota limit"
  RECOMMEND: bolta.quota.status to view usage

IF daily_posts_used >= daily_post_limit:
  BLOCK: All posts:write skills
  RECOMMEND: Increase quota via bolta.workspace.config
```

#### Rule 6: Autonomy Mode Routing
```
IF autonomy_mode == "assisted":
  INCLUDE: Content plane (draft only)
  EXCLUDE: Automation plane (no cron jobs)

IF autonomy_mode == "managed":
  INCLUDE: Content + Review planes
  INCLUDE: bolta.cron.generate_to_review (safe automation)
  EXCLUDE: bolta.cron.generate_and_schedule (requires autopilot)

IF autonomy_mode == "autopilot":
  INCLUDE: All automation skills
  REQUIRE: Safe Mode OFF
  RECOMMEND: Quota monitoring (quota.status)
```

---

## Registry Flow (Detailed)

### Step 1: Gather Workspace Context
**API Call:** `GET /api/v1/workspaces/{workspace_id}`

**Extract:**
- `safe_mode` (boolean)
- `autonomy_mode` (assisted/managed/autopilot/governance)
- `max_posts_per_day` (int, nullable)
- `max_api_requests_per_hour` (int, nullable)

### Step 2: Identify Principal
**API Call:** `GET /api/v1/me` or use request context

**Extract:**
- `principal_type` (user or agent)
- `role` (owner/admin/editor/creator/reviewer/viewer)
- If agent: `permissions` array, `autonomy_override`

### Step 3: Check Voice Profile Status
**API Call:** `GET /api/v1/workspaces/{workspace_id}/voice-profiles`

**Extract:**
- `voice_profile_count` (0 = needs bootstrap)
- Latest `version` (higher version = more refined)
- `status` (active/draft/archived)

### Step 4: Check Quota Usage
**API Call:** `GET /api/v1/workspaces/{workspace_id}/quota-status` (via `bolta.quota.status`)

**Extract:**
- `daily_posts.used` / `daily_posts.limit`
- `hourly_api_requests.used` / `hourly_api_requests.limit`

### Step 5: Apply Decision Rules
Run through decision matrix (see above) to filter skills.

**Output:**
- `recommended_skills` - Array of skill slugs
- `excluded_skills` - Array with exclusion reasons
- `warnings` - Array of configuration issues

### Step 6: Return Structured Response
```json
{
  "workspace_id": "uuid",
  "safe_mode": true,
  "autonomy_mode": "managed",
  "role": "editor",
  "principal_type": "user",
  "voice_profile_status": {
    "exists": true,
    "version": 3,
    "status": "active"
  },
  "quota_status": {
    "daily_posts": {
      "used": 12,
      "limit": 100,
      "percentage": 12
    },
    "hourly_api_requests": {
      "used": 45,
      "limit": 1000,
      "percentage": 4.5
    }
  },
  "recommended_mode": "managed",
  "recommended_skills": [
    "bolta.draft.post",
    "bolta.loop.from_template",
    "bolta.week.plan",
    "bolta.inbox.triage",
    "bolta.review.digest",
    "bolta.review.approve_and_route",
    "bolta.voice.validate",
    "bolta.cron.generate_to_review"
  ],
  "excluded_skills": [
    {
      "skill": "bolta.cron.generate_and_schedule",
      "reason": "Requires autonomy_mode=autopilot (current: managed)"
    },
    {
      "skill": "bolta.workspace.config",
      "reason": "Requires role owner/admin (current: editor)"
    }
  ],
  "warnings": [],
  "next_steps": [
    "Install recommended skills via MCP or API",
    "Run bolta.voice.validate to check content quality",
    "Configure daily digest via bolta.review.digest"
  ]
}
```

---

## Output Examples

### Example 1: New Workspace (First-Time Setup)
```json
{
  "workspace_id": "550e8400-e29b-41d4-a716-446655440000",
  "safe_mode": true,
  "autonomy_mode": "assisted",
  "role": "owner",
  "principal_type": "user",
  "voice_profile_status": {
    "exists": false,
    "version": 0,
    "status": null
  },
  "quota_status": {
    "daily_posts": {"used": 0, "limit": 100, "percentage": 0},
    "hourly_api_requests": {"used": 0, "limit": 1000, "percentage": 0}
  },
  "recommended_mode": "assisted",
  "recommended_skills": [
    "bolta.voice.bootstrap"
  ],
  "excluded_skills": [],
  "warnings": [
    {
      "type": "missing_voice_profile",
      "message": "No voice profile found. Run bolta.voice.bootstrap to get started.",
      "severity": "high"
    }
  ],
  "next_steps": [
    "1. Run bolta.voice.bootstrap to create your brand voice",
    "2. After voice setup, install content plane skills",
    "3. Create your first post with bolta.draft.post"
  ]
}
```

### Example 2: Managed Mode (Typical Production)
```json
{
  "workspace_id": "660e8400-e29b-41d4-a716-446655440001",
  "safe_mode": true,
  "autonomy_mode": "managed",
  "role": "admin",
  "principal_type": "user",
  "voice_profile_status": {
    "exists": true,
    "version": 5,
    "status": "active"
  },
  "quota_status": {
    "daily_posts": {"used": 18, "limit": 50, "percentage": 36},
    "hourly_api_requests": {"used": 142, "limit": 1000, "percentage": 14.2}
  },
  "recommended_mode": "managed",
  "recommended_skills": [
    "bolta.draft.post",
    "bolta.loop.from_template",
    "bolta.week.plan",
    "bolta.content.repurpose",
    "bolta.inbox.triage",
    "bolta.review.digest",
    "bolta.review.approve_and_route",
    "bolta.voice.validate",
    "bolta.voice.evolve",
    "bolta.cron.generate_to_review",
    "bolta.team.create_agent_teammate",
    "bolta.audit.export_activity",
    "bolta.quota.status"
  ],
  "excluded_skills": [
    {
      "skill": "bolta.cron.generate_and_schedule",
      "reason": "Requires autonomy_mode=autopilot AND safe_mode=OFF"
    }
  ],
  "warnings": [],
  "next_steps": [
    "Configure daily content generation via bolta.cron.generate_to_review",
    "Set up review workflow with digest notifications",
    "Consider voice evolution (version 5 is mature)"
  ]
}
```

### Example 3: Autopilot Mode (High Volume)
```json
{
  "workspace_id": "770e8400-e29b-41d4-a716-446655440002",
  "safe_mode": false,
  "autonomy_mode": "autopilot",
  "role": "owner",
  "principal_type": "user",
  "voice_profile_status": {
    "exists": true,
    "version": 12,
    "status": "active"
  },
  "quota_status": {
    "daily_posts": {"used": 47, "limit": 200, "percentage": 23.5},
    "hourly_api_requests": {"used": 523, "limit": 2000, "percentage": 26.15}
  },
  "recommended_mode": "autopilot",
  "recommended_skills": [
    "bolta.draft.post",
    "bolta.loop.from_template",
    "bolta.week.plan",
    "bolta.content.repurpose",
    "bolta.content.thread_builder",
    "bolta.inbox.triage",
    "bolta.review.digest",
    "bolta.review.approve_and_route",
    "bolta.voice.validate",
    "bolta.voice.evolve",
    "bolta.cron.generate_to_review",
    "bolta.cron.generate_and_schedule",
    "bolta.auto.respond_to_trending",
    "bolta.auto.content_gap_fill",
    "bolta.recurring.from_template",
    "bolta.quota.status",
    "bolta.workspace.config"
  ],
  "excluded_skills": [],
  "warnings": [
    {
      "type": "high_autonomy",
      "message": "Autopilot mode bypasses human review. Monitor quota usage and validate voice compliance regularly.",
      "severity": "medium"
    },
    {
      "type": "quota_usage",
      "message": "Daily quota at 23.5% usage. Consider monitoring trends to avoid hitting limit.",
      "severity": "low"
    }
  ],
  "next_steps": [
    "Monitor quota usage daily via bolta.quota.status",
    "Run voice validation spot-checks (10% of published posts)",
    "Review JobRun stats weekly for error trends"
  ]
}
```

### Example 4: Agent Principal (API Key)
```json
{
  "workspace_id": "880e8400-e29b-41d4-a716-446655440003",
  "safe_mode": true,
  "autonomy_mode": "managed",
  "role": "creator",
  "principal_type": "agent",
  "agent": {
    "id": "agent-uuid",
    "name": "Content Bot",
    "permissions": ["posts:write", "posts:read", "templates:read"],
    "autonomy_override": null
  },
  "voice_profile_status": {
    "exists": true,
    "version": 7,
    "status": "active"
  },
  "quota_status": {
    "daily_posts": {"used": 8, "limit": 30, "percentage": 26.67},
    "hourly_api_requests": {"used": 67, "limit": 500, "percentage": 13.4}
  },
  "recommended_mode": "managed",
  "recommended_skills": [
    "bolta.draft.post",
    "bolta.loop.from_template"
  ],
  "excluded_skills": [
    {
      "skill": "bolta.week.plan",
      "reason": "Requires posts:schedule permission (agent lacks this)"
    },
    {
      "skill": "bolta.review.approve_and_route",
      "reason": "Requires posts:approve permission (agent lacks this)"
    },
    {
      "skill": "bolta.voice.evolve",
      "reason": "Requires voice:write permission (agent lacks this)"
    },
    {
      "skill": "bolta.workspace.config",
      "reason": "Requires workspace:admin permission (agent role: creator)"
    }
  ],
  "warnings": [
    {
      "type": "limited_permissions",
      "message": "Agent has limited permissions. Some skills are unavailable.",
      "severity": "info"
    }
  ],
  "next_steps": [
    "Use bolta.draft.post to create content",
    "Use bolta.loop.from_template for batch generation",
    "Human reviewers should use bolta.review.approve_and_route to publish"
  ]
}
```

### Example 5: Quota Limit Reached
```json
{
  "workspace_id": "990e8400-e29b-41d4-a716-446655440004",
  "safe_mode": true,
  "autonomy_mode": "managed",
  "role": "editor",
  "principal_type": "user",
  "voice_profile_status": {
    "exists": true,
    "version": 4,
    "status": "active"
  },
  "quota_status": {
    "daily_posts": {"used": 100, "limit": 100, "percentage": 100},
    "hourly_api_requests": {"used": 234, "limit": 1000, "percentage": 23.4}
  },
  "recommended_mode": "managed",
  "recommended_skills": [
    "bolta.inbox.triage",
    "bolta.review.digest",
    "bolta.review.approve_and_route",
    "bolta.voice.validate",
    "bolta.quota.status",
    "bolta.policy.explain"
  ],
  "excluded_skills": [
    {
      "skill": "bolta.draft.post",
      "reason": "Daily quota limit reached (100/100 posts)"
    },
    {
      "skill": "bolta.loop.from_template",
      "reason": "Daily quota limit reached (100/100 posts)"
    },
    {
      "skill": "bolta.week.plan",
      "reason": "Daily quota limit reached (100/100 posts)"
    }
  ],
  "warnings": [
    {
      "type": "quota_exceeded",
      "message": "Daily post quota limit reached. No new posts can be created until tomorrow (resets at UTC midnight).",
      "severity": "high"
    }
  ],
  "next_steps": [
    "Review and approve existing posts in queue",
    "Consider increasing daily quota via bolta.workspace.config (admin only)",
    "Check quota status at midnight UTC for reset"
  ]
}
```

### Example 6: Incompatible Configuration (Autopilot + Safe Mode)
```json
{
  "workspace_id": "aa0e8400-e29b-41d4-a716-446655440005",
  "safe_mode": true,
  "autonomy_mode": "autopilot",
  "role": "owner",
  "principal_type": "user",
  "voice_profile_status": {
    "exists": true,
    "version": 8,
    "status": "active"
  },
  "quota_status": {
    "daily_posts": {"used": 5, "limit": 150, "percentage": 3.33},
    "hourly_api_requests": {"used": 12, "limit": 1500, "percentage": 0.8}
  },
  "recommended_mode": "ERROR",
  "recommended_skills": [],
  "excluded_skills": [
    {
      "skill": "ALL",
      "reason": "Incompatible configuration: autopilot mode requires Safe Mode OFF"
    }
  ],
  "warnings": [
    {
      "type": "configuration_conflict",
      "message": "Autopilot mode is incompatible with Safe Mode ON. Autopilot bypasses human review, which contradicts Safe Mode's intent.",
      "severity": "critical"
    }
  ],
  "next_steps": [
    "Choose one of the following:",
    "  A) Disable Safe Mode to use autopilot (workspace.config)",
    "  B) Switch to 'managed' autonomy mode to keep Safe Mode ON",
    "Current config blocks all agent operations until resolved."
  ],
  "error": {
    "code": "INCOMPATIBLE_CONFIGURATION",
    "message": "Autopilot autonomy mode requires Safe Mode to be OFF. Please update workspace configuration."
  }
}
```

---

## Integration with Authorization System

The registry integrates with Bolta's authorization layer to ensure skill recommendations respect workspace policies.

### Authorization Flow Integration

**Step 1: Pre-flight Authorization Check**
Before recommending a skill, check if the principal is authorized:

```python
from users.authorization import authorize, PostAction

# Check if user can create posts
auth_result = authorize(
    principal_type="user",
    role="editor",
    workspace=workspace,
    action=PostAction.CREATE,
    requested_status="Scheduled",
    agent=None  # or agent instance if principal is agent
)

if not auth_result.allowed:
    # Exclude skill with reason
    excluded_skills.append({
        "skill": "bolta.week.plan",
        "reason": auth_result.reason
    })
```

**Step 2: Respect Autonomy Mode Routing**
Skills that create posts must account for autonomy mode routing:

```python
# Autonomy mode routing table
AUTONOMY_ROUTING = {
    "assisted": {
        "Draft": "Draft",           # Always Draft
        "Scheduled": "Draft",       # Routed to Draft
        "Posted": "Draft"           # Routed to Draft
    },
    "managed": {
        "Draft": "Draft",
        "Scheduled": "Pending Approval",  # Routed to review
        "Posted": "Pending Approval"      # Routed to review
    },
    "autopilot": {
        "Draft": "Draft",
        "Scheduled": "Scheduled",    # No routing (requires Safe Mode OFF)
        "Posted": "Posted"           # No routing (requires Safe Mode OFF)
    },
    "governance": {
        "Draft": "Pending Approval",
        "Scheduled": "Pending Approval",
        "Posted": "Pending Approval"
    }
}

# Skills should document expected output status after routing
```

**Step 3: Quota Enforcement**
Skills that create posts must respect quota limits:

```python
from posts.quota_enforcement import QuotaEnforcer

# Check quota before recommending bulk operations
allowed, reason = QuotaEnforcer.check_daily_post_quota(
    workspace=workspace,
    count=10  # e.g., bolta.loop.from_template with count=10
)

if not allowed:
    excluded_skills.append({
        "skill": "bolta.loop.from_template",
        "reason": reason  # e.g., "Daily quota exceeded (95/100)"
    })
```

**Step 4: Safe Mode Compatibility**
Some skills are incompatible with Safe Mode:

```python
SAFE_MODE_INCOMPATIBLE = [
    "bolta.cron.generate_and_schedule",  # Bypasses review
]

if workspace.safe_mode and skill in SAFE_MODE_INCOMPATIBLE:
    excluded_skills.append({
        "skill": skill,
        "reason": "Incompatible with Safe Mode ON (requires human review bypass)"
    })
```

---

## Skill Metadata Schema

Each skill should provide structured metadata for registry indexing:

```yaml
skill:
  slug: bolta.draft.post
  display_name: Draft Post
  version: 1.2.0
  plane: content

permissions:
  required:
    - posts:write
  optional:
    - voice:read  # For voice profile selection

compatibility:
  safe_mode: compatible  # compatible | incompatible | n/a
  autonomy_modes:
    - assisted
    - managed
    - autopilot
  roles:
    - owner
    - admin
    - editor
    - creator

quotas:
  posts_created: 1  # Impact on daily quota
  api_requests: 2   # Typical API call count

dependencies:
  required:
    - voice_profile  # Must have voice profile
  optional:
    - templates      # Enhanced with templates

execution:
  typical_duration_seconds: 45
  max_duration_seconds: 120
  idempotent: true
  retryable: true

outputs:
  post_status: Draft  # Before autonomy routing
  job_tracked: true   # Creates JobRun record
  audit_logged: true  # Creates PostActivity record
```

---

## Version History

**0.4.0** (Current)
- Added comprehensive skill descriptions with metadata
- Added detailed decision matrix and authorization integration
- Added 6 output examples covering all scenarios
- Added quota enforcement and compatibility checks
- Added voice plane skills (validate, evolve)
- Added automation plane skills (trending, gap-fill)
- Added control plane skills (quota, workspace config)
- Added skill metadata schema

**0.3.0**
- Added recommended install sets (assisted, managed, autopilot, governance)
- Added plane groupings (voice, content, review, automation, control)
- Added registry flow documentation
- Added basic output example

**0.2.0**
- Added initial skill index
- Added plane definitions

**0.1.0**
- Initial registry structure

---


## Support

For skill installation issues, contact: support@bolta.ai
