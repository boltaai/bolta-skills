---
name: bolta-review-queue
description: >
  Work the Bolta review and approval queues. Use this skill when the user asks
  "what needs my review", "show the approval queue", "approve pending posts",
  "review my content", "what's waiting for approval", "clear my review queue",
  "anything to approve", "approve the agent drafts", "any replies to send", "send
  that reply", or wants to triage, approve, reject, edit-and-send, or push content
  into review. Handles ALL inbox sources: the standard review queue, the
  agent-produced recurring queue, hunter reply drafts (edit + send), and agent
  reports. This skill is the standing inbox — triage whatever is already waiting.
  To trigger an agent run and then review its output in one loop, use
  bolta-agent-run-and-review. Not for writing new content (use bolta-draft-post)
  or reading analytics (use bolta-analytics-report).
---

# Bolta Review Queue

Triage and clear what's waiting for a human decision. **Prefer `list-inbox-items`** —
the unified inbox that returns everything pending review in one call (each item is
labeled with its `source`: `team`, `recurring`, `hunter`, or `report`). Hunter rows
carry the mention/lead context they respond to and are fully actionable here —
edit the draft (`update-hunter-reply`) and send it (`send-hunter-reply`). Report rows
carry the agent report and its download link. Pass `agent_id` to scope the inbox to
one agent's output. The two per-queue tools remain available when you need one queue
in isolation: the **standard review queue** (`list-reviews`) and the **agent-produced
recurring queue** (`list-recurring-reviews`). Show what's waiting and act — approving,
rejecting, or sending each item, with rejection reasons that feed Bolta's voice
learning.

## When to use
Any time the user wants to see, triage, or clear pending approvals — or to push their own
drafts into review for someone else to approve. If the user wants to *trigger an agent run
first* and then review what it produced, use bolta-agent-run-and-review instead — this skill
works the queue as it stands.

## Tools this skill uses
| Tool | Why |
|-|-|
| `list-workspaces` | Resolve `workspace_id` if unknown. |
| `list-inbox-items` | **Preferred**: unified inbox of everything pending (team + recurring + hunter + report), filterable by `source`/`status`, scopable to one agent via `agent_id`. |
| `list-reviews` | Review queue — **defaults to BOTH workflows** (team + recurring). Pass `workflow_type="team"` for the standard queue in isolation. |
| `list-recurring-reviews` | Agent-produced pending drafts (the agent → human queue); scope to one agent via `agent_creator_id`. |
| `get-post` | Optional — pull full detail for a queued item before deciding. |
| `approve-post` | Approve a standard-queue post (optionally schedule at approval). Echo the row's `content_fingerprint` as `expected_fingerprint`. |
| `approve-recurring-review` | Approve an agent draft (optionally schedule at suggested time). |
| `reject-recurring-review` | Reject an agent draft with a reason (feeds voice learning). |
| `update-hunter-reply` | Edit a hunter reply draft without sending it (already-sent replies 409). |
| `send-hunter-reply` | Approve + send a hunter reply; optional `content` overrides the draft in the same call. Double-send prevented server-side. |
| `submit-for-review` | Push the user's own drafts into the review queue. |

## Prerequisites
- `workspace_id` — resolve once via `list-workspaces`, reuse for every call. Auth is automatic
  via the Bolta connector's OAuth grant — never ask for an API key. Default new content to
  Draft; confirm before publish/delete.
- Approving/rejecting requires an **owner/admin/creator** role (viewers are read-only;
  workspace roles are owner/admin/creator/viewer). If a call returns a permission error,
  run `get-my-capabilities` and explain the missing role plainly rather than retrying.

## Workflow

### 1. Resolve the workspace
Call `list-workspaces` and use the active workspace's `id`. Never guess a UUID.

### 2. Pull the inbox
Prefer one call: `list-inbox-items(workspace_id)` — the unified inbox. Each item carries a
`source` (`team`, `recurring`, `hunter`, `report`); filter with `source`/`status` when asked
for one slice, and pass `agent_id` when the user asks about ONE agent's output ("what did
Hunter produce that needs me?"). Fall back to the per-queue tools only when you need
queue-specific filters:
- `list-reviews(workspace_id, workflow_type="team")` — standard queue (`reviewer_id` filter
  also available). **Without `workflow_type`, list-reviews returns BOTH workflows** (team +
  recurring), so calling it bare alongside `list-recurring-reviews` double-counts the agent
  drafts. Always pass `workflow_type="team"` when segmenting the two queues.
- `list-recurring-reviews(workspace_id)` — agent drafts (`status`, `template_id` filters;
  pass `agent_creator_id` — an agent id from `list-agents` — to triage one agent's drafts).
Present a single combined summary: how many from each source, and a one-line preview per item
(content snippet, target account/platform, for agent items the suggested schedule time, and
for hunter items the mention/lead being replied to). For `report` items, surface the report
summary and its download link — reports are read-and-download, not approve/reject. Make clear
which source each item belongs to, since they're actioned through different tools.
Two extra fields on team rows matter:
- **`workflow_run_id`** — items sharing one came from the same workflow run; group them as a
  batch ("3 drafts from your launch workflow") and, where the flag-gated `get-workflow-run`
  tool is available, offer the run's overall status (see bolta-workflow-run).
- **Status `autonomous`** — the post was **scheduled by the autonomy policy, not approved by
  a human**. Never describe an autonomous row as human-approved; say it was auto-scheduled
  under the workspace's autonomy settings.

### 3. Inspect (optional)
For any item the user wants to see in full before deciding, call `get-post(post_id)` for the
complete content, media, and target accounts. Do this when a snippet isn't enough to judge.

### 4. Act on each item
- **Standard-queue item** → `approve-post(workspace_id, post_id)`. **Always pass the item's
  `content_fingerprint` (from the inbox/workflow-run read) as `expected_fingerprint`** — it
  guarantees you approve exactly the revision the user just saw, not whatever the post
  contains now. Optionally pass `schedule_mode` / `fixed_time` to schedule it on approval,
  and `comments` for approver notes.
- **Agent (recurring) item, approve** → `approve-recurring-review(review_id)`. Pass
  `approveWithSchedule` + `useSuggestedTime` to schedule at the agent's suggested time, and
  `approvalComments` for notes.
- **Agent (recurring) item, reject** → `reject-recurring-review(review_id, rejectionReason, rejectionCategories)`. ALWAYS also pass `rejectionCategories` when the objection fits a code — structured categories train the voice far better than free text. Valid codes: too_casual, too_formal, wrong_tone, off_brand, too_long, too_short, wrong_format, factual_error, spelling_grammar, missing_cta, wrong_cta, wrong_emoji, wrong_hashtag, not_engaging, platform_mismatch, too_salesy, off_topic, repetitive, other (anything else is silently dropped).
  Always include a concrete reason — rejections and edits are what teach Bolta the brand's
  voice, so a specific reason ("too hypey", "wrong CTA") improves future drafts more than a
  bare reject.
- **Hunter reply draft** (source=`hunter`; `reply_id` from the inbox row) → show the draft
  alongside the mention/lead it responds to, then:
  - Send as-is → `send-hunter-reply(workspace_id, reply_id)`.
  - Send with a tweak → `send-hunter-reply(workspace_id, reply_id, content=<revised text>)` —
    one call edits and sends.
  - Edit but hold → `update-hunter-reply(workspace_id, reply_id, content)` (only unsent drafts;
    already-sent replies 409). Confirm the final text with the user before sending — replies go
    out publicly on the platform. Double-send is prevented server-side, so a retry is safe.
- **Report item** (source=`report`) → nothing to approve; present the summary and download link.

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
- `approve-post` returns **409 `stale_review`** → the post changed (content, media,
  destination, or scheduled time) after the user last saw it. **NEVER blindly retry** — the
  409 deliberately carries no fingerprint, so a blind retry cannot succeed. Recovery flow:
  re-read the item (`list-inbox-items` or `get-post`; `get-workflow-run` for workflow
  drafts), SHOW the user the current content, get a fresh explicit decision, then approve
  again passing the fresh `content_fingerprint` as `expected_fingerprint`. (Alternative:
  `submit-for-review` re-stamps the reviewed revision.)
- Empty queues → say both are clear; offer to push drafts in via `submit-for-review`.
- Permission error on approve/reject → run `get-my-capabilities`, report the missing role,
  do not retry.
- Wrong tool for the queue (e.g. `approve-post` on an agent item) errors — route standard
  items through `approve-post` and agent items through the `*-recurring-review` tools.
- `update-hunter-reply` returns 409 → the reply was already sent; report that and re-pull the
  inbox rather than retrying.
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
