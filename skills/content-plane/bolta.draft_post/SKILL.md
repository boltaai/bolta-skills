# bolta.draft_post

**Version:** 2.0.0  
**Category:** Content Creation  
**Agent Types:** `content_creator`, `custom`  
**Roles Allowed:** All (creates drafts for review)

---

## Purpose

Create a draft post for review using the workspace's voice profile. The draft is sent to the Inbox for human approval before publishing.

This is the **primary content creation tool** for all content_creator agents.

---

## When An Agent Uses This

**Content Creator reasoning:**
- "I've gathered context (voice profile, recent posts, business DNA)"
- "I've decided on the content approach (educational vs. promotional, format, hook)"
- "Now I'll draft the post and send it for review"

**Job execution flow:**
1. Job fires with brief: "Create 3 LinkedIn posts about remote work"
2. Agent calls `get_voice_profile()` to load tone/style
3. Agent calls `list_recent_posts()` to avoid repetition
4. Agent calls `get_business_context()` for product info
5. Agent drafts content
6. Agent calls `draft_post()` to create draft in Inbox
7. Human reviews and approves

---

## What This Does

1. Creates Post object with `status="Draft"`
2. Links voice_profile_id for tone reference
3. Links account_ids for platform targeting
4. Adds notes_for_reviewer (agent's reasoning)
5. Routes to Inbox for human review

---

## Parameters

```json
{
  "content": "string (required)",      // Post content (text, with formatting)
  "platform": "string (required)",     // twitter, linkedin, instagram, etc.
  "voice_profile_id": "string (UUID)", // Voice profile to apply
  "account_id": "string (UUID, required)",  // Social account to post from
  "notes": "string (optional)"         // Notes for human reviewer
}
```

### Schema (Claude Messages API format)

```json
{
  "name": "bolta.draft_post",
  "description": "Create a draft post for review. The draft will be sent to the Inbox for human approval before publishing. Use the voice_profile_id to match the brand's tone and style.",
  "input_schema": {
    "type": "object",
    "properties": {
      "content": {
        "type": "string",
        "description": "The post content (text, with formatting if needed)"
      },
      "platform": {
        "type": "string",
        "description": "Target platform (twitter, linkedin, instagram, etc.)"
      },
      "voice_profile_id": {
        "type": "string",
        "description": "Voice profile UUID to apply"
      },
      "account_id": {
        "type": "string",
        "description": "Social account UUID to post from"
      },
      "notes": {
        "type": "string",
        "description": "Optional notes for human reviewer"
      }
    },
    "required": ["content", "platform", "account_id"]
  }
}
```

---

## Returns

```json
{
  "success": true,
  "draft_id": "uuid",
  "message": "Draft created successfully. Post ID: abc-123",
  "status": "Draft",
  "review_url": "/inbox?post_id=abc-123"
}
```

---

## Hard Rules

**MUST:**
- Create post with `status="Draft"` (never published directly)
- Link to voice_profile_id if provided
- Link to account_id (validates account belongs to workspace)
- Mark as `is_ai_generated=True` and `post_creator="agent"`
- Route to Inbox for human review

**MUST NOT:**
- Publish directly (even if role=editor, Safe Mode enforced)
- Skip voice_profile_id for content_creator agents
- Create post without account_id
- Bypass Inbox review (humans must approve)

**SHOULD:**
- Include agent reasoning in `notes_for_reviewer`
- Reference what the agent considered (recent posts, voice profile, etc.)
- Explain any creative choices made

---

## Example Agent Usage

**Context:** Content Creator executing job "Create LinkedIn post about remote work"

```
Agent reasoning:
1. I need voice profile to match tone → call get_voice_profile()
2. I should check recent posts to avoid repetition → call list_recent_posts()
3. I should understand the business → call get_business_context()
4. Now I'll draft content matching voice profile
5. Educational performs better (from memory) → use how-to format
6. Create draft → call draft_post()

Tool call:
draft_post(
  content="🏠 5 remote work mistakes I made (so you don't have to):\n\n1. No boundaries...",
  platform="linkedin",
  account_id="550e8400-e29b-41d4-a716-446655440000",
  voice_profile_id="284de8cd-6344-4c8c-8c4d-6da61b97e807",
  notes="Educational format (performs 3x better per memory). Used numbered list (high engagement on LinkedIn). Hook: personal story (builds trust). Matches voice: direct, specific, no jargon."
)

Returns:
{
  "success": true,
  "draft_id": "660e8400-e29b-41d4-a716-446655440001",
  "status": "Draft",
  "review_url": "/inbox?post_id=660e8400-e29b-41d4-a716-446655440001"
}

Agent completes:
"Task completed. Draft created with ID 660e8400-e29b-41d4-a716-446655440001. 
Ready for review in Inbox."
```

---

## Integration with Other Skills

**Before draft_post:**
- `bolta.get_voice_profile` — Load tone, style, dos/donts
- `bolta.list_recent_posts` — Check recent content to avoid repetition
- `bolta.get_business_context` — Load products, audience, positioning
- `bolta.get_account_info` — Validate account details
- `bolta.recall` — Retrieve agent memory (best practices learned)

**After draft_post:**
- `bolta.approve_post` — Reviewer agent or human approves
- `bolta.reject_post` — Reviewer agent or human rejects with feedback
- `bolta.schedule_post` — If approved, schedule for publishing

---

## Voice Profile Application

The voice_profile_id is used to:
- Match tone (playful vs. professional, direct vs. diplomatic)
- Follow dos/donts (e.g., "Lead with benefits" / "No corporate jargon")
- Apply platform-specific adaptations
- Use brand vocabulary and avoid forbidden phrases
- Match content size preference (short/standard/long)

**Agent's responsibility:** Read the voice profile, internalize it, apply it to content.

---

## State Flow

```
Draft Created (this skill)
  ↓
Inbox (awaits human/reviewer agent)
  ↓
Approved (human or reviewer agent)
  ↓
Scheduled (if schedule_time set)
  ↓
Published (by scheduler or manual publish)
```

**Safe Mode enforcement:**
- Even if agent role=editor, draft MUST go to Inbox first
- Only explicit human action or reviewer agent approval moves it forward
- This prevents accidental auto-posting

---

## Error Handling

**Common errors:**

1. **Account not found:**
```json
{
  "success": false,
  "error": "Account abc-123 not found in workspace xyz-789"
}
```

2. **Voice profile missing (for content_creator):**
```json
{
  "success": false,
  "error": "Voice profile is required for content_creator agents"
}
```

3. **Invalid platform:**
```json
{
  "success": false,
  "error": "Platform 'myspace' not supported. Use: twitter, linkedin, instagram"
}
```

---

## Metrics to Track

- **Draft creation rate** — How many drafts per agent per day
- **Approval rate** — % of drafts approved without changes
- **Revision rate** — % requiring human edits before approval
- **Voice consistency score** — How well drafts match voice profile

---

## Notes

- This is the **most-used skill** by content_creator agents
- Quality depends on context provided (voice profile, recent posts, memory)
- The better the system prompt + context, the better the draft
- Agent reasoning in `notes` helps humans understand choices made
- Voice profile is **canonical reference** — agents must match it exactly
