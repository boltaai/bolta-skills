# Bolta Skills Pack (OpenAI Apps / Claude Skills)

Reusable skills for the **Bolta** plugin. Two layers:

1. **Brand Voice (foundational).** Capture a brand's voice from its existing materials and
   published content, turn it into an enforceable guideline, and apply + validate that voice
   on any content — social posts, emails, proposals, blog posts, decks. Modeled on the
   discover → generate → enforce → validate loop, wired into Bolta's Voice Profile / Business
   DNA model.
2. **Behavior skills.** Outcome-shaped skills that drive the live curated Bolta MCP surface
   (68 tools). These describe *what should be accomplished* — publish, engage, answer the
   inbox, review results — and end by offering to save the same outcome as a scheduled
   **Routine**.
3. **Automation is Routines only.** There is no agent-control tier any more: the
   Agent/Job/Run/Preset and workflow-run tools were demoted off the MCP surface, and the
   skills that drove them were deleted with them. See "Routines vs Agents" below.

Brand voice is the foundation: the guideline it produces feeds `voice-generate`, ad-hoc
drafts, and every routine run, so quality styling is consistent everywhere.

## Skills

### Brand Voice
| Skill | Does |
|-|-|
| `brand-voice-discover` | Find brand signal across uploaded docs/transcripts + Bolta's Business DNA, Voice Profiles, and published posts → a discovery report. |
| `brand-voice-generate` | Synthesize a Bolta Brand Voice Guideline (We Are / We Are Not, tone-by-context matrix, terminology, confidence scores) and express it as `voice-generate` parameters. |
| `brand-voice-enforce` | Apply the guideline to any content request; validate and explain the brand choices. |
| `brand-voice-validate` | Score content 0–100 against the guideline with a deviation report. |

### Behavior skills (start here)
| Skill | Does |
|-|-|
| `social-publishing` | Write, tailor, schedule and publish the brand's own content — one post or many, one platform or several. Long-form WordPress goes to `wordpress-blog`. |
| `reddit-engagement` | Discover Reddit threads worth joining, read them, draft native replies, publish after approval, verify the canonical URL. |
| `cross-platform-engagement` | The same loop on Threads / Bluesky / Mastodon (discovery) and X / LinkedIn (URL supplied), with the capability matrix stated honestly. |
| `social-inbox` | Triage and answer inbound comments and mentions across every connected platform. |
| `analytics-review` | Read performance and say what to do about it. Read-only. |
| `wordpress-blog` | Full editorial procedure for one long-form SEO article: search intent, research, writing, SEO package, hero-image art direction and QA, WordPress delivery, verification. |
| `lucia-test` | Composite acceptance run: the whole loop end to end, then saved as a scheduled routine with no Agent configured. |

### Content & Publishing (focused tools)
| Skill | Does |
|-|-|
| `bolta-setup` | The on-ramp: readiness checklist (workspace → accounts → voice → routines → permissions) and the standard recovery path for typed setup/entitlement errors (`setup_required`, `plan_required`, `trial_runs_exhausted`, `workflow_backpressure`) — other skills hand off here instead of retrying. |
| `bolta-draft-post` | Voice-aware single draft (loads voice context, creates a Draft). |
| `bolta-schedule-and-batch` | Schedule posts and create many at once via the bulk pipeline. |
| `bolta-post-media` | Attach ChatGPT-generated images or user files (image/video) to posts. |
| `bolta-platform-tailoring` | Set per-platform options — Threads polls, Reddit, TikTok/Pinterest/YouTube. |
| `bolta-accounts-and-buckets` | See what's connected; create/update social buckets (named account groups for one-shot multi-account publishing); resolve "post to my <bucket> bucket". |

### Agents and workflow runs (no longer part of this pack)

The four agent skills (`bolta-hire-agent`, `bolta-agent-run-and-review`,
`bolta-agent-status`, `bolta-agent-manage`) and `bolta-workflow-run` were
deleted when the Agent / Job / Run / Preset and workflow-run tools were demoted
off the MCP surface
(`SERVER: resources/architecture/SKILLS_FIRST_ARCHITECTURE_AUDIT_2026-08.md`).
Those endpoints are still REST-live and still documented in `TOOLS.md`; they
are just not tools a model is offered any more, so no skill can call them.
Everything recurring goes through Routines — `list-routine-templates` →
`create-routine` → `activate-routine`, which every behavior skill above offers
at the end, and which `bolta-setup` walks as a readiness step.

### Review & Analytics
| Skill | Does |
|-|-|
| `bolta-review-queue` | Work the standard + routine-produced review queues (approve/reject/schedule). |
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

## Routines vs Agents

A **Routine** is what a customer configures: a repeatable outcome + a trigger + an
execution policy. It binds to a **WorkflowDefinition** (the server-enforced runtime
contract — objective schema, execution modes, and a hard tool allowlist that is never
exposed over MCP) and is usually created from a **RoutineTemplate** (the user-facing
behavior description and its compatibility matrix).

An **Agent** is the internal execution principal a run borrows — model, tool allowlist,
credentials, billing identity. Customers should not have to configure one to automate
something.

So: `create-routine` + `activate-routine`. The lower-level agent tools are no longer named
on the model-facing MCP surface at all — the endpoints still exist and the dashboard still
calls them, but a model is only ever offered the Routine layer. That is the point: a tool
list is read as the menu of legitimate approaches, and "first create an Agent, then create
an Agent Job" is the two-step doorway Routines were built to replace.

Routine tools: `list-routine-templates`, `list-workflow-definitions`, `list-routines`,
`get-routine`, `create-routine`, `update-routine`, `activate-routine`, `pause-routine`,
`resume-routine`, `archive-routine`, `run-routine-now`, `list-routine-runs`.

Three things worth stating to a user every time:
- A new routine is a **draft**. It does not fire until `activate-routine`.
- Schedule times are **wall clock** in the routine's timezone. Never send a UTC offset,
  never convert the user's stated time yourself.
- `approval_policy` can only ever **tighten** the workspace policy, and the engagement
  templates do not permit `auto` at all — every scheduled reply waits for a human.

## Inbound vs outbound engagement

These are different writing tasks and Bolta uses a different server-side writer for each.
Do not mix them up:

- **Outbound** — replying to somebody else's post, in a community we do not own.
  `search-engagement-opportunities` → `get-engagement-conversation` →
  `draft-engagement-reply` → `publish-engagement-reply` → `get-engagement-status`.
  Skills: `reddit-engagement`, `cross-platform-engagement`.
- **Inbound** — replying to a comment or mention on our own content.
  `list-inbox-items` → `draft-inbound-reply` → `reply-to-social-content` (or
  `send-hunter-reply` for a hunter row). Skill: `social-inbox`.

`draft-inbound-reply` and `draft-engagement-reply` are the two halves of the split.
Both return text a human approves before anything is sent; neither is a publish tool.
`voice-generate` is a post writer, not a reply writer — do not press it into service
for either side.

The reply text is written server-side in both cases. A skill's job is choosing the target
and getting approval — not writing the words in a prompt.

## Ground rules (all skills)
- **`workspace_id` is optional on every tool.** The connector's OAuth grant already
  scopes the call, and the MCP layer defaults it to the key's workspace. The Routine
  tools take no `workspace_id` in their schema at all — write `list-routine-templates()`,
  `activate-routine(routine_id)`. Pass it explicitly only when a key spans several
  workspaces and the user named one.
- Resolve `workspace_id` once via `list-workspaces`; reuse it.
- Auth is automatic via the Bolta connector's OAuth grant — never ask for an API key.
- Default to Draft; confirm before `publish-post` / `delete-post`.
- Load voice context (or an active brand-voice guideline) before writing.

See `references/bolta-tools.md` for the exact tool ids and parameters. Skills reference tools
by those live ids inline in their SKILL.md bodies (there is no `tools_required` frontmatter
field) — no other tool names exist.
