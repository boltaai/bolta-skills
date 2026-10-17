---
name: verdict-draft-campaign
description: 'C3: the verdict on a campaign Claude wrote (never started, so the dashboard shows it as not started) whose dates have passed, next to a finished one that must not be added to it.'
tags: [smoke, happy]
expected_outcome: 'results or campaign fires; reads the campaign fresh; says how it ran (5 of 6 went out), per account (LinkedIn 3, X 2), a plain verdict and one next step; never finishes or changes the campaign; never adds the two campaigns together.'
max_turns: 20
timeout_seconds: 300
allowed_tools: [Skill]
---
How did the pricing launch do?
