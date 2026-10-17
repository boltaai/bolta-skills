---
name: route-social-inbox
description: 'One natural phrasing for social-inbox.'
tags: [smoke, routing]
expected_outcome: 'social-inbox fires; reads the inbox; shows the reply draft; states it cannot see comments on the user''s own posts; sends nothing.'
max_turns: 15
timeout_seconds: 300
allowed_tools: [Skill]
---
Any new mentions or replies I should answer?
