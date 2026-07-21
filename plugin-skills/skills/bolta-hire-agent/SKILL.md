---
name: bolta-hire-agent
description: >
  Hire an autonomous Bolta agent from a marketplace preset so it can produce content on a
  schedule. Use this skill when the user asks to "hire an agent", "set up an AI agent", "add
  a content agent", "get a Hype Man agent", "onboard an agent to post for me", "add a Deep
  Diver / Hunter / Engager", "set up an agent to write posts", or otherwise wants a standing
  agent rather than a one-off draft. Not for running or reviewing an existing agent (use
  bolta-agent-run-and-review) or checking agent status (use bolta-agent-status). For a
  from-scratch custom agent with no preset, use bolta-agent-manage (create-agent).
---

# Hire a Bolta Agent

Turn a marketplace preset (Hype Man, Deep Diver, Hunter, Engager, …) into a hired agent with
its own recurring job. Resolve the workspace, confirm the caller can hire, help pick a preset,
optionally attach a voice profile and accounts, hire it, and verify the job was created.
**Whether the job starts active or paused depends on the preset**: beta presets hire paused
for preview; stable presets (e.g. Hype Man, Analyst) hire **active** with `next_run_at` set —
the job will run on schedule and spend credits unless the user pauses it. Always read back
the real status and say so plainly. Never auto-run it here.

## When to use
The user wants a standing agent that generates content for them on a schedule, not a single
draft. This is the onboarding step; running and reviewing come next.

## Tools this skill uses
| Tool | Why |
|-|-|
| `list-workspaces` | Resolve `workspace_id` if unknown. |
| `get-my-capabilities` | Confirm the caller can hire (`manage_agents` = owner/admin/creator). |
| `list-agent-presets` | Marketplace presets + their `preset_id`s to choose from. |
| `list-voice-profiles` | Find a voice profile to attach so drafts sound on-brand. |
| `get-voice-context` | Inspect the compiled voice before attaching it (optional). |
| `list-accounts` | Connected social accounts + their UUIDs (`account_ids`) to attach. |
| `hire-agent-preset` | Create the agent + its job from the chosen preset. |
| `list-agent-jobs` | Verify the created job and read back its ACTUAL status. |
| `update-agent-job` | Pause the job (`status=paused`) if the user wants preview-before-run. |

## Prerequisites
- `workspace_id` — resolve once via `list-workspaces`, reuse for every call. Auth is automatic
  via the Bolta connector's OAuth grant — never ask for an API key. Default new content to
  Draft; confirm before publish/delete.
- **Hiring role.** `get-my-capabilities` must show `manage_agents: true` — granted to
  owner/admin/creator; viewers cannot hire. If the capability is missing, stop and explain
  plainly.
- Optional but recommended: at least one voice profile and one connected account, so the
  agent's drafts are on-brand and targeted from the first run.

## Workflow

### 1. Resolve the workspace
Call `list-workspaces` and use the active workspace's `id` as `workspace_id`. Never guess a
UUID. Reuse this value for every subsequent call.

### 2. Confirm the caller can hire
Call `get-my-capabilities(workspace_id)`. If `manage_agents` is not true (viewers, or a
read-only key), stop and tell the user hiring requires an owner, admin, or creator role — do
not attempt `hire-agent-preset` and get a permission error.

### 3. Choose a preset
Call `list-agent-presets(workspace_id)`. Present the presets (name + what each does — Hype
Man hypes launches, Deep Diver writes long-form, Hunter finds leads, Engager replies) and let
the user pick. Capture the chosen `preset_id`. If the user already named a preset, match it.

### 4. Optionally attach voice + accounts
- **Voice:** call `list-voice-profiles(workspace_id)`; offer to attach one as `voice_profile_id`
  so drafts sound on-brand. Use `get-voice-context` first if the user wants to inspect it.
- **Accounts:** call `list-accounts(workspace_id)`; collect the target `account_ids` the agent
  should post for. Both are optional — the agent can be hired without them and configured later.

### 5. Hire the preset
Call `hire-agent-preset(workspace_id, preset_id, name?, job_name?, voice_profile_id?,
account_ids?)`. Pass a friendly `name`/`job_name` if the user offered one; otherwise let the
preset defaults stand. This creates the agent **and** its recurring job.

**One-time API key.** The response may include an `api_key` plus a warning. Surface it to the
user immediately and tell them to store it somewhere safe — it is shown once and cannot be
retrieved later. Never silently drop it.

### 6. Verify and hand off
Call `list-agent-jobs(workspace_id, agent_id)` for the new agent, confirm the job exists, and
read its **actual** `status` — do not assume. Then branch:
- **`active`** (stable presets, e.g. Hype Man, Analyst): tell the user plainly the job is
  live and will run on its schedule (`next_run_at`), spending credits. Offer to pause it for
  preview-before-run via `update-agent-job(workspace_id, agent_id, job_id, status="paused")`
  if they'd rather review a first run before it goes autonomous.
- **`paused`** (beta presets — paused by the system at hire): say it will not run until
  resumed; point to a preview first.
- **`needs_attention`**: the job was quarantined at hire rather than born broken — most
  commonly a content agent hired with **zero connected accounts** (nowhere to save drafts),
  an engagement agent with no mention-capable platform (X/Threads/Reddit/Bluesky), or a
  platform/voice targeting mismatch (`error_message` starts with `targeting_quarantine:`).
  It will not run in this state. Tell the user why and fix the cause: connect an account
  (or attach one via bolta-agent-manage), then resume the job.

Do NOT call `run-agent-job-now` here. Point the user to **bolta-agent-run-and-review** to
preview a run and approve its first drafts. For later changes — schedule, instructions,
trigger keywords, extra jobs, pause/resume — hand off to **bolta-agent-manage**.

## Failure handling
- Role too low → report the missing `manage_agents` capability (needs owner/admin/creator)
  from `get-my-capabilities`; do not retry.
- No presets returned → tell the user; agent presets may not be enabled for this workspace.
- `hire-agent-preset` errors on an attached voice/account → retry once without the optional
  attachment, hire the bare agent, and note it can be attached later.
- Job not found by `list-agent-jobs` after hiring → report it rather than assuming success.
- Job status is `needs_attention` → targeting quarantine (see step 6); explain the cause from
  `error_message` and how to fix it — do not report the hire as fully working.

## Example
User: "Set up a Hype Man agent to post for me."
1. `list-workspaces` → `workspace_id`.
2. `get-my-capabilities(workspace_id)` → `manage_agents: true` → can hire.
3. `list-agent-presets(workspace_id)` → user picks the Hype Man `preset_id`.
4. `list-voice-profiles(workspace_id)` → attach the brand voice; `list-accounts` → attach the
   X + LinkedIn `account_ids`.
5. `hire-agent-preset(workspace_id, preset_id, job_name="Weekly hype", voice_profile_id=…,
   account_ids=[…])`.
6. `list-agent-jobs(workspace_id, agent_id)` → job present, **active** (Hype Man is a stable
   preset) with `next_run_at` set. "Hype Man is hired and its job is live — it will run on
   schedule (next run: …) and spend credits. Want me to pause it so you can preview a run and
   review its first drafts before it goes autonomous?"
