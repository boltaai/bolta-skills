---
name: bolta.review.digest
version: 1.0.0
description: Produce an admin-friendly digest of items awaiting review, with risk flags, suggested edits, and approval recommendations.
category: review
roles_allowed: [Owner, Admin]
tools_required:
  - bolta.get_workspace_policy
  - bolta.list_inbox_items
inputs_schema:
  type: object
  required: [workspace_id]
  properties:
    workspace_id: { type: string }
    limit: { type: number, default: 30 }
outputs_schema:
  type: object
  properties:
    ready_to_approve: { type: array, items: { type: object } }
    needs_edit: { type: array, items: { type: object } }
    high_risk: { type: array, items: { type: object } }
    summary: { type: string }
---

## Goal
Help Admins approve fast without reading every word deeply.

## Steps
1. Fetch policy.
2. List pending review items.
3. For each item, label:
   - Ready: clean voice, clear CTA, low risk
   - Needs edit: minor fixes
   - High risk: compliance/claims, tone mismatch, sensitive topics
4. Output a digest with short bullet suggestions per item.

## Output
Three lists + a short summary.
