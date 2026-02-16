---
name: bolta.draft.post
version: 1.0.0
description: Create a single draft post using a workspace voice profile and optional template, then route it to Draft or Pending Review based on workspace policy + actor role.
category: creator
roles_allowed: [Owner, Admin, Creator]
safe_defaults:
  never_publish: true
  never_schedule_unless_explicit: true
tools_required:
  - bolta.get_workspace_policy
  - bolta.get_my_capabilities
  - bolta.get_voice_profile
  - bolta.list_templates
  - bolta.render_template
  - bolta.create_post
  - bolta.submit_for_review
inputs_schema:
  type: object
  required: [workspace_id, voice_profile_id, prompt]
  properties:
    workspace_id: { type: string }
    voice_profile_id: { type: string }
    prompt: { type: string }
    template_id: { type: string }
    account_ids: { type: array, items: { type: string } }
    requested_action: { type: string, enum: [draft_only, send_to_review, schedule, publish] }
    suggested_time: { type: string, description: "ISO timestamp; only used if schedule allowed" }
outputs_schema:
  type: object
  properties:
    post_id: { type: string }
    final_state: { type: string, enum: [draft, pending_review, scheduled, published] }
    review_item_id: { type: string }
    notes_for_reviewer: { type: string }
    warnings: { type: array, items: { type: string } }
organization: bolta.ai
author: Max Fritzhand
---

## Goal
Create one post in the user's Brand Voice (or Founder Voice), optionally using a template, and route it safely.

## Voice Profile Modes

### Brand Voice
- Company/brand speaking
- Focus on tone, style rules, vocabulary
- Professional and consistent across content

### Founder Voice (Advanced)
- Founder speaking personally
- Includes founder_signals: beliefs, lessons, contrarian opinions, scars, backstory moments
- More authentic, personal, thought-leadership focused
- founder_signals are injected as constraints in content generation

## Policy Rules (must follow)
1. Always call `bolta.get_workspace_policy` + `bolta.get_my_capabilities` first.
2. If workspace Safe Mode is ON: you MUST NOT schedule or publish directly. Route to `pending_review`.
3. If actor role does not include the required capability for an action (schedule/publish), you MUST NOT attempt it.
4. If `requested_action` is omitted: default to `send_to_review` (pending review) if Safe Mode is ON, otherwise default to `draft`.

## How Voice Profiles Constrain Generation

### Tone Constraints (all modes)
Content generation respects tone scores (playful, professional, direct, thoughtful):
- Tone scores guide sentence structure, vocabulary choice, emoji usage
- Direct tone (9/10) = fewer hedges, more imperatives
- Thoughtful tone (7/10) = more context, nuance, depth

### Style Rules (all modes)
- `dos`: Patterns to follow (lead with pain points, use short sentences)
- `donts`: Patterns to avoid (no corporate jargon, avoid hedging)
- `styleKeywords`: Vocabulary bias (emphasize direct, confident, specific)

### Founder Signals (founder mode only)
When `speakerMode: "founder"` and `founderSignals` provided:
- **Beliefs**: Constraints that shape main arguments
  - Example: If belief is "Ship fast beats planning," posts favor speed over perfection
- **Lessons**: Constraints that shape advice given
  - Example: If lesson is "Users teach more than docs," content leads with user validation
- **Contrarian Opinions**: Constraints that enable pushback
  - Example: If contrarian is "Engagement metrics are vanity," posts optimize for substance over reach
- **Scars**: Constraints that enable vulnerability
  - Example: If scar is "Built feature no one asked for," posts emphasize user research
- **Backstory Moments**: Constraints that enable narrative coherence
  - Example: If backstory is "Spent years ghostwriting," posts demonstrate writing from real experience

**Founder Signal Injection Example:**
```
Prompt: "Write about validating product ideas"
Voice Profile:
  - speakerMode: "founder"
  - beliefs: ["Ship fast", "Users teach more than docs"]
  - lesson: "Build what users ask for"
  - scar: "Built feature no one wanted"

Generated Content Characteristics:
- Opens with user validation (belief: users teach)
- Mentions framework for speed (belief: ship fast)
- Includes personal example of failure (scar: built wrong feature)
- Gives specific, actionable advice (lesson learned)
- Tone: Direct + thoughtful (8/10 and 7/10)

Generated: "Most founders waste months on features no one asked for—here's my 3-question filter..."
(This naturally demonstrates the beliefs/lessons/scars without being forced)
```

## Steps
1. Fetch policy: `bolta.get_workspace_policy(workspace_id)`
2. Fetch capabilities: `bolta.get_my_capabilities(workspace_id)`
3. Fetch voice: `bolta.get_voice_profile(voice_profile_id)`
   - If founder mode: Extract founder_signals for generation constraints
4. If template_id provided:
   - Load template list if needed: `bolta.list_templates(workspace_id)`
   - Render: `bolta.render_template(template_id, {prompt, voice_profile_id})`
   - Use rendered text as the post body.
   Else:
   - Generate body using voice profile constraints:
     - Tone scores (all modes)
     - Style rules (all modes)
     - Founder signals (if founder mode)
     - Custom rules and keywords
5. Create the post:
   - `bolta.create_post({workspace_id, voice_profile_id, account_ids, body, status: "draft"})`
6. Decide route:
   - If Safe Mode ON OR requested_action == send_to_review: submit:
     - `bolta.submit_for_review({workspace_id, post_id, note: "AI draft ready"})`
     - final_state = pending_review
   - Else if requested_action == draft_only OR omitted: final_state = draft
   - Else if requested_action == schedule:
     - Only if capability includes `posts:schedule` AND Safe Mode OFF
     - Call `bolta.schedule_post({post_id, time: suggested_time})`
     - final_state = scheduled
   - Else if requested_action == publish:
     - Only if capability includes `posts:publish` AND Safe Mode OFF
     - Call `bolta.publish_post({post_id})`
     - final_state = published

## Output
Return: post_id, final_state, optional review_item_id, notes_for_reviewer, warnings.

## Failure handling
- If any tool call returns unauthorized/forbidden: downgrade to `pending_review` (if possible) or leave in `draft`.
- Never retry publish/schedule more than once.
