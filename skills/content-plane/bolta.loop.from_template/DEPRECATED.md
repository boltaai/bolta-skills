# ⚠️ DEPRECATED: bolta.loop.from_template

**Status:** Deprecated as of V2 (2026-02-20)  
**Replacement:** Job execution via `bolta.job.execute`

---

## Why This Was Deprecated

`bolta.loop.from_template` represented the V1 template-based automation paradigm:
- Load template → Fill variables → Post
- No agent reasoning
- No context accumulation
- No adaptive behavior

**This is not what Bolta V2 is.**

---

## What to Use Instead

### V1 (Old):
```
RecurringTemplate:
  template: "{{topic}} tips for {{audience}}"
  cron: "0 9 * * *"
  
→ Every run: exact same format, no adaptation
```

### V2 (New):
```
Agent: "content_creator"
Job:
  name: "Daily tips for audience"
  run_instructions: "Create helpful tips about [topic] for [audience]"
  voice_profile_id: "uuid"
  schedule: {"cron": "0 9 * * *"}
  
→ Agent reasons about task, checks context, adapts approach
→ Different executions based on recent posts, audience response, memory
```

---

## Migration Path

1. **Identify RecurringTemplates** in your workspace
2. **Create Agent** (type: content_creator)
3. **Create Job** with natural language instructions (not template)
4. **Bind voice_profile_id** (required)
5. **Bind account_ids**
6. **Activate job**
7. **Delete old RecurringTemplate**

---

## Why V2 Is Better

- **Reasoning:** Agent thinks about what to create, not just fill-in-blanks
- **Context:** Agent considers recent posts, voice profile, audience insights
- **Learning:** Agent accumulates memory and improves over time
- **Adaptation:** Same job, different approaches based on what works
- **Quality:** LLM-level intelligence vs. template substitution

---

## Support

Template loops are no longer supported in Bolta V2.

For migration assistance, see `/docs/v1-to-v2-migration.md` or contact support.
