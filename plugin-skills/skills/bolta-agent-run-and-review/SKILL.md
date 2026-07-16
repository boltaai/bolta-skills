---
name: bolta-agent-run-and-review
description: >
  Run a Bolta agent's job on demand and review the drafts it produces — the core agent loop.
  Use this skill when the user asks to "run my agent now", "have the agent make posts",
  "trigger the agent job", "preview a run", "review the agent's drafts", "approve what the
  agent made", "reject that draft", or "what did my agent create". Covers triggering a run,
  watching it work, and approving/rejecting each draft so Bolta learns the brand's voice. Not
  for hiring a new agent (use bolta-hire-agent) or a read-only status report (use
  bolta-agent-status).
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
| `list-recurring-reviews` | The pending drafts the run produced (agent → human queue). |
| `approve-recurring-review` | Approve a draft; optionally schedule it at the suggested time. |
| `reject-recurring-review` | Reject a draft with a reason (this teaches the voice). |

For the full tool contract see `../../references/bolta-tools.md` and
`../../references/bolta-ecosystem.md`.

## Prerequisites
- `workspace_id` — resolve once via `list-workspaces`, reuse.
- A hired agent with a job. If none exists, point the user to **bolta-hire-agent** first.
- Approving/rejecting drafts needs editor+ (see `get-my-capabilities`); if the caller can only
  view, they can trigger and watch a run but not act on its drafts — say so.

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
scope the run to a single connected account. This kicks off a run immediately.

### 4. Watch the run
Call `list-agent-job-runs(workspace_id, agent_id, job_id, limit?)` and read the newest run:
status (running → completed/failed), tools it used, tokens, cost, and its output. Summarize
what it did in plain language. Runs are async — if still running, note that and re-check
rather than assuming failure.

### 5. Fetch the drafts it produced
Agent drafts land in the recurring-review queue, not the standard one. Call
`list-recurring-reviews(workspace_id, status="pending")` to get the drafts this run created.
If empty right after a completed run, the run may still be finalizing — re-check once before
concluding it produced nothing.

### 6. Review each draft — approve or reject
Present each draft to the user, then act on their decision:
- **Approve:** `approve-recurring-review(review_id, approvalComments?, approveWithSchedule?,
  useSuggestedTime?)`. Set `approveWithSchedule`/`useSuggestedTime` to schedule it at Bolta's
  suggested time instead of leaving it as an approved draft.
- **Reject:** `reject-recurring-review(review_id, rejectionReason)`. Always pass a concrete
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
- No pending reviews after a completed run → re-check `list-recurring-reviews` once, then tell
  the user the run produced no drafts.
- Approve/reject permission error → the caller lacks editor+; report it and leave the draft
  pending.

## Example
User: "Run my Hype Man agent and show me what it made."
1. `list-workspaces` → `workspace_id`.
2. `list-agents(workspace_id)` → Hype Man `agent_id`; `list-agent-jobs(…)` → `job_id`.
3. `run-agent-job-now(workspace_id, agent_id, job_id, run_instructions="focus on the v2 launch")`.
4. `list-agent-job-runs(…)` → completed, 3 tools, $0.04, 3 drafts.
5. `list-recurring-reviews(workspace_id, status="pending")` → 3 drafts.
6. Draft 1 approved with `useSuggestedTime=true`; draft 2 rejected with
   `rejectionReason="opens with a hype cliché"`; draft 3 approved as a draft.
7. "Approved 2 (one scheduled for the suggested slot), rejected 1 — the reason is now feeding
   voice learning, so the next run should avoid that opener."
