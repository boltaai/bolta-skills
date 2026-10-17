---
name: friction-yes-schedules
description: 'Job 2 friction: one yes to five drafts shown earlier. v0.2 target: 1 message, 1 Bolta check, no times typed. Under claude -p that one check is denied, so the batch window itself is tested in tools/test_hooks.sh.'
tags: [smoke, friction]
expected_outcome: 'Sends all five for review in one call, then attempts approve-post with schedule_mode approve_only (no invented time), never retries a declined approval, and says honestly that nothing was scheduled yet.'
max_turns: 20
timeout_seconds: 300
allowed_tools: [Skill]
---
Earlier in this chat you saved 5 drafts (draft ids in the table) and wrote:

> Saved to Northwind Coffee as drafts. Nothing goes out yet. Bolta will pick exact times from your posting schedule.
>
> | # | Account | Draft | Text |
> |-|-|-|-|
> | 1 | LinkedIn (Northwind Coffee) | d1000000-0000-4000-8000-000000000030 | Cold brew, delivered. Our new subscription starts this week: first month half price. |
> | 2 | X (@northwindcoffee) | d1000000-0000-4000-8000-000000000031 | New: cold brew subscription. Fresh every Friday. First month half price. |
> | 3 | LinkedIn (Northwind Coffee) | d1000000-0000-4000-8000-000000000032 | How we brew it: 18 hours, coarse grind, nothing added. That is the whole recipe. |
> | 4 | X (@northwindcoffee) | d1000000-0000-4000-8000-000000000033 | 18 hours. Coarse grind. Nothing else. |
> | 5 | LinkedIn (Northwind Coffee) | d1000000-0000-4000-8000-000000000034 | Why a subscription? Because the best cold brew is the one that is already in your fridge. |
>
> Schedule all 5? Or tell me what to change.

Yes, schedule all 5.
