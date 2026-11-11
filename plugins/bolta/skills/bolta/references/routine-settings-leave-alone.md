# Bolta routine settings to leave alone

`create-routine` and `update-routine` accept these, but Bolta sets them, ignores them, or only its own pages can fill them. Read when a user, a copied routine or `get-routine` shows one. The settings that matter: [routine-settings.md](routine-settings.md).

## Set by what the routine makes

- `outcome_category`: `social_posts`, `seo_articles`, `engagement_replies`, `repurposing`, `performance_reporting` or `audience_research`. It must match the routine's kind, so leave it out; Bolta fills it.
- `workflow_definition_key`: never; send `template_key`. Neither changes after saving.
- `update-routine` names the routine by `routine_id`, from `list-routines`. It can't change `status`: switch on, pause and stop have their own calls.

## Stored, never read when it runs

- `capability_keys`: a label, not a permission. Leave it out.
- `conditions`, `guardrails`, `performance_objective`, `autonomy_override`: put the rule in `instructions` instead.
- `destination_config` `behavior` (`save_draft` or `schedule`) and `account_refs`: `schedule` schedules nothing. Posting without asking is `approval_policy: "auto"`, and accounts are `source_bindings`. On update, sending `destination_config` with only `voice_profile_id` resets `behavior` to `save_draft`: harmless.
- `reference_image_url` in `get-routine` `output_config` is a preview of `reference_media_id`; sending it does nothing.
- `time_window` is refused.

## Filled by Bolta's own pages

- App sources in `source_bindings` beyond `provider` and `ref`: `kind` is fixed by the routine; `filters` narrow what an app sends; `meeting_category` (meeting transcripts only: `internal_strategy`, the strictest and the default, `customer_conversation`, `webinar_public`, `sales_call`) decides what may be quoted. Bolta's builder or planner sets them when the app is picked; never guess them.
- A Library-only routine's `library` settings (`per_topic` 1-5, default 2; `voice_mode` `rotate` or `cascade`; `include_images`) belong to the routine Brand > Library makes (bolta.ai/dashboard/knowledge-base?tab=library). `create-routine` refuses that kind; on a post routine `library` takes only `enabled`, `voice_profile_ids` and `send_to_client` ([routine-outputs.md](routine-outputs.md)).
- `trigger_config` comes with app-fed routines; leave it.

## Two people editing

`update-routine` overwrites what it sends. When someone may be editing the same routine on Bolta's page, read `get-routine` just before the change and resend only what changes.

## Always

- Never set a field here to make a rule happen; write the rule in `instructions`.
- Never guess an id or an app setting; ask, or send the user to the routine's page.
