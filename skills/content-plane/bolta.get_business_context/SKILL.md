# bolta.get_business_context

**Version:** 2.0.0  
**Category:** Content Creation  
**Agent Types:** All  
**Roles Allowed:** All

---

## Purpose

Get business context including products, audience, values, and brand DNA. Use this to understand what the business does and who it serves before creating content.

---

## When An Agent Uses This

**Content Creator:** "I need to understand the products and audience before drafting"  
**Acquisition:** "I need ICP details for outreach personalization"

---

## Parameters

```json
{
  // No parameters required - scoped to workspace automatically
}
```

---

## Returns

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
      "key_features": [...],
      "target_audience": "Engineering managers"
    }
  ],
  "business_dna": {
    "problem_solved": "...",
    "target_customer": "...",
    "unique_value_prop": "..."
  }
}
```

---

## Hard Rules

- **MUST** load from OrgBrandContext (workspace-level)
- **MUST** include products if defined
- **SHOULD** include business DNA if linked
