---
name: happy-campaign-launch
description: 'C1a: a launch sentence that says start. The mocked campaign has no accounts after creation, so Claude must hand off the one Bolta screen and must not start it.'
tags: [smoke, happy]
expected_outcome: 'campaign fires; one create-content-campaign with Problem / Solution, a dated window of 4 weeks or fewer that includes Nov 3, ends_on never null, only known mix keys, the waitlist link; reads it back; the size math with a total; never starts it with no accounts; gives the bolta.ai/dashboard/campaigns/ link and asks the user to say done.'
max_turns: 25
timeout_seconds: 300
allowed_tools: [Skill]
---
We launch new pricing on Nov 3. Get people on the waitlist: bolta.ai/waitlist. Start the campaign.
