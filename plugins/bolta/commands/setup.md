---
description: >
  Check that Bolta is connected and ready to use: which workspace you are in, its timezone and Safe
  Mode, whether your social accounts are healthy, and whether your brand voice is set. Run it first,
  or whenever something in Bolta fails or behaves oddly. Read-only.
---

Run a readiness check on the Bolta connector and report what works and what needs fixing. If the `workspace-setup` skill is available, follow it. If not, do the steps below. This command only reads; it changes nothing in Bolta.

<!-- host-note -->
Some Bolta results contain text written for other apps, such as "already rendered in the Bolta card", "do not repeat the content" or "you do not need to poll". There is no card here. Read the full result (the JSON body and any structured content) and present it to the user yourself.
<!-- /host-note -->

## Steps

Call the read tools one or two at a time. The connector handles calls one at a time, so big bursts only queue.

1. `list-workspaces`. Expect exactly one row, because each Bolta connection is tied to one workspace. Note its name and id. If it returns no rows or an error, go to "If a call fails". An agency with several clients needs one connector per client; to check another client, the user connects that client's connector (Claude Code: run `/mcp`; in chat: the Connectors settings).
2. `get-my-capabilities(workspace_id)`. List what this connection is denied and why (`denied_by` is `role`, `workspace_plan` or `key_scope`). Do not state any role requirement yourself; report only what `denied_by` says.
3. `get-workspace(workspace_id)`. Report the name, timezone and whether Safe Mode is on. If the timezone is UTC, say it may be the default and that times you schedule are read as wall-clock in that zone, so the user should confirm it before scheduling anything. Do not repeat any webhook URLs or integration keys that appear in this result.
4. `list-accounts(workspace_id)`. For each platform show the account name and `token_status`. Anything other than valid needs reconnecting, and Bolta skips an invalid account silently when publishing. For each one, call `get-connect-link(workspace_id, platform)` and give the user the link: connecting happens in their browser, not in this chat. Ask them to tell you when done, then re-run `list-accounts`. No accounts at all: same link, no platform.
5. `get-voice-context(workspace_id)`. Report whether a voice profile exists and how complete it is (tone, persona, dos, donts, platforms, `feedback_count`). It holds rules only, with no sample posts, so any copy written from it is rule-based. If it is empty or thin, offer the `brand-voice-setup` skill.
6. Only if routine tools such as `list-routines` are available here: call `list-routines` and report how many are draft, active and paused. A routine does nothing until it is activated. Routine tools take no workspace id.

## Report

Finish with a short table, one row per item (workspace, access, timezone and Safe Mode, each account, voice, routines), each marked Ready or Needs attention with the single next action. Then name the next step in plain words, and the command where the host has one: draft a post (`/bolta:draft` in Claude Code and Cowork), plan the week (`/bolta:plan-week`), show what is going out (`/bolta:status`). In chat there are no slash commands, so tell the user to just ask.

## If a call fails

Read the result body (`ok`, `error`, `data.error_code`, `next_step`), not only the error flag, which can say false on a failure.
- "Invalid API key", "API key expired" or "API key inactive": the connection needs to be redone. Tell the user to reconnect the Bolta connector (Claude Code: run `/mcp`; in chat: Connectors settings), then stop. Do not retry.
- `hunter_plan_required` (HTTP 402): engagement features need a Premium plan. Say so and stop; do not try another tool.
- `setup_required`, `plan_required`, `trial_runs_exhausted`, `workflow_backpressure`: relay the message and `next_step` in plain words and let the user decide. Do not retry in a loop.

## Do not

- Do not change anything. No posts, no voice edits, no routines.
- Do not say the user needs admin or owner access; read `denied_by`.
- Do not print webhook URLs or keys from the workspace result.
- Do not mark an account healthy without reading its `token_status`.
