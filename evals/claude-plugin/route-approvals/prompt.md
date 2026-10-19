---
name: route-approvals
description: 'One natural phrasing for the review list. v0.2 routes it to review.'
tags: [smoke, routing]
expected_outcome: 'review fires; reads the review list; shows the items; approves nothing.'
max_turns: 15
timeout_seconds: 300
allowed_tools: [Skill]
---
What's waiting for my approval?
