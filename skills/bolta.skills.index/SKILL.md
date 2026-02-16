# SKILL: bolta.skills.index

Display name: Bolta Skills Registry  
Slug: bolta-skills-registry  
Version: 0.2.1  
Tags: registry,catalog,bootstrap,workspace,index  
Organization: bolta.ai  
Author: Max Fritzhand

## Purpose

This skill is the **single index** of all Bolta skills. It provides a structured catalog grouped by operational plane, with one-line descriptions and file references. Use it to discover skills, recommend an install set from workspace policy and role, and route to the correct skill file for full instructions.

This skill does not perform content operations directly. It orchestrates discovery and setup.

---

## Source

Canonical repository:

https://github.com/boltaai/bolta-skills

All skill paths below are relative to the repository root.

---

## Full skill index

When you need the full behavior, inputs, or steps for a skill, read the SKILL file at the path given.

### Content Plane
| Skill | Description | Path |
|-------|-------------|------|
| **bolta.draft.post** | Create a single draft post with voice + optional template; route to Draft or Pending Review per policy and role. | `skills/content-plane/bolta.draft.post/SKILL.md` |
| **bolta.loop.from_template** | Create a recurring content loop from a template; all generated posts go to Inbox Review as a bundle. | `skills/content-plane/bolta.loop.from_template/SKILL.md` |
| **bolta.week.plan** | Generate a 7-day content calendar draft with voice + optional templates; route to Draft or Pending Review per Safe Mode. | `skills/content-plane/bolta.week.plan/SKILL.md` |

### Review Plane
| Skill | Description | Path |
|-------|-------------|------|
| **bolta.inbox.triage** | Cluster inbox items, flag risks, suggest edits/actions, optionally create improved draft variants for human review. | `skills/review-plane/bolta.inbox.triage/SKILL.md` |
| **bolta.review.digest** | Produce an admin digest of items awaiting review with risk flags, suggested edits, and approval recommendations. | `skills/review-plane/bolta.review.digest/SKILL.md` |
| **bolta.review.approve_and_route** | Approve pending review posts and route to scheduled or back to draft per workspace policy and per-post settings. | `skills/review-plane/bolta.review.approve_and_route/SKILL.md` |

### Automation Plane
| Skill | Description | Path |
|-------|-------------|------|
| **bolta.cron.generate_to_review** | Cron: create N posts from voice + template and submit as a bundle to review every run (never schedule/publish). | `skills/automation-plane/bolta.cron.generate_to_review/SKILL.md` |
| **bolta.cron.generate_and_schedule** | Cron: generate and optionally schedule posts only if Safe Mode is OFF and principal has schedule permission; else route to review. | `skills/automation-plane/bolta.cron.generate_and_schedule/SKILL.md` |

### Control Plane
| Skill | Description | Path |
|-------|-------------|------|
| **bolta.team.create_agent_teammate** | Create an agent identity (service account) in the workspace and issue an API key with least privilege. | `skills/control-plane/bolta.team.create_agent_teammate/SKILL.md` |
| **bolta.team.rotate_key** | Rotate or revoke an existing API key for a human or agent principal and issue a replacement key. | `skills/control-plane/bolta.team.rotate_key/SKILL.md` |
| **bolta.policy.explain** | Explain workspace policy and the caller’s effective capabilities (allowed/forbidden actions) in plain language. | `skills/control-plane/bolta.policy.explain/SKILL.md` |
| **bolta.audit.export_activity** | Export audit/activity events for a workspace (agent + human actions) for debugging and compliance. | `skills/control-plane/bolta.audit.export_activity/SKILL.md` |

### Voice Plane
| Skill | Description | Path |
|-------|-------------|------|
| **bolta.voice.bootstrap** | Create a default Voice Profile for a new workspace (onboarding, no active voice, level 0). | `skills/init-plane/bolta.voice.bootstrap/SKILL.md` |
| **bolta.voice.learn_from_samples** | Extract structured voice rules from past content; upgrade from bootstrap or refine brand consistency. | `skills/init-plane/bolta.voice.learn_from_samples/SKILL.md` |
| **bolta.voice.evolve** | Refine Voice Profile from engagement signals; version voice with change log (periodic/autopilot optimization). | `skills/init-plane/bolta.voice.evolve/SKILL.md` |
| **bolta.voice.validate** | Evaluate content against a Voice Profile (compliance score, deviation report, optional suggested rewrite). | `skills/init-plane/bolta.voice.validate/SKILL.md` |

---

## Planes summary

- **Voice Plane:** bootstrap, learn from samples, evolve, validate.
- **Content Plane:** drafting, loops, weekly planning.
- **Review Plane:** triage, digest, approve-and-route.
- **Automation Plane:** cron generate-to-review, cron generate-and-schedule.
- **Control Plane:** team/agents, keys, policy explain, audit export.

---

## Recommended install sets

These are suggested “modes” based on workspace policy and role.

### Assisted Mode (safe default)
- bolta.voice.bootstrap
- bolta.draft.post
- bolta.loop.from_template
- bolta.week.plan

### Managed Automation (team review workflows)
- Assisted Mode +
- bolta.inbox.triage
- bolta.review.digest
- bolta.review.approve_and_route

### Autopilot (policy-aware automation)
- Managed Automation +
- bolta.cron.generate_to_review
- bolta.cron.generate_and_schedule (only if Safe Mode OFF + scheduling allowed)

### Governance (ops & compliance)
- bolta.policy.explain
- bolta.audit.export_activity
- bolta.team.create_agent_teammate
- bolta.team.rotate_key

---

## Behavior (registry flow)

1. Call `bolta.get_workspace_policy`.
2. Call `bolta.get_my_capabilities`.
3. Determine Safe Mode state and role.
4. Recommend one install set: Assisted / Managed / Autopilot / Governance.
5. Output recommended skill slugs to import.
6. For full instructions of any skill, use the **Path** in the index tables above.

---

## Output example

```json
{
  "safe_mode": "on",
  "role": "owner",
  "recommended_skills": [
    "bolta.voice.bootstrap",
    "bolta.draft.post",
    "bolta.loop.from_template",
    "bolta.week.plan"
  ],
  "next_step": "Import Assisted Mode skills; use the index tables to open the SKILL.md paths for full behavior."
}
