# bolta.agent.mention

**Version:** 2.0.0  
**Category:** Agent Lifecycle  
**Agent Types:** All  
**Roles Allowed:** All (read-only mode)

---

## Purpose

Handle @mention interactions where users ask agents for quick feedback on posts/drafts.

This is **lightweight agent interaction** — no write permissions, just conversational feedback.

---

## When Used

User @mentions agent in comment:
- "@HypeMan punch up this hook"
- "@QABot does this match our voice?"
- "@AnalyticsBot what performed better last week?"

---

## What This Does

1. Detects @mention in post/draft comments
2. Loads agent in `mention` mode (read-only tools)
3. Agent reads post + comment thread context
4. Agent responds as comment with specific feedback
5. Human applies suggestions or dismisses

---

## Hard Rules

- **MUST** use `mode="mention"` (no write tools)
- **MUST** provide post/draft context to agent
- **MUST** respond as comment (not edit directly)
- **MUST NOT** grant write access (approve, publish, edit)

---

## Agent Behavior

Different agents provide different perspectives:

**@HypeMan (Content Creator):**
- Focuses on engagement, hooks, energy
- "This hook is generic. Try: 'We cut onboarding from 2 weeks to 2 days.'"

**@QABot (Reviewer):**
- Focuses on brand compliance, strategy
- "Remove 'leverage' (not in voice profile). Otherwise approved."

**@AnalyticsBot (Analytics):**
- Provides data context
- "Thursday posts get 2x engagement. Consider rescheduling."

---

## Integration

**Polling endpoint:** `/api/v1/mentions/pending`
**Response format:** Comment on the post/draft
**Typical latency:** < 5 seconds for agent response
