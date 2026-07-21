---
name: bolta-agent-run-and-review
description: >
  Run a Bolta agent's job on demand and review the drafts it produces — the core agent loop.
  Use this skill when the user asks to "run my agent now", "have the agent make posts",
  "trigger the agent job", "preview a run", "review the agent's drafts", "approve what the
  agent made", "reject that draft", or "what did my agent create". Covers triggering a run,
  watching it work, and approving/rejecting each draft so Bolta learns the brand's voice. Not
  for hiring a new agent (use bolta-hire-agent), a read-only status report (use
  bolta-agent-status), or standing inbox triage of whatever has accumulated across agents
  (use bolta-review-queue) — this skill owns the trigger-then-review loop for one run.
---

# Run & Review a Bolta Agent

The core loop: trigger a job now, watch the run, then approve or reject every draft it
produced. Approvals and rejections feed Bolta's voice learning, so the agent gets better each
cycle. Close the loop explicitly — a run isn't done until its drafts are reviewed.

## When to use
The user wants an agent to produce content now and then wants to act on what it made. This is
where hired agents earn their keep, and where voice learning happens.

## Tools this skill uses
| Tool | Why |
|-|-|
| `list-workspaces` | Resolve `workspace_id` if unknown. |
| `list-agents` | Find the hired agent + its `agent_id`. |
| `list-agent-jobs` | Find the job to run + its `job_id` (schedule, status). |
| `run-agent-job-now` | Trigger the job immediately (optional one-off instructions). |
| `list-agent-job-runs` | Watch the run: status, tools used, tokens, cost, output. |
| `list-recurring-reviews` | Pending drafts from content agents (scope with `agent_creator_id`). |
| `list-inbox-items` | The full inbox — hunter reply drafts (source=hunter) and agent reports (source=report). |
| `approve-recurring-review` | Approve a content draft — schedules it by default (see step 6). |
| `reject-recurring-review` | Reject a draft with a reason (this teaches the voice). |
| `send-hunter-reply` / `update-hunter-reply` | Act on an acquisition agent's reply drafts. |

## Prerequisites
- `workspace_id` — resolve once via `list-workspaces`, reuse. Auth is automatic via the Bolta
  connector's OAuth grant — never ask for an API key. Default new content to Draft; confirm
  before publish/delete.
- A hired agent with a job. If none exists, point the user to **bolta-hire-agent** first.
- **Triggering a run needs `agents:manage`** (owner/admin/creator — check
  `get-my-capabilities`); a viewer's `run-agent-job-now` call 403s. Viewers can watch runs
  and read the queues but cannot trigger runs or act on drafts — say so instead of retrying.
  Non-owner teammates also have a daily manual-run cap (429 `run_now_member_daily_cap`).

## Workflow

### 1. Resolve the workspace
Call `list-workspaces` and use the active workspace's `id`. Reuse it everywhere.

### 2. Identify the agent and job
Call `list-agents(workspace_id)` to get the target `agent_id`, then
`list-agent-jobs(workspace_id, agent_id)` to get the `job_id`. If the user named an agent,
match it; if there are several, list them and let the user pick.

### 3. Run the job now
Call `run-agent-job-now(workspace_id, agent_id, job_id, run_instructions?, account_id?)`. Pass
`run_instructions` for a one-off steer ("focus on the pricing launch") and `account_id` to
scope the run to a single connected account. This kicks off a run immediately — note it runs
even if the JOB is paused (only an agent-level pause blocks it, with a 409); warn the user
before manually running a job they paused on purpose.

### 4. Watch the run
Call `list-agent-job-runs(workspace_id, agent_id, job_id, limit?)` and read the newest run:
status (running → completed/failed), tools it used, tokens, cost, and its output. Summarize
what it did in plain language. Runs are async — if still running, note that and re-check
rather than assuming failure.

### 5. Fetch what it produced — the surface depends on the agent's type
Not everything lands in the recurring-review queue. Branch on the agent's type (from
`list-agents`/`get-agent`):
- **Content agents** (`content_creator`, `content_repurposer`): drafts land in the
  recurring-review queue. Call `list-recurring-reviews(workspace_id, status="pending",
  agent_creator_id=<agent_id>)` — the `agent_creator_id` filter scopes it to this agent so
  another agent's backlog doesn't muddy the run's output.
- **Acquisition (Hunter) / engagement agents:** output is reply drafts, not posts. Call
  `list-inbox-items(workspace_id, agent_id=<agent_id>)` and look at `source=hunter` rows.
- **Analytics agents:** output is a report — `list-inbox-items` rows with `source=report`,
  or the run's own output in `list-agent-job-runs`.

Checking only the recurring queue for a hunter or analytics agent yields a false "produced
nothing" report. If the right surface is empty right after a completed run, the run may
still be finalizing — re-check once before concluding it produced nothing.

### 6. Review each draft — approve or reject
Present each draft to the user, then act on their decision. For hunter reply drafts, edit
with `update-hunter-reply` and send with `send-hunter-reply`. For content drafts:
- **Approve:** `approve-recurring-review(review_id, approvalComments?, approveWithSchedule?,
  useSuggestedTime?)`. **`approveWithSchedule` defaults to TRUE** — a plain approve
  SCHEDULES the post (agent drafts even auto-fill a future slot). To approve without
  scheduling — keep it as an approved draft — pass `approveWithSchedule=false` explicitly.
  Tell the user which they got: "approved and scheduled for X" vs "approved as a draft".
- **Reject:** `reject-recurring-review(review_id, rejectionReason, rejectionCategories)`. Pass `rejectionCategories` codes whenever the objection fits one (too_casual, too_formal, wrong_tone, off_brand, too_long, too_short, wrong_format, factual_error, spelling_grammar, missing_cta, wrong_cta, wrong_emoji, wrong_hashtag, not_engaging, platform_mismatch, too_salesy, off_topic, repetitive, other; invalid codes are silently dropped) — they feed voice learning better than prose. Always pass a concrete
  `rejectionReason` — explain to the user that the reason is what teaches Bolta's voice, so
  specific feedback ("too salesy", "wrong CTA") makes the next run better.

### 7. Close the loop
Report what was approved (and whether scheduled) vs. rejected, and note that the feedback has
been captured for voice learning. If drafts remain unreviewed, say so — don't leave the queue
half-processed.

## Failure handling
- `run-agent-job-now` errors → surface the message; if it's permission-related, report the
  missing role from `get-my-capabilities` rather than retrying.
- Run status = failed → read the run's output/tools for the reason and relay it; offer to
  re-run with adjusted `run_instructions`.
- Nothing pending after a completed run → make sure you checked the RIGHT surface for the
  agent's type (step 5), re-check once, then tell the user the run produced nothing.
- Approve/reject permission error → the caller's role can't act on drafts (see
  `get-my-capabilities`); report it and leave the draft pending.

## Example
User: "Run my Hype Man agent and show me what it made."
1. `list-workspaces` → `workspace_id`.
2. `list-agents(workspace_id)` → Hype Man `agent_id`; `list-agent-jobs(…)` → `job_id`.
3. `run-agent-job-now(workspace_id, agent_id, job_id, run_instructions="focus on the v2 launch")`.
4. `list-agent-job-runs(…)` → completed, 3 tools, $0.04, 3 drafts.
5. Hype Man is a content agent → `list-recurring-reviews(workspace_id, status="pending",
   agent_creator_id=<agent_id>)` → 3 drafts.
6. Draft 1 approved with `useSuggestedTime=true`; draft 2 rejected with
   `rejectionReason="opens with a hype cliché"`; draft 3 approved with
   `approveWithSchedule=false` (user wanted it kept as a draft).
7. "Approved 2 — one scheduled for the suggested slot, one kept as an unscheduled draft —
   rejected 1; the reason is now feeding voice learning, so the next run should avoid that
   opener."
