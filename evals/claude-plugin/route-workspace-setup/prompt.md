---
name: route-workspace-setup
description: 'One natural phrasing for a set-up check. v0.2 routes it to connect (or today, or start for a first session).'
tags: [smoke, routing]
expected_outcome: 'connect, today or start fires; reads the workspace and accounts; reports the time zone, the disconnected Instagram account and a reconnect link; changes nothing.'
max_turns: 15
timeout_seconds: 300
allowed_tools: [Skill]
---
I just connected Bolta. Can you check that everything is set up properly?
