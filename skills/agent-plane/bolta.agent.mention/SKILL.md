---
name: bolta.agent.mention
version: 2.0.0
description: Handle @mention interactions where users ask agents for quick feedback on posts and drafts
category: agent
roles_allowed: [Viewer, Creator, Editor, Admin]
agent_types: [content_creator, reviewer, analytics, engagement, custom]
safe_defaults:
  read_only_mode: true
  no_write_permissions: true
tools_required:
  - bolta.get_post
  - bolta.get_voice_profile
  - bolta.add_comment
  - bolta.list_recent_posts
inputs_schema:
  type: object
  required: [agent_id, post_id, mention_comment_id]
  properties:
    agent_id: { type: string, description: "Agent being mentioned" }
    post_id: { type: string, description: "Post or draft where mention occurred" }
    mention_comment_id: { type: string, description: "Comment containing the @mention" }
    context: { type: string, description: "Additional context from the comment" }
outputs_schema:
  type: object
  properties:
    comment_id: { type: string, description: "Response comment ID" }
    response_text: { type: string, description: "Agent's feedback" }
organization: bolta.ai
author: Bolta Team
---

## Goal
Handle @mention interactions where users ask agents for quick feedback on posts/drafts. This is **lightweight agent interaction** with read-only tools for conversational feedback.

## Which Agents Use This
- **content_creator** — Punch up hooks, suggest alternatives, provide creative feedback
- **reviewer** — Check brand compliance, voice profile matching, strategy alignment
- **analytics** — Provide performance context, timing suggestions, data insights
- **engagement** — Suggest engagement tactics, audience resonance predictions
- All agent types can provide their specialized perspective via @mentions

## Hard Rules
1. MUST use read-only mode (no write tools like approve, publish, edit)
2. MUST provide post/draft context to agent
3. MUST respond as comment (not edit directly)
4. MUST NOT grant write access to mentioned agents
5. Response time should be < 5 seconds

## Steps

### 1. Parse mention
- Extract agent name from @mention in comment
- Identify which agent is being requested
- Load mention_comment_id to get user's specific question

### 2. Load context
- `bolta.get_post(post_id)` → get full post content
- Load comment thread for context
- If content job: `bolta.get_voice_profile(voice_profile_id)` for reference

### 3. Invoke agent in mention mode
- Set mode="mention" (read-only tools only)
- Provide context: post content, comment thread, user question
- Agent analyzes and formulates response

### 4. Post response
- `bolta.add_comment(post_id, response_text, reply_to=mention_comment_id)`
- Response appears as threaded reply to original mention

### 5. Return confirmation
- Return comment_id and response_text

## Output
```json
{
  "comment_id": "uuid",
  "response_text": "This hook is generic. Try: 'We cut onboarding from 2 weeks to 2 days.'"
}
```

## Failure Handling
- If agent_id not found: return error "Agent not found"
- If post_id not found: return error "Post not found"
- If agent response times out (> 10s): return "Agent is thinking... check back in a moment"
- If agent has no relevant context: agent responds "I don't have enough context to help with this"

## Agent-Specific Behaviors

**@HypeMan (Content Creator):**
- Focuses on engagement, hooks, energy
- Example: "This hook is generic. Try: 'We cut onboarding from 2 weeks to 2 days.'"

**@QABot (Reviewer):**
- Focuses on brand compliance, voice profile matching
- Example: "Remove 'leverage' (not in voice profile). Otherwise looks good."

**@AnalyticsBot (Analytics):**
- Provides data context, timing suggestions
- Example: "Thursday posts get 2x engagement. Consider rescheduling to Thursday 9am."

**@EngageBot (Engagement):**
- Suggests audience resonance tactics
- Example: "Add a question at the end to boost comment engagement."

## Example Usage

### Scenario: User asks HypeMan to punch up hook
**User comment:** "@HypeMan can you make this hook stronger?"
**Post content:** "We just launched a new feature..."

**Agent response:**
"This hook is announcement-focused. Try benefit-led instead:
'We cut onboarding from 2 weeks to 2 days.'

This is more specific and compelling. Lead with the transformation, not the release."

### Scenario: User asks QABot for voice check
**User comment:** "@QABot does this match our voice?"
**Post content:** "Leverage our platform to optimize your workflow..."

**Agent response:**
"❌ 'Leverage' not in voice profile (avoid corporate jargon)
❌ 'Optimize' too vague
✅ Rest matches voice

Suggestion: 'Use our platform to save 5 hours per week on admin tasks.'"
