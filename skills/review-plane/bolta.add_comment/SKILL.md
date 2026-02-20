---
name: bolta.add_comment
version: 2.0.0
description: Add a review comment to a draft without approving or rejecting - used for suggestions, questions, or notes
category: review
roles_allowed: [Viewer, Creator, Editor, Admin]
agent_types: [reviewer, custom]
safe_defaults: {}
tools_required: []
inputs_schema:
  type: object
  required: [post_id, comment]
  properties:
    post_id: { type: string, description: "Draft post UUID" }
    comment: { type: string, description: "Comment text" }
    comment_type: { type: string, enum: [suggestion, question, note, praise], default: note }
outputs_schema:
  type: object
  properties:
    success: { type: boolean }
    comment_id: { type: string }
    message: { type: string }
organization: bolta.ai
author: Bolta Team
---

## Goal
Add a review comment to a draft without approving or rejecting it. Used for suggestions, questions, or notes during review process.

## Which Agents Use This
- **reviewer** — Add suggestions before approval, ask questions, note observations
- **custom** — Any agent participating in review process
- Humans can also add comments during review

## Hard Rules
1. MUST attach comment to post
2. SHOULD specify comment_type for context (suggestion, question, note, praise)
3. SHOULD be specific and actionable
4. Comments don't change post status (still in review)

## Steps

### 1. Validate input
- Verify post_id exists
- Verify comment is non-empty
- Validate comment_type if provided

### 2. Create comment
- Attach comment to post
- Record comment_type
- Record author (agent or human)
- Timestamp comment

### 3. Return confirmation
- Return comment_id and success message

## Output
```json
{
  "success": true,
  "comment_id": "uuid",
  "message": "Comment added to post."
}
```

## Failure Handling
- If post_id not found: return error "Post not found"
- If comment empty: return error "Comment text required"

## Example Usage

### Scenario 1: Reviewer adding suggestion
```json
{
  "post_id": "uuid",
  "comment": "Consider changing 'utilize' to 'use' (voice profile prefers simpler words)",
  "comment_type": "suggestion"
}
```
**Result:** Comment added to draft for creator to review

### Scenario 2: Reviewer asking question
```json
{
  "post_id": "uuid",
  "comment": "Is this stat current? I see different numbers in our latest report.",
  "comment_type": "question"
}
```
**Result:** Question flagged for creator or human to answer before approval
