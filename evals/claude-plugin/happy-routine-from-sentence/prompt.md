---
name: happy-routine-from-sentence
description: 'R1: a Bolta routine from one sentence, then a yes to its one summary (pasted as the earlier turn). The routine is created as ask me first in this session, so switching it on passes guard v2 silently and the mock answers.'
tags: [smoke, happy]
expected_outcome: 'routine fires; create-routine with weekly_social_posts, an object binding to the LinkedIn account, ask me first, the workspace time zone and no monthly interval; activate-routine reaches Bolta (not denied) and its reply carries next_run_at (get-routine after is optional); no run now; the reply says Bolta routine and reads back the first drafts: Mon Oct 19, 8:00 am (Sydney), never the UTC time.'
max_turns: 25
timeout_seconds: 300
allowed_tools: [Skill]
---
Earlier in this chat I asked "Keep me posting 3 times a week on LinkedIn about hiring." You replied:

> **Bolta routine: Weekly LinkedIn, hiring**
> - Every Monday 8:00 am (Sydney), Bolta writes 3 LinkedIn drafts about hiring.
> - They wait for your yes. Runs on Bolta even when Claude is closed; uses credits each run.
>
> Turn it on?

Yes, turn it on.
