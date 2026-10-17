---
name: route-workspace-setup
description: 'One natural phrasing for workspace-setup.'
tags: [smoke, routing]
expected_outcome: 'workspace-setup fires; runs the read-only checklist; reports timezone, the invalid Instagram token and a reconnect path; changes nothing.'
max_turns: 15
timeout_seconds: 300
allowed_tools: [Skill]
---
I just connected Bolta. Can you check that everything is set up properly?
