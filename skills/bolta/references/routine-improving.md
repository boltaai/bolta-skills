# Making a Bolta routine better: decisions, recommendations, rejections

Read for "its drafts keep missing", "is it working?", before adding another routine, and after a review pass with several no's. Labels as in [routine-settings.md](routine-settings.md).

## First: are its drafts being decided?

A routine only learns from yes and no. `get-routine` `performance_summary`: `artifacts_created`, `artifacts_approved`, `artifacts_rejected`, `artifacts_published`, `artifacts_awaiting_review`. Decided is approved plus rejected; compare it with created, not created alone.

- Most still waiting: the problem is review time, not the writing. Say it: "It wrote 12; 2 were decided and 10 are waiting." Offer to go through them now ([review](review.md)) or make it smaller. Add no routine and raise no count.
- Seen: in 22 of 28 brands running weekly posts, nobody ever decided a draft. When people decide, 94% are yes.
- `recommend-routines` returns `review_load` for the whole brand; `list-inbox-items` (`source="team"`, `status="pending"`) counts what waits.

## Bolta's recommendations for a routine

Every Monday Bolta reviews each routine's last 28 days (at least 3 runs, and 5 decisions before it judges rates). `list-routine-recommendations` (`routine_id` for one) returns rows with `title`, `reason`, `proposed_change` and `status`:

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

`list-bolta-suggestions` turns approvals, edits and rejections into one change each, for example: pause a routine whose last 3 decided drafts were all no; post less often; move a routine's time to when drafts get moved to; add a phrase the user keeps adding to its brief; carousels of the brand's own photos; only their own photos; a seasonal campaign; reuse best posts. Show its title, reason and every change it lists: accepting can change a voice or schedule, switch a routine on or off, or start a campaign. Only an owner or admin can decide (`can_decide`). On a yes: `decide-bolta-suggestion` `accept`; `undo` works for 7 days.

## The rejection loop

1. Each no carries the user's reason in their words: `reject-post` `reason`, plus `categories` that fit (`too_long`, `wrong_tone`, `off_brand`, `factual_error`, `missing_cta`). A drop with no reason teaches nothing.
2. The same reason twice from one routine: read its recommendations and Bolta's suggestions first. Name the pattern ("Your last 3 were turned down as too salesy"), give Bolta's change, apply only on a yes.
3. Nothing there: offer one change of your own, the smallest that addresses the reason. Wording or facts: one sentence added to `instructions` (current text plus the sentence, sent whole). Topic: `goal`, pillars or a document. Too many: `count`. How it sounds everywhere: the voice ([voice](voice.md)), not the routine.
4. One change, one yes, then read it back. Check again after its next run.

## Always

- Check decisions, not just drafts made, before adding or growing anything.
- Show every change a recommendation or suggestion makes before the yes.
