# Routine without Bolta's planner

Read only when `plan` is an unknown tool. With it, use [routine-planner.md](routine-planner.md): `plan`, `confirm-plan` (saved switched off), then its own yes to switch on.

## Save it switched off

- Before saving, show one summary using their goal, a creatable template and its defaults. Honor their stated cadence, network and count; propose missing choices for confirmation instead of asking about every field. Ask only what blocks valid setup; never invent account IDs, source bindings or permission. On their yes: `create-routine` with `name`, `goal` (their words), `template_key` and the confirmed choices. Scheduled: send `trigger_type: "schedule"`, the agreed `schedule` and IANA `timezone`; manual: `trigger_type: "manual"`, no schedule.
- Keep `approval_policy: "review_every_artifact"` for draft routines. Bind selected usable accounts when present. With no accounts, compatible review-only drafts may omit social bindings and use the requested `output_config.platforms`; publishing, source, history and company-page requirements still apply. A saved voice or brand record is optional.
- `output_config` includes `artifact_type`; preserve the template count unless they chose another. `instructions`: their words and supplied facts, never invented founder/customer history or results. No `activate-routine` yet.
- Say it is saved, switched off: "Saved to Acme, switched off. Switch it on?"

## Switch it on

- Only on their separate yes: `activate-routine`, then read `next_run_at` back in the brand's clock: "Bolta routine on. First drafts Mon Nov 16, 8:00 am (New York). On Monday, say 'what's waiting'."
- Switching on is not running: never `run-routine-now` in the same breath.

## Always

- Follow the house rules in the Bolta skill.
- Say it's on only after `next_run_at` is read back.
