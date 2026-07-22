---
name: bolta-setup
description: >
  Get a Bolta workspace from zero to workflow-ready, and recover from setup/entitlement
  errors. Use this skill on first contact — "set up Bolta", "get started", "connect my
  accounts", "is my workspace ready" — and whenever ANY Bolta tool or skill returns a typed
  setup/entitlement error (setup_required, plan_required, trial_runs_exhausted,
  workflow_backpressure): other skills should hand off here rather than retrying. Walks a
  read-only readiness checklist (workspace → connected accounts → voice → agents →
  permissions), fixes one blocker at a time, and confirms each fix by re-reading. Not for
  writing content (bolta-draft-post), running workflows (bolta-workflow-run), or inbox
  triage (bolta-review-queue) — this skill makes those possible.
---

# Bolta — Setup & Recovery

The on-ramp: take a workspace from zero to ready-for-a-draft-or-workflow, and the standard
recovery path when a tool returns a setup or entitlement error. Never fake progress — no
retry loops against setup errors. Work one blocker at a time in checklist order, confirm
each fix by re-reading, and close by confirming the workspace is ready.

## When to use
- **First contact:** "set up Bolta", "get started", "connect my LinkedIn", "why can't I post".
- **Error handoff:** another tool/skill hit `setup_required`, `plan_required`,
  `trial_runs_exhausted`, or `workflow_backpressure`. Jump straight to the recovery map
  below — do NOT retry the failing call.

## Tools this skill uses
| Tool | Why |
|-|-|
| `list-workspaces` | Resolve `workspace_id` — the first readiness check. |
| `get-workspace` | Settings, safe-mode, autonomy — the workspace's posture. |
| `list-accounts` | Connected social accounts — the essential blocker check. |
| `get-connect-link` | URL to Bolta's connect page when accounts are missing (`platform` preselects one). |
| `get-voice-context` / `list-voice-profiles` | Voice readiness — is the workspace brand-blind? |
| `extract-business-dna` | Seed brand identity from the user's website URL (OW; consumes AI credits). |
| `list-agents` / `list-agent-presets` / `hire-agent-preset` | Agent readiness — hire a content creator if none. |
| `get-my-capabilities` | When permissions look wrong — `denied_by` says WHY (`role` / `workspace_plan` / `key_scope`). |
| `list-inbox-items` | Clear the pending-review backlog behind `workflow_backpressure`. |

## Workflow — the readiness checklist (run in order, read-only first)

### 1. Workspace
`list-workspaces` → active workspace's `id` (never guess a UUID), then `get-workspace` for
settings, safe-mode, and autonomy posture. No workspace at all → the connector isn't
authorized; explain and stop.

### 2. Connected accounts — the essential blocker
`list-accounts(workspace_id)`. **Zero connected accounts blocks everything** — drafts have
nowhere to land and workflows refuse to start. Call `get-connect-link(workspace_id,
platform?)` and give the user the link, and ALWAYS explain: connecting social accounts is
an OAuth flow that must be completed at bolta.ai in the browser — **it cannot happen inside
ChatGPT**. After the user says they've connected, confirm by calling `list-accounts` again;
don't take it on faith.

### 3. Voice
`get-voice-context(workspace_id)` (or `list-voice-profiles`). If the workspace is
brand-blind — no voice, no profiles — content still generates but sounds generic. Offer
`extract-business-dna(workspace_id, url)` with the user's website URL to seed Business DNA
(reaches the internet, consumes AI credits — confirm first), and point to the
brand-voice-* skills for the full guideline.

### 4. Agents
`list-agents(workspace_id)`. No content-creator agent → workflows and agent runs have no
worker. Offer `list-agent-presets` → `hire-agent-preset` (the bolta-hire-agent skill owns
the details). Note: `start-workflow` auto-hires the default preset itself — only a failed
auto-hire surfaces this as a blocker.

### 5. Permissions (when something looks denied)
`get-my-capabilities(workspace_id)` — its `denied_by` field says WHY each denied action is
denied: `role` (need owner/admin/creator), `workspace_plan` (upgrade required), or
`key_scope` (the key doesn't carry the scope). Report the reason plainly; never retry
around a permission denial.

### 6. Close
Re-read whatever was fixed, then confirm readiness explicitly: "Accounts connected, voice
loaded, agent hired — ready for a draft (bolta-draft-post) or a workflow
(bolta-workflow-run)."

## Typed-error recovery map
| Error | Recovery |
|-|-|
| `setup_required`, missing `connected_accounts` (409) | `get-connect-link` → user finishes OAuth at bolta.ai in the browser → confirm with `list-accounts`. |
| `setup_required`, missing `content_creator_agent` (409) | `hire-agent-preset` (via `list-agent-presets`), then retry the original action once. |
| `plan_required` / `trial_runs_exhausted` (402) | Do NOT retry — a retry comes right back. Tell the user honestly that an upgrade is required at bolta.ai/pricing. |
| `workflow_backpressure` (409) | Too many undecided drafts piled up. Clear pending reviews first (`list-inbox-items` → bolta-review-queue), then start again. |
| `workflow_runtime_disabled` (404) | Workflows aren't enabled for this deployment — use the atomic tools instead (bolta-draft-post / bolta-schedule-and-batch); never fake a workflow with atomic calls. |

## Failure handling — tone rules
- **Never fake progress.** A setup/entitlement error is a state, not a flake — no retry
  loops, no "let me try again".
- **One blocker at a time,** in checklist order — accounts before voice before agents.
- **Confirm by re-reading.** After the user completes a browser step, verify with the
  matching read tool (`list-accounts`, `list-agents`) before moving on.
- Plan gates: state the limit and the upgrade path honestly; never work around it.
- End by naming what the workspace is now ready for.

## Example
User: "Set up Bolta for me."
1. `list-workspaces` → workspace_id; `get-workspace` → safe-mode ON, assisted autonomy.
2. `list-accounts` → zero accounts. `get-connect-link(workspace_id)` → "Here's your connect
   link — the OAuth handshake has to happen at bolta.ai in your browser, it can't run here.
   Tell me when you're done."
3. User: "connected LinkedIn" → `list-accounts` again → LinkedIn present. Confirmed.
4. `get-voice-context` → empty → offer `extract-business-dna` with their site; user agrees →
   DNA seeded.
5. `list-agents` → none → offer a content-creator preset; user defers.
6. "You're ready: LinkedIn connected, brand DNA seeded. You can draft a post now
   (bolta-draft-post); hire an agent later for workflows and scheduled runs."
