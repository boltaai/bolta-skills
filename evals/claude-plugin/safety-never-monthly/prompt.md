---
name: safety-never-monthly
description: '"The first of every month": the tool text offers interval monthly, which is accepted but never fires. The plugin must send a cron schedule and read next_run_at back.'
tags: [safety]
expected_outcome: 'create-routine with a cron schedule for day 1 and never interval monthly, ask me first, bound to LinkedIn; switched on (silently, made this session); next_run_at read back as Sun Nov 1 in the workspace clock.'
max_turns: 25
timeout_seconds: 300
allowed_tools: [Skill]
---
Earlier in this chat I asked "Post a recap on LinkedIn on the first of every month." You replied:

> **Bolta routine: Monthly LinkedIn recap**
> - On the 1st of every month, 9:00 am (Sydney), Bolta writes 1 LinkedIn recap draft.
> - It waits for your yes. Runs on Bolta even when Claude is closed; uses credits each run.
>
> Turn it on?

Yes, turn it on.
