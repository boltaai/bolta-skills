---
name: bolta.inbox.triage
version: 2.0.0
description: V2 Reviewer agent skill - Cluster inbox items, flag risks, propose edits, optionally create improved variants. Makes the inbox manageable.
category: reviewer
roles_allowed: [Viewer, Creator, Editor, Admin]
agent_types: [reviewer, custom]
safe_defaults:
  never_approve: true
  never_publish: true
  read_only_for_viewers: true
tools_required:
  - bolta.get_workspace_policy
  - bolta.get_my_capabilities
  - bolta.list_inbox_items
  - bolta.get_inbox_item
  - bolta.get_voice_profile
  - bolta.update_post
  - bolta.draft_post
  - bolta.add_comment
  - bolta.remember
  - bolta.recall
inputs_schema:
  type: object
  required: [workspace_id]
  properties:
    workspace_id: { type: string }
    agent_id: { type: string, description: "V2 - Reviewer agent executing this skill" }
    status_filter: { type: string, enum: [inbox, draft, approved], default: "inbox" }
    limit: { type: number, default: 20 }
    create_variants: { type: boolean, default: false, description: "Create improved draft variants for flagged items" }
    client_tag: { type: string, description: "V2 - Filter by client tag (agency feature)" }
outputs_schema:
  type: object
  properties:
    clusters: { type: array, items: { type: object } }
    risk_flags: { type: array, items: { type: object } }
    suggested_actions: { type: array, items: { type: object } }
    created_variant_post_ids: { type: array, items: { type: string } }
    triage_summary: { type: string }
organization: bolta.ai
author: Max Fritzhand
---

## Goal
Make the inbox manageable: cluster related content, flag quality/risk issues, propose specific actions, and optionally create improved variants.

## V2 Changes
- **Reviewer agent context** — this is the primary skill for `reviewer` agent type
- **State machine updated** — `inbox` (replaces "pending_review"), `approved`, `scheduled`, `published`
- **Agent memory integration** — recalls review patterns, common issues, voice alignment rules
- **Client tag filtering** — agencies can triage by client
- **@mention context** — if called via @mention on inbox page, scopes to visible items

## When This Skill Is Called
- **Manual trigger** — User clicks "Triage Inbox" button in Bolta web
- **Scheduled job** — Reviewer agent runs daily/weekly triage
- **@mention** — User @mentions reviewer agent: "@QABot review the inbox"
- **Event trigger** — When inbox count > threshold (future enhancement)

## Policy Rules
1. **Viewers can only produce a read-only report** (no updates, no variants, no comments)
2. **Creators can create variants and add comments** but cannot approve/schedule/publish
3. **Editor/Admin can add comments and create variants** (approval is separate skill)
4. **Never approve or schedule posts** — this skill is purely advisory (use `bolta.review.approve_and_route` for that)

## Steps

1. **Check policy & capabilities:**
   - `bolta.get_workspace_policy(workspace_id)` → extract `safe_mode` (informational)
   - `bolta.get_my_capabilities(workspace_id)` → verify what agent can do
   - If role is Viewer: `create_variants = false` (force read-only)

2. **Load agent memory for context:**
   - If `agent_id` provided:
     - `bolta.recall(agent_id, "common_quality_issues")` → prioritize known problems
     - `bolta.recall(agent_id, "voice_alignment_rules")` → check consistency
     - `bolta.recall(agent_id, "approval_patterns")` → learn what gets approved
     - `bolta.recall(agent_id, "rejection_patterns")` → learn what gets rejected

3. **Fetch inbox items:**
   - `bolta.list_inbox_items({workspace_id, status: status_filter, limit})`
   - If `client_tag` provided: filter results by client_tag (agency feature)
   - For each item, also fetch full details:
     - `bolta.get_inbox_item(inbox_item_id)` → post content, metadata, creator agent, etc.

4. **Cluster items by similarity:**
   - Group by:
     - **Topic similarity** — same product/feature/theme
     - **CTA type** — engagement (like/comment), conversion (click link), educational (no CTA)
     - **Format** — thread starter, single post, carousel, poll
     - **Creator agent** — group by which agent created them (for pattern detection)
     - **Client tag** — agency users see clusters per client
   
   - Output clusters as:
     ```json
     {
       "cluster_id": "topic-product-launch",
       "label": "Product Launch Posts",
       "item_count": 5,
       "inbox_item_ids": ["uuid1", "uuid2", ...],
       "common_theme": "New feature announcement"
     }
     ```

5. **Flag risks and quality issues:**
   - For each inbox item, check against voice profile + brand rules:
     
     **Risk categories:**
     - **Tone mismatch** — doesn't match voice profile tone (check against `bolta.get_voice_profile`)
     - **Overly salesy** — too promotional, not enough value (check CTA density)
     - **Unverified claims** — mentions stats/numbers without source
     - **Too long** — exceeds platform best practices (>280 chars for Twitter, >3000 for LinkedIn)
     - **Unclear CTA** — has CTA but it's vague or weak
     - **No CTA** — missing CTA when one is expected (based on post goal)
     - **Banned phrases** — uses words from voice profile banned list
     - **Repetition** — very similar to recently published post
     - **Platform mismatch** — content doesn't fit platform norms (thread on Instagram, carousel on Twitter, etc.)
   
   - Risk severity: `low | medium | high`
   - Output risk flags as:
     ```json
     {
       "inbox_item_id": "uuid",
       "risks": [
         {
           "category": "tone_mismatch",
           "severity": "medium",
           "detail": "Post feels corporate; voice profile specifies 'conversational and punchy'"
         },
         {
           "category": "overly_salesy",
           "severity": "high",
           "detail": "3 CTAs in 280 characters — too aggressive"
         }
       ]
     }
     ```

6. **Propose specific actions:**
   - For each inbox item, recommend ONE of:
     
     - **Approve as-is** — if quality high, voice aligned, no risks
     - **Edit [specific issue]** — e.g., "Edit: shorten hook from 2 sentences to 1"
     - **Rewrite [section]** — e.g., "Rewrite: make CTA more specific"
     - **Create variant** — if fixable, suggest improved version
     - **Reject [reason]** — if unfixable or off-brand
     - **Split into thread** — if too long, better as multi-part
     - **Combine with [item_id]** — if two items cover same topic
     - **Schedule for later** — if time-sensitive and too early
   
   - Output suggested actions as:
     ```json
     {
       "inbox_item_id": "uuid",
       "suggested_action": "edit",
       "action_detail": "Shorten hook from 2 sentences to 1. Remove second CTA. Change 'Check it out' to 'Try it free for 14 days'",
       "reasoning": "Post is 90% there — minor edits will make it great",
       "confidence": "high"
     }
     ```

7. **Create improved variants (if enabled):**
   - If `create_variants == true` AND agent has Creator+ role:
     - For items flagged with `medium` or `high` risks BUT are salvageable:
       - Load voice profile: `bolta.get_voice_profile(voice_profile_id)`
       - Generate improved version that fixes identified issues:
         - Fix tone mismatch
         - Remove banned phrases
         - Clarify CTA
         - Adjust length
         - Maintain original message/value prop
       - Create new draft: `bolta.draft_post({...original metadata, content: improved_version, status: "draft"})`
       - Link to original via metadata: `{original_inbox_item_id: "uuid"}`
       - Add comment on original: `bolta.add_comment(original_post_id, "I created an improved variant that fixes [issues]. See draft [variant_post_id].")`
       - Collect `variant_post_id`
   
   - Variants stay in `draft` state (don't auto-submit to inbox)
   - Human can compare original vs variant and choose

8. **Generate triage summary:**
   - High-level overview for human reviewer:
     ```
     Inbox Triage Summary:
     - 20 items reviewed
     - 3 clusters identified (Product Launch, Weekly Tips, Engagement Posts)
     - 5 items flagged high-risk (tone mismatch, overly salesy)
     - 8 items ready to approve
     - 4 items need minor edits
     - 3 items should be rejected
     - 2 improved variants created
     
     Recommended priority order:
     1. Review high-risk items first (ids: uuid1, uuid2, ...)
     2. Batch-approve the 8 ready items
     3. Compare variants for the 2 flagged posts
     ```

9. **Update agent memory:**
   - If `agent_id` provided:
     - `bolta.remember(agent_id, "last_triage_run", ISO_timestamp)`
     - `bolta.remember(agent_id, "common_quality_issues", issue_frequency_map)` → learn patterns
     - `bolta.remember(agent_id, "variant_success_rate", success_count / total_count)` → track if variants get approved

## Output
```json
{
  "clusters": [
    {
      "cluster_id": "topic-product-launch",
      "label": "Product Launch Posts",
      "item_count": 5,
      "inbox_item_ids": ["uuid1", "uuid2", "uuid3", "uuid4", "uuid5"]
    },
    ...
  ],
  "risk_flags": [
    {
      "inbox_item_id": "uuid1",
      "risks": [
        {
          "category": "tone_mismatch",
          "severity": "medium",
          "detail": "..."
        }
      ]
    },
    ...
  ],
  "suggested_actions": [
    {
      "inbox_item_id": "uuid1",
      "suggested_action": "edit",
      "action_detail": "Shorten hook...",
      "reasoning": "...",
      "confidence": "high"
    },
    ...
  ],
  "created_variant_post_ids": ["variant-uuid1", "variant-uuid2"],
  "triage_summary": "Inbox Triage Summary:\n- 20 items reviewed\n..."
}
```

## Failure Handling
- If inbox empty: return empty arrays + summary "Inbox is empty"
- If voice profile missing for an item: flag as risk, suggest re-linking voice
- If variant creation fails: add to warnings, continue with others
- If agent lacks permissions for variants: skip variant creation, return advisory-only output

## Agent Types That Use This Skill
- **reviewer** — Primary use case (inbox quality control)
- **custom** — User-defined agents with review capabilities

## Example Use Cases

**Scenario 1: Daily Inbox Triage Job**
- Reviewer agent runs daily at 8am
- Triages overnight content from creator agents
- Flags issues, proposes actions
- Human reviews summary over coffee, takes bulk actions

**Scenario 2: @Mention on Inbox Page**
- User opens inbox, sees 30 items, feels overwhelmed
- Types "@QABot review the inbox"
- QABot triages, returns summary with priority order
- User follows recommendations, clears inbox in 10 minutes

**Scenario 3: Agency Client Review**
- Agency has 15 clients, each with active content agents
- Reviewer agent runs triage filtered by `client_tag: "Acme Corp"`
- Returns Acme-specific triage summary
- Agency team member reviews only Acme content, approves/edits

**Scenario 4: Variant Creation Workflow**
- Creator agent generates 5 posts, 2 are flagged high-risk
- Reviewer agent creates improved variants for the 2
- Human sees: Original (flagged) vs Variant (improved)
- Approves variant, rejects original
- Reviewer agent learns: "This type of improvement works"
