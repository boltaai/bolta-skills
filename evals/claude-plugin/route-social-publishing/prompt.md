---
name: route-social-publishing
description: 'One natural phrasing for writing one post, without saying Bolta. v0.2 routes it to post.'
tags: [smoke, routing]
expected_outcome: 'post fires; a plain Draft is saved on the LinkedIn account with no extra question; nothing moves; the reply names the workspace.'
max_turns: 20
timeout_seconds: 300
allowed_tools: [Skill]
---
Draft a LinkedIn post announcing our Fitzroy roastery opening this spring. I want to see it before anything goes out.
