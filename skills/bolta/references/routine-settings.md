# Bolta routine settings: what, when, who decides

Top-level settings of `create-routine` and `update-routine`; `output_config`: [routine-settings-output.md](routine-settings-output.md). Labels: **Bolta**, Bolta's rule or default; **seen**, what customers keep (never quote counts); **advice**, judgement.

## What it is

- `name` (required, up to 255): "Weekly LinkedIn, hiring". Display only.
- `goal` (required, up to 2000): their words, audience plus purpose: "Help clinic owners see why posture coaching beats one-off treatment." Never invent one. Not a dated event: it repeats every run. Bolta's sample goals ("Post consistently each week") count as no topic, so with no brand details the run is skipped (Bolta).
- `instructions` (up to 8,000; 4,000 on an older Bolta): the brief for every run: tone, words to avoid, facts to use, "Never invent facts, numbers, prices or dates." A `goal` or `instructions` starting "reply to…", "respond to…" or "draft replies" is refused on a post routine (`reply_workflow_required`): reword it as a topic, or use a reply routine.
- `template_key`: what it makes ([routine-templates.md](routine-templates.md)). It never changes: another kind is a new routine. Leave `workflow_definition_key` and `outcome_category` out.

## When it runs

- `trigger_type`: `schedule`, `manual` or `source_event`. Default `manual`, unless a create sends a `schedule`. Send `schedule` for anything that repeats: manual runs only on run now (seen: 5 of 6 manual routines never ran). `source_event` is for routines fed by an app.
- `schedule` and `timezone` (both required; the zone has no fallback): [routine-schedules.md](routine-schedules.md). A cron Bolta can't read is refused at save. Weekly, one weekday morning, is the default shape (Bolta's planner: Monday 09:00; seen: 4 of 7 daily routines got paused).

## Where it posts

- `source_bindings` (up to 25, replaced whole on update): `[{"provider":"social_account","ref":"<id from list-accounts>"}]`, one per network. With none, Bolta may post from any connected account. An account on a network the routine doesn't write for is refused. Apps (GitHub, a blog, Square, HubSpot) are bound by Bolta's planner once connected; a Drive file only by picking it on bolta.ai/dashboard/routines.

## Who decides

- `approval_policy`: `review_every_artifact` ("ask me first", Bolta's default on every post routine: use it), `inherit` (the brand's Approvals setting; the only choice for reports), `auto` (posts without asking).
  - `auto` only on their words, and only on `weekly_social_posts`, `founder_story_series`, `customer_win_social_proof`, `linkedin_thought_leadership` and `square_service_spotlight`; anywhere else it is refused at save, and one saved earlier fails every run (`unsupported_execution_mode`): switch it to ask me first.
  - Also refused while the brand's `safe_mode` is on or its `autonomy_mode` (`list-workspaces`) is manual or assisted. Client sign-off still reviews everything. `auto` turns off sending straight to the client. What else decides, and the one-way `owner_v1` move: [no-approval](routine-no-approval.md).
- `default_reviewer_ids` (up to 20): teammates who review its drafts, ids from `list-workspace-members`; client reviewers are refused. Left out: the brand's default reviewer. On update it replaces the list; `[]` restores the default.
- `destination_config`: `{"voice_profile_id":"<id from get-voice-context all_profiles>"}`, a voice of this brand; left out, the brand's default voice. Accepted by post routines on Bolta's main writer (weekly posts, founder stories, customer wins, LinkedIn positions, Square), research series and weekly articles; refused on best-posts, thread, reply and report routines and on those fed by GitHub, a blog, HubSpot, Drive or a meeting. A person's voice for first-person and story routines; else the brand voice.

## Settings that do nothing

`capability_keys` and `destination_config` `behavior` and `account_refs` are stored, never read. `conditions`, `guardrails`, `performance_objective` and `autonomy_override` show in `get-routine` but these tools don't take them. Use `instructions`. More: [routine-settings-leave-alone.md](routine-settings-leave-alone.md).

## Always

- Send `trigger_type: "schedule"`, `schedule`, the brand's `timezone`, bound accounts and `approval_policy` explicitly on every create.
- Put every rule in `instructions`, written as the user said it.
