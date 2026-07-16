---
name: bolta-agent-status
description: >
  Report on the Bolta agent workforce — who's active or paused, what they've been producing,
  and what it's costing. Use this skill when the user asks "how are my agents doing", "show my
  agents", "agent activity", "what have my agents been doing", "agent run history", "is my
  agent working", or wants a status roll-up of their hired agents. Read-only. Not for hiring
  (use bolta-hire-agent) or triggering/reviewing a run (use bolta-agent-run-and-review).
---

# Bolta Agent Status Report

Produce a readable status report on the hired agents: persona and status per agent, each job's
schedule and status, and recent run outcomes (status, cost, tokens, output). Read-only — this
gathers and summarizes, it never triggers runs or touches drafts.

## When to use
The user wants to know how their autonomous agents are doing — who's running, who's paused,
what they've produced lately, and what it's costing. This is the same data that backs the
agent-runs widget in the Bolta dashboard.

## Tools this skill uses
| Tool | Why |
|-|-|
| `list-workspaces` | Resolve `workspace_id` if unknown. |
| `list-agents` | The hired agents + their ids and top-line status. |
| `get-agent` | One agent's persona/config/status detail. |
| `list-agent-jobs` | An agent's jobs — schedule and status (active/paused). |
| `list-agent-job-runs` | Recent runs per job: status, cost, tokens, output. |

For the full tool contract see `../../references/bolta-tools.md` and
`../../references/bolta-ecosystem.md`.

## Prerequisites
- `workspace_id` — resolve once via `list-workspaces`, reuse.
- No write role needed; every tool here is read-only, so any role (viewer+) can run this.

## Workflow

### 1. Resolve the workspace
Call `list-workspaces` and use the active workspace's `id`. Reuse it for every call.

### 2. List the agents
Call `list-agents(workspace_id)`. If the user named or implied a single agent, scope the report
to it; otherwise cover them all. If there are no agents, tell the user and offer
**bolta-hire-agent**.

### 3. Gather detail per agent
For each agent in scope, in parallel where possible:
- `get-agent(workspace_id, agent_id)` — persona/config and current status.
- `list-agent-jobs(workspace_id, agent_id)` — each job's schedule and status (active/paused).
- `list-agent-job-runs(workspace_id, agent_id, job_id, limit)` — the recent runs for each job.
  Use a small `limit` (e.g. 5) so the report stays recent and readable.

### 4. Summarize into a report
Roll the data into a plain-language report:
- **Per agent:** name, persona, active vs. paused.
- **Jobs:** schedule (cadence) and whether each is active or paused.
- **Recent activity:** last run status (completed/failed/running), when, what it produced, and
  cost/tokens. Flag anything notable — repeated failures, a paused job that should be active,
  or unusually high cost.
- **Roll-up:** total agents, how many active, aggregate recent cost. Mention this is the data
  behind the dashboard's agent-runs widget.

### 5. Suggest next steps
If a job is paused and has never previewed, point to **bolta-agent-run-and-review** to preview
it. If runs produced drafts, note they may be waiting in the recurring-review queue.

## Failure handling
- No agents → report it and offer **bolta-hire-agent**; don't fabricate activity.
- `get-agent` or `list-agent-job-runs` fails for one agent → note it and continue with the
  rest rather than aborting the whole report.
- A job with zero runs → report it as "no runs yet (likely paused for preview)", not a failure.
- Long lists → cap `list-agent-job-runs` with `limit` and summarize rather than dumping every
  run.

## Example
User: "How are my agents doing?"
1. `list-workspaces` → `workspace_id`.
2. `list-agents(workspace_id)` → Hype Man (active), Deep Diver (paused).
3. Hype Man: `get-agent`, `list-agent-jobs` → daily job active; `list-agent-job-runs(limit=5)`
   → 5 completed runs, ~$0.03 each, 12 drafts total. Deep Diver: job paused, 0 runs.
4. Report: "2 agents. Hype Man is active — 5 clean runs this week, 12 drafts, ~$0.15 total.
   Deep Diver is paused and hasn't previewed a run yet."
5. "Want to preview a Deep Diver run to see its first drafts?"
