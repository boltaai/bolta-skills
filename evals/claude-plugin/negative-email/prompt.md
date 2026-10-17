---
name: negative-email
description: '"Don''t trigger": an email, not a social post.'
tags: [smoke, negative]
expected_outcome: 'Drafts the email (or asks what Friday is about) in chat; no Bolta skill fires and nothing is saved to Bolta.'
max_turns: 10
timeout_seconds: 300
allowed_tools: [Skill]
---
Draft an email to my team about Friday.
