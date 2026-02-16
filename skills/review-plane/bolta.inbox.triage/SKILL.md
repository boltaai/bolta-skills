---
name: bolta.inbox.triage
version: 1.0.0
description: Review Inbox items or drafts, cluster them, propose edits/actions, and optionally create improved draft variants for human review.
category: creator
roles_allowed: [Owner, Admin, Creator, Viewer]
safe_defaults:
  never_approve: true
  never_publish: true
tools_required:
  - bolta.get_workspace_policy
  - bolta.get_my_capabilities
  - bolta.list_inbox_items
  - bolta.update_post
  - bolta.create_post
  - bolta.submit_for_review
inputs_schema:
  type: object
  required: [workspace_id]
  properties:
    workspace_id: { type: string }
    status_filter: { type: string, enum: [pending_review, draft, scheduled] }
    limit: { type: number, default: 20 }
    create_variants: { type: boolean, default: true }
outputs_schema:
  type: object
  properties:
    clusters: { type: array, items: { type: object } }
    suggested_actions: { type: array, items: { type: object } }
    created_variant_post_ids: { type: array, items: { type: string } }
---

## Goal
Make the inbox easier: cluster + risk flag + actionable suggestions.

## Rules
- Viewers can only produce a report (no updates, no variants).
- Creators can create variants but cannot approve/schedule/publish.

## Steps
1. Fetch policy + capabilities.
2. List inbox items: `bolta.list_inbox_items({workspace_id, status: status_filter, limit})`
3. Cluster by:
   - topic similarity
   - CTA type
   - product mention vs general content
4. For each item:
   - Flag risks: overly salesy, claims, tone mismatch, too long, unclear CTA.
   - Recommend action: approve (if admin), edit, rewrite, discard, split thread.
5. If create_variants == true AND capability includes `posts:create`:
   - Create 1 improved variant per high-value item via `bolta.create_post(...)` referencing original_id in metadata.
6. If Safe Mode ON, optionally bundle variants into review via `bolta.submit_for_review(...)`.

## Output
Return clusters, suggested_actions, created_variant_post_ids.
