# Bolta routine settings: what, when, who decides

Top-level settings of `create-routine` and `update-routine`; `output_config`: [routine-settings-output.md](routine-settings-output.md). Labels: **Bolta**, Bolta's rule or default; **seen**, what customers keep (never quote counts); **advice**, judgement.

[Setup](routine-preferences.md).

## What it is

- `name` (required, up to 255): "Weekly LinkedIn, hiring". Display only.
- `goal` (required, up to 2000): their words, audience plus purpose: "Help clinic owners see why posture coaching beats one-off treatment." Never invent one. Not a dated event: it repeats every run. Bolta's sample goals ("Post consistently each week") count as no topic, so with no brand details the run is skipped (Bolta).
- `instructions` (up to 8,000; 4,000 on an older Bolta): the brief for every run: tone, words to avoid, facts to use, "Never invent facts, numbers, prices or dates." A `goal` or `instructions` starting "reply to…", "respond to…" or "draft replies" is refused on a post routine (`reply_workflow_required`): reword it as a topic, or use a reply routine.
- `template_key`: what it makes ([routine-templates.md](routine-templates.md)). It never changes: another kind is a new routine. Leave `workflow_definition_key` and `outcome_category` out.

## When it runs

- `trigger_type`: `schedule`, `manual` or `source_event`. Default `manual`, unless a create sends a `schedule`. Send `schedule` for anything that repeats: manual runs only on run now (seen: 5 of 6 manual routines never ran). `source_event` is for routines fed by an app.
- For `schedule`, both `schedule` and `timezone` are required; the zone has no fallback: [routine-schedules.md](routine-schedules.md). Honor the user's cadence; unknown day, time or network is a question, not a web default. A cron Bolta can't read is refused at save.

## Where it posts

- `source_bindings` (up to 25, replaced whole on update): `[{"provider":"social_account","ref":"<id from list-accounts>"}]`. Bind selected usable accounts; never silently target others. With no accounts, compatible review-only drafts may omit these and use requested `output_config.platforms`. Source, published-history and company-page requirements remain. Apps belong to this brand; Drive uses a selected file id read through its grant, not a connection id.

## Who decides

- `approval_policy`: `review_every_artifact` ("ask me first", Bolta's default on every post routine: use it), `inherit` (the brand's Approvals setting; the only choice for reports), `auto` (posts without asking).
  - `auto` only on their words, and only on `weekly_social_posts`, `founder_story_series`, `customer_win_social_proof`, `linkedin_thought_leadership` and `square_service_spotlight`; anywhere else it is refused at save, and one saved earlier fails every run (`unsupported_execution_mode`): switch it to ask me first.
  - Also refused while the brand's `safe_mode` is on or its `autonomy_mode` (`list-workspaces`) is manual or assisted. Client sign-off still reviews everything. `auto` turns off sending straight to the client. The brand is the ceiling: [no-approval](routine-no-approval.md).
- `default_reviewer_ids` (up to 20): teammates who review its drafts, ids from `list-workspace-members`; client reviewers are refused. Left out: the brand's default reviewer. On update it replaces the list; `[]` restores the default.
- `destination_config`: `{"voice_profile_id":"<id from get-voice-context all_profiles>"}`, an optional voice of this brand; left out, available default context applies. Compatible drafts need no saved voice or brand record. Accepted by Bolta's main writer, research series and weekly articles; other kinds may refuse it. First-person founder stories still need real owner-supplied events and permission to retell them; a voice is not factual evidence.

## Settings that do nothing

`capability_keys` and `destination_config` `behavior` and `account_refs` are stored, never read. `conditions`, `guardrails`, `performance_objective` and `autonomy_override` show in `get-routine` but these tools don't take them. Use `instructions`. More: [routine-settings-leave-alone.md](routine-settings-leave-alone.md).

## Always

- Honor the agreed trigger, network and review policy; only scheduled work needs a schedule and timezone. Keep selected usable accounts scoped to this brand.
- Put every rule in `instructions`, written as the user said it.
