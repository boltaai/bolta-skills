---
name: bolta-review-queue
description: >
  Work the Bolta review and approval queues. Use this skill when the user asks
  "what needs my review", "show the approval queue", "approve pending posts",
  "review my content", "what's waiting for approval", "clear my review queue",
  "anything to approve", "approve the agent drafts", or wants to triage, approve,
  reject, or push content into review. Handles BOTH queues: the standard review
  queue and the agent-produced recurring queue. Not for writing new content (use
  brand-voice-enforce) or reading analytics (use bolta-analytics-report).
---

# Bolta Review Queue

Triage and clear what's waiting for a human decision. **Prefer `list-inbox-items`** —
the unified inbox that returns everything pending review in one call (each item is
labeled with its `source`: `team`, `recurring`, or `hunter`). The two per-queue tools
remain available when you need one queue in isolation: the **standard review queue**
(`list-reviews`) and the **agent-produced recurring queue** (`list-recurring-reviews`).
Show what's waiting and act — approving or rejecting each item, with rejection reasons
that feed Bolta's voice learning.

## When to use
Any time the user wants to see, triage, or clear pending approvals — or to push their own
drafts into review for someone else to approve.

## Tools this skill uses
| Tool | Why |
|-|-|
| `list-workspaces` | Resolve `workspace_id` if unknown. |
| `list-inbox-items` | **Preferred**: unified inbox of everything pending (team + recurring + hunter), filterable by `source`/`status`. |
| `list-reviews` | Standard review queue only (posts routed to review). |
| `list-recurring-reviews` | Agent-produced pending drafts (the agent → human queue). |
| `get-post` | Optional — pull full detail for a queued item before deciding. |
| `approve-post` | Approve a standard-queue post (optionally schedule at approval). |
| `approve-recurring-review` | Approve an agent draft (optionally schedule at suggested time). |
| `reject-recurring-review` | Reject an agent draft with a reason (feeds voice learning). |
| `submit-for-review` | Push the user's own drafts into the review queue. |

## Prerequisites
- `workspace_id` — resolve once via `list-workspaces`, reuse for every call. Auth is automatic
  via the Bolta connector's OAuth grant — never ask for an API key. Default new content to
  Draft; confirm before publish/delete.
- Approving/rejecting requires **editor** or above. If a call returns a permission error,
  run `get-my-capabilities` and explain the missing role plainly rather than retrying.

## Workflow

### 1. Resolve the workspace
Call `list-workspaces` and use the active workspace's `id`. Never guess a UUID.

### 2. Pull the inbox
Prefer one call: `list-inbox-items(workspace_id)` — the unified inbox. Each item carries a
`source` (`team`, `recurring`, `hunter`); filter with `source`/`status` when asked for one
slice. Fall back to the per-queue tools only when you need queue-specific filters:
- `list-reviews(workspace_id)` — standard queue (`reviewer_id`, `workflow_type` filters).
- `list-recurring-reviews(workspace_id)` — agent drafts (`status`, `template_id` filters).
Present a single combined summary: how many from each source, and a one-line preview per item
(content snippet, target account/platform, and — for agent items — the suggested schedule
time). Make clear which source each item belongs to, since they approve through different tools.

### 3. Inspect (optional)
For any item the user wants to see in full before deciding, call `get-post(post_id)` for the
complete content, media, and target accounts. Do this when a snippet isn't enough to judge.

### 4. Act on each item
- **Standard-queue item** → `approve-post(workspace_id, post_id)`. Optionally pass
  `schedule_mode` / `fixed_time` to schedule it on approval, and `comments` for approver notes.
- **Agent (recurring) item, approve** → `approve-recurring-review(review_id)`. Pass
  `approveWithSchedule` + `useSuggestedTime` to schedule at the agent's suggested time, and
  `approvalComments` for notes.
- **Agent (recurring) item, reject** → `reject-recurring-review(review_id, rejectionReason)`.
  Always include a concrete reason — rejections and edits are what teach Bolta the brand's
  voice, so a specific reason ("too hypey", "wrong CTA") improves future drafts more than a
  bare reject.

Approving finalizes content toward publishing. Confirm the batch with the user before mass
approvals, and never publish outside these approve paths without an explicit ask.

### 5. Push drafts into review (when asked)
If the user wants their own drafts routed for someone else to approve, call
`submit-for-review(workspace_id, post_ids, note)` with the draft ids and an optional note.
This lands them in the standard queue.

### 6. Report
Summarize what was approved, scheduled, rejected (with reasons), and what remains in each
queue. Note that rejection reasons feed the voice-learning loop.

## Failure handling
- Empty queues → say both are clear; offer to push drafts in via `submit-for-review`.
- Permission error on approve/reject → run `get-my-capabilities`, report the missing role,
  do not retry.
- Wrong tool for the queue (e.g. `approve-post` on an agent item) errors — route standard
  items through `approve-post` and agent items through the `*-recurring-review` tools.
- `get-post` not found → the item may have been actioned elsewhere; re-pull the queues.

## Example
User: "What needs my review?"
1. `list-workspaces` → workspace_id.
2. `list-inbox-items(workspace_id)` → 2 team posts + 3 agent drafts (Hype Man, each with a
   suggested time), each labeled by `source`.
3. Present: "5 waiting — 2 in your review queue, 3 agent drafts. Approve all, or review each?"
4. User: "Approve the agent ones at their suggested times, reject the standard LinkedIn one —
   too salesy." →
   - `approve-recurring-review(review_id, approveWithSchedule=true, useSuggestedTime=true)` ×3.
   - `approve-post(workspace_id, post_id)` for the good standard post; for the LinkedIn one,
     it's an agent draft? No — standard, so it can only be approved or left. Confirm the user
     wants it rejected; agent-style rejection with a reason isn't available for standard posts,
     so leave it pending and note that.
5. Report: 3 agent drafts approved + scheduled, 1 standard approved, 1 held. Rejection reasons
   captured feed voice learning.
