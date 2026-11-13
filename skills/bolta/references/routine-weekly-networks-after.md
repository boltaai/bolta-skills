# A weekly Bolta routine once it's on

Read after a weekly routine is switched on: run it again, times, deleted drafts, the daily email, posts nobody asked for. Setting it up: [routine-weekly-networks.md](routine-weekly-networks.md).

## Never run it again on top of a week

Before `run-routine-now`, read `list-routine-runs` and the scheduled queue (`list-workspace-posts`). The last run's posts still waiting or scheduled:

> This week's 3 posts haven't gone out yet. Running again writes 3 more on the same brief, and both sets would post. Wait for Monday, or should I take this week's off the schedule first?

Run only on a clear yes to one of those. Never as a test after a settings change: show what changed and wait for the next run.

## Times in their clock

- Every time is read back in the brand's clock with its city: "Tue Nov 17, 9:00 am (Denver)".
- An approve result with `what_happened`: say it. `scheduled_local` is a bare brand-clock time (`2026-11-17T09:00`): say it as above, never raw. Without them, `scheduled_time` is UTC: convert it before saying it.
- A yes with no time still schedules Bolta's drafts at the next posting slot. Say so before the yes: "Approving schedules each one at your next posting time."

## Deleted drafts

Deleting a run's drafts is a choice, not a failure. The run may read "You deleted this run's drafts", or failed on an older Bolta; say nothing went wrong. Deleted drafts leave the review list and the daily email. `restore-deleted` brings one back within 7 days ([undo](fix-undo-delete.md)).

## The daily email

Each day Bolta emails the drafts waiting from its runs. It only lists them; deciding happens on the review list. Each person turns it off for themselves at bolta.ai/dashboard/settings/notifications ("Agent Daily Digest"). Nothing here changes it.

## Posts nobody asked for, or two of everything

An older Bolta automation (a job set up at bolta.ai/dashboard/agents before routines) may still be writing. Ask them to pause that job there, with its own switch. Never suggest pausing the writer it belongs to: the Bolta routine writes through the same one, and its runs would then show Blocked ([runs](routine-runs.md)). Nothing here pauses a job.

## Always

- Read the queue before any run now.
- Say every time in the brand's clock, with the city.
