---
name: bolta-agent-manage
description: >
  Manage the Bolta agent workforce — pause, resume, reschedule, edit, create, or delete
  agents and their jobs. Use this skill when the user asks to "pause my agent", "pause the
  daily job", "resume it", "change the schedule", "make it run at 6pm", "update the
  instructions", "add a keyword to the hunter job", "add a LinkedIn job", "create a custom
  agent", "delete that job", or "remove the agent". Not for hiring from a preset (use
  bolta-hire-agent), status reports (bolta-agent-status), or triggering/reviewing runs
  (bolta-agent-run-and-review).
---

# Manage Bolta Agents & Jobs

Full lifecycle management of agents and their jobs: pause/resume at the right scope,
reschedule, edit instructions and trigger config, create new jobs or custom agents, and
delete with confirmation. The cardinal rules: **resolve pause scope before acting**,
**read-modify-write any config object**, and **confirm every delete**.

## Tools this skill uses
| Tool | Why |
|-|-|
| `list-workspaces` | Resolve `workspace_id` if unknown. |
| `get-my-capabilities` | Writes need `manage agents` (owner/admin/creator). Check before mutating. |
| `list-agents` / `get-agent` | Find the agent; learn its type before creating jobs for it. |
| `list-agent-jobs` | The agent's jobs — needed to resolve pause-scope ambiguity. |
| `get-agent-job` | Full job detail incl. `paused_by` and current `trigger_config`/`schedule`. **Always fetch before editing or resuming.** |
| `create-agent` | Custom agent from scratch (prefer `hire-agent-preset` when a preset fits). |
| `update-agent` | Rename, safe-mode, config — and the AGENT-level pause (cascades to all jobs). |
| `delete-agent` | Irreversible agent removal (confirm; offer pause as the soft option). |
| `list-recently-deleted` / `restore-deleted` | Undo path for job deletes within the 7-day window. |
| `create-agent-job` | Add a job: schedule/trigger/voice/accounts/instructions. |
| `update-agent-job` | The JOB-level pause/resume, reschedule, instruction and config edits. |
| `delete-agent-job` | SOFT delete — restorable for 7 days (still confirm; offer pause first). |

## The pause-scope rule (most important)
"Pause the agent" is ambiguous — the user often means one job.
- **Agent-level** (`update-agent status=paused`) stops EVERYTHING that agent does:
  every active job cascade-pauses. Resuming the agent reverses exactly that cascade —
  jobs that were already paused for other reasons stay paused.
- **Job-level** (`update-agent-job status=paused`) stops only that job; the agent and
  its other jobs keep running. This is the right default for "pause the daily posts",
  "stop the Threads job", "skip this week".

Procedure: if the agent has **one** job, either level works — do the job-level pause and
say which level you used. If it has **multiple** jobs and the user said "pause the agent",
show the jobs and ask whether they mean everything or one schedule — do NOT blind-fire
the agent-level pause.

Caveat: a job-level pause stops *scheduled* runs only — `run-agent-job-now` still
executes a paused job on demand (only an agent-level pause blocks it with a 409). Manual
runs by non-owner teammates also hit a daily cap (429 `run_now_member_daily_cap`); the
owner is exempt.

## Resuming — check `paused_by` first
`get-agent-job` first, always. `paused_by` says why it's paused and whether resuming works:
`user` → only on explicit ask; `agent` → resume via the agent or the job; `trial_quota` /
`plan_gate` → a status flip comes right back, an upgrade is required — say so honestly;
`backpressure` → the review backlog must be cleared first (offer the review queue);
`system` → look at recent runs (`list-agent-job-runs`) before resuming.

## Editing config — read-modify-write, never partial
`trigger_config` and `schedule` are **full-replace** on the server. To "add one keyword":
1. `get-agent-job` → take the returned `trigger_config`.
2. Add the keyword to the copy, keeping every other key (subreddits, negative keywords…).
3. Send the WHOLE object back via `update-agent-job`.
A partial send silently wipes the keys you omitted. Same for `schedule`. Scalar fields
(`name`, `run_instructions`, `status`, `voice_profile_id`, `account_ids`, `max_retries`)
are normal partial updates.

Schedule edits: send the full schedule object (e.g. `{"interval":"daily","time":"18:00"}`)
— the server recalculates `next_run_at`. Times are naive wall-clock, interpreted in the
workspace's timezone. **Omit `timezone`** unless the user explicitly names a zone ("6pm
Pacific" → add `"timezone":"America/Los_Angeles"`); never infer one from your own locale
or the conversation. Report the new next-run time back to the user.

## Creating
- **Jobs:** `get-agent` first — the agent's type dictates the config shape
  (`content_creator`/`content_repurposer` = scheduled + voice + accounts; `engagement` =
  on_new_mention/on_new_comment; `acquisition` = keyword_match + keywords[]/subreddits[];
  `analytics`/`moderator` may omit voice). When a similar job exists, mirror it via
  `get-agent-job` instead of guessing.
- **Agents:** `create-agent` needs `name` + `type` (valid types: `content_creator`,
  `engagement`, `acquisition`, `reviewer`, `analytics`, `moderator`, `content_repurposer`,
  `custom` — "content" alone is not a valid enum). Free workspaces are capped at 1 agent —
  a 402 means an upgrade is required; explain it, don't retry. Prefer `bolta-hire-agent`
  (presets) unless the user explicitly wants a custom agent.

## Deleting — confirm, and know which delete is which
The two deletes are NOT equally destructive:
- **`delete-agent-job` is a SOFT delete** — the job is hidden but restorable for **7 days**
  via `list-recently-deleted` → `restore-deleted`. Its Hunter/Engager campaign still
  cascades, so confirm anyway — but if the user says "undo", the job itself comes back.
- **`delete-agent` is irreversible** and cascades hard: jobs paused, its service-account
  API keys purged, campaigns removed. No restore window.

ALWAYS confirm before either delete and offer `status=paused` as the reversible
alternative. Never delete as a side effect of any other request. If a user regrets a
job delete within 7 days, restore it instead of recreating it.

## Failure handling
- 403 naming `agents:manage` or a role error → the caller can't manage agents; say who can
  (owner/admin/creator) — don't retry.
- 402 on create → free-tier cap; explain the upgrade honestly.
- Validation 400 → surface the failing field plainly; fix and retry once.
- After any mutation, re-read (`get-agent-job` / `get-agent`) and report the ACTUAL state —
  never claim a change you didn't verify.

## Example
User: "Pause my content agent's daily job and make the weekly one run at 6pm instead."
1. `list-workspaces` → `workspace_id`; `list-agents` → the content agent.
2. `list-agent-jobs` → "Daily drafts" (active), "Weekly roundup" (active).
3. `update-agent-job(job=Daily drafts, status=paused)` → paused (job-level; agent untouched).
4. `get-agent-job(Weekly roundup)` → copy schedule; `update-agent-job` with the full schedule
   object at `18:00` → next_run_at recalculated.
5. "Daily drafts is paused (just that job — the agent's still active). Weekly roundup now
   runs at 6:00 PM; next run is Monday 6 PM."
