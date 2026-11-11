# Bolta routine runs: state, why, and fixing a failed one

Read for "why didn't it run?", "it failed", a refused run now, credits, or Bolta's suggestions. Start with `get-routine`, then `list-routine-runs`.

## Its state

`get-routine` `display_state` is the one to say: `archived`, `draft` (never switched on), `blocked`, `paused`, `failed` (last run), `waiting` (drafts wait for a yes), `running`, `on_track`. A paused one still shows its waiting count.

- **Paused**, by `pause_reason`:

| `pause_reason` | Say |
|-|-|
| `plan_gate` | "Your plan doesn't include this routine right now. Upgrade at bolta.ai/pricing." |
| `trial_quota` | "Your trial's runs are used up." |
| `disconnected_source` | "An account it uses got disconnected. Reconnect it, then it can go back on." ([connect](connect.md)) |
| `user_requested`, `user` | "Someone paused it. Turn it back on?" |
| `backpressure` | "Too many drafts are waiting." Decide those ([review](review.md)), then `activate-routine` to resume. |
| `system` | Bolta paused it; try `activate-routine` once, then say what came back. |

- **Blocked**: Bolta's writer for it is paused. `blocked.paused_by` holding `billing` means the plan is paused or unpaid; otherwise "Bolta's writer for this is paused, so it can't run. Switch it back on at bolta.ai/dashboard/agents."

## Why a run went wrong

In `list-routine-runs`, each run's `status` is `running`, `awaiting_approval` (drafts wait for a yes), `scheduled`, `completed`, `partial` (some didn't make it), `failed` or `cancelled`. Read `error_code` and `error_summary`; paraphrase the summary, it can be a raw error. `cancelled` with `run_skipped`: Bolta chose not to write; the summary says why (for example no business details and no topic). A run's drafts are its `run_details.artifacts[].id` (`type` `post`).

No run at all, say the first that fits:

- Off or never switched on: "It's off. Turn it on?"
- No schedule: "It only runs when you ask. Run it now, or give it a schedule?"
- On, `next_run_at` empty: the schedule can't fire. Fix it with `update-routine` and read `next_run_at` again.
- Missed slot: "Bolta skipped that slot. Usually: its source didn't change, a plan limit, too many drafts waiting, or it was already running."
- A slot over 6 hours late is skipped, not caught up; the next runs as normal.
- Late drafts around 17:45-18:15 UTC (say it in their clock): Bolta's servers are busy then, not the user or the routine.
- A disconnected account: [connect](connect.md) for the link.
- It ran, nothing went out: the drafts wait for your yes ([review](review.md)).

## Run now refused, or out of credits

A refused `run-routine-now` or credits run out: [routine-runs-refused.md](routine-runs-refused.md).

## Fix a failed run

1. `get-routine` and `list-routine-runs`.
2. Explain in 2-4 plain sentences what went wrong.
3. Propose one change, to `goal`, `instructions`, `schedule` with `timezone`, or the one setting the error names (no reply `topics`; `auto` where the routine can't post without asking: back to ask me first). Offer one run after: "Change it and run it now? Uses credits."
4. On that one yes: `get-routine` again, `update-routine` (an `instructions` change is the current text plus the new sentence, sent whole), `run-routine-now`.

Example, a skipped run: "Monday's run skipped: Bolta doesn't know what the business does yet, and this routine has no topic, so it didn't write generic posts. Add 'Write about our spring workshops' to its instructions and run it once now? Uses credits." Steps: [fix-a-failed-run](../examples/fix-a-failed-run.json).

A disconnected account or an app to connect: [connect](connect.md).

## Bolta's weekly recommendations

Read and apply them, on a yes: [routine-improving.md](routine-improving.md). Deeper results: [results](results.md).

## Always

- Say what went wrong in plain words before proposing any fix.
- One change, one yes, then read it back.
