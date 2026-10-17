---
name: negative-calendar
description: '"Don''t trigger": a calendar event, not a Bolta post (Bolta''s "calendar" is where posts show, which can pull a model the wrong way).'
tags: [smoke, negative]
expected_outcome: 'Says it can''t add calendar events from here (or offers what it can do); no Bolta skill fires; nothing is saved or scheduled in Bolta.'
max_turns: 10
timeout_seconds: 300
allowed_tools: [Skill]
---
Add a team lunch to my calendar for Thursday at noon.
