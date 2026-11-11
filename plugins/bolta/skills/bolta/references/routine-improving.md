# Making a Bolta routine better: decisions, recommendations, rejections

Read for "its drafts keep missing", "is it working?", before adding another routine, and after a review pass with several no's. Labels as in [routine-settings.md](routine-settings.md).

## First: are its drafts being decided?

A routine only learns from yes and no. `get-routine` `performance_summary`: `artifacts_created`, `artifacts_approved`, `artifacts_rejected`, `artifacts_published`, `artifacts_awaiting_review`. Decided is approved plus rejected; compare it with created, not created alone.

- Most still waiting: the problem is review time, not the writing. Say it: "It wrote 12; 2 were decided and 10 are waiting." Offer to go through them now ([review](review.md)) or make it smaller. Add no routine and raise no count.
- Undecided drafts are the usual reason a routine seems not to work (advice): check this before changing the writing.
- `recommend-routines` returns `review_load` for the whole brand; `list-inbox-items` (`source="team"`, `status="pending"`) counts what waits.

## Bolta's recommendations for a routine

Every Monday Bolta reviews each routine's last 28 days (at least 3 runs, and 5 decisions before it judges rates). `list-routine-recommendations` (`routine_id` for one) returns rows with `title`, `reason`, `proposed_change` (empty: advice only) and `status` (`proposed`, or `applied`, which can be undone); at most 3 open per routine:

| Says | Changes |
|-|-|
| Most drafts rejected (half or more) | Halves the drafts per run |
| Over half approved only after edits | Nothing: add what you keep changing to its instructions |
| 8 or more waiting | One fewer per run (or pause it) |
| Decided after 3+ days | Nothing: move the run nearer when you review |
| Nothing published | Nothing: approve to get results |
| Every run failed | Nothing: check its accounts and sources ([routine-runs.md](routine-runs.md)) |
| Approved 80%+ and published, none waiting | One more per run |
| On but not run | Nothing: check the schedule |

Show the reason and the exact change; on a yes `decide-routine-recommendation` with `decision: "apply"`. `dismiss` keeps the record; `undo` reverses an applied one.

## Bolta's suggestions for the brand

`list-bolta-suggestions`: one change each, made from approvals, edits and rejections (pause a routine that keeps missing, post less often, move its time). What they are and how to accept or undo one: [routine-improving-suggestions.md](routine-improving-suggestions.md).

## The rejection loop

1. Each no carries the user's reason in their words: `reject-post` `reason` (what is wrong, not what to do instead), plus `categories` that fit (`too_salesy`, `wrong_tone`, `too_long`, `off_topic`, `repetitive`, `no_substance`, `factual_error`, `missing_cta`, `other`). No reason given: ask first; it can't be added afterwards. Bolta's voice learning reads it. A drop with no reason teaches nothing.
2. The same reason twice from one routine: read its recommendations and Bolta's suggestions first. Name the pattern ("Your last 3 were turned down as too salesy"), give Bolta's change, apply only on a yes.
3. Nothing there: offer one change of your own, the smallest that addresses the reason. Wording or facts: one sentence added to `instructions` (current text plus the sentence, sent whole). Topic: `goal`, pillars or a document. Too many: `count`. How it sounds everywhere: the voice ([voice](voice.md)), not the routine.
4. One change, one yes, then read it back. Check again after its next run.

## Always

- Check decisions, not just drafts made, before adding or growing anything.
- Show every change a recommendation or suggestion makes before the yes.
