---
name: happy-campaign-claude-writes
description: 'C1b: a one-week, text-only offer the user wants written now. Claude writes it, saves the drafts into a not-started campaign, and never starts it.'
tags: [smoke, happy]
expected_outcome: 'campaign fires; create-content-campaign with Offer & Promotion ending on the Friday; one all-Draft batch on LinkedIn; status polled; the created post ids attached to the campaign; never started; no price but 20% and no link the user did not give.'
max_turns: 30
timeout_seconds: 300
allowed_tools: [Skill]
---
Plan a one-week, text-only promo for our 20% off sale ending Friday on LinkedIn. Write all the posts now.
