# Looking after a Bolta routine

Read for changes, pausing, stopping, running now and Monday's drafts. Start with `get-routine`. Why it didn't run, a failed or refused run: [routine-runs.md](routine-runs.md). Pictures, the client, stories, Library posts: [routine-outputs.md](routine-outputs.md).

## Change, pause, stop, run now

| They say | Do | Bolta check |
|-|-|-|
| "Make it 2 a week" | `update-routine` with the whole `output_config` | One, except as below |
| "Move it to Tuesday 9" | `update-routine` with `schedule` and `timezone` | Same |
| "Pause it", "hold off this week" | `pause-routine` | Never |
| "Turn it back on" | `activate-routine` (paused, or never switched on) | One, unless set up as ask me first in this conversation |
| "Stop it for good" | `archive-routine` | One. Say first: "This can't be undone. Pausing stops it for now." |
| "Run it now" | `run-routine-now` | One: "Uses credits now. Drafts usually land in a few minutes." |
| "Copy it" | `get-routine`, then `create-routine` with the same settings | As for a new one |

- `update-routine` takes only what changes. `source_bindings`, `output_config` and `destination_config` are replaced whole: read, then resend them complete. Inside `output_config`, `review`, `story` and `library` are kept when left out.
- **A change needs no check** on a routine made here as ask me first, or on one already ask me first when the change resends `approval_policy: "review_every_artifact"`. Resend it only where it is already set.
- "Use my workspace setting" or "post without asking" only on their words: one Bolta check, plus one to switch on. Which routines and brands allow `auto`: [routine-settings.md](routine-settings.md). The brand's rule changes in Bolta: Settings > Rules > Approvals.
- **Schedules:** daily, weekly with a `day`, or monthly (the 1st). Another day of the month, or weekdays: a cron, `{"cron":"0 9 15 * *"}` or `{"cron":"0 9 * * 1-5"}`; "weekdays" is not an interval. After any schedule or clock change, read `next_run_at` back.
- **Voice and reviewers:** `get-routine` `destination_config.voice_profile_id` (empty: brand default) and `default_reviewer_ids`. Change the voice with `update-routine` `destination_config`: the new `voice_profile_id` plus the `account_refs` and `behavior` `get-routine` returned, or those are cleared. Copy both onto a copy.
- Its kind can't change. Make a new one.
- Switching on can be refused (a missing source, a disconnected account, a plan limit, a paused writer). Say the reason; it stays off. Don't retry.
- Pausing: a run already going may still deliver drafts. Stopped, its history stays.
- Run now works only when it's on. While a run is going, or on a second press within 30 seconds (`started: false`), say "It's already running." Check `list-routine-runs` once; don't loop. Other refusals: [routine-runs-refused.md](routine-runs-refused.md).
- Stopping everything at once, campaigns too: [fix](fix.md).

## Monday: what it wrote

1. `list-routine-runs`: the newest runs (50 at most). Each run's drafts are its `run_details.artifacts[].id`.
2. Or list them all: `get-routine` `review_queue[].agent_id`, then `list-inbox-items(source="team", status="pending", agent_id=<that id>, limit=100)`, paging with `offset`, keeping rows whose `workflow_run_id` is one of those runs.
3. Hand the list to [review](review.md). They already wait for a yes: never resend them, or look in the recurring queue.

Drafts sent straight to the client wait on the client, not the team: `get-routine` `review.waiting`. Report routines post nothing: Bolta emails the report. Reply drafts belong to [replies](replies.md).

## Where ideas come from

From the brand's documents, one idea per piece: [routine-settings-output.md](routine-settings-output.md). Dropbox connects in Settings > Integrations.

## Always

- Read `get-routine` before any change, and resend whole what is replaced whole.
- One change per yes; read `next_run_at` back after schedule or switch-on changes.
