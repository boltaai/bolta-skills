# When a Bolta routine runs: time zone, monthly, weekdays, cron

Set in `schedule` on `create-routine` or `update-routine`; read `get-routine` first when changing one.

- `timezone` is required for a schedule (no fallback): pass the workspace's from `list-workspaces`. Manual and new-source routines don't need one.
- `next_run_at` is UTC; say it in the workspace clock: "First drafts Mon Oct 19, 8:00 am (New York)."
- Every day: `{"interval":"daily","time":"08:00"}`.
- Weekly ("every Monday morning"): `{"interval":"weekly","day":"monday","time":"08:00"}`; a weekly schedule needs its `day`.
- Monthly ("once a month"): `{"interval":"monthly","time":"09:00"}` runs on the 1st; say "First drafts Tue Dec 1, 9:00 am". Another day, or weekdays, is a cron: `{"cron":"0 9 15 * *"}`, `{"cron":"0 9 * * 1-5"}` ("weekdays" is not an interval). A cron is a 5-field string.
- Spread out ("a post Monday, Wednesday and Friday"): `{"cron":"0 9 * * 1,3,5"}`, count 1. `count` is per run, across networks.
- Every other week can't be expressed: offer weekly with a smaller `count`.
- A cron Bolta can't read is refused at save; build crons only from the shapes above.
- Bolta's planner takes `days` and `day_of_month` instead ([routine-planner.md](routine-planner.md)).
- Time-sensitive slots: avoid 17:45-18:15 UTC (say it in their clock), when Bolta's servers are busiest.

## When posts go out: `posting_times`

`schedule` decides when drafts are written; `output_config.posting_times` on `create-routine` or `update-routine` decides when posts go out. `[{"time": "09:00"}]` is every day at 9:00; add a `day` (`monday`, `tuesday`, `wednesday`, `thursday`, `friday`, `saturday`, `sunday`) for one weekday: `[{"day": "tuesday", "time": "09:00"}, {"day": "friday", "time": "09:00"}]`. 24-hour wall clock in the brand's time zone, never a UTC offset; at most 21 times. Each post takes the next free time after the run within 14 days, one post per account per time (a run's posts for different accounts share a time). Leave it out, or send `[]`, for Bolta's best times. `get-routine` reads it back as `posting_times.summary`; none there means best times.

## Always

- Send the brand's `timezone` with every schedule, and say times in that clock.
- Read `next_run_at` back after any schedule change.
