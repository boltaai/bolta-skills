# Grouping what's waiting

Read with [finding what's waiting](review-finding-drafts.md) to sort the numbered list under plain headings.

## The groups

- **From Bolta routine "X":** only if some row has a `workflow_run_id`. `list-routines(status="active,paused")`, then always `list-routine-runs` for each: `last_run` is only the newest run, and drafts from earlier runs still wait. A row whose `workflow_run_id` equals one of that routine's run ids belongs to it; a run's `run_details.artifacts` also list its posts (`id`), so use either link. `why` lines are reasons, never a routine name.
- **From campaign "Y":** `list-content-campaigns(status="draft,scheduled,active,paused,completed")`; for each with `posts_count` above 0, `list-content-campaign-posts`. A row whose `post_id` is in that list belongs to it. That call ignores its status and limit filters, so filter yourself (`has_pending_review`).
- **Library:** rows with `is_library` true or a `library_topic`. Test this first: they also carry a `cascade_name`. See [more decisions](review-more-decisions.md).
- **One idea, N versions:** rows sharing a `cascade_name` (one draft per person or angle). Show the idea once, then each version.
- **Saved by you or me:** everything else ("me" is you, the assistant). Use a teammate's name from `post_creator` when it isn't the user. A leftover row with a `workflow_run_id` is "from Bolta".

## Always

- Follow the house rules in the Bolta skill.
