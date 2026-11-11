# When a Bolta routine runs: time zone, monthly, weekdays, cron

Set in `schedule` on `create-routine` or `update-routine`; read `get-routine` first when changing one.

- `timezone` is required for a schedule (no fallback): pass the workspace's from `get-workspace`. Manual and new-source routines don't need one.
- `next_run_at` is UTC; say it in the workspace clock: "First drafts Mon Oct 19, 8:00 am (New York)."
- Every day: `{"interval":"daily","time":"08:00"}`.
- Weekly ("every Monday morning"): `{"interval":"weekly","day":"monday","time":"08:00"}`; a weekly schedule needs its `day`.
- Monthly ("once a month"): `{"interval":"monthly","time":"09:00"}` runs on the 1st; say "First drafts Tue Dec 1, 9:00 am". Another day, or weekdays, is a cron: `{"cron":"0 9 15 * *"}`, `{"cron":"0 9 * * 1-5"}` ("weekdays" is not an interval). A cron is a 5-field string.
- Spread out ("a post Monday, Wednesday and Friday"): `{"cron":"0 9 * * 1,3,5"}`, count 1. `count` is per run, across networks.
