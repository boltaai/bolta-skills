# V2 Skills Review - Status Report

**Last Updated:** 2026-04-05  
**Status:** Complete

---

## Summary

All skills have been audited and updated:

- **38 skills** across 8 planes (voice, content, review, automation, agent, analytics, engagement, control)
- **100% schema.json coverage** — every skill has a valid schema.json for MCP tool invocation
- **Skills index** up to date with all skills including new voice skills (evolve, validate)
- **TOOLS-ALIGNMENT.md** documents mapping between skills pack and backend tool implementations
- **1 deprecated skill** (`bolta.loop.from_template`) marked clearly, no schema generated

## What Was Done (2026-04-05)

### Schema Generation
- Generated schema.json for 30 skills that were missing them
- All schemas follow consistent format: `{ name, description, input_schema }`
- Field naming standardized to `input_schema` (singular, MCP convention)
- Voice skills (bootstrap, learn_from_samples, evolve, validate) — schemas derived from documentation body since frontmatter lacked structured `inputs_schema`

### Index Updates
- Added `bolta.voice.evolve` and `bolta.voice.validate` to skills index
- Index now lists all 38 skills across 8 planes

### Documentation
- README.md updated with new voice skills and control plane skills
- Schema.json section updated to note 100% coverage
- TOOLS-ALIGNMENT.md created documenting backend tool mapping

### Backend Fixes (SERVER/agents/)
- Fixed JSON truncation bug in `execution.py` (malformed suffix)
- Added OpenAI models (gpt-5.4, gpt-5.4-mini, gpt-4o, gpt-4o-mini, gpt-4-turbo) to cost table in `tasks.py`
- Added `permissions=["workspace:read"]` to 6 endpoints missing permission checks in `views.py`
- Updated SERVER agents README.md to reflect current production state

## Skill Coverage by Plane

| Plane | Skills | SKILL.md | schema.json |
|-|-|-|-|
| Voice | 4 | 4/4 | 4/4 |
| Content | 8 | 8/8 | 7/8 (1 deprecated) |
| Review | 6 | 6/6 | 6/6 |
| Automation | 2 | 2/2 | 2/2 |
| Agent | 6 | 6/6 | 6/6 |
| Analytics | 3 | 3/3 | 3/3 |
| Engagement | 3 | 3/3 | 3/3 |
| Control | 6 | 6/6 | 6/6 |
| **Total** | **38** | **38/38** | **37/38** |
