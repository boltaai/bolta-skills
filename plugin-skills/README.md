# Bolta Skills Pack (OpenAI Apps / Claude Skills)

Reusable skills for the **Bolta** plugin. Two layers:

1. **Brand Voice (foundational).** Capture a brand's voice from its existing materials and
   published content, turn it into an enforceable guideline, and apply + validate that voice
   on any content — social posts, emails, proposals, blog posts, decks. Modeled on the
   discover → generate → enforce → validate loop, wired into Bolta's Voice Profile / Business
   DNA model.
2. **Tool orchestration.** Workflow skills that drive the live curated Bolta MCP surface (43 tools) and
   its autonomous agents to their fullest — drafting, scheduling, batching, media, per-platform
   tailoring, the full hire → run → review agent loop, the review queue, and analytics.

Brand voice is the foundation: the guideline it produces feeds `voice-generate`, ad-hoc
drafts, and every autonomous agent, so quality styling is consistent everywhere.

## Skills

### Brand Voice
| Skill | Does |
|-|-|
| `brand-voice-discover` | Find brand signal across uploaded docs/transcripts + Bolta's Business DNA, Voice Profiles, and published posts → a discovery report. |
| `brand-voice-generate` | Synthesize a Bolta Brand Voice Guideline (We Are / We Are Not, tone-by-context matrix, terminology, confidence scores) and express it as `voice-generate` parameters. |
| `brand-voice-enforce` | Apply the guideline to any content request; validate and explain the brand choices. |
| `brand-voice-validate` | Score content 0–100 against the guideline with a deviation report. |

### Content & Publishing
| Skill | Does |
|-|-|
| `bolta-draft-post` | Voice-aware single draft (loads voice context, creates a Draft). |
| `bolta-schedule-and-batch` | Schedule posts and create many at once via the bulk pipeline. |
| `bolta-post-media` | Attach ChatGPT-generated images or user files (image/video) to posts. |
| `bolta-platform-tailoring` | Set per-platform options — Threads polls, Reddit, TikTok/Pinterest/YouTube. |

### Agents
| Skill | Does |
|-|-|
| `bolta-hire-agent` | Discover presets and hire an agent (paused for preview). |
| `bolta-agent-run-and-review` | Run a job now, watch the run, then approve/reject the drafts it produced. |
| `bolta-agent-status` | Report on hired agents, their jobs, and recent run history. |

### Review & Analytics
| Skill | Does |
|-|-|
| `bolta-review-queue` | Work the standard + agent review queues (approve/reject/schedule). |
| `bolta-analytics-report` | Cross-platform + per-account performance reporting. |

## Structure
```
plugin-skills/
  README.md
  skills/<skill>/SKILL.md   # the upload target — each SKILL.md is fully self-contained
  references/               # optional dev/Claude-Code extra — NOT uploaded, NOT required by the skills
  agents/                   # optional dev/Claude-Code extra — NOT uploaded, NOT required by the skills
```

Only the `skills/` folder is uploaded to the OpenAI plugin builder. The pack-level `references/`
and `agents/` directories are convenience material for local development / Claude Code; the
skills do not depend on them — every SKILL.md carries its own tool contract and behavior inline.

## Ground rules (all skills)
- Resolve `workspace_id` once via `list-workspaces`; reuse it.
- Auth is automatic via the Bolta connector's OAuth grant — never ask for an API key.
- Default to Draft; confirm before `publish-post` / `delete-post`.
- Load voice context (or an active brand-voice guideline) before writing.

See `references/bolta-tools.md` for the exact tool ids and parameters. Every skill's
`tools_required` uses those live ids — no other tool names exist.
