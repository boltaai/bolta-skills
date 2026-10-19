---
name: happy-campaign-done-starts
description: 'C1a, the second message: the user picked accounts on the campaign page. The mocked campaign now has LinkedIn and X, so Claude re-reads it and attempts the start once. Under claude -p that Bolta check is denied.'
tags: [smoke, happy]
expected_outcome: 'Reads the campaign again, sees the two accounts, attempts set-content-campaign-status activate exactly once on that campaign, writes no drafts itself, and says honestly that it has not started yet because the check was not confirmed.'
max_turns: 20
timeout_seconds: 300
allowed_tools: [Skill]
---
Earlier you set up the campaign "New pricing" for Northwind Coffee: Problem / Solution, Oct 19 to Nov 8, 3 images + 1 carousel a week x 3 weeks = 12 drafts, Bolta writes it. You asked me to pick the accounts on its page, bolta.ai/dashboard/campaigns/ca000000-0000-4000-8000-000000000004, and say done.

Done.
