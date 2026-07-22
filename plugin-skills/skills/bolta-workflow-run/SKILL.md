---
name: bolta-workflow-run
description: >
  Start and track a durable Bolta content workflow for a multi-step OUTCOME. Use this
  skill when the user asks to "keep our launch active this week", "prepare next week's
  content", "get 5 posts ready for the product announcement", "run the weekly content
  workflow", or later asks "how's the workflow doing", "is the launch workflow done",
  "did those posts get scheduled". A workflow drafts several posts and then either
  routes them for review or schedules them automatically — governed by the workspace's
  autonomy policy, which a request can tighten but never loosen. Requires the
  flag-gated Workflow Runtime tools (start-workflow / get-workflow-run). Not for one
  explicit post (use bolta-draft-post), not for bulk-creating a list of posts the user
  already wrote (use bolta-schedule-and-batch), and not for standing inbox triage
  (use bolta-review-queue).
---

# Bolta — Run a Workflow

Turn a stated outcome into a durable workflow run: Bolta drafts the posts, then — per the
workspace's autonomy policy — either parks them for human approval or schedules them
automatically for future publication. Nothing EVER publishes immediately through a
workflow; immediate publication stays with `publish-post`. Start the run, poll it, read
the result back honestly, and route pending drafts into the review flow.

## Availability gate — check before anything else
`start-workflow` and `get-workflow-run` are flag-gated. Never assume they exist because
documentation mentions them — check the CURRENT tool list first:
- **Both `start-workflow` AND `get-workflow-run` available** → use the workflow flow below.
- **Either one missing** → do NOT attempt those tools — no speculative calls, no retries.
  If the user's request is genuinely atomic (one explicit post, one schedule, one approval),
  use the matching existing atomic tool (`create-post`, `schedule-post`, `approve-post`).
  Otherwise tell the user plainly that workflow execution is not enabled for this workspace
  yet and offer the atomic alternative — **never fake a workflow with a burst of atomic
  calls**.

## When to use
Route by intent — this steering matters more than anything else in this skill:
- **One explicit post** ("draft a post about X") → `create-post` via **bolta-draft-post**. NOT a workflow.
- **A multi-step outcome** ("keep our launch active this week", "prep next week's content") → `start-workflow`.
- **"What needs my approval?"** → `list-inbox-items` via **bolta-review-queue**, not a new workflow.
- **A follow-up on a run you started** ("how's the launch workflow doing?") → `get-workflow-run` with the saved `workflow_run_id`.

## Tools this skill uses
| Tool | Why |
|-|-|
| `list-workspaces` | Resolve `workspace_id` if unknown. |
| `list-accounts` | Optional — resolve `account_ids` when the user names specific accounts. |
| `start-workflow` | Start the durable run (flag-gated; returns a `workflow_run_id` immediately). |
| `get-workflow-run` | Poll the run: status, counts, autonomy policy applied, artifacts, next actions. Read-only. |
| `list-inbox-items` | Review the drafts a run parked for approval (hand off to bolta-review-queue to act). |
| `list-scheduled-posts` | Show what an auto-scheduling run put on the calendar. |

## Prerequisites
- `workspace_id` — resolve once via `list-workspaces`, reuse for every call. Auth is automatic
  via the Bolta connector's OAuth grant — never ask for an API key.
- **The Workflow Runtime is flag-gated** (the tool surface is 62 tools instead of the
  60-tool baseline when it's on). The availability gate above governs everything — never
  call a tool name that isn't exposed.
- An `objective` in the user's own words. **Never invent the objective** — if the user hasn't
  stated a goal, ask for one before starting anything.

## Workflow

### 1. Resolve the workspace
Call `list-workspaces`; use the active workspace's `id`. Never guess a UUID.

### 2. Pick the execution mode from the user's language
`execution_mode` requests can **tighten but never loosen** workspace safety — the workflow
never overrides the workspace's autonomy settings. Map conservatively:

| User says | Mode |
|-|-|
| "let me review", "show me first", "before it goes out" | `require_review` |
| "schedule automatically", "handle the schedule for me", "just schedule it" | `auto_schedule` |
| "keep our launch active", "run this campaign this week" | `inherit` |
| No explicit preference | `inherit` (default — it respects what the user already configured) |

**Vague delegation language ("take care of this", "handle it", "you decide") is NOT explicit
authorization to increase autonomy — it maps to `inherit`, never `auto_schedule`.** Only an
explicit scheduling request selects `auto_schedule`, and even then the server may fall back
to review with a typed `fallback_reason` (`safe_mode` or `autonomy_insufficient`) — read it
back to the user. Even `auto_schedule` only ever **schedules for future publication** via
the normal scheduler — it never publishes on the spot.

### 3. Start the run
Call `start-workflow(workspace_id, objective, …)`:
- `objective`* — the outcome in the user's own words.
- `workflow_key` — default `weekly_content_prepare`; omit unless the user asked for a specific workflow.
- `post_count` — 1–10, default 4.
- `platforms` — comma-separated, only platforms the user asked for.
- `account_ids` — comma-separated UUIDs from `list-accounts`; omit to let the agent pick.
- `time_window` / `notes` — timeframe and extra guidance, when given.
- `execution_mode` — from step 2.
- `idempotency_key` — pass a stable value so retries are safe: the same key always returns
  the same run. Even without one, the server replays identical objectives started within
  the last 30 minutes — so a repeated "start the launch workflow" returns the SAME run
  rather than a duplicate. Treat that as dedup working, not an error.

The call returns immediately with a durable `workflow_run_id`. **Save it** — every follow-up
question about this run goes through it. The run consumes agent credits where applicable.

### 4. Poll and read the run back
Call `get-workflow-run(workspace_id, workflow_run_id)` — read-only and side-effect free, safe
to poll. Translate the payload honestly:

| `status` | Meaning / what to say |
|-|-|
| `running` | Still working — report progress counts, offer to check again. |
| `awaiting_approval` | Drafts are parked for review — offer to open the review queue (step 5). |
| `scheduled` | Posts were auto-scheduled — report `next_scheduled_time` and offer `list-scheduled-posts`. |
| `partial` | Some posts scheduled AND some still need review. **This is a normal mixed outcome, never a failure** — report both halves and offer the review queue for the pending ones. |
| `completed` | Everything done — summarize what was produced. |
| `failed` | Report `error_summary`; offer to adjust the objective and `start-workflow` again. |
| `cancelled` | The run was cancelled; nothing more will happen. |

Also read back:
- **Counts** — `draft_count`, `scheduled_count`, `review_count`, `failed_count` — in plain
  language ("4 drafts: 2 scheduled, 2 waiting for your approval").
- **Policy** — `requested_execution_mode`, `effective_autonomy`, `approval_required`, and
  `fallback_reason`. When the user asked for `auto_schedule` but `fallback_reason` is set
  (`safe_mode` | `autonomy_insufficient`), explain it plainly: the workspace's safety
  settings require review, and a workflow request can tighten but never loosen them —
  changing that means changing the workspace/agent autonomy settings, not retrying the call.
- **Artifacts** — each has `post_id`, `platforms`, `review_status`, `content_preview`,
  `scheduled_time`, and `content_fingerprint` (the revision token — needed to approve, step 5).
- **`next_actions`** — the server's suggested follow-ups; mirror them in your offer.

### 5. Route pending drafts into review
When status is `awaiting_approval` or `partial`, the pending drafts live in the unified
inbox: `list-inbox-items(workspace_id)`. Hand the approve/reject flow to
**bolta-review-queue**. Two contract points that matter here:
- When approving via `approve-post`, pass the item's `content_fingerprint` as
  `expected_fingerprint` so you approve exactly the revision the user saw.
- Review rows with status `autonomous` were **scheduled by the autonomy policy, not
  approved by a human** — never describe them as human-approved.

### 6. Follow-ups
Later questions about the run ("how's the launch workflow doing?", "did those posts go
out?") → `get-workflow-run` with the saved `workflow_run_id`. Don't start a new workflow to
answer a status question. Summarize deltas since the last check (newly scheduled, newly
approved, still pending).

## Failure handling
- `start-workflow` or `get-workflow-run` missing from the tool list → the Workflow Runtime
  flag is off. Follow the availability gate: no speculative calls, no retries; atomic request
  → matching atomic tool; otherwise say workflow execution isn't enabled yet and offer the
  atomic alternative. Never simulate a workflow with a burst of atomic calls.
- `fallback_reason` set (`safe_mode` / `autonomy_insufficient`) → not an error. Explain that
  workspace safety required review, and route to the review queue. Never re-request
  `auto_schedule` hoping for a different answer.
- `status=partial` → never report it as a failure; it's a mixed outcome (step 4).
- `status=failed` → relay `error_summary`, offer to adjust the objective and start again.
- Duplicate-looking response (same `workflow_run_id` returned again) → idempotent replay
  (same `idempotency_key`, or same objective within 30 minutes). Report the existing run's
  status instead of treating it as a new run.
- Permission error → run `get-my-capabilities` and explain the missing role; don't retry.
- On `setup_required` or plan errors (`plan_required` / `trial_runs_exhausted`), switch to
  the **bolta-setup** flow — don't retry.

## Example
User: "Keep our product launch active on LinkedIn and Threads this week — I want to approve
everything first."
1. `list-workspaces` → workspace_id.
2. "approve everything first" → `execution_mode="require_review"`.
3. `start-workflow(workspace_id, objective="Keep our product launch active on LinkedIn and
   Threads this week", platforms="linkedin,threads", time_window="this week",
   execution_mode="require_review", idempotency_key="launch-week-2026-07")` → `workflow_run_id`.
4. `get-workflow-run(…)` → `status=awaiting_approval`, `draft_count=4`, `review_count=4`,
   `approval_required=true`.
5. "4 launch drafts are ready and waiting for your approval — nothing goes out until you
   approve. Want to review them now?" → hand off to bolta-review-queue (approving with each
   item's `content_fingerprint` as `expected_fingerprint`).
6. Next day: "how's the launch workflow?" → `get-workflow-run(same id)` → `partial`: "2
   approved and scheduled (next goes out Tue 9am), 2 still waiting for your review."
