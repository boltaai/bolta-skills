---
name: bolta.review.digest
version: 2.0.0
description: V2 - Generate a human-readable review summary (daily/weekly digest) of inbox activity, agent performance, and pending actions.
category: review
roles_allowed: [Viewer, Creator, Editor, Admin]
agent_types: [reviewer, analytics, custom]
tools_required:
  - bolta.get_workspace_policy
  - bolta.list_inbox_items
  - bolta.list_recent_posts
  - bolta.get_post_metrics
inputs_schema:
  type: object
  required: [workspace_id]
  properties:
    workspace_id: { type: string }
    agent_id: { type: string, description: "V2 - Agent generating digest" }
    period: { type: string, enum: [daily, weekly, monthly], default: "weekly" }
    client_tag: { type: string, description: "V2 - Filter by client (agency feature)" }
outputs_schema:
  type: object
  properties:
    summary_text: { type: string }
    stats: { type: object }
    top_performing_posts: { type: array, items: { type: object } }
    action_items: { type: array, items: { type: string } }
organization: bolta.ai
author: Max Fritzhand
---

## Goal
Produce a concise, actionable summary of review activity for human consumption.

## V2 Changes
- **Agent-aware:** References which agents created content, which approved it
- **State machine updated:** Uses V2 states (inbox, approved, scheduled, published)
- **Client tag filtering:** Agency users can get per-client digests
- **Performance metrics:** Includes engagement data if available

## Steps
1. **Fetch inbox items from period:**
   - `bolta.list_inbox_items({workspace_id, created_after: period_start, limit: 100})`
   - Filter by `client_tag` if provided

2. **Calculate stats:**
   - Total items in inbox during period
   - Items approved vs rejected vs still pending
   - Average time-to-approval
   - By agent: posts created, approval rate, average quality

3. **Identify top performers:**
   - `bolta.list_recent_posts({workspace_id, published_after: period_start, limit: 50})`
   - `bolta.get_post_metrics(post_id)` for each
   - Rank by engagement (likes, comments, shares)

4. **Generate action items:**
   - "X posts still awaiting review (oldest: Y days)"
   - "Agent Z has low approval rate (40%) - review persona"
   - "Client ABC has 5 posts ready to schedule"

5. **Format summary:**
   ```
   Weekly Review Digest (Feb 14-20, 2026)
   
   📊 Stats:
   - 45 posts created (by 3 agents)
   - 32 approved (71% approval rate)
   - 8 rejected (18%)
   - 5 still pending review
   
   🏆 Top Performers:
   1. "How we 10x'd engagement" - 234 likes, 45 comments
   2. "Founder story: Why we built this" - 189 likes, 32 shares
   
   🤖 Agent Performance:
   - HypeMan: 20 posts, 85% approval rate ⭐
   - ContentBot: 15 posts, 60% approval rate ⚠️
   - WeeklyPlanner: 10 posts, 100% approval rate 🎯
   
   ✅ Action Items:
   - 5 posts pending review (oldest: 3 days)
   - ContentBot needs persona review (approval rate dropped)
   - Client Acme Corp: 8 posts ready to schedule
   ```

## Output
Return `summary_text` (markdown formatted), `stats` (object), `top_performing_posts`, `action_items`.

## Agent Types That Use This Skill
- **reviewer** — Generate digest as part of weekly review job
- **analytics** — Broader reporting capabilities
- **custom** — User-defined agents with reporting enabled
