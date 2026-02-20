---
name: bolta.reject_post
version: 2.0.0
description: Reject a draft post with specific feedback, sending it back for revision to enforce brand standards
category: review
roles_allowed: [Editor, Admin]
agent_types: [reviewer, custom]
safe_defaults:
  require_specific_feedback: true
tools_required:
  - bolta.update_post
  - bolta.add_comment
inputs_schema:
  type: object
  required: [draft_id, reason, suggestions]
  properties:
    draft_id: { type: string, description: "Draft post UUID to reject" }
    reason: { type: string, description: "WHY rejected (specific)" }
    suggestions: { type: string, description: "WHAT to fix (actionable)" }
    severity: { type: string, enum: [minor, major, blocking], default: major }
outputs_schema:
  type: object
  properties:
    success: { type: boolean }
    post_id: { type: string }
    status: { type: string, enum: [Rejected] }
    message: { type: string }
organization: bolta.ai
author: Bolta Team
---

## Goal
Reject a draft post with specific feedback, sending it back for revision. Reviewer agents use this to enforce brand standards and strategic fit.

## Which Agents Use This
- **reviewer** — Enforce voice profile compliance, brand guidelines, and content strategy
- **custom** — Any agent with review permissions
- Requires Editor or Admin role

## Hard Rules
1. MUST provide specific reason (not "needs improvement")
2. MUST provide actionable suggestions (WHAT to fix, not just WHY it's wrong)
3. MUST cite voice profile when applicable
4. SHOULD be constructive, not just critical
5. Severity levels help creators prioritize fixes

## Steps

### 1. Validate permissions
- Verify user/agent has Editor or Admin role
- Verify draft_id exists and is in reviewable state

### 2. Validate feedback quality
- Verify reason is specific (not vague)
- Verify suggestions are actionable
- If voice profile violation: cite specific rule

### 3. Reject post
- Update post status: Draft → Rejected
- Record rejector (agent_id or user_id)
- Add rejection reason and suggestions as comment
- Set severity level
- Timestamp rejection

### 4. Return confirmation
- Return post_id, new status, confirmation message

## Output
```json
{
  "success": true,
  "post_id": "uuid",
  "status": "Rejected",
  "message": "Post rejected. Feedback provided."
}
```

## Failure Handling
- If not Editor/Admin role: return error "Permission denied - Editor role required"
- If draft_id not found: return error "Draft not found"
- If reason/suggestions empty: return error "Specific feedback required"

## Example Usage

### Scenario 1: Voice profile violation
```json
{
  "draft_id": "uuid",
  "reason": "Uses 'leverage' which is forbidden in voice profile (avoid corporate jargon)",
  "suggestions": "Replace 'leverage our platform' with 'use our platform' or 'build with our tools'",
  "severity": "major"
}
```
**Result:** Post rejected with specific fix

### Scenario 2: Repetitive content
```json
{
  "draft_id": "uuid",
  "reason": "Posted about pricing yesterday - too repetitive",
  "suggestions": "Try educational content instead (how-to, case study, best practices). Refer to content calendar.",
  "severity": "minor"
}
```
**Result:** Post rejected with strategic guidance
