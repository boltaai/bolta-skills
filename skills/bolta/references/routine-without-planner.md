# Routine without Bolta's planner

Read only when `plan` is an unknown tool. With it, use [routine-planner.md](routine-planner.md): `plan`, `confirm-plan` (saved switched off), then its own yes to switch on.

## Save it switched off

- On the yes to the summary: `create-routine` with `name`, `goal` (their words), `template_key`, `trigger_type: "schedule"`, `schedule: {"interval":"weekly","day":"monday","time":"08:00"}`, the workspace `timezone`, `approval_policy: "review_every_artifact"`, accounts bound, `output_config: {"artifact_type":"post","count":3}` (`platforms` only if they limited networks), `instructions`: their words plus "Never invent facts, numbers, prices or dates." No `activate-routine` yet.
- Say it is saved, switched off: "Saved to Acme, switched off. Switch it on?"

## Switch it on

- Only on their separate yes: `activate-routine`, then read `next_run_at` back in the brand's clock: "Bolta routine on. First drafts Mon Nov 16, 8:00 am (New York). On Monday, say 'what's waiting'."
- Switching on is not running: never `run-routine-now` in the same breath.

## Always

- Follow the house rules in the Bolta skill.
- Say it's on only after `next_run_at` is read back.
