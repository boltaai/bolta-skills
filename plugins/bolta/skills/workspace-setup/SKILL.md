---
name: workspace-setup
description: >
  Check that a Bolta workspace is ready to use, or fix what is blocking it. Use for "set up Bolta",
  "get started", "is my workspace ready", "I just connected Bolta, what now", "which workspace am I
  on", "how do I add another client", "what is Safe Mode", "can anything go out without sign-off",
  and whenever a Bolta tool returns an error such as setup_required, plan_required,
  hunter_plan_required, "Approval required" or "Invalid API key". Runs a read-only checklist and
  fixes one blocker at a time. Not for writing or scheduling posts (social-publishing), voice
  profiles (brand-voice-setup), or checking one account or buckets (accounts-and-buckets).
---

# Workspace setup and error recovery

Take a Bolta workspace from "just connected" to "ready for a first draft", and handle any typed error another skill hits. Read first, change nothing, fix one blocker at a time in checklist order, and confirm each fix by reading again. A setup or plan error is a state, not a glitch: never retry it in a loop.

<!-- host-note -->
Some Bolta results contain text written for other apps, such as "already rendered in the Bolta card", "do not repeat the content" or "you do not need to poll". There is no card here. Read the full result (the JSON body and any structured content) and present it to the user yourself.
<!-- /host-note -->

## How a Bolta connection works (tell the user once)

- **One connection is pinned to one workspace**, chosen when the user authorized the connector. `list-workspaces` returns exactly one row. There is no tool to switch workspaces or to list a user's other workspaces. Always pass the `workspace_id` that `list-workspaces` returned, and restate the workspace name whenever you ask for a go-ahead on a write.
- **Agencies and anyone with several clients: one connector per client.** Each connector is authorized separately and the user picks the workspace at that step. Name each one after the client, and keep "bolta" in the name (for example "bolta-acme"), because the plugin's safety check only watches servers whose name contains "bolta". On Claude Code the command is `claude mcp add --transport http bolta-acme https://mcp.bolta.ai/mcp`, then `/mcp` to authorize it. In Claude Cowork or chat, add a custom connector with the same URL from the connector settings. If the user asks to "switch to client X" or "show all my clients", explain this instead of guessing; you cannot see the other connectors' workspaces from this one.
- **Drafts first.** On a connector authorized by signing in, the server routes anything you create beyond a Draft to Pending Approval and refuses to schedule or publish a post the user has not approved. Behave the same on every connection: the readiness report should say "I can draft; nothing goes live until you approve that exact post".
- **Confirmations.** On Claude Code the plugin shows a "Confirmation needed (Bolta plugin safety check)" prompt before anything public, approving, automated, brand-changing or deleting, and Cowork may too. If the user declines, or the call comes back denied, that action is finished: say what was not done, do not retry it and do not reach the same effect with another tool. Chat has no such prompt, so you must ask in words and wait.

## The readiness checklist

Run these in order. Steps 1 to 5 are read-only. Keep a running list of what is fine and what blocks.

### 1. Workspace: `list-workspaces`
Take the single row's `id` and `name`. Most other tools require `workspace_id` (routine, campaign and a few post tools take none), so you need this id first. If the call fails with an auth message ("Invalid API key", "API key expired", "API key inactive", "Not authenticated"), the connection is dead: go to "Reconnecting" below and stop. Zero rows or more than one row is unexpected: show what came back and ask the user which workspace they mean.

### 2. Settings: `get-workspace(workspace_id)`
Read `name`, `timezone`, `safe_mode` and `autonomy_mode` from the body and report them in one line.
- **Timezone.** Times the user states are wall-clock in this timezone. If it is `UTC` and the user has not said they work in UTC, ask once which timezone they mean. Tell them it is changed in the Bolta dashboard workspace settings; no tool changes it. Do not guess from your own locale.
- **Safe Mode on.** Everything goes through review, immediate publishing is blocked, and `schedule-post` on an approved post can bounce it back to Pending Approval. Say so, so the user is not surprised later. No tool turns Safe Mode off; the dashboard does. Never suggest turning it off to get past a refusal.
- `autonomy_mode` is read-only context: report it, do not interpret it beyond what the user asks.

### 3. Permissions: `get-my-capabilities(workspace_id)`
Report which actions are allowed and, for each denied one, `denied_by`: `role`, `workspace_plan` or `key_scope`. Never state a role requirement from memory. Two cautions: the key's scopes come from the role of the person who authorized the connector, so a read-only connection means that person had read-only access; and the matrix can say "allowed" for an action the server later refuses. If a write is refused with a sentence, relay the server's sentence (see references/errors.md); do not argue with it.

### 4. Accounts: `list-accounts(workspace_id)`
Show a short table: platform, username, `token_status`. Possible values are `valid` and `invalid`; an `invalid` account is silently dropped from publishes, so it is a blocker.
- **No accounts at all** blocks publishing. **An invalid account** blocks that platform. Either way call `get-connect-link(workspace_id, platform="...")` and give the user the URL.
- Say plainly: connecting an account is an OAuth flow that must be completed in the user's browser on bolta.ai. It cannot happen inside this conversation, and you cannot do it for them.
- **The link carries no workspace id.** The Bolta dashboard connects to whichever workspace is selected in the browser. Before they click, ask them to check the workspace switcher in the dashboard shows "<workspace name>". For agencies this is the step that decides whether the account lands on the right client.
- Facebook Pages and LinkedIn organizations appear as extra rows (`is_page`, `is_organization`) that inherit the parent's `token_status`; reconnecting the parent fixes them. Ignore `connected_platforms` in the connect-link result for Facebook; `list-accounts` is the truth.
- When the user says they finished, call `list-accounts(workspace_id, platform="...")` again and confirm. Do not take it on faith. If it still shows `invalid`, say so and ask them to retry the connection; do not claim success.
- Buckets and "post to my X bucket" belong to accounts-and-buckets.

### 5. Voice: `get-voice-context(workspace_id)`
- A "No voice profile" 404 means the workspace has none yet. Otherwise read `missing_fields` (it can list `business.overview`, `writing.tone`, `writing.persona`, `business_dna`) and `feedback_count`.
- Report it honestly: the voice is rules (tone, persona, dos and don'ts), not example posts, so copy you write from it follows rules only. Bolta's own drafting learns from the user's approvals and edits; text you write is also stamped as an AI draft, so the user's approvals and edits of it feed the same learning.
- Do not run `extract-business-dna` from here. It fetches the open web and spends AI credits. Offer to continue in brand-voice-setup, which confirms that first.

### 6. Routines (only if the routine tools are available to you)
If `list-routines` is not among your tools, skip this step and say nothing about routines. Otherwise call `list-routines()` (it takes no `workspace_id`) and report counts by status: `draft`, `active`, `paused`. A draft does nothing until activated. Do not create or activate anything during setup unless the user asked for something recurring; if they did, hand off to routines. Output from routines lands in the review queue (approvals).

### 7. Close
Give a short readiness report and name what the workspace is ready for:

```
Workspace: Acme Co (timezone Australia/Sydney, Safe Mode off)
Accounts: LinkedIn valid, X valid, Instagram INVALID (reconnect link sent)
Voice: profile "Acme" found; missing: business_dna
Routines: none
Ready for: drafts on LinkedIn and X. Blocked: Instagram until reconnected.
```

If everything is fine, say what to do next: draft a first post (social-publishing), plan a week (content-planning) or set up the voice (brand-voice-setup).

## When another skill hands you an error

Do not retry the failing call. Read the body of the result: `ok`, `error`, `error_kind`, and inside `data` the `error_code` or `code`, plus `next_step` on successes. The host's `isError` flag is unreliable (auth failures arrive as ordinary results), and some tools return only the text `Error: <message>`, so match on the message as well as the code. Then find the row in references/errors.md and do exactly that row's action. The six you will meet most:

| You see | Do |
|-|-|
| "Invalid API key", "API key expired", "API key inactive", "Not authenticated" | Reconnect (below). Do not retry. |
| "Approval required: an assistant may only schedule a post that has been explicitly approved ..." | Not an outage. Follow the publishing ladder in social-publishing: submit for review, get the user's approval of that exact post, then `approve-post`. Do not try another tool to get around it. |
| `stale_review` | The post changed. Re-read it, show the user the current text, get a fresh decision, retry once with the fresh `expected_fingerprint`. See approvals. |
| `hunter_plan_required` | Replying to conversations and finding customers need a Premium plan. Stop and tell the user; no workaround. |
| `plan_required`, `trial_runs_exhausted` | Upgrade at bolta.ai/pricing. Exception: if the message says "We couldn't verify plan access. Try again in a moment", retry once after a short wait. |
| `workflow_backpressure` | Too many drafts are waiting. Clear the review queue (approvals), then start again. |

Unknown errors: show the user the exact `error` text, say what you did not do, and ask. Do not paraphrase it into something more reassuring.

## Reconnecting

Say which workspace's connection needs it.
- **Claude Code:** run `/mcp`, select the `bolta` server (or the client-specific name) and choose to re-authenticate. The plugin's hook may already have added this instruction after an auth failure.
- **Claude Cowork and chat:** open the Bolta connector in the connector settings, disconnect it if needed and connect it again. Chat has no hook that tells you when the connection died, so watch for the auth messages above.
- When authorizing, the user chooses the workspace; for an agency, make sure it is the right client. Afterwards call `list-workspaces` and confirm the name before doing anything else. Each connection's key lasts 60 days and is normally renewed by the client, so an old connector that suddenly fails is a likely cause.

## Sign-off for regulated teams

"Can anything go out without sign-off?" Read `get-workspace` (`safe_mode`, `autonomy_mode`) and `get-my-capabilities`, and answer from what they show. With Safe Mode on, nothing publishes immediately and posts wait for approval in Bolta. But a chat connection can approve on behalf of the connected user: if that user is an admin or owner, an `approve-post` call from this conversation counts as their approval. If a named person must sign off, tell the user to keep Safe Mode on, leave posts in Pending Approval and approve them in the Bolta Hub, and ask their workspace admin who may approve. Say what the plugin does and does not do: on Claude Code it asks for confirmation before approving, chat has no such prompt, and you cannot show who approved a post or when from here.

## Do not

- Do not retry a typed setup, plan, gate or auth error, and do not call a different tool to reach the same effect.
- Do not say an account is connected, or that setup is done, before `list-accounts` confirms it.
- Do not run `extract-business-dna`, create a routine or activate one as part of "setup" without the user asking.
- Do not state which role can do what. Read `get-my-capabilities` and the server's own sentence.
- Do not tell the user a connection covers other clients' workspaces, or invent a way to switch workspaces.
- Do not paraphrase an error away; quote it.
