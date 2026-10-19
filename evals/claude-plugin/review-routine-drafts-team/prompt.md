---
name: review-routine-drafts-team
description: 'R2: the review list holds drafts from a Bolta routine and a campaign as team rows (workflow_run_id matches the routine''s run ids). They must be found and grouped, never looked for in the legacy recurring queue, and the agent''s name never shown.'
tags: [smoke, happy]
expected_outcome: 'review (or today) fires; reads team rows and the routine''s runs; groups the two routine drafts under "Monday LinkedIn tips" and the two campaign drafts under "Know your beans", with full text; decides nothing.'
max_turns: 25
timeout_seconds: 300
allowed_tools: [Skill]
---
What's waiting for me?
