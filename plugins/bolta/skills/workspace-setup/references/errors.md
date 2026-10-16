# Bolta typed errors and what to do

Quoted text is what the server sends, read from its source. Match on the code in `data.error_code` (sometimes `data.code`) and on the sentence, because some tools show you only `Error: <message>`.

## How an error reaches you

- Envelope fields: `ok` (false on failure), `error` (the sentence), `error_kind`, `data` (the server's raw body, where the typed code lives) and `next_step` (successes only: the unfinished half of what the user asked).
- Top-level `error_kind` is derived from the HTTP status, which you never see: 401 and 403 give `denied`, 404 `not_found`, 429 `rate_limited`, any other 4xx (including 402 and 409) `invalid`, 5xx `unavailable`. A Premium-feature refusal (`hunter_plan_required`) also carries `data.error_kind = "plan_gate"`; other plan codes do not.
- The host's `isError` flag is unreliable: auth failures arrive as ordinary results. Read `ok`.
- A success can still be unfinished: if `next_step` is present, do it or tell the user plainly what is not done.
- If a write fails with an unclear outcome (`unavailable`, timeout, 5xx), the outcome is unknown: read before you retry (`list-workspace-posts`, `get-post`, `list-routines`).
- Never retry a row marked "stop". Never reach the same effect through a different tool.

## Connection and access

| You see | Code | Do |
|-|-|-|
| "Invalid API key" (message "The provided API key is not valid"); "API key expired"; "API key inactive" (message "This API key is expired|inactive and cannot be used") | none, `ok:false` | The connection is dead. Tell the user to reconnect (Claude Code: `/mcp`; Cowork or chat: Bolta connector settings). Stop; no retry. |
| "Not authenticated: set an Authorization: Bearer header (OAuth access token or bolta_sk_ API key)" | `error_kind: denied` | No credentials reached the server. Same as above: reconnect. |
| "API key does not have access to this workspace" | none (routine tools add `workspace_mismatch`) | You passed a `workspace_id` that is not this connection's. Use the id from `list-workspaces`. If the user wants another client, that needs a different connector. |
| "Rate limit exceeded" with `data.rate_limit.reset_time` | `rate_limited` | The one retry-safe case. Wait until `reset_time`, then retry once. |
| "This API key needs the 'agents:manage' scope to create or modify routines." (most other tools: "Insufficient permissions" with `required_permissions`, no code) | `insufficient_scope` | The connection was granted narrower access when it was authorized. Run `get-my-capabilities` and report `denied_by`. Only reconnecting as a Bolta user with more access in this workspace changes it. Stop. |
| "You do not have permission to schedule posts. Requires <role> or higher role." (also publish, approve) | none | Relay the sentence, which names the role it needs. Say the action is not available to this connection and that someone with that access would need to do it. `get-my-capabilities` can still say "allowed" for it; the sentence wins. Stop. |

## The assistant gate and Safe Mode

| You see | Code | Do |
|-|-|-|
| "Approval required: an assistant may only schedule a post that has been explicitly approved (status Approved / Ready for Scheduling / Scheduled; this post is 'Draft'). Submit it for review and have the user approve it (approve-post) first." (same wording with "publish") | none; 403 | The gate working as designed. Run the publishing ladder in social-publishing: `submit-for-review`, user's go-ahead on that exact post, `approve-post(..., schedule_mode=..., expected_fingerprint=...)`, then `schedule-post` or `publish-post` if the state allows. |
| "Immediate publishing is disabled when Safe Mode is ON. Posts must be approved before publishing." (`data.safe_mode_enforced: true`) | none; 403 | Safe Mode blocks `publish-post`. Use `submit-for-review` then `approve-post` with `schedule_mode="set_fixed_time"` and `fixed_time`. Do not tell the user to switch Safe Mode off. |
| A create succeeds but the post's `status` is `Pending Approval` | none (success) | Expected when anything non-Draft is requested. Create Drafts instead (never pass `requested_action`), then use the ladder. |
| "This post changed after it was submitted for review (content, media, destination, or scheduled time). Fetch the post's current revision (list-inbox-items or get-workflow-run), review it, then retry passing expected_fingerprint from that fresh read — or re-submit it for review." | `stale_review` (409) | The workflow-run read named in the message is not available here: re-read with `list-inbox-items` or `list-reviews`. The error carries no fingerprint, so a blind retry fails again. Show the user the current text, get a fresh decision, retry once with the new `expected_fingerprint`. If it fails again, re-submit with `submit-for-review`. |

## Accounts

| You see | Code | Do |
|-|-|-|
| "No social account is connected to this workspace, so the post cannot be published. Connect an account in Settings → Account → Socials ..." | `no_connected_account` | `get-connect-link`, user connects in the browser, confirm with `list-accounts`. |
| "No publishable account was selected for this post. Add at least one connected account id ..." | `no_account_selected` | Ask which account; take ids from `list-accounts`. |
| "None of the selected accounts can publish — they need to be reconnected: <names>. Reconnect them ..." | `accounts_need_reconnect` | `get-connect-link(workspace_id, platform=...)` for each; confirm with `list-accounts` before drafting again. |

## Plan, trial and routine runs

These come from starting a run (`run-routine-now`, `set-content-campaign-status`). `activate-routine` re-validates the routine and can fail with `invalid_routine`.

| You see | Code | Do |
|-|-|-|
| "No social accounts are connected to this workspace. Connect at least one account (get-connect-link) before starting a content workflow that publishes." (`detail.missing: connected_accounts`) | `setup_required` (409) | `get-connect-link`, user connects, confirm with `list-accounts`, then retry once. |
| "This workspace has no content-creator agent available, and the default one cannot be provisioned automatically. A workspace owner needs to set this up in Bolta before routines that create content can run." or "No content-creator agent could be provisioned for this workspace." (`detail.missing: content_creator_agent`) | `setup_required` (409) | No tool can fix this. Tell the user a workspace owner must set it up in the Bolta dashboard. Do not create or activate routines to "provision" one. Stop. |
| "Active paid subscription required for AI agents (subscriptionStatus=..., paid=...). Upgrade at bolta.ai/pricing." | `plan_required` (402) | Tell the user an upgrade is needed, with the link. Stop; a retry comes straight back. |
| "We couldn't verify plan access. Try again in a moment." | `plan_required` (402) | The plan lookup failed; it is not a refusal. Retry once after a short wait; if it repeats, tell the user. |
| "You've used all 15 trial agent runs. Subscribe for full access at bolta.ai/pricing." | `trial_runs_exhausted` (402) | Say the trial runs are used and point to bolta.ai/pricing. Stop. |
| "On your trial, use Run Now, scheduled jobs (within your trial limit), or the team chat. Upgrade for unlimited automation." | `plan_required` (402) | This trigger is not allowed on a trial. Say so; offer `run-routine-now` instead. |
| "Your free demo runs are used. Upgrade to keep your agents running." | `demo_runs_exhausted` (402) | Same as trial: upgrade, stop. |
| "Generation paused: N drafts are already waiting for your review (limit L). Approve or dismiss drafts to resume automatic generation." or "Generation paused: N drafts are waiting and nothing has been reviewed in D days. Approve or dismiss a draft to resume automatic generation." (`data.detail.backpressure` has the counts) | `workflow_backpressure` (409) | Not retryable and no override on this surface. Show N, then clear the queue with approvals (`list-inbox-items`), and start again afterwards. |
| "You've hit the daily limit of 25 manual agent runs for this workspace. This applies to team members ..." | `run_now_member_daily_cap` (429) | Say it resets tomorrow, or a workspace owner can run it. Stop. |
| "The workflow runtime is not enabled for this deployment." | `workflow_runtime_disabled` (404) | Nothing to fix. Say the automated run is unavailable and offer to draft the posts directly (social-publishing). Stop. |
| "This routine can't run as configured." with `detail.errors` / `invalid_routine` on activation | `routine_invalid`, `invalid_routine` (422/400) | Read the per-field errors (for example a disconnected account), fix the configuration with the user, then retry once. |

## Premium features

| You see | Code | Do |
|-|-|-|
| "Replying to conversations is part of Premium. Upgrade to turn this on." (engagement tools, drafting or sending inbox replies) or "Finding customers needs a Premium or Team plan. Upgrade to turn it on." (outreach routines). Body has `error_kind: "plan_gate"`, `upgrade_required: true`, `retryable: false` | `hunter_plan_required` (402) | Stop. Tell the user this feature needs a Premium plan and that you cannot do it until then. Do not look for another tool that replies. Reading rows already in the inbox still works. |
| `plan_notice` on a `list-inbox-items` success: "Answering X (Twitter) replies from one inbox needs a Premium or Team plan ..." | `x_replies_plan_required` (or `hunter_plan_required` with the engagement sentence for other platforms) | Not an error. Tell the user those replies are missing because of the plan. Never say the inbox is clear. |
| 404 "No voice profile": "This workspace has no Voice Profile yet. Create one in Bolta first." | none | Hand off to brand-voice-setup (it can create one with `create-voice-profile` after confirming). |
