# Autonomy Modes: Understanding Agent Behavior Levels

**Complete guide to Bolta's autonomy system - from fully assisted to autopilot.**

---

## Overview

Autonomy modes control **how much decision-making power your agent has** when creating and scheduling content.

Think of it as a **dial** you can turn up or down:
- **Low autonomy** (Assisted) - Agent creates drafts, human decides everything
- **Medium autonomy** (Managed) - Agent creates + routes to review, human approves
- **High autonomy** (Autopilot) - Agent creates + schedules directly, human monitors

Each mode has different **routing behavior** and **permission requirements**.

---

## The Four Autonomy Modes

### 1. Assisted Mode

**Tagline:** "Agent creates, you decide."

**Behavior:**
- Agent creates posts in **Draft status only**
- **All** requested actions (schedule, publish) → Draft
- Human must manually review and schedule each post

**Use Cases:**
- Learning Bolta for the first time
- Testing new voice profiles
- High-stakes brands (legal, medical, financial)
- Paranoid mode (maximum human control)

**Routing Table:**

| Requested Action | Final Status |
|-----------------|--------------|
| `draft_only` | Draft |
| `send_to_review` | Draft |
| `schedule` | **Draft** (downgraded) |
| `publish` | **Draft** (downgraded) |

**Example Workflow:**
```
1. Agent creates 10 posts → All in Draft
2. Human reviews each post manually
3. Human schedules approved posts individually
```

**Pros:**
- ✅ Maximum control
- ✅ Zero risk of unwanted publishing
- ✅ Learn agent behavior safely

**Cons:**
- ❌ High manual effort
- ❌ Slow scaling
- ❌ Defeats automation benefits

**When to Use:**
- First 1-2 weeks with Bolta
- Testing new voice profiles
- Compliance-heavy industries

---

### 2. Managed Mode (Recommended)

**Tagline:** "Agent generates, human approves."

**Behavior:**
- Agent creates posts
- **Scheduled posts** → Pending Approval (if Safe Mode ON)
- **Scheduled posts** → Scheduled directly (if Safe Mode OFF)
- Human reviews queue and bulk approves

**Use Cases:**
- Production content workflows
- Teams with 1-2 reviewers
- Brands publishing 5-20 posts/day
- **Default recommended mode**

**Routing Table:**

| Requested Action | Safe Mode ON | Safe Mode OFF |
|-----------------|--------------|---------------|
| `draft_only` | Draft | Draft |
| `send_to_review` | Pending Approval | Pending Approval |
| `schedule` | **Pending Approval** | Scheduled |
| `publish` | **Pending Approval** | Published |

**Example Workflow:**
```
1. Agent creates 20 posts overnight → Pending Approval
2. Daily digest email arrives at 9am
3. Human triages inbox (10 min review)
4. Bulk approve 18 posts, edit 2
5. Posts auto-schedule to calendar
```

**Pros:**
- ✅ Balanced autonomy + oversight
- ✅ Efficient bulk review workflow
- ✅ Safe Mode compatible
- ✅ Scales to high volume

**Cons:**
- ❌ Requires daily human review
- ❌ Bottleneck if reviewer unavailable

**When to Use:**
- After learning Bolta (week 2+)
- Production workflows
- When you trust your voice profile
- Teams with dedicated reviewers

---

### 3. Autopilot Mode

**Tagline:** "Agent runs autonomously, human monitors."

**Behavior:**
- Agent creates + schedules posts **without human approval**
- **Bypasses Pending Approval queue**
- Human reviews **after publishing** (spot checks)
- **Requires Safe Mode OFF**

**Use Cases:**
- High-volume content (10+ posts/day)
- Mature voice profiles (version 5+)
- Trusted agents with proven track record
- Low-risk content (tips, quotes, links)

**Routing Table:**

| Requested Action | Final Status |
|-----------------|--------------|
| `draft_only` | Draft |
| `send_to_review` | Pending Approval |
| `schedule` | **Scheduled** (directly) |
| `publish` | **Published** (directly) |

**CRITICAL Requirements:**
- ⚠️ Safe Mode **MUST be OFF** (incompatible)
- ⚠️ Voice profile version >= 5 recommended
- ⚠️ Quotas **MUST be configured**
- ⚠️ Audit logging **MUST be monitored**

**Example Workflow:**
```
1. Cron job runs daily at 6am
2. Agent generates 15 posts → Scheduled directly
3. Posts publish throughout the day
4. Human reviews analytics weekly
5. Voice profile adjusted based on performance
```

**Pros:**
- ✅ True automation (no daily review)
- ✅ Scales to 50+ posts/day
- ✅ Minimal human intervention

**Cons:**
- ❌ No human approval before publish
- ❌ Risk of off-brand content
- ❌ Requires mature voice profile
- ❌ Incompatible with Safe Mode

**When to Use:**
- After 3+ months with Bolta
- Voice profile refined (v5+)
- Proven agent performance
- Non-critical content

**Safety Measures:**
```yaml
Required safeguards for Autopilot:
- Quota: max_posts_per_day <= 20 (start conservative)
- Voice validation: Run bolta.voice.validate weekly
- Spot checks: Review 10% of published posts
- Analytics: Monitor engagement metrics
- Rollback plan: Switch to "managed" if quality drops
```

---

### 4. Governance Mode

**Tagline:** "Control plane for admins."

**Behavior:**
- **This is NOT an autonomy level for content creation**
- It's an **admin-focused install set**
- All content requests → Pending Approval (maximum oversight)

**Use Cases:**
- Workspace administrators
- Compliance officers
- Security teams
- Audit/governance roles

**Skills Included:**
- `bolta.policy.explain` - Authorization troubleshooting
- `bolta.audit.export_activity` - Compliance exports
- `bolta.team.create_agent_teammate` - Agent provisioning
- `bolta.team.rotate_key` - Security operations
- `bolta.workspace.config` - Workspace administration
- `bolta.quota.status` - Usage monitoring

**Example Workflow:**
```
1. Monthly: Export audit logs for compliance
2. Weekly: Review quota usage
3. Quarterly: Rotate API keys
4. As needed: Investigate authorization failures
5. As needed: Onboard new agents/team members
```

---

## Choosing the Right Mode

### Decision Tree

```
START
  ↓
New to Bolta?
  YES → Use "Assisted" for 1-2 weeks
  NO → Continue
  ↓
Do you have a mature voice profile (v3+)?
  NO → Use "Assisted" until voice is refined
  YES → Continue
  ↓
How many posts per day?
  1-5 → Use "Managed" (efficient review workflow)
  6-20 → Use "Managed" (scales well with bulk approve)
  20+ → Consider "Autopilot" (if voice proven)
  ↓
Are you comfortable with agent publishing directly?
  NO → Use "Managed" (human approval required)
  YES → Use "Autopilot" (set quotas first!)
  ↓
Do you need Safe Mode ON?
  YES → Use "Managed" (Autopilot incompatible with Safe Mode)
  NO → Use "Autopilot" (if all other criteria met)
```

### Recommended Adoption Path

**Month 1: Assisted Mode**
```
Goal: Learn the system, build voice profile
- Create voice profile
- Generate 20-30 draft posts
- Manually review and schedule
- Refine voice based on feedback
→ Graduate to Managed when voice v3+ reached
```

**Month 2-3: Managed Mode**
```
Goal: Scale content production with oversight
- Set up daily digest workflow
- Use bulk approve workflow
- Generate 50-100 posts total
- Monitor voice compliance
→ Graduate to Autopilot when voice v5+ and proven performance
```

**Month 4+: Autopilot Mode (Optional)**
```
Goal: Autonomous high-volume content
- Set conservative quotas (max 20 posts/day)
- Monitor analytics weekly
- Spot-check 10% of posts
- Adjust voice profile as needed
→ Stay in Autopilot or return to Managed if quality issues
```

---

## Autonomy Mode Routing Matrix

### Combined with Safe Mode

| Autonomy Mode | Safe Mode | Schedule Request → | Publish Request → |
|---------------|-----------|-------------------|-------------------|
| **Assisted** | ON | Draft | Draft |
| **Assisted** | OFF | Draft | Draft |
| **Managed** | ON | Pending Approval | Pending Approval |
| **Managed** | OFF | Scheduled | Published |
| **Autopilot** | ON | **ERROR** (incompatible) | **ERROR** |
| **Autopilot** | OFF | Scheduled | Published |
| **Governance** | ON | Pending Approval | Pending Approval |
| **Governance** | OFF | Pending Approval | Pending Approval |

### Key Insights

1. **Assisted** always routes to Draft (regardless of Safe Mode)
2. **Managed** respects Safe Mode (ON → review, OFF → direct)
3. **Autopilot** requires Safe Mode OFF (else error)
4. **Governance** always routes to review (maximum oversight)

---

## Configuring Autonomy Mode

### Via Web UI (Admin Only)

1. Go to **bolta.ai/settings/workspace**
2. Find "Autonomy Mode" section
3. Select mode from dropdown:
   - Assisted
   - Managed (recommended)
   - Autopilot
   - Governance
4. Click "Save Changes"

### Via API

```bash
curl -X PATCH https://platty.boltathread.com/v1/workspaces/${BOLTA_WORKSPACE_ID} \
  -H "Authorization: Bearer ${BOLTA_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "autonomy_mode": "managed"
  }'
```

### Via Skill

```
Can you change my workspace to managed autonomy mode?
```

Agent runs `bolta.workspace.config` and updates the setting.

---

## Agent-Level Autonomy Overrides

**Individual agents can override the workspace default.**

### Use Cases

- **Conservative agent** in Autopilot workspace → Override to "managed"
- **Experimental agent** in Managed workspace → Override to "assisted"
- **Admin agent** → Override to "governance" (control-plane only)

### Configuration

```bash
# Set agent override via API
curl -X PATCH https://platty.boltathread.com/v1/agents/${AGENT_ID} \
  -H "Authorization: Bearer ${BOLTA_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "autonomy_override": "managed"
  }'
```

### Precedence Rules

```python
effective_autonomy_mode = agent.autonomy_override ?? workspace.autonomy_mode

# Examples:
# Agent override: "assisted", Workspace: "autopilot" → Uses "assisted"
# Agent override: null, Workspace: "managed" → Uses "managed"
```

---

## Safety Guardrails by Mode

### All Modes

- ✅ Role-based permissions enforced
- ✅ Quota limits respected
- ✅ Audit logging for all actions
- ✅ API key scoped to workspace

### Assisted Mode

- ✅ No automatic scheduling (zero risk)
- ✅ Every post reviewed by human

### Managed Mode

- ✅ Safe Mode routing (if enabled)
- ✅ Bulk review workflow
- ✅ Daily digest notifications

### Autopilot Mode

- ⚠️ **Required safeguards:**
  - Quota: `max_posts_per_day` configured
  - Voice: Validation score monitoring
  - Monitoring: Weekly analytics review
  - Fallback: Circuit breaker if quota hit

---

## Common Mistakes

### Mistake 1: Skipping Assisted Mode

**Problem:** Jumping directly to Autopilot without learning the system

**Result:** Off-brand content, wasted posts, voice drift

**Solution:** Start with Assisted, graduate through Managed

---

### Mistake 2: Autopilot + Safe Mode ON

**Problem:** Enabling Autopilot while Safe Mode is ON

**Result:** All operations fail with "Incompatible configuration" error

**Solution:**
```
Choose one:
A) Disable Safe Mode (requires admin)
B) Switch to "managed" mode (keeps Safe Mode protection)
```

---

### Mistake 3: No Quotas in Autopilot

**Problem:** Running Autopilot without daily/hourly quotas

**Result:** Runaway agent creates 1000s of posts

**Solution:**
```bash
# Set conservative quotas BEFORE enabling Autopilot
curl -X PATCH https://platty.boltathread.com/v1/workspaces/${WORKSPACE_ID} \
  -d '{"max_posts_per_day": 20, "max_api_requests_per_hour": 500}'
```

---

### Mistake 4: Immature Voice in Autopilot

**Problem:** Using Autopilot with voice profile v1-2

**Result:** Inconsistent, off-brand content

**Solution:**
- Refine voice to v5+ before Autopilot
- Use `bolta.voice.validate` to score quality
- Run `bolta.voice.evolve` on approved posts

---

## Monitoring & Analytics

### Key Metrics by Mode

**Assisted Mode:**
- Posts created (should be low volume)
- Time spent reviewing (hours/week)
- Posts scheduled vs abandoned

**Managed Mode:**
- Posts in review queue (trending over time)
- Approval rate (target: >85%)
- Review→schedule lag (target: <24h)

**Autopilot Mode:**
- Posts published/day (vs quota limit)
- Voice validation score (target: >80)
- Engagement metrics (likes, shares, clicks)
- Error rate (posts that failed)

### Dashboards

```
Use bolta.quota.status to monitor:
- Daily post usage (X/100)
- Hourly API usage (X/1000)
- Approaching limit warnings
```

---

## Version History

**v1.0** - Initial autonomy modes documentation
- Assisted, Managed, Autopilot, Governance
- Routing tables
- Safety guardrails

---

## See Also

- [safe-mode.md](./safe-mode.md) - Understanding Safe Mode
- [quotas.md](./quotas.md) - Quota enforcement
- [voice-versioning.md](./voice-versioning.md) - Voice profile evolution

---

## Need Help?

**Choosing the right mode?**
- Start with **Managed** (best balance)
- Move to Assisted if too autonomous
- Move to Autopilot after proven performance

**Questions:**
- GitHub: [github.com/boltaai/bolta-skills/issues](https://github.com/boltaai/bolta-skills/issues)
- Email: support@bolta.ai
