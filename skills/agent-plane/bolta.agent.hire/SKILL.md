# bolta.agent.hire

**Version:** 2.0.0  
**Category:** Agent Lifecycle  
**Agent Types:** `custom` (typically used by system/onboarding flows)  
**Roles Allowed:** `admin`, `editor`

---

## Purpose

Create and onboard a new AI agent teammate from the marketplace with conversational discovery. This is NOT a form-fill — it's a hiring conversation where the agent proposes its own configuration based on understanding the business.

This skill transforms workspace setup from "configure software" to "hire a team member."

---

## When An Agent Uses This

**Typical context:**
- User says "I want to hire a content creator"
- User browses agent marketplace and selects a preset
- Onboarding flow guides user through agent setup
- System agent (onboarding assistant) uses this skill to instantiate the hired agent

**Agent reasoning:**
- "User selected 'The Hype Man' preset — I need to gather their business context, voice preferences, and content goals"
- "Rather than presenting a form, I'll have a conversation to understand what they need"
- "Once I have enough context, I'll create the agent + jobs in paused state"
- "Then I'll generate a preview draft so they can see the voice before activating"

---

## What This Skill Does

1. **Conversational Discovery:**
   - Asks about business, content goals, target platforms, posting frequency
   - Adapts questions based on agent preset type
   - Agent proposes its own configuration based on responses

2. **Agent Creation:**
   - Instantiates Agent model with type, role, persona from preset
   - Applies user customizations from conversation
   - Sets appropriate model tier (Sonnet/Opus for creators, Haiku for engagement)

3. **Job Setup:**
   - Creates Jobs in `paused` status
   - Pre-fills run_instructions based on conversation
   - Binds voice_profile_id (if exists) or prompts creation
   - Binds account_ids from user selection

4. **Preview Generation:**
   - Generates sample draft using the new agent
   - Shows user what the voice/output will look like
   - Allows voice adjustment before activation

---

## How It Works Differently Than V1

**V1 Approach (Template Loop Setup):**
```
Fill form:
- Name: ___
- Posting frequency: ___
- Topics: ___
- Tone: ___
- Template: ___
→ RecurringTemplate created
```

**V2 Approach (Agent Hiring):**
```
System Agent: "Tell me about your business."
User: "B2B SaaS for project management."

System Agent: "What's your content strategy?"
User: "Thought leadership on remote work."

System Agent: "How often do you want to post?"
User: "3x/week on LinkedIn."

System Agent: "Perfect. I'll set up The Hype Man to:
- Create 3x/week LinkedIn thought pieces on remote work
- Use professional but bold tone
- Focus on actionable insights

Want to see a sample post first?"
→ Agent created with Jobs (paused)
→ Sample draft generated
→ User tweaks voice
→ Jobs activated
```

**The difference:** The agent PROPOSES its own setup. The user confirms or adjusts.

---

## Parameters

### Input

```json
{
  "preset_id": "string (UUID)",          // AgentPreset ID from marketplace
  "workspace_id": "string (UUID)",       // Target workspace
  "conversation_context": {              // Gathered from conversational flow
    "business_description": "string",
    "content_goals": "string",
    "platforms": ["linkedin", "twitter"],
    "posting_frequency": "3x/week",
    "tone_preference": "professional_bold"
  },
  "voice_profile_id": "string (UUID, optional)",  // If already exists
  "account_ids": ["string (UUID)"],               // Social accounts to use
  "agent_name": "string (optional)",              // Override preset name
  "persona_overrides": "string (optional)"        // Customize persona
}
```

### Output

```json
{
  "success": true,
  "agent_id": "string (UUID)",
  "agent_name": "The Hype Man",
  "agent_type": "content_creator",
  "jobs_created": [
    {
      "job_id": "string (UUID)",
      "name": "LinkedIn Thought Leadership",
      "schedule": "cron: 0 9 * * 1,3,5",
      "status": "paused",
      "run_instructions": "Create engaging LinkedIn posts..."
    }
  ],
  "preview_draft_id": "string (UUID, optional)",
  "next_steps": [
    "Review the preview draft",
    "Adjust voice profile if needed",
    "Activate jobs when ready"
  ],
  "activation_url": "/agents/{agent_id}/activate"
}
```

---

## Hard Rules

**MUST:**
- Create agent in database (Agent model)
- Create jobs in `paused` status (Job model)
- Generate preview draft before activation (Post model, status=Draft)
- Bind voice_profile_id to jobs (required for content_creator agents)
- Bind account_ids to jobs

**MUST NOT:**
- Activate jobs immediately (user must explicitly activate)
- Skip preview draft generation (user needs to see voice first)
- Create agent without persona (defaults to preset persona, but must exist)
- Allow content_creator agents without voice_profile_id

**SHOULD:**
- Ask clarifying questions if conversation_context is incomplete
- Suggest voice profile creation if none exists
- Show clear "what you'll get" summary before creation
- Offer voice adjustment after preview

---

## Agent Type Mapping

Different agent types require different conversation flows:

**content_creator:**
- Ask: business, content goals, platforms, frequency, tone
- Bind: voice_profile_id (required), account_ids
- Preview: sample post draft

**reviewer:**
- Ask: review standards, what to flag, approval criteria
- Bind: voice_profile_id (as reference), account_ids (optional)
- Preview: sample review comment

**engagement:**
- Ask: engagement style, escalation rules, response speed
- Bind: voice_profile_id (for brand voice), account_ids
- Preview: sample reply to mention

**analytics:**
- Ask: metrics to track, reporting frequency, format
- Bind: account_ids, reporting schedule
- Preview: sample analytics report

**acquisition:**
- Ask: ICP, outreach style, follow-up rules
- Bind: voice_profile_id (for outreach tone), lead sources
- Preview: sample outreach message

---

## Example: Hiring a Content Creator

**Conversation Flow:**

```
System Agent (using this skill):

"You're hiring The Hype Man — a content creator agent that crafts bold, engaging posts.

Tell me about your business in 1-2 sentences."

→ User responds: "B2B SaaS for async team collaboration."

"Got it. What's your content goal?"

→ User: "Establish thought leadership on remote work."

"Perfect. Which platforms?"

→ User: "LinkedIn mainly, maybe Twitter later."

"How often should The Hype Man post?"

→ User: "3 times per week."

"Great. I'll configure The Hype Man to:
- Create LinkedIn posts 3x/week (Mon, Wed, Fri at 9am)
- Focus on remote work best practices
- Use professional but bold tone (your audience is B2B)

Do you already have a voice profile set up?"

→ User: "No, not yet."

"No problem. I'll create jobs in paused mode. You can set up your voice profile next, then activate.

Want me to generate a sample post so you can see the style first?"

→ User: "Yes."

[Creates agent + jobs (paused) + generates preview draft]

"Here's a sample post The Hype Man would create:
[Shows draft]

Like the voice? You can tweak it in voice settings, then activate The Hype Man's jobs."
```

---

## Integration with Other Skills

**Before this skill:**
- User browses AgentPreset marketplace
- User selects preset (e.g., "The Hype Man")
- User triggers hire flow

**After this skill:**
- `bolta.agent.configure` — Adjust persona, model tier, skills
- `bolta.voice.bootstrap` — Create voice profile if none exists
- `bolta.agent.activate_job` — Activate jobs (preview → schedule → go live)

**Related skills:**
- `bolta.agent.memory` — Agents use this to remember learnings
- `bolta.job.execute` — The execution engine that runs the jobs

---

## Metrics to Track

- **Time to hire** — How long from preset selection to agent creation
- **Activation rate** — % of hired agents that get activated within 7 days
- **Preview satisfaction** — Did user accept/reject preview draft
- **Voice adjustment rate** — % of users who modify voice after preview

---

## Error Handling

**Common scenarios:**

1. **No voice profile exists (content_creator hire):**
   - Pause job creation
   - Guide user to create voice profile first
   - Resume hiring after voice created

2. **No social accounts connected:**
   - Pause job creation
   - Guide user to connect account
   - Resume hiring after account connected

3. **Preset not found:**
   - Show marketplace link
   - Suggest similar agent types
   - Ask user to select valid preset

4. **Insufficient permissions:**
   - Check user role (must be editor/admin)
   - Show clear permission error
   - Suggest who can grant access

---

## Notes

- Agent hiring is an **explicit trust moment** — make it clear what the agent will do
- Jobs start **paused** by default — activation is a separate, deliberate step
- Preview drafts are critical — users need to SEE the agent's work before trusting it
- Voice profile binding is HARD REQUIREMENT for content_creator agents
- The conversational flow makes onboarding feel like hiring, not configuring
