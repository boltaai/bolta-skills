# Looking after a Bolta routine

Read for changes, pausing, stopping, running now, Monday's drafts and "why didn't it run?". Start with `get-routine`.

## Change, pause, stop, run now

| They say | Do | Bolta check |
|-|-|-|
| "Make it 2 a week" | `update-routine` with the whole `output_config` | One, except as below |
| "Move it to Tuesday 9" | `update-routine` with `schedule` and `timezone` | Same |
| "Pause it", "hold off this week" | `pause-routine` | Never |
| "Turn it back on" | `resume-routine` (paused) or `activate-routine` (never switched on) | One, unless set up as ask me first in this conversation |
| "Stop it for good" | `archive-routine` | One. Say first: "This can't be undone. Pausing stops it for now." |
| "Run it now" | `run-routine-now` | One: "Uses credits now. Drafts land in a few minutes." |
| "Copy it" | `get-routine`, then `create-routine` with the same settings | As for a new one |

- `update-routine` takes only what changes, but `output_config` and `source_bindings` are replaced whole: read, then resend them complete.
- **A change needs no check** on a routine made here as ask me first, or on one already ask me first when the change resends `approval_policy: "review_every_artifact"`. Resend it only where it is already set.
- "Use my workspace setting" or "post without asking" only on their words: one Bolta check, plus one to switch on.
- The kind of routine can't change. Make a new one.
- Switching on can be refused (a missing source, a disconnected account, a plan limit, Bolta paused it). Say the reason; it stays off. Don't retry.
- Pausing: a run already going may still deliver drafts. Stopped for good, its history stays.
- Run now works only when it's on. `started: false` (a second press within 30 seconds) or an already-running refusal: "It's already running." Check `list-routine-runs` once; don't loop.
- Stopping everything at once, campaigns too: `fix`.

## Monday: what it wrote

1. `get-routine`: `review_queue[].agent_id`. `list-routine-runs`: the run ids (newest 50 at most).
2. `list-inbox-items(source="team", status="pending", agent_id=<that id>, limit=100)`, paging with `offset`.
3. Keep rows whose `workflow_run_id` is one of those run ids. Runs carry no post ids, so this match is the only link.
4. Hand the list to `review`. They already wait for a yes: never resend them, or look in the recurring queue.

Report routines post nothing: Bolta emails the report. Reply drafts belong to `replies`.

## "Why didn't it run?"

Read `get-routine` (status, `blocked`, `next_run_at`, `last_run`), then `list-routine-runs`. Say the first that fits:

- Paused or never switched on: "It's off. Turn it on?"
- `blocked`: "Bolta's writer for this is paused, so it can't run. Switch it back on at bolta.ai/dashboard/agents."
- No schedule: "It only runs when you ask. Run it now, or give it a schedule?"
- On, but `next_run_at` is empty: the schedule can't fire (often "monthly"). Change it to a cron and read `next_run_at` again.
- A failed or skipped run: its own reason, in plain words.
- No run at the expected time: "Bolta skipped that slot and didn't record why. Usually: your page didn't change, a plan limit, a disconnected account, or a busy server."
- A slot over 6 hours late is skipped, not caught up; the next runs as normal.
- Drafts late around 17:45-18:15 UTC (say it in their clock): Bolta's servers are busy then, not the user or the routine.
- A disconnected account: `connect` for the link.
- It ran, nothing went out: the drafts wait for your yes (`review`).
