# Bolta routine runs: run now refused, and credits

Read when `run-routine-now` comes back refused, or for credits. Back to the run's state and failures: [references/routine-runs.md](routine-runs.md).

## Run now refused

| Refusal | Say or do |
|-|-|
| `workflow_already_running`, or `started: false` (pressed twice in 30 seconds) | "It's already running." Check `list-routine-runs` once |
| `workflow_backpressure` | Too many drafts wait; decide those first ([review](review.md)) |
| `run_now_member_daily_cap` | Teammates' 25 manual runs a day (shared by everyone but the owner) are used up |
| `routine_invalid` | `detail.errors` names the setting; fix it with `update-routine` |
| `routine_not_runnable`, `routine_not_active` | Paused or a draft: resume or switch it on first |
| `routine_archived` | Stopped for good: copy it instead |
| `hidden_job_paused` | Its writer was paused by hand; switch it back on at bolta.ai/dashboard/agents |

## Refused on a setting

Bolta refuses these before a run starts: `run-routine-now` returns the code, and a scheduled slot refused this way leaves no run in `list-routine-runs` (a missed slot). On, with no new runs: check the settings below against `get-routine`.

| Code | Means | Fix, on a yes |
|-|-|-|
| `unsupported_execution_mode` | Set to post without asking, which this routine can't do | `update-routine` `approval_policy: "review_every_artifact"` |
| `invalid_objective` | Something it needs is missing; on a reply routine, its `topics` | Add it: the whole `output_config` ([routine-settings-output.md](routine-settings-output.md)) |
| `source_unavailable`, `source_unchanged` | Its page or app couldn't be read, or hasn't changed (a scheduled run) | A page that changes, or reconnect the app |
| `company_page_required` | Needs a LinkedIn page bound | Bind the page's account |

## A save refused

`create-routine` or `update-routine` refused as `invalid_routine`: `detail.errors` lists every problem; fix them all in one call. `reply_workflow_required`: a line of `goal` or `instructions` asks for replies on a post routine; reword it or use a reply routine. A reply routine refused for the brand's plan needs Premium ([routine-templates-replies-reports.md](routine-templates-replies-reports.md)).

Older outreach routines scan instead; they refuse with `scan_cooldown` (try in a few minutes), `outreach_no_monitors`, `outreach_nothing_to_scan`, or `hunter_plan_required` (needs Premium or Team).

Say the refusal in plain words, never the code, and don't press run now again in a loop.

## Credits

Each run uses credits; no amount is readable here. Out of credits, Bolta pauses the brand's writing and tells the owner; it picks up again once credits are added at bolta.ai/dashboard/settings/billing. Then read `get-routine` again.

## Always

- Say the refusal plainly and fix the one setting it names, on a yes.
- Never press run now again in a loop.
