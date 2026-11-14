# Posting without a yes each time

Read when the user asks for a Bolta routine's or campaign's posts to go out without their yes on each one ("no approval", "just post them"). Only on their words; never offer it, never in a scheduled run.

## One rule decides

The brand's automation level (`autonomy_mode`) and review mode (`safe_mode`) are the ceiling. A routine's or campaign's `approval_policy` (`inherit`, `auto`, `review_every_artifact`) and a campaign's `autonomy_override` (`""` follows the brand; `manual`, `assisted`, `auto`, `aggressive`) can only be stricter. Client sign-off still applies. An older writer setting no longer decides.

## Read what decides today

`get-routine` (or `get-content-campaign`): `approval_policy`, `updated_at`, `effective_policy`. The brand row from `list-workspaces`: `autonomy_mode`, `safe_mode` and, where shown, `connection_automation_permission`. Say it in plain words:

- `effective_policy.approval_required` true: "Posts wait for your yes because <`decided_explanation`, in plain words>."
- false: it already posts without asking. Say so and stop.
- `resolution_status` `not_resolved` (it hasn't run yet): "Bolta can tell after the first run."

## Work out every change, ask once

1. **This connection may do it.** `connection_automation_permission` `not_granted`: refused (`automation_not_granted`): "This is switched off for this app on Acme. An owner or admin can turn it on in Bolta (Settings > API > AI app connections)." Follow `what_to_do`; stop; never retry. `granted` or `not_asked`: the user's role and yes decide.
2. **The brand.** `autonomy_mode` manual or assisted, or `safe_mode` on: it must go to Auto.
3. **The routine or campaign.** `approval_policy` to `auto` (routines: weekly posts, founder stories, customer wins, LinkedIn positions, Square only); a campaign's stricter `autonomy_override` to `""`.

Put everything needed in one plain sentence and one question:

> To post this without asking you, I'll switch Acme to Auto and set Weekly posts to publish on its own. The client still signs off, and the 3 drafts already waiting still need you. OK?

Leave out the brand part when the brand already allows it.

## On one yes, make all of them

1. Brand, if needed: `set-brand-approval` preview (no `acknowledge`), then the same call with `acknowledge: true` ([brand approval](connect-brand-approval.md)). If the preview shows more publishing without review than the sentence said (`newly_without_review`), show that and ask again before acknowledging.
2. `update-routine` (or `update-content-campaign`): `approval_policy: "auto"` and `expected_updated_at` (the exact `updated_at` they saw). `configuration_changed`: someone changed it; read again, show it, ask again; never resend under the old yes.
3. Read `get-routine` back. Say "posts without asking" only when `effective_policy.approval_required` is false; otherwise say what still decides, from `decided_explanation`. Still `not_resolved`: "Set. Bolta confirms it after the first run; until then treat drafts as waiting for you."

Tightening a campaign or routine (`review_every_artifact`, a stricter `autonomy_override`) needs only their yes, nothing else.

## Always

- This yes is separate from "Turn it on?".
- These settings are Bolta's rule for a Bolta routine's or campaign's own runs. They never approve, schedule or publish a post from this app (that needs a yes on its exact text) and never skip a client's sign-off.
- Read Bolta back before saying anything posts without asking.
- A refusal naming the role or this connection: say it plainly and stop.
- No draft already waiting is approved by this.
