# Quota Enforcement: Preventing Runaway Agents

**Complete guide to Bolta's quota system - the safety net that prevents resource abuse.**

---

## What are Quotas?

**Quotas are workspace-level limits that cap how many posts/requests an agent can make.**

Two types of quotas:
1. **Daily Post Limit** - Maximum posts created per day (UTC midnight reset)
2. **Hourly API Limit** - Maximum API requests per hour (rolling window)

**Purpose:** Prevent runaway agents from creating thousands of posts or overwhelming the API.

---

## Default Quotas

```yaml
Default limits (if not overridden):
  max_posts_per_day: 100 posts
  max_api_requests_per_hour: 1000 requests
```

**These apply to ALL workspaces unless explicitly overridden.**

---

## How Quotas Work

### Daily Post Quota

**Enforcement Point:** Before post creation

```python
# Check quota before creating
allowed, reason = QuotaEnforcer.check_daily_post_quota(workspace, count=1)

if not allowed:
    return HTTP 429 Too Many Requests
    {
      "error": "Daily post quota exceeded",
      "limit": 100,
      "used": 100,
      "remaining": 0,
      "reset_at": "2024-03-16T00:00:00Z"
    }

# Create post
post = create_post(...)

# Increment quota AFTER success
QuotaEnforcer.increment_daily_post_count(workspace, count=1)
```

**Reset:** UTC midnight daily

**Tracking:** WorkspaceDailyQuota table (one record per workspace per day)

---

### Hourly API Quota

**Enforcement Point:** On API request

```python
# Check quota on incoming request
allowed, reason = QuotaEnforcer.check_hourly_api_quota(workspace)

if not allowed:
    return HTTP 429 Too Many Requests

# Process request
process_request(...)

# Increment quota
QuotaEnforcer.increment_api_request_count(workspace)
```

**Reset:** Rolling 1-hour window (cache-based)

**Tracking:** Redis cache with 1-hour TTL

---

## Viewing Quota Usage

### Via Skill

```
What's my current quota usage?
```

Agent runs `bolta.quota.status` and returns:

```json
{
  "daily_posts": {
    "limit": 100,
    "used": 47,
    "remaining": 53,
    "percentage": 47.0
  },
  "hourly_api_requests": {
    "limit": 1000,
    "used": 234,
    "remaining": 766,
    "percentage": 23.4
  },
  "date": "2024-03-15"
}
```

### Via API

```bash
curl https://platty.boltathread.com/v1/workspaces/${BOLTA_WORKSPACE_ID}/quota-status \
  -H "Authorization: Bearer ${BOLTA_API_KEY}"
```

### Via Web UI

Dashboard shows quota usage meters:
```
Daily Posts:    ████████░░ 47/100 (47%)
Hourly API:     ██░░░░░░░░ 234/1000 (23%)
```

---

## Configuring Custom Quotas

### Via Web UI (Admin Only)

1. Go to **bolta.ai/settings/workspace**
2. Find "Quota Limits" section
3. Set custom values:
   ```
   Max Posts Per Day: [  100  ]  (default: 100)
   Max API Requests Per Hour: [ 1000  ]  (default: 1000)
   ```
4. Click "Save Changes"

### Via API

```bash
curl -X PATCH https://platty.boltathread.com/v1/workspaces/${BOLTA_WORKSPACE_ID} \
  -H "Authorization: Bearer ${BOLTA_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "max_posts_per_day": 200,
    "max_api_requests_per_hour": 2000
  }'
```

### Via Skill

```
Increase my daily post limit to 200
```

Agent runs `bolta.workspace.config` skill.

---

## Recommended Quotas by Use Case

### Learning / Testing
```yaml
max_posts_per_day: 20
max_api_requests_per_hour: 200
```
**Why:** Small enough to prevent accidents, large enough to test

### Production (Low Volume)
```yaml
max_posts_per_day: 50
max_api_requests_per_hour: 500
```
**Why:** 5-10 posts/day with buffer

### Production (Medium Volume)
```yaml
max_posts_per_day: 100
max_api_requests_per_hour: 1000
```
**Why:** 10-20 posts/day (default setting)

### Production (High Volume)
```yaml
max_posts_per_day: 200
max_api_requests_per_hour: 2000
```
**Why:** 20-50 posts/day for high-frequency brands

### Enterprise / Autopilot
```yaml
max_posts_per_day: 500
max_api_requests_per_hour: 5000
```
**Why:** Multiple agents, automated workflows

---

## Quota Exceeded Behavior

### What Happens When Quota Hit

**429 Response:**
```json
{
  "error": {
    "code": "QUOTA_EXCEEDED",
    "message": "Daily post quota exceeded. Limit: 100 posts/day, Current usage: 100, Remaining: 0",
    "quota_type": "daily_posts",
    "limit": 100,
    "used": 100,
    "remaining": 0,
    "reset_at": "2024-03-16T00:00:00Z",
    "retry_after": "2024-03-16T00:00:00Z"
  }
}
```

**Agent Behavior:**
- Stop creating posts
- Log the quota error
- Wait for reset (or notify human)

**Human Notification:**
- Email alert sent
- Dashboard shows quota exceeded warning
- Skill returns quota status

---

## Quota Monitoring & Alerts

### Warning Thresholds

**80% Warning:**
```json
{
  "warning": "Approaching daily quota limit: 85/100 posts created today"
}
```

**90% Critical:**
```json
{
  "warning": "Critical: 95/100 posts created today. Quota will be exceeded soon."
}
```

**100% Exceeded:**
```json
{
  "error": "Daily post quota exceeded. No more posts can be created until midnight UTC."
}
```

### Email Alerts

**Configure notifications:**

```yaml
Quota alerts:
  - 80% threshold: Warning email to admins
  - 90% threshold: Critical alert to all members
  - 100% exceeded: Immediate notification + block

Frequency: Real-time (triggered on quota check)
```

---

## Best Practices

### 1. Start Conservative

**Recommendation:** Use default (100/day) or lower (50/day) when starting

**Why:**
- Learn agent behavior
- Prevent accidental overuse
- Catch runaway scripts early

**Increase gradually:**
```
Week 1: 50/day  → Monitor usage patterns
Week 2: 100/day → If consistently hitting 50
Month 2: 200/day → If proven need for higher volume
```

---

### 2. Monitor Quota Trends

**Weekly review:**
```bash
# Export quota usage logs
curl https://platty.boltathread.com/v1/workspaces/${WORKSPACE_ID}/quota-history?days=30
```

**Look for:**
- Spikes (unusual activity)
- Trends (increasing usage over time)
- Patterns (daily vs weekly cycles)

**Adjust quotas based on:**
- Actual usage (if hitting limit regularly → increase)
- Business needs (seasonal campaigns → temporary increase)
- Agent trust (mature agents → higher limits)

---

### 3. Use Quotas as Circuit Breakers

**Quotas are NOT just limits** - they're safety mechanisms.

**Example: Runaway Agent**
```
Without quotas:
Agent bug → Creates 10,000 posts → $10,000 in API costs + brand damage

With quotas (100/day):
Agent bug → Creates 100 posts → Quota exceeded → Agent stops
            → Human notified → Bug fixed → $100 in costs
```

**Set quotas to prevent worst-case scenarios.**

---

### 4. Different Quotas for Different Agents

**Feature (coming soon):** Per-agent quota overrides

```yaml
# Workspace default
max_posts_per_day: 100

# High-trust agent override
agent_production:
  max_posts_per_day: 200  # Double workspace limit

# Low-trust agent override
agent_experimental:
  max_posts_per_day: 20   # Conservative limit
```

Currently: Quotas apply workspace-wide (all agents share the same pool)

---

## Quota Bypass (Admin Emergency)

**Scenario:** Urgent campaign, need to exceed quota

**Options:**

**Option 1: Temporarily Increase Quota**
```bash
# Increase to 500 for today
curl -X PATCH .../workspaces/${WORKSPACE_ID} \
  -d '{"max_posts_per_day": 500}'

# Reset to 100 tomorrow
```

**Option 2: Manual Quota Reset**
```bash
# Admin-only: Reset today's quota count to 0
curl -X POST .../workspaces/${WORKSPACE_ID}/quota-reset \
  -H "Authorization: Bearer ${ADMIN_API_KEY}"

# USE WITH CAUTION: This bypasses safety mechanism
```

**Option 3: Create Posts via Different Workspace**
```
# Multi-workspace architecture
# Each workspace has separate quotas
```

---

## Troubleshooting

### Issue: "Quota Exceeded but Usage Looks Low"

**Symptom:** API returns 429 but quota status shows 50/100

**Causes:**
1. **Multiple agents** sharing the same quota pool
2. **Pending posts** counted but not visible
3. **Cache desync** (rare)

**Solutions:**
```bash
# Check actual database count
curl .../workspaces/${WORKSPACE_ID}/quota-status?source=database

# Check all agents' activity
curl .../workspaces/${WORKSPACE_ID}/audit-log?action_category=create&date=today
```

---

### Issue: "Quota Never Resets"

**Symptom:** Still blocked after midnight UTC

**Cause:** Timezone confusion (local midnight ≠ UTC midnight)

**Solution:**
```
Quota resets at:
UTC 00:00 = 7pm EST (previous day)
UTC 00:00 = 4pm PST (previous day)
UTC 00:00 = 12am GMT
UTC 00:00 = 8am SGT (next day)

Check current UTC time:
date -u
```

---

### Issue: "Need Higher Quotas"

**Symptom:** Consistently hitting daily limit

**Diagnosis:**
```bash
# Check usage trends
curl .../quota-history?days=30

# If usage > 80% of limit for 7+ consecutive days:
# → Increase limit
```

**Process:**
1. Document business justification
2. Request admin to increase quota
3. Admin updates via workspace config
4. Monitor for 1 week to verify new limit is adequate

---

## Enterprise Quota Management

### Multi-Workspace Strategy

**Large organizations:**

```yaml
Workspace: Marketing (high volume)
  max_posts_per_day: 500
  max_api_requests_per_hour: 5000

Workspace: Support (medium volume)
  max_posts_per_day: 100
  max_api_requests_per_hour: 1000

Workspace: Experimental (low volume, high risk)
  max_posts_per_day: 20
  max_api_requests_per_hour: 200
```

**Each workspace has independent quotas.**

---

### Cost Control

**Quotas as budget control:**

```
Assumption: $0.10 per post (AI generation cost)

Quota: 100 posts/day
Max daily cost: $10/day
Max monthly cost: $300/month

If budget is $500/month:
Safe quota = 166 posts/day
```

**Set quotas to prevent budget overruns.**

---

## Version History

**v1.0** - Initial quota documentation
- Daily and hourly quotas
- Enforcement behavior
- Best practices
- Troubleshooting

---

## See Also

- [safe-mode.md](./safe-mode.md) - Safe Mode enforcement
- [autonomy-modes.md](./autonomy-modes.md) - Autonomy levels
- [getting-started.md](./getting-started.md) - Quickstart guide

---

## Need Help?

**Quota questions:**
- Default limits too restrictive? Contact support@bolta.ai
- Need enterprise quotas? Email sales@bolta.ai
- GitHub: [github.com/boltaai/bolta-skills/issues](https://github.com/boltaai/bolta-skills/issues)
