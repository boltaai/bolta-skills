# Skills Pack ↔ Backend Tools Alignment

This document maps skills pack definitions to their backend implementations in `SERVER/agents/`.

## Fully Implemented (Backend + Skills Pack)

These skills have both a schema.json definition AND a working backend tool handler.

| Skill | Backend Location | Notes |
|-|-|-|
| `bolta.draft_post` | tools_atomic.py | V2 draft creation |
| `bolta.get_account_info` | tools.py | Social account details |
| `bolta.get_business_context` | tools.py | Business DNA loader |
| `bolta.get_voice_profile` | tools.py | Voice profile retrieval |
| `bolta.list_recent_posts` | tools.py | Recent content check |
| `bolta.get_post_metrics` | tools.py | Post performance data |
| `bolta.get_audience_insights` | tools.py | Audience demographics |
| `bolta.get_best_posting_times` | tools.py | Optimal posting schedule |
| `bolta.get_mentions` | tools_wave3.py | Mention fetching |
| `bolta.get_comments` | tools_wave3.py | Comment fetching |
| `bolta.reply_to_mention` | tools_wave3.py | Reply in brand voice |
| `bolta.approve_post` | tools.py | Review approval |
| `bolta.reject_post` | tools.py | Review rejection |
| `bolta.add_comment` | tools.py | Review comments |
| `bolta.inbox.triage` | tools.py | Inbox listing with priority |
| `bolta.review.digest` | tools.py | Review activity summary |
| `bolta.review.approve_and_route` | tools.py | Bulk approve + schedule routing |
| `bolta.voice.validate` | tools.py | Content voice compliance check |
| `bolta.quota.status` | tools.py | Credit/rate limit status |
| `bolta.workspace.config` | tools.py | Workspace settings reader |
| `bolta.week.plan` | tools.py | Content calendar planning context |
| `bolta.agent.hire` | tools.py | Hire preset via create_agent_from_preset |
| `bolta.agent.activate_job` | tools.py | Toggle job status to active |
| `bolta.agent.configure` | tools.py | Update agent persona/model/status |
| `bolta.voice.bootstrap` | tools.py | Create voice profile |
| `bolta.voice.learn_from_samples` | tools.py | Refine voice from samples |
| `bolta.voice.evolve` | tools.py | Evolve voice from feedback |
| `bolta.policy.explain` | tools.py | Explain workspace policies |
| `bolta.audit.export_activity` | tools.py | Export activity log |
| `bolta.team.create_agent_teammate` | tools.py | Create agent service account |
| `bolta.team.rotate_key` | tools.py | Rotate agent API key |
| `bolta.cron.generate_and_schedule` | tools.py | Trigger job with auto-schedule |
| `bolta.cron.generate_to_review` | tools.py | Trigger job with review routing |

## Skills Pack Only (Routed via MCP / Conductor)

These skills are defined in the pack with schema.json but are handled by the MCP server or conductor layer rather than direct tool handlers in tools.py.

| Skill | Routing | Notes |
|-|-|-|
| `bolta.agent.memory` | tools.py (remember/recall) | Both remember and recall tool handlers exist |
| `bolta.agent.mention` | consumers.py | Real-time WebSocket event, not tool call |
| `bolta.job.execute` | tasks.py | Documentation-only skill (execution is internal) |
| `bolta.voice.validate` | tools.py | Also available as tool (dual path) |
| `bolta.draft.post` | tools_atomic.py | Legacy alias for bolta_draft_post |

## Backend Only (Not in Skills Pack)

These are internal/atomic tools used by the execution engine. They don't need skills pack definitions because they're not user-facing — they're building blocks the agent uses internally.

**Content Pipeline:**
generate_post_content, save_draft, review_content, refine_content, humanize_content, format_for_platform, qa_score_content, evaluate_voice_quality, generate_reply_content, generate_companion_images, bulk_draft_posts

**Research & SEO:**
research_topic, generate_blog_outline, generate_blog_post, generate_seo_metadata, extract_content_structure

**Engagement (Granular):**
score_mention, score_mentions_batch, hide_comment, reply_to_comment, flag_for_review, block_user, classify_comment

**CRM:**
create_crm_contact, get_crm_contacts, update_crm_contact, add_crm_contact_to_list, create_crm_list, create_crm_task, get_crm_pipeline

**Platform Operations:**
delete_post, edit_post, like_post, repost, get_conversation_thread, get_publication_status

**System:**
remember, fire_webhook, notify_workspace, trigger_agent_job, trigger_voice_training

**Analytics (Granular):**
analyze_sentiment, analyze_account_voice, analyze_edit_patterns, get_growth_trends, get_conversion_metrics, get_moderation_stats

## Summary

| Category | Count |
|-|-|
| Fully implemented (both sides) | 33 |
| Dual-path (tool + MCP/event) | 3 |
| Documentation-only | 1 |
| Deprecated | 1 |
| Backend only (internal tools) | 60+ |
| **Total skills pack** | **38** |
