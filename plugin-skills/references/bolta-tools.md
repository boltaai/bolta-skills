# Bolta MCP Tools — Canonical Reference

The single source of truth for every tool the Bolta plugin exposes. Skills MUST use
these exact tool ids and parameter names. The server is **mcp.bolta.ai/mcp** (StreamableHTTP,
stateless). 41 tools are exposed. Any tool name not on this list does not exist — do not call it.

## Universal rules

- **`workspace_id` is required by almost every tool.** If you don't have it, call
  `list-workspaces` first and use the active workspace's `id`. Never guess a workspace UUID.
- **Auth is automatic in ChatGPT.** The Bolta connector's OAuth grant mints a scoped
  `bolta_sk_` API key; you never pass an API key as a tool argument.
- **Annotations** below drive ChatGPT's confirmation behavior:
  `RO` = readOnlyHint (safe, no writes), `DES` = destructiveHint (irreversible — confirm first),
  `OW` = openWorldHint (touches the public internet / external platforms).
- **Post lifecycle:** a post is created as a Draft, can be submitted for review, approved,
  scheduled, then published. `create-post` accepts `requested_action` to jump straight to a
  target state (see below).

## Discovery & workspace (read-only)

| Tool | Method | Params | Notes |
|-|-|-|-|
| `list-workspaces` | GET · RO | — | Start here to resolve `workspace_id`. |
| `get-workspace` | GET · RO | `workspace_id`* | Settings, safe-mode, autonomy. |
| `get-my-capabilities` | GET · RO | `workspace_id`* | Caller's role/scopes — check before writes. |
| `list-accounts` | GET · RO | `workspace_id`*, `platform` | Connected social accounts + their UUIDs (`account_ids`). |

## Reading posts (read-only)

| Tool | Method | Params | Notes |
|-|-|-|-|
| `list-workspace-posts` | GET · RO | `workspace_id`*, `status`, `account_ids`, `limit`, `page` | All posts; filter by status (Draft/Scheduled/Published/…). Also the best source of **published-content voice samples**. |
| `list-scheduled-posts` | GET · RO | `workspace_id`*, `limit`, `page` | Upcoming scheduled queue. |
| `get-post` | GET · RO | `post_id`* | Single post detail. |
| `get-post-platform-details` | GET · RO | `post_id`*, `platform`* | Per-platform metadata (Threads poll, Reddit flair, TikTok/Pinterest/YouTube fields, …). |

## Writing posts

| Tool | Method | Params | Notes |
|-|-|-|-|
| `create-post` | POST | `workspace_id`*, `content`*, `account_ids`*, `media`, `scheduled_time`, `requested_action`, `poll`, `idempotency_key` | Primary creation tool. See `requested_action` + `media` + `poll` below. |
| `update-post` | PATCH | `post_id`*, `content`, `media`, `poll`, `scheduled_time` | Edit an existing post (incl. swapping media). |
| `delete-post` | DELETE · **DES** | `post_id`* | Irreversible — confirm first. |
| `update-post-platform-details` | PATCH | `post_id`*, `platform`*, `fields`* | Set per-platform options (poll, flair, title, privacy…). `fields` is an object. |
| `bulk-create-posts` | POST | `workspace_id`*, `posts`* | `posts` = array of post objects. Returns a `task_id`. |
| `bulk-create-status` | GET · RO | `task_id`* | Poll the bulk job; returns per-item progress + previews. |
| `schedule-post` | POST | `workspace_id`*, `post_id`*, `time`* | Schedule an existing Draft (`time` = ISO8601). |
| `publish-post` | POST · **DES · OW** | `workspace_id`*, `post_id`* | Publishes NOW to the live platform. Irreversible + public — always confirm. |
| `submit-for-review` | POST | `workspace_id`*, `post_ids`*, `note` | Route drafts into the review queue. |

### `create-post` — `requested_action` values
- omitted / `draft` → creates a **Draft** (default).
- `schedule` → requires `scheduled_time`; lands **Scheduled**.
- `submit_for_review` → routes into the approval queue.
- `publish` → publishes now (**destructive + public** — confirm with the user first).

### `create-post` / `update-post` — `media`
`media` is an **array of file objects**. Each object MUST use ChatGPT's documented file
schema: `download_url` (required), `file_id` (required), `mime_type` (optional),
`file_name` (optional). Both ChatGPT-generated images and user-attached files (image/video)
arrive as these file objects — pass them straight through. Bolta re-hosts them to durable
storage automatically.

### `create-post` — `poll` (Threads, X, etc.)
`poll` is an object, e.g. `{ "options": ["A","B"], "duration_minutes": 1440 }`. For richer
per-platform options use `update-post-platform-details`.

## Review & approval

| Tool | Method | Params | Notes |
|-|-|-|-|
| `approve-post` | POST | `workspace_id`*, `post_id`*, `schedule_mode`, `fixed_time`, `comments` | Approve a post in review. |
| `list-reviews` | GET · RO | `workspace_id`*, `reviewer_id`, `workflow_type` | Standard review queue. |
| `list-recurring-reviews` | GET · RO | `workspace_id`*, `status`, `template_id` | **Pending drafts produced by agents** (recurring/agent runs). This is the agent → human queue. |
| `approve-recurring-review` | POST | `review_id`*, `approvalComments`, `approveWithSchedule`, `useSuggestedTime` | Approve an agent-produced draft; optionally schedule at the suggested time. |
| `reject-recurring-review` | POST | `review_id`*, `rejectionReason` | Reject an agent-produced draft (feeds voice learning). |

## Analytics (read-only)

| Tool | Method | Params | Notes |
|-|-|-|-|
| `cross-platform-analytics` | GET · RO | `workspace_id`*, `days` | Workspace-wide rollup across platforms. |
| `list-account-insights` | GET · RO | `workspace_id`*, `days` | Per-account snapshot for every connected account. |
| `get-account-analytics` | GET · RO | `workspace_id`*, `account_id`*, `days` | Time series for one account. |

## Voice & brand (read-only + generation)

| Tool | Method | Params | Notes |
|-|-|-|-|
| `get-voice-context` | GET · RO | `workspace_id`*, `voice_profile_id`, `platforms` | The compiled voice context (tone, dos/donts, exemplars) Bolta injects into its writer. **Load this before drafting.** |
| `list-voice-profiles` | GET · RO | `workspace_id`* | All voice profiles + ids. |
| `get-voice-profile` | GET · RO | `workspace_id`*, `profile_id`* | One voice profile. |
| `create-voice-profile` | POST | `workspace_id`*, `name`*, `tone`, `writing_sample`, `tone_of_voice`, `target_audience`, `dos`, `donts`, `content_size`, `pacing`, `speaker_mode`, `default_post_intent` | **Persist a captured brand voice as a native Bolta Voice Profile.** Provide `tone` (a 0-100 dials object, e.g. `{"playful":30,"professional":80,"direct":70,"thoughtful":60}`) **or** a `writing_sample` (≥50 chars — the server extracts the tone from it). |
| `update-voice-profile` | PATCH | `workspace_id`*, `profile_id`*, `name`, `tone`, `tone_of_voice`, `target_audience`, `dos`, `donts`, `content_size`, `pacing`, `speaker_mode`, `default_post_intent` | **Evolve** a voice profile over time. Partial update — only the fields you send change; omitted fields are preserved. |
| `list-business-dna` | GET · RO | `workspace_id`* | Business DNA records (industry, audience, positioning). |
| `get-business-dna` | GET · RO | `workspace_id`*, `dna_id`* | One Business DNA record. |
| `extract-business-dna` | POST · **OW** | `workspace_id`*, `url`*, `name`, `set_as_default` | Scrape a brand's public website → a new Business DNA record. Reaches the internet + consumes AI credits. |
| `voice-generate` | POST | `workspace_id`*, `topics`*, `dateRange`*, `time`*, `maxPosts`*, `voiceProfileId`, `context`, `businessName`, `niche`, `tone`, `dos`, `donts`, `customRules`, `enableMultiPlatform`, `selectedAccountsOrBuckets`, `platform` | Bolta's voice-aware writer. Brand-voice guidelines map directly onto `tone` / `dos` / `donts` / `customRules` / `context`. |

> **Brand-voice bridge (persistent):** a captured brand guideline can be **written back into
> Bolta**. `brand-voice-generate` maps the guideline onto `create-voice-profile` (`tone` object
> or `writing_sample`, plus `tone_of_voice`, `dos`, `donts`, `target_audience`) so it becomes a
> native Voice Profile that `voice-generate` **and every autonomous agent** then consume. As the
> brand evolves, `update-voice-profile` refines it in place (partial update — safe, no field
> wipes). `extract-business-dna` seeds the Business DNA from the brand's website. For a one-off
> draft without persisting, the guideline can still be passed inline to `voice-generate`.

## Agents (the autonomous workforce)

| Tool | Method | Params | Notes |
|-|-|-|-|
| `list-agent-presets` | GET · RO | `workspace_id`* | Marketplace presets (Hype Man, Deep Diver, Hunter, Engager, …) + their `preset_id`s. |
| `hire-agent-preset` | POST | `workspace_id`*, `preset_id`*, `name`, `job_name`, `voice_profile_id`, `account_ids` | Hire a preset → creates the agent + its job (starts paused for preview). |
| `list-agents` | GET · RO | `workspace_id`* | Hired agents + ids. |
| `get-agent` | GET · RO | `workspace_id`*, `agent_id`* | One agent's config/persona/status. |
| `list-agent-jobs` | GET · RO | `workspace_id`*, `agent_id`* | An agent's jobs (schedule, status). |
| `run-agent-job-now` | POST | `workspace_id`*, `agent_id`*, `job_id`*, `run_instructions`, `account_id` | Trigger a job immediately (optional one-off instructions). |
| `list-agent-job-runs` | GET · RO | `workspace_id`*, `agent_id`*, `job_id`*, `limit` | Run history: status, tools used, tokens, cost, output. |

### The full agent loop
`list-agent-presets` → `hire-agent-preset` → (verify) `list-agent-jobs` →
`run-agent-job-now` → `list-agent-job-runs` (watch it work) →
`list-recurring-reviews` (its drafts land here) → `approve-recurring-review` /
`reject-recurring-review`. This closes the loop: the agent proposes, the human approves,
and rejections/edits feed Bolta's voice learning so it gets better.

\* = required parameter.
