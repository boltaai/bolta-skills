# Bolta routine runs: run now refused, and credits

Read when `run-routine-now` comes back refused, or for credits. Back to the run's state and failures: [references/routine-runs.md](routine-runs.md).

## Run now refused

| Refusal | Say or do |
|-|-|
| `workflow_already_running`, or `started: false` (pressed twice in 30 seconds) | "It's already running." Check `list-routine-runs` once |
| `workflow_backpressure` | Too many drafts wait; decide those first ([review](review.md)) |
| `run_now_member_daily_cap` | A teammate's 25 manual runs a day are used up |
| `routine_invalid` | `detail.errors` names the setting; fix it with `update-routine` |
| `routine_not_runnable`, `routine_not_active` | Paused or a draft: resume or switch it on first |
| `routine_archived` | Stopped for good: copy it instead |
| `hidden_job_paused` | Its writer was paused by hand; switch it back on at bolta.ai/dashboard/agents |

Older outreach routines scan instead; they refuse with `scan_cooldown` (try in a few minutes), `outreach_no_monitors`, `outreach_nothing_to_scan`, or `hunter_plan_required` (needs Premium or Team).

Say the refusal in plain words, never the code, and don't press run now again in a loop.

## Credits

Each run uses credits; no amount is readable here. Out of credits, Bolta pauses the brand's writing and tells the owner; it picks up again once credits are added at bolta.ai/dashboard/settings/billing. Then read `get-routine` again.
