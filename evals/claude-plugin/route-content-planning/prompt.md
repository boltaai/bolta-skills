---
name: route-content-planning
description: 'A dated launch phrased as a plan request. v0.2 routes it to campaign; the user asks to see the plan before anything is saved.'
tags: [smoke, routing]
expected_outcome: 'campaign fires; grounds itself in the workspace; shows the plan around Nov 3 for LinkedIn and X with the size math; saves nothing (no campaign, no drafts) and moves nothing.'
max_turns: 20
timeout_seconds: 300
allowed_tools: [Skill]
---
Plan my content for November around our new cold brew subscription launching November 3rd. LinkedIn and X, about 3 posts a week. Show me the plan before you save anything.
