# Posting without a yes each time

Read when the user asks for a Bolta routine's or campaign's posts to go out without their yes on each one ("no approval", "just post them"). Only on their words; never offer it, never in a scheduled run. Making review stricter needs none of this.

## Read what decides today

`get-routine`: `approval_policy`, `autonomy_policy_version`, `updated_at`, `effective_policy`. The brand row from `list-workspaces`: `autonomy_mode`, `safe_mode` and, where shown, `connection_automation_permission`. Say the answer in plain words:

- `effective_policy.approval_required` true: "Posts wait for your yes because <`decided_explanation`, in plain words>."
- false: it already posts without asking. Say so and stop.
- `resolution_status` `not_resolved` (it hasn't run yet): "Bolta can tell after the first run."

## What all has to be true

1. **The brand allows it.** A routine can only be stricter than its brand: `autonomy_mode` not manual or assisted, review mode (`safe_mode`) off. Only an owner or admin changes these, at bolta.ai/dashboard/settings. Say what the brand needs and where, once.
2. **The routine asks for it.** `approval_policy`: `auto` (weekly posts, founder stories, customer wins, LinkedIn positions, Square only) or `inherit` (follow the brand).
3. **The brand decides, not an old writer setting.** Routines start on `legacy`, where an older setting on Bolta's writer can decide ahead of the brand (`effective_policy.decided_by` `agent`, or `follows_workspace_candidate` true). `autonomy_policy_version` `owner_v1` hands it to the brand and routine settings. Owner or admin only, one-way. It can loosen on its own: with `inherit` on a brand that allows it, posts stop waiting. Only `review_every_artifact` keeps asking for sure. It approves no draft already waiting.
4. **This connection may do it.** `connection_automation_permission`: `granted`, fine; `not_asked` (connected before the choice), the user's role decides; `not_granted`, it is refused (`automation_not_granted`): "This connection can't turn approval off for Acme. An owner or admin can reconnect this app and tick 'Let this AI app change approval and automation settings for Acme' (Bolta Settings > API, AI app connections), or change it in Bolta." Stop; never retry.
5. **Client sign-off stays.** A brand that needs the client's yes still sends every post to the client.

## The change, on one yes

> From the next run, Weekly posts goes out without your yes, at your posting times. Acme's settings decide this from now on, not the old writer setting, and that can't be undone. The client still signs off. The 3 drafts already waiting still need you. Go ahead?

Then one `update-routine`: `approval_policy: "auto"`, `autonomy_policy_version: "owner_v1"`, `acknowledge_autonomy_migration: true`, `expected_updated_at` (the exact `updated_at` from the `get-routine` they saw). Already `owner_v1`: send only `approval_policy`. `configuration_changed`: someone changed it; read `get-routine` again, show it, ask again; never resend under the old yes.

Read `get-routine` back. Say "posts without asking" only when `effective_policy.approval_required` is false; otherwise say what still decides, from `decided_explanation`. Still `not_resolved`: "Set. Bolta confirms it after the first run; until then treat drafts as waiting for you."

## Campaigns

`update-content-campaign` takes the same: `approval_policy` (`inherit`, `review_every_artifact`, `auto`), `autonomy_override` (`""` follows the brand; `manual`, `assisted`, `auto`, `aggressive` are only ever stricter), and the move with `autonomy_policy_version: "owner_v1"`, `acknowledge_autonomy_migration: true` and `expected_updated_at` from `get-content-campaign`. Older campaigns always ask first until moved. Same yes, same read-back (`effective_policy`).

## Always

- One yes for this change alone, separate from "Turn it on?".
- Read Bolta back before saying anything posts without asking.
- A refusal naming the role, the brand or this connection: say it plainly and stop.
