# Bolta Skills Pack (OpenAI Apps / Claude Skills)

Reusable skills for the **Bolta** plugin. Two layers:

1. **Brand Voice (foundational).** Capture a brand's voice from its existing materials and
   published content, turn it into an enforceable guideline, and apply + validate that voice
   on any content — social posts, emails, proposals, blog posts, decks. Modeled on the
   discover → generate → enforce → validate loop, wired into Bolta's Voice Profile / Business
   DNA model.
2. **Tool orchestration.** Workflow skills that drive the live curated Bolta MCP surface (60 tools) and
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
| `bolta-accounts-and-buckets` | See what's connected; create/update social buckets (named account groups for one-shot multi-account publishing); resolve "post to my <bucket> bucket". |

### Agents
| Skill | Does |
|-|-|
| `bolta-hire-agent` | Discover presets and hire an agent. Beta presets start paused; stable presets hire active and run on schedule — read back job status and offer a pause for preview. |
| `bolta-agent-run-and-review` | Run a job now, watch the run, then approve/reject the drafts it produced. |
| `bolta-agent-status` | Report on hired agents, their jobs, and recent run history (incl. why a job is paused). |
| `bolta-agent-manage` | Pause/resume at the right scope, reschedule, edit instructions & trigger config, add jobs, create custom agents, delete with confirmation. |

### Review & Analytics
| Skill | Does |
|-|-|
| `bolta-review-queue` | Work the standard + agent review queues (approve/reject/schedule). |
| `bolta-analytics-report` | Cross-platform + per-account performance reporting. |

### Cross-connector
| Skill | Does |
|-|-|
| `bolta-winners-to-ads` | Organic→paid loop with Meta's Ads AI Connector (mcp.facebook.com/ads): top organic winners → paid gap read (Meta read-only) → voice-true ad variants + paste-ready campaign structure. Degrades gracefully when either connector is missing. |

## Structure
```
plugin-skills/
  README.md
  skills/<skill>/SKILL.md          # the upload target
  skills/<skill>/references/       # skill-local references (some skills, e.g. brand-voice-generate,
                                   # brand-voice-enforce) — uploaded WITH the skill and required by it
  references/                      # pack-level dev/Claude-Code extra — NOT uploaded, NOT required by the skills
  agents/                          # pack-level dev/Claude-Code extra — NOT uploaded, NOT required by the skills
```

Only the `skills/` folder is uploaded to the OpenAI plugin builder. The pack-level `references/`
and `agents/` directories are convenience material for local development / Claude Code; no skill
depends on them — each SKILL.md carries its tool contract and behavior inline (plus, for some
skills, files in its own skill-local `references/` folder, which ship as part of the skill).

## Ground rules (all skills)
- Resolve `workspace_id` once via `list-workspaces`; reuse it.
- Auth is automatic via the Bolta connector's OAuth grant — never ask for an API key.
- Default to Draft; confirm before `publish-post` / `delete-post`.
- Load voice context (or an active brand-voice guideline) before writing.

See `references/bolta-tools.md` for the exact tool ids and parameters. Skills reference tools
by those live ids inline in their SKILL.md bodies (there is no `tools_required` frontmatter
field) — no other tool names exist.
