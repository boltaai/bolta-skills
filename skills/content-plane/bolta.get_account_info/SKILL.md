# bolta.get_account_info

**Version:** 2.0.0  
**Category:** Content Creation  
**Agent Types:** All  
**Roles Allowed:** All

---

## Purpose

Get social account details (platform, handle, status, token validity).

---

## When An Agent Uses This

**Content Creator:** "I need to verify which platform I'm posting to"  
**Engagement:** "I need to check token status before replying"

---

## Parameters

```json
{
  "account_id": "string (UUID, required)"
}
```

---

## Returns

```json
{
  "success": true,
  "account_id": "uuid",
  "platform": "linkedin",
  "username": "acmecorp",
  "handle": "@acmecorp",
  "display_name": "Acme Corp",
  "token_status": "valid",
  "is_active": true
}
```

---

## Hard Rules

- **MUST** validate account belongs to workspace
- **MUST** include token_status (valid/invalid/expired)
- **SHOULD** warn if token_status != "valid"
