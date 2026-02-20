---
name: bolta.skills.index
version: 2.0.0
description: Bolta Skills Registry - central index of all available skills organized by plane and category
category: registry
type: documentation
roles_allowed: []
agent_types: []
tools_required: []
inputs_schema:
  type: object
  description: "This is a registry index, not a callable skill"
  properties: {}
outputs_schema:
  type: object
  description: "This is a registry index, not a callable skill"
  properties: {}
organization: bolta.ai
author: Bolta Team
---

## Goal
Serve as the central registry and index of all available Bolta skills, organized by plane and category for easy discovery.

## What This Is

The Skills Index is a **registry**, not a callable skill. It provides:
- Complete list of all skills
- Organization by plane (voice, content, review, automation, agent, analytics, engagement, control)
- Quick reference for skill discovery
- Links to individual skill documentation

## Skill Planes

### Plane 0: Voice
- bolta.voice.bootstrap
- bolta.voice.learn_from_samples

### Plane 1: Content
- bolta.draft.post
- bolta.draft_post
- bolta.get_account_info
- bolta.get_business_context
- bolta.get_voice_profile
- bolta.list_recent_posts
- bolta.loop.from_template (deprecated)
- bolta.week.plan

### Plane 2: Review
- bolta.add_comment
- bolta.approve_post
- bolta.reject_post
- bolta.review.approve_and_route
- bolta.inbox.triage
- bolta.review.digest

### Plane 3: Automation
- bolta.cron.generate_and_schedule
- bolta.cron.generate_to_review

### Plane 4: Agent
- bolta.agent.activate_job
- bolta.agent.configure
- bolta.agent.hire
- bolta.agent.memory
- bolta.agent.mention
- bolta.job.execute (documentation)

### Plane 5: Analytics
- bolta.get_audience_insights
- bolta.get_best_posting_times
- bolta.get_post_metrics

### Plane 6: Engagement
- bolta.get_comments
- bolta.get_mentions
- bolta.reply_to_mention

### Plane 7: Control
- bolta.audit.export_activity
- bolta.policy.explain
- bolta.quota.status
- bolta.team.create_agent_teammate
- bolta.team.rotate_key
- bolta.workspace.config

## Usage

This index helps:
- Developers discover available skills
- Agents understand their tool surface
- Users navigate skill documentation
- System builders understand skill organization

For individual skill details, refer to each skill's SKILL.md file in its respective plane directory.
