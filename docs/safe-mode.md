# Safe Mode: Human-in-the-Loop Content Protection

**Complete guide to Bolta's Safe Mode - the safety net that prevents unwanted publishing.**

---

## What is Safe Mode?

**Safe Mode is a workspace-level setting that routes all scheduled/published posts through human review.**

Think of it as a **circuit breaker** between agent generation and live publishing:
- **Safe Mode ON** → All scheduled posts → Pending Approval (human must approve)
- **Safe Mode OFF** → Posts can be scheduled/published directly (based on permissions)

**Key Insight:** Safe Mode is **the primary safety mechanism** in Bolta. It ensures humans have final say before content goes live.

---

## How Safe Mode Works

### Routing Behavior

**With Safe Mode ON:**
```
Agent requests: "Schedule this post for 2pm tomorrow"
                    ↓
             Authorization Layer
                    ↓
        "Safe Mode ON detected"
                    ↓
      Route: Scheduled → Pending Approval
                    ↓
         Post enters review queue
                    ↓
    Human approves → Post scheduled
```

**With Safe Mode OFF:**
```
Agent requests: "Schedule this post for 2pm tomorrow"
                    ↓
             Authorization Layer
                    ↓
       "Safe Mode OFF, check permissions"
                    ↓
      Has posts:schedule permission?
         YES → Post scheduled directly
         NO → Permission denied error
```

### Status Flow

```
Draft
  ↓
[Agent requests schedule]
  ↓
Safe Mode ON?
  ├─ YES → Pending Approval → (Human approves) → Scheduled → Published
  └─ NO  → Scheduled (directly) → Published
```

---

## When to Use Safe Mode

### ✅ Use Safe Mode ON (Default, Recommended)

**Scenarios:**
- New to Bolta (learning phase)
- Testing new voice profiles
- High-stakes content (legal, medical, financial, PR)
- Brand reputation sensitive
- Compliance requirements (SOC2, GDPR, industry regulations)
- Multiple agents with varying trust levels
- Intern-level agents (untested, experimental)

**Benefits:**
- ✅ Zero risk of unwanted publishing
- ✅ Catch errors before they go live
- ✅ Build trust in agent-generated content
- ✅ Audit trail of approvals
- ✅ Learn agent behavior patterns

---

### ⚠️ Use Safe Mode OFF (Advanced)

**Scenarios:**
- Mature voice profiles (v5+)
- Trusted agents with proven track record
- High-volume low-risk content (daily tips, quotes)
- **Autopilot mode** (requires Safe Mode OFF)
- Non-critical content streams

**Requirements:**
```yaml
Before disabling Safe Mode:
- Voice profile version: >= 5
- Agent performance: >90% approval rate
- Quota limits: Configured (max 20 posts/day recommended)
- Monitoring: Analytics dashboard active
- Rollback plan: Can re-enable Safe Mode immediately
```

**Risks:**
- ❌ Posts publish without human review
- ❌ Off-brand content can go live
- ❌ Higher stakes if agent malfunctions
- ❌ Requires active monitoring

---

## Safe Mode + Autonomy Mode Matrix

| Autonomy Mode | Safe Mode ON | Safe Mode OFF |
|---------------|--------------|---------------|
| **Assisted** | Posts → Draft (no routing) | Posts → Draft (no routing) |
| **Managed** | Posts → Pending Approval | Posts → Scheduled (direct) |
| **Autopilot** | **ERROR** (incompatible) | Posts → Scheduled (direct) |
| **Governance** | Posts → Pending Approval | Posts → Pending Approval |

### Key Insights

1. **Assisted mode** ignores Safe Mode (always Draft anyway)
2. **Managed mode** respects Safe Mode (most common combination)
3. **Autopilot mode** is incompatible with Safe Mode ON
4. **Governance mode** always routes to review (even if Safe Mode OFF)

---

## Enabling/Disabling Safe Mode

### Via Web UI (Admin Only)

1. Go to **bolta.ai/settings/workspace**
2. Find "Safe Mode" toggle
3. Click to enable/disable
4. Confirm the change (modal warning if disabling)

**Warning shown when disabling:**
```
⚠️ Disabling Safe Mode

Posts will be scheduled/published without human approval.
Only disable if:
- Voice profile is mature (v5+)
- Agents are proven trustworthy
- Quotas are configured
- You have monitoring in place

Are you sure you want to continue?
[Cancel]  [Yes, Disable Safe Mode]
```

### Via API

```bash
# Enable Safe Mode
curl -X PATCH https://platty.boltathread.com/v1/workspaces/${BOLTA_WORKSPACE_ID} \
  -H "Authorization: Bearer ${BOLTA_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "safe_mode": true
  }'

# Disable Safe Mode (admin only)
curl -X PATCH https://platty.boltathread.com/v1/workspaces/${BOLTA_WORKSPACE_ID} \
  -H "Authorization: Bearer ${BOLTA_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "safe_mode": false
  }'
```

### Via Skill

```
Can you enable Safe Mode for my workspace?
```

Agent runs `bolta.workspace.config` skill to toggle the setting.

---

## The Pending Approval Queue

### What Happens in Pending Approval

When Safe Mode routes a post:

1. **Post status** → `Pending Approval`
2. **TeamPostReview record** created with:
   - Content preview
   - Scheduled time (if provided)
   - Platform info
   - Notes for reviewer
   - Post creator (agent or user)

3. **Notifications sent** (if configured):
   - Email digest (daily summary)
   - Slack alert (immediate)
   - Dashboard badge count

4. **Human reviews** via:
   - Web UI: bolta.ai/inbox
   - Skill: `bolta.inbox.triage`
   - API: `GET /v1/workspaces/{id}/reviews`

5. **Reviewer actions:**
   - Approve → Post scheduled
   - Edit → Post updated, stays in queue
   - Reject → Post → Draft with feedback

### Bulk Review Workflow

**For high-volume workspaces:**

```
Morning routine (10-15 minutes):

1. Check daily digest email
   → "12 posts awaiting review"

2. Use bolta.inbox.triage to organize:
   → Group by topic, platform, urgency

3. Bulk approve with bolta.review.approve_and_route:
   → Select 10 posts
   → Click "Approve & Schedule"
   → Posts auto-schedule to calendar

4. Edit 2 posts that need tweaks:
   → Make edits
   → Re-submit for review (or schedule directly)

Total time: 10-15 min for 12 posts
```

---

## Safe Mode Enforcement

### Server-Side Enforcement

**Critical:** Safe Mode is enforced server-side, not client-side.

```python
# Server authorization logic (simplified)
def authorize_post_creation(workspace, requested_status):
    if workspace.safe_mode and requested_status in ['Scheduled', 'Published']:
        # Route to Pending Approval
        return AuthResult(
            allowed=True,
            routed_status='Pending Approval',
            safe_mode_enforced=True,
            reason="Safe Mode ON: scheduled posts require approval"
        )

    return AuthResult(allowed=True, routed_status=requested_status)
```

**Agents cannot bypass Safe Mode:**
- ❌ Cannot disable Safe Mode themselves (requires admin)
- ❌ Cannot publish directly (even with `posts:publish` permission)
- ❌ Cannot override routing (server enforces)

### Audit Trail

Every Safe Mode routing is logged:

```json
{
  "action": "created",
  "post_id": "...",
  "requested_status": "Scheduled",
  "final_status": "Pending Approval",
  "safe_mode_enforced": true,
  "policy_context": {
    "safe_mode": true,
    "autonomy_mode": "managed",
    "role": "creator"
  },
  "principal_type": "agent",
  "timestamp": "2024-03-15T10:00:00Z"
}
```

Use `bolta.audit.export_activity` to export full audit logs.

---

## Common Scenarios

### Scenario 1: Learning Bolta (Week 1)

**Config:**
- Safe Mode: ON
- Autonomy Mode: assisted

**Behavior:**
```
Agent creates post → Draft
Human schedules manually → Scheduled
```

**Why this works:**
- Assisted mode keeps everything in Draft
- Safe Mode doesn't matter (nothing requests scheduling)
- Human has full control

---

### Scenario 2: Production Workflow (Month 2)

**Config:**
- Safe Mode: ON
- Autonomy Mode: managed

**Behavior:**
```
Agent creates 20 posts → Pending Approval
Daily digest sent to reviewer
Human bulk approves 18, edits 2
Approved posts → Scheduled
```

**Why this works:**
- Managed mode requests scheduling
- Safe Mode routes to review
- Human approves in bulk (efficient)

---

### Scenario 3: High-Volume Automation (Month 4+)

**Config:**
- Safe Mode: OFF
- Autonomy Mode: autopilot
- Quotas: max_posts_per_day = 20

**Behavior:**
```
Cron job runs daily → 15 posts created
Agent schedules directly → Scheduled (no review)
Posts publish throughout day
Human reviews analytics weekly
```

**Why this works:**
- Autopilot mode requires Safe Mode OFF
- Agent trusted after 3+ months
- Quotas prevent runaway generation
- Weekly spot-checks catch issues

---

## Troubleshooting

### Issue: "Posts Always Go to Review"

**Symptom:** Every scheduled post → Pending Approval

**Cause:** Safe Mode ON

**Solutions:**
1. **If intended:** This is correct behavior
2. **If not intended:**
   - Check: `GET /v1/workspaces/{id}` → `safe_mode: true`
   - Disable Safe Mode (requires admin)
   - OR: Keep Safe Mode ON and use bulk approve workflow

---

### Issue: "Cannot Enable Autopilot"

**Symptom:** Error when setting autonomy_mode to "autopilot"

**Cause:** Safe Mode ON (incompatible)

**Solution:**
```
Choose one:
A) Disable Safe Mode (bolta.workspace.config)
B) Keep Safe Mode ON and use "managed" mode
```

---

### Issue: "Agent Published Without Approval"

**Symptom:** Post went live without human review

**Diagnosis:**
1. Check workspace config: `safe_mode: false`
2. Check audit log: `was_denied: false`, `safe_mode_enforced: false`
3. Check autonomy mode: likely "autopilot" or "managed" with Safe Mode OFF

**Prevention:**
- Enable Safe Mode
- OR: Use "governance" autonomy mode (always routes to review)
- OR: Set agent.autonomy_override = "assisted"

---

## Best Practices

### 1. Start with Safe Mode ON

**Recommendation:** Enable Safe Mode for first 1-3 months

**Why:**
- Learn agent behavior patterns
- Catch voice drift early
- Build trust in generated content
- Prevent costly mistakes

---

### 2. Gradual Transition

**Phase 1 (Month 1):** Safe Mode ON + Assisted
```
Goal: Learn the system
Review: Every post manually
```

**Phase 2 (Month 2-3):** Safe Mode ON + Managed
```
Goal: Scale production
Review: Bulk approve workflow
```

**Phase 3 (Month 4+):** Safe Mode OFF + Autopilot (optional)
```
Goal: Autonomous operation
Review: Weekly analytics + spot checks
```

---

### 3. Use Per-Agent Overrides

**For mixed-trust environments:**

```python
# High-trust agent → Allow direct scheduling
agent_trusted.autonomy_override = None  # Use workspace default (autopilot)

# Low-trust agent → Force review
agent_experimental.autonomy_override = "governance"  # Always review

# Workspace: Safe Mode OFF, Autopilot
# Result:
# - Trusted agent schedules directly
# - Experimental agent routes to review
```

---

### 4. Configure Alerts

**If disabling Safe Mode:**

```yaml
Required monitoring:
- Quota warnings: Email when 80% of daily limit reached
- Daily digest: Summary of published posts
- Weekly analytics: Engagement metrics review
- Voice validation: Weekly compliance scoring
```

---

## Compliance & Security

### SOC2 / GDPR Requirements

**If you need compliance certification:**

**Recommendation:** Keep Safe Mode ON permanently

**Why:**
- Audit trail of human approvals
- Demonstrate human oversight
- Prevent unauthorized publishing
- Clear accountability chain

**Alternative:** Use Safe Mode OFF + detailed audit logging + weekly reviews

---

### Security Considerations

**Safe Mode as Defense-in-Depth:**

```
Layer 1: Role-Based Access Control (RBAC)
  → Permissions limit what agents can request

Layer 2: Safe Mode
  → Routes scheduled posts to human review

Layer 3: Quota Enforcement
  → Limits total volume (even if approved)

Layer 4: Audit Logging
  → Full traceability of all actions

Layer 5: Voice Validation
  → Quality scoring catches off-brand content
```

Safe Mode is **Layer 2** - critical for production safety.

---

## Migration Guide: Disabling Safe Mode

**If you're ready to disable Safe Mode:**

### Pre-Flight Checklist

- [ ] Voice profile version >= 5
- [ ] Agent approval rate > 90% (last 100 posts)
- [ ] Voice validation scores > 80 (last 50 posts)
- [ ] Quotas configured (max 20 posts/day recommended)
- [ ] Monitoring dashboards active
- [ ] Team aligned on the change
- [ ] Rollback plan documented
- [ ] Weekly review scheduled

### Step-by-Step Migration

**Week 1: Preparation**
```
1. Export audit logs (last 3 months)
2. Calculate approval rate
3. Run voice validation on recent posts
4. Set conservative quotas
```

**Week 2: Pilot**
```
1. Create test agent with Safe Mode OFF override
2. Run for 1 week
3. Monitor all published posts
4. Measure quality vs control group
```

**Week 3: Rollout**
```
1. If pilot successful: Disable Safe Mode workspace-wide
2. Announce change to team
3. Monitor closely for 2 weeks
4. Be ready to re-enable if issues arise
```

**Week 4+: Monitoring**
```
1. Weekly analytics review
2. Monthly voice validation scoring
3. Quarterly audit log export
4. Adjust quotas based on performance
```

---

## Version History

**v1.0** - Initial Safe Mode documentation
- Core concepts
- Routing behavior
- Best practices
- Migration guide

---

## See Also

- [autonomy-modes.md](./autonomy-modes.md) - Understanding autonomy levels
- [quotas.md](./quotas.md) - Quota enforcement
- [getting-started.md](./getting-started.md) - Quickstart guide

---

## Need Help?

**Questions about Safe Mode?**
- GitHub: [github.com/boltaai/bolta-skills/issues](https://github.com/boltaai/bolta-skills/issues)
- Email: support@bolta.ai

**Default Recommendation:** Keep Safe Mode ON until you have proven agent performance.
