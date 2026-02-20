---
name: bolta.get_business_context
version: 2.0.0
description: Get business context including products, audience, values, and brand DNA for informed content creation
category: content
roles_allowed: [Viewer, Creator, Editor, Admin]
agent_types: [content_creator, reviewer, analytics, engagement, custom]
safe_defaults: {}
tools_required: []
inputs_schema:
  type: object
  description: "No parameters required - scoped to workspace automatically"
  properties: {}
outputs_schema:
  type: object
  properties:
    success: { type: boolean }
    workspace_name: { type: string }
    business_overview: { type: string }
    brand_values: { type: array, items: { type: string } }
    tone_of_voice: { type: string }
    products: { type: array, items: { type: object } }
    target_audience: { type: string }
    positioning: { type: string }
organization: bolta.ai
author: Bolta Team
---

## Goal
Get business context including products, audience, values, and brand DNA. Use this to understand what the business does and who it serves before creating content.

## Which Agents Use This
- **content_creator** — Understand products and audience before drafting
- **reviewer** — Verify content aligns with business positioning
- **engagement** — Personalize responses based on business context
- All agents need business context for informed decision-making

## Hard Rules
1. MUST be scoped to current workspace automatically
2. SHOULD include products, audience, values, and positioning
3. Cache business context for performance (updates are infrequent)

## Steps

### 1. Load workspace business context
- Query workspace BusinessContext model
- No parameters needed (auto-scoped to workspace)

### 2. Return structured business data
- Business overview
- Brand values
- Tone of voice
- Products with features and target audience
- Target audience and positioning

## Output
```json
{
  "success": true,
  "workspace_name": "Acme Corp",
  "business_overview": "B2B SaaS for async collaboration...",
  "brand_values": ["Speed", "Clarity", "Authenticity"],
  "tone_of_voice": "Professional but bold...",
  "products": [
    {
      "id": "uuid",
      "name": "Acme Platform",
      "description": "...",
      "key_features": ["Feature 1", "Feature 2"],
      "target_audience": "Engineering managers"
    }
  ],
  "target_audience": "B2B SaaS teams 10-50 employees",
  "positioning": "The fastest way to collaborate async"
}
```

## Failure Handling
- If business context not configured: return partial data with warning
- Always return success (empty context is valid for new workspaces)

## Example Usage

### Scenario: Content creator loading context before drafting
```json
{}
```
**Result:** Receive full business context for workspace to inform content strategy
