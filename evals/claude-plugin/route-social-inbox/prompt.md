---
name: route-social-inbox
description: 'One natural phrasing for replies. v0.2 routes it to replies.'
tags: [smoke, routing]
expected_outcome: 'replies fires; reads the review list; shows the reply draft; says it cannot see comments on the user''s own posts; sends nothing.'
max_turns: 15
timeout_seconds: 300
allowed_tools: [Skill]
---
Any new mentions or replies I should answer?
