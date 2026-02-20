---
name: bolta.draft_post
version: 2.0.0
description: Create a draft post using workspace voice profile - routes to Inbox for review before publishing
category: content
roles_allowed: [Viewer, Creator, Editor, Admin]
agent_types: [content_creator, custom]
safe_defaults:
  never_publish_directly: true
  always_route_to_inbox: true
tools_required:
  - bolta.create_post
inputs_schema:
  type: object
  required: [content, platform, account_id]
  properties:
    content: { type: string, description: "Post content (text, with formatting)" }
    platform: { type: string, description: "Target platform (twitter, linkedin, instagram, etc.)" }
    voice_profile_id: { type: string, description: "Voice profile UUID to apply" }
    account_id: { type: string, description: "Social account UUID to post from" }
    notes: { type: string, description: "Optional notes for human reviewer" }
outputs_schema:
  type: object
  properties:
    success: { type: boolean }
    draft_id: { type: string }
    status: { type: string, enum: [Draft] }
    review_url: { type: string }
organization: bolta.ai
author: Bolta Team
---

## Goal
Create a draft post for review using the workspace's voice profile. The draft is sent to the Inbox for human approval before publishing. This is the **primary content creation tool** for all content_creator agents.

## Which Agents Use This
- **content_creator** — Primary use case for generating content drafts
- **custom** — Any agent with content creation enabled

## Hard Rules
1. MUST create post with status="Draft" (never published directly)
2. MUST link to voice_profile_id if provided
3. MUST link to account_id (validates account belongs to workspace)
4. MUST mark as is_ai_generated=True and post_creator="agent"
5. MUST route to Inbox for human review
6. MUST NOT publish directly (even if role=editor, Safe Mode enforced)
7. SHOULD include agent reasoning in notes_for_reviewer

## Steps

### 1. Validate input
- Verify account_id exists and belongs to workspace
- Verify voice_profile_id exists if provided
- Validate platform is supported

### 2. Create draft post
- Create Post object with status="Draft"
- Link voice_profile_id for tone reference
- Link account_id for platform targeting
- Add notes_for_reviewer (agent's reasoning)

### 3. Route to Inbox
- Post transitions to inbox state
- Awaits human or reviewer agent approval

### 4. Return confirmation
- Return draft_id, status, review_url

## Output
```json
{
  "success": true,
  "draft_id": "uuid",
  "message": "Draft created successfully. Post ID: abc-123",
  "status": "Draft",
  "review_url": "/inbox?post_id=abc-123"
}
```

## Failure Handling
- If account not found: return error "Account abc-123 not found in workspace"
- If voice_profile missing for content_creator: return error "Voice profile is required"
- If invalid platform: return error "Platform 'xyz' not supported"

## Example Usage

### Scenario: Content Creator executing job
**Job brief:** "Create LinkedIn post about remote work"

**Agent reasoning:**
1. Call get_voice_profile() → load tone/style
2. Call list_recent_posts() → check for repetition
3. Call get_business_context() → understand products
4. Draft content matching voice profile
5. Call draft_post()

**Tool call:**
```json
{
  "content": "🏠 5 remote work mistakes I made (so you don't have to):\n\n1. No boundaries...",
  "platform": "linkedin",
  "account_id": "uuid",
  "voice_profile_id": "uuid",
  "notes": "Educational format (performs 3x better per memory). Hook: personal story."
}
```
**Result:** Draft created, sent to Inbox for review
