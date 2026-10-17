---
name: route-approvals
description: 'One natural phrasing for approvals.'
tags: [smoke, routing]
expected_outcome: 'approvals fires; reads the inbox; shows the items; approves nothing.'
max_turns: 15
timeout_seconds: 300
allowed_tools: [Skill]
---
What's waiting for my approval?
