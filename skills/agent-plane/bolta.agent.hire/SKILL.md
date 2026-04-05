---
name: bolta.agent.hire
version: 2.0.0
description: Create and onboard a new AI agent teammate from marketplace presets with conversational discovery and preview generation.
category: agent_lifecycle
roles_allowed: [Editor, Admin]
safe_defaults:
  jobs_start_paused: true
  require_preview_approval: true
tools_required:
  - bolta.get_workspace_policy
  - bolta.get_my_capabilities
  - bolta.get_voice_profile
  - bolta.list_agent_presets
  - bolta.create_agent
  - bolta.create_job
  - bolta.draft_post
  - bolta.get_business_context
inputs_schema:
  type: object
  required: [workspace_id, preset_id]
  properties:
    workspace_id: { type: string }
    preset_id: { type: string, description: "Agent marketplace preset (e.g., 'hype_man', 'qa_bot')" }
    business_context: { type: string, description: "Business description from conversation" }
    content_goals: { type: string, description: "Content strategy from conversation" }
    posting_frequency: { type: string, description: "e.g., '3x/week', 'daily'" }
    platform_ids: { type: array, items: { type: string } }
    voice_profile_id: { type: string, description: "Existing voice profile or null to create new" }
    custom_persona: { type: string, description: "User-requested persona adjustments" }
outputs_schema:
  type: object
  properties:
    agent_id: { type: string }
    job_ids: { type: array, items: { type: string } }
    preview_post_id: { type: string }
    status: { type: string, enum: [paused, ready_to_activate] }
    next_step: { type: string }
organization: bolta.ai
author: Max Fritzhand
---

## Goal
Hire and configure a new AI agent teammate from marketplace presets using conversational onboarding instead of forms.

## Which Agent Types Use This
- **custom** (system/onboarding flows)
- Typically triggered by user selecting preset in marketplace UI

## Hard Rules
1. Jobs MUST start in `paused` status — never auto-activate without preview approval.
2. MUST generate preview draft before allowing activation.
3. If no voice_profile_id provided, MUST prompt user to create one before agent activation.
4. Never create agents without explicit user intent (no auto-hiring).

## Steps

### 1. Check policy & capabilities
- `bolta.get_workspace_policy(workspace_id)` → verify agent hiring allowed
- `bolta.get_my_capabilities(workspace_id)` → verify Editor/Admin role

### 2. Load marketplace preset
- `bolta.list_agent_presets()` → get available presets
- Find preset by `preset_id` (e.g., "hype_man", "qa_bot", "analytics_pro")
- Extract default configuration:
  - `agent_type` (content_creator, reviewer, analytics, etc.)
  - `default_persona` (personality + behavioral guidelines)
  - `recommended_model_tier` (Sonnet/Opus for creators, Haiku for engagement)
  - `default_job_templates` (job types this agent excels at)

### 3. Gather business context (conversational)
- Load existing: `bolta.get_business_context(workspace_id)`
- If missing or incomplete, conduct discovery conversation:
  - "Tell me about your business" → business_context
  - "What's your content strategy?" → content_goals
  - "How often do you want to post?" → posting_frequency
  - "Which platforms?" → platform_ids
- Store responses for agent configuration

### 4. Validate voice profile
- If `voice_profile_id` provided:
  - `bolta.get_voice_profile(voice_profile_id)` → verify it exists
- If null:
  - Prompt user: "This agent needs a voice profile to match your brand. Create one now?"
  - Link to `bolta.voice.bootstrap` flow
  - BLOCK agent creation until voice exists

### 5. Create agent
- `bolta.create_agent({
    workspace_id,
    type: preset.agent_type,
    name: user_chosen_name || preset.default_name,
    persona: custom_persona || preset.default_persona,
    model_tier: preset.recommended_model_tier,
    voice_profile_id,
    enabled_skills: preset.default_skills
  })`
- Returns `agent_id`

### 6. Create jobs (paused)
- For each job template in preset.default_job_templates:
  - `bolta.create_job({
      workspace_id,
      agent_id,
      run_instructions: fill_template(template, {business_context, content_goals}),
      schedule: derive_schedule(posting_frequency),
      status: "paused",
      metadata: {source: "agent_hiring"}
    })`
  - Collect `job_ids`

### 7. Generate preview draft
- Use the newly created agent to generate a sample post:
  - `bolta.draft_post({
      workspace_id,
      agent_id,
      voice_profile_id,
      account_ids: platform_ids,
      prompt: "Create a sample post to demonstrate your voice and style",
      requested_action: "draft_only",
      metadata: {preview_draft: true}
    })`
- Returns `preview_post_id`

### 8. Return for user review
- Status: `paused` (jobs not active yet)
- Show user:
  - Agent name and persona
  - Job schedule and instructions
  - **Preview draft** (critical — user sees actual output before activation)
- Next step: "Review preview. If you like it, activate jobs. If not, adjust voice or persona."

## Output
```json
{
  "agent_id": "uuid",
  "job_ids": ["job-uuid1", "job-uuid2"],
  "preview_post_id": "draft-uuid",
  "status": "paused",
  "next_step": "Review preview draft (ID: draft-uuid). If approved, call bolta.agent.activate_job."
}
```

## Failure Handling
- If voice_profile_id missing and user declines creation: fail with clear message.
- If preview draft generation fails: agent still created but jobs remain paused, add warning.
- If job creation fails: agent created but incomplete, return partial job_ids + error details.
- Never auto-activate jobs on partial failures.

## V2 Agent Context

**Why conversational instead of forms?**

Hiring an agent should feel like hiring a team member, not configuring software. The conversation:
1. Gathers context naturally
2. Lets the agent propose its own setup
3. Adapts based on user's business
4. Shows a preview before activation

**Example conversation flow:**
```
System: "You selected The Hype Man. Tell me about your business."
User: "B2B SaaS for project management."

System: "What's your content strategy?"
User: "Thought leadership on remote work."

System: "How often do you want to post?"
User: "3x/week on LinkedIn."

System: "Perfect. I'll set up The Hype Man to create 3x/week LinkedIn 
thought pieces on remote work. Let me generate a sample post first..."

[Preview draft generated]

System: "Here's a sample. Like the voice? If yes, I'll activate the jobs."
```

## Example Usage

### Scenario: Hire Content Creator
```json
{
  "workspace_id": "uuid",
  "preset_id": "hype_man",
  "business_context": "B2B SaaS for project management",
  "content_goals": "Thought leadership on remote work",
  "posting_frequency": "3x/week",
  "platform_ids": ["linkedin-uuid"],
  "voice_profile_id": "uuid"
}
```

**Result:**
- Agent created (The Hype Man)
- 1 job created (3x/week LinkedIn content)
- Preview draft generated
- Jobs paused until user approves preview
