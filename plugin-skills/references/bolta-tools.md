# Bolta MCP Tools — Canonical Reference

The single source of truth for every tool the Bolta plugin exposes. Skills MUST use
these exact tool ids and parameter names. The server is **mcp.bolta.ai/mcp** (StreamableHTTP,
stateless). 60 baseline tools are exposed, plus 2 flag-gated Workflow Runtime tools
(`start-workflow`, `get-workflow-run`) when `WORKFLOW_RUNTIME_V1` is on — 62 total. Any tool
name not on this list does not exist — do not call it.

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

## Discovery, workspace & buckets

| Tool | Method | Params | Notes |
|-|-|-|-|
| `list-workspaces` | GET · RO | — | Start here to resolve `workspace_id`. |
| `get-workspace` | GET · RO | `workspace_id`* | Settings, safe-mode, autonomy. |
| `get-my-capabilities` | GET · RO | `workspace_id`* | Caller's role/scopes — check before writes. |
| `list-accounts` | GET · RO | `workspace_id`*, `platform` | Connected social accounts + their UUIDs (`account_ids`). |
| `get-connect-link` | GET · RO | `workspace_id`*, `platform` | URL to Bolta's social-account connect page. Use when the workspace has no connected account for the target platform — OAuth can't run in chat; share the link, then re-check with `list-accounts`. `platform` preselects it on the page. |
| `list-buckets` | GET · RO | `workspace_id`* | Social buckets — named groups of accounts for one-shot multi-account publishing — with member accounts (id, platform, username). Renders the accounts card's Buckets tab. |
| `create-social-bucket` | POST | `workspace_id`*, `name`*, `account_ids` | Create a bucket (name unique per workspace). `account_ids` = base account UUIDs from `list-accounts` (not virtual `linkedin_org_`/`facebook_page_` ids). |
| `update-social-bucket` | PATCH | `workspace_id`*, `bucket_id`*, `name`, `account_ids` | Rename and/or replace members. `account_ids` is a **full replacement list** — fetch current members via `list-buckets`, adjust, resend the whole list. |

## Reading posts (read-only)

| Tool | Method | Params | Notes |
|-|-|-|-|
| `list-workspace-posts` | GET · RO | `workspace_id`*, `status`, `platform`, `start_date`, `end_date`, `include_metrics`, `metrics_platforms`, `limit`, `page`, `sort_by`, `sort_order` | All posts; filter by status (Draft/Scheduled/Published/…). `include_metrics=true` attaches per-platform engagement (views, likes, comments, reposts) + `published_at` — THE tool for "how did my post(s) do" (combine `status=published` + a date window). Metrics sync **nightly**: for posts <24h old, zeros mean "not synced yet", not poor performance. Also the best source of **published-content voice samples**. |
| `list-scheduled-posts` | GET · RO | `workspace_id`*, `limit`, `page`, `start_date`, `end_date` | Upcoming scheduled queue; window it with ISO dates ("what's going out this week"). |
| `get-post` | GET · RO | `post_id`* | Single post detail. |
| `get-post-platform-details` | GET · RO | `post_id`*, `platform`* | Per-platform metadata (Threads poll, Reddit flair, TikTok/Pinterest/YouTube fields, …). |

## Writing posts

| Tool | Method | Params | Notes |
|-|-|-|-|
| `create-post` | POST | `workspace_id`*, `content`*, `account_ids`, `social_buckets`, `media`, `scheduled_time`, `requested_action`, `poll`, `idempotency_key` | Primary creation tool. `account_ids` optional for plain drafts, required to schedule/publish — or pass `social_buckets` (bucket IDs from `list-buckets`) to target a whole named account group. See `requested_action` + `media` + `poll` below. |
| `update-post` | PATCH | `post_id`*, `content`, `media`, `poll`, `scheduled_time`, `accounts` | Edit an existing post (incl. swapping media). `accounts` retargets the post — it is a FULL replacement list; resend every account the post should keep. |
| `delete-post` | DELETE · **DES** | `post_id`* | **Soft delete** — hidden immediately, recoverable for 7 days via `list-recently-deleted` → `restore-deleted`, then permanently purged. Still confirm first. |
| `update-post-platform-details` | PATCH | `post_id`*, `platform`*, `fields`* | Set per-platform options (poll, flair, title, privacy…). `fields` is an object. |
| `bulk-create-posts` | POST | `workspace_id`*, `posts`*, `timezone` | ALWAYS use this for multiple posts — looping `create-post` renders one card per call and the user only sees one; the server forbids that pattern. Available to assistant sessions: per-item authorization routes assistant-created posts through the approval inbox (no 403). Each `posts` item takes the same FLAT keys as `create-post`: `{content, account_ids, social_buckets, status: "Draft"\|"Scheduled", scheduled_time (required when Scheduled; naive wall-clock, no offset), media}` — the nested `{contents:[…]}` shape is also accepted. Either `account_ids` or `social_buckets` required per item. `timezone` (IANA) only when the user names a zone. Returns a `task_id`; the card polls status itself — do NOT re-poll. |
| `bulk-create-status` | GET · RO | `task_id`* | Poll the bulk job; returns per-item progress + previews. |
| `schedule-post` | POST | `workspace_id`*, `post_id`*, `time`* | Schedule an existing Draft (`time` = ISO8601). |
| `publish-post` | POST · **DES · OW** | `workspace_id`*, `post_id`* | Publishes NOW to the live platform. Irreversible + public — always confirm. |
| `submit-for-review` | POST | `workspace_id`*, `post_ids`*, `note` | Route drafts into the review queue. |

## Undo (soft-delete window)

| Tool | Method | Params | Notes |
|-|-|-|-|
| `list-recently-deleted` | GET · RO | `workspace_id`* | Posts and agent jobs deleted in the last 7 days that can still be restored. Each item: type (`post`\|`job`), label, deleted-at, days remaining before permanent purge. |
| `restore-deleted` | POST | `workspace_id`*, `item_type`* (`post`\|`job`), `item_id`* | Undo a delete (ids from `list-recently-deleted`). 404 if the item is live, already purged, or in another workspace. Restoring a job does NOT bring back its Hunter/Engager campaign — that cascade is permanent. |

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
| `approve-post` | POST | `workspace_id`*, `post_id`*, `schedule_mode`, `expected_fingerprint`, `fixed_time`, `timezone`, `comments` | Approve a post in review. **Pass `expected_fingerprint`** — the `content_fingerprint` from your most recent read of the item (`list-inbox-items` / `get-workflow-run`) — to guarantee you approve exactly the revision reviewed. A **409 `stale_review`** means the post changed since review; the 409 deliberately carries no fingerprint, so NEVER blindly retry — re-read the item, show the user the current content, get a fresh decision, then retry with the fresh fingerprint. Review rows with status `autonomous` were scheduled by autonomy policy, not human-approved. |
| `list-reviews` | GET · RO | `workspace_id`*, `reviewer_id`, `workflow_type`, `limit`, `page` | Standard review queue. |
| `list-recurring-reviews` | GET · RO | `workspace_id`*, `status`, `template_id`, `agent_creator_id`, `limit`, `page` | **Pending drafts produced by agents** (recurring/agent runs). This is the agent → human queue. |
| `list-inbox-items` | GET · RO | `workspace_id`*, `source` (team\|recurring\|hunter\|report), `status`, `agent_id`, `limit`, `offset` | **Unified inbox** of everything pending review — team posts, recurring/agent drafts, hunter reply drafts (with the mention/lead context they respond to), and agent reports (with download links). Pass `agent_id` to answer "what did <agent> produce that needs me?". Prefer this for "what's waiting for me". Team rows carry `content_fingerprint` (echo as `expected_fingerprint` on `approve-post`) and, for workflow-produced drafts, `workflow_run_id` (group them as one batch). |
| `approve-recurring-review` | POST | `review_id`*, `approvalComments`, `approveWithSchedule`, `useSuggestedTime`, `newScheduleTime`, `account_ids` | Approve an agent-produced draft. `newScheduleTime` (ISO8601) = "approve it but post Friday 9am" in one call; `account_ids` retargets at approval time. |
| `reject-recurring-review` | POST | `review_id`*, `rejectionReason`, `rejectionCategories` | Reject an agent-produced draft (feeds voice learning). ALWAYS pass `rejectionCategories` when the objection fits a code — structured categories train the voice far better than free text. Valid codes: too_casual, too_formal, wrong_tone, off_brand, too_long, too_short, wrong_format, factual_error, spelling_grammar, missing_cta, wrong_cta, wrong_emoji, wrong_hashtag, not_engaging, platform_mismatch, too_salesy, off_topic, repetitive, other (invalid codes are silently dropped). |
| `send-hunter-reply` | POST | `workspace_id`*, `reply_id`*, `content` | Approve + send a hunter reply draft (from `list-inbox-items`, `source=hunter`). Optional `content` overrides the draft text in the same call. Double-send is prevented server-side. |
| `update-hunter-reply` | PATCH | `workspace_id`*, `reply_id`*, `content`* | Edit a hunter reply draft **without sending** (already-sent replies 409). Send later via `send-hunter-reply`. |

## Workflows (flag-gated: Workflow Runtime V1)

Registered ONLY when the deployment's `WORKFLOW_RUNTIME_V1` flag is on (surface = 62 tools).
If `start-workflow` is not in the tool list, the feature is off — fall back to
`create-post` / `bulk-create-posts` and say so; never call an unexposed name.

| Tool | Method | Params | Notes |
|-|-|-|-|
| `start-workflow` | POST | `workspace_id`*, `objective`*, `workflow_key`, `post_count`, `platforms`, `account_ids`, `time_window`, `notes`, `execution_mode`, `idempotency_key` | Start a durable workflow for a multi-step OUTCOME ("keep our launch active this week") — for a single explicit post use `create-post` instead. `objective` = the user's own goal; NEVER invent it. `workflow_key` defaults `weekly_content_prepare`; `post_count` 1–10 (default 4). `execution_mode`: `inherit` (default — follow workspace/agent autonomy: assisted→review, eligible auto→automatic SCHEDULING), `require_review` (always pause for approval — use whenever the user says anything like "let me review first"), `auto_schedule` (honored only when existing autonomy allows; otherwise falls back to review with `fallback_reason` = `safe_mode` \| `autonomy_insufficient`). A request can tighten but never loosen workspace safety, and nothing EVER publishes immediately via workflows (that stays `publish-post`). Returns a durable `workflow_run_id` immediately — reuse it for all follow-ups. Retries are safe: same `idempotency_key` (or identical objective within 30 min) returns the SAME run. Consumes agent credits where applicable. |
| `get-workflow-run` | GET · RO | `workspace_id`*, `workflow_run_id`* | Poll a run (side-effect free). Returns `status` (`running` \| `awaiting_approval` \| `scheduled` \| `completed` \| `partial` \| `failed` \| `cancelled`), `draft_count`/`scheduled_count`/`review_count`/`failed_count`, the policy applied (`requested_execution_mode`, `effective_autonomy`, `approval_required`, `fallback_reason`), `next_scheduled_time`, `artifacts[]` (`post_id`, `platforms`, `review_status`, `content_fingerprint` — echo as `expected_fingerprint` on `approve-post` — `scheduled_time`, `content_preview`), error info, and `next_actions`. `partial` = some scheduled + some awaiting review — a normal mixed outcome, NEVER a failure; offer the review queue (`list-inbox-items`). |

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
| `create-voice-profile` | POST | `workspace_id`*, `name`*, `tone`, `writing_sample`, `tone_of_voice`, `target_audience`, `dos`, `donts`, `content_size`, `pacing`, `speaker_mode`, `default_post_intent`, `business_dna_id`, `is_default`, `description`, `custom_rules`, `topics`, `language` | **Persist a captured brand voice as a native Bolta Voice Profile.** `business_dna_id` links the profile to a specific Business DNA record (from `list-business-dna` / `extract-business-dna`) — wire the extract → profile flow explicitly with it; `is_default` makes it the workspace default. Provide `tone` (a 0-100 dials object, e.g. `{"playful":30,"professional":80,"direct":70,"thoughtful":60}`) **or** a `writing_sample` (≥50 chars — the server extracts the tone from it). |
| `update-voice-profile` | PATCH | `workspace_id`*, `profile_id`*, `name`, `tone`, `tone_of_voice`, `target_audience`, `dos`, `donts`, `content_size`, `pacing`, `speaker_mode`, `default_post_intent`, `business_dna_id`, `is_default` | **Evolve** a voice profile over time. Partial update — only the fields you send change; omitted fields are preserved. |
| `list-business-dna` | GET · RO | `workspace_id`* | Business DNA records (industry, audience, positioning). |
| `get-business-dna` | GET · RO | `workspace_id`*, `dna_id`* | One Business DNA record. |
| `extract-business-dna` | POST · **OW** | `workspace_id`*, `url`*, `name`, `set_as_default` | Scrape a brand's public website → a new Business DNA record. Reaches the internet + consumes AI credits. |
| `update-business-dna` | PATCH | `workspace_id`*, `dna_id`*, `fields`* | **Safe partial merge** — only keys you send change; omitted fields are preserved server-side. `fields` is a flat object: brand basics (`name`, `tagline`, `tagline_on_images`, `business_overview`, `website_url`), visual identity (`colors` hex[], `fonts`, `visual_aesthetics`, `brand_values`, `logo_url`), image settings (`logo_placement`, `custom_image_instructions`), local identity (`city`, `neighborhood`, `service_area`, `years_in_business`, `owner_name`, `staff_names`), story (`origin_story`, `community_involvement`, `testimonials`). Call `get-business-dna` first to see current values. |
| `voice-generate` | POST | `workspace_id`*, `topics`, `date_range`, `time`, `max_posts`, `voice_profile_id`, `context`, `business_name`, `niche`, `tone`, `dos`, `donts`, `custom_rules`, `enable_multi_platform`, `selected_accounts_or_buckets`, `platform`, `generate_images`, `post_intent`, `language` | Bolta's voice-aware writer (consumes AI credits). All params snake_case (unified 2026-07-19). Only `workspace_id` is required — but ALWAYS pass `topics` (omitting it generates generic content). Server defaults: `max_posts` 7, `time` "12:00 PM" (12-hour format). Brand-voice guidelines map onto `tone` / `dos` / `donts` / `custom_rules` / `context`. |

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
| `hire-agent-preset` | POST | `workspace_id`*, `preset_id`*, `name`, `job_name`, `voice_profile_id`, `account_ids` | Hire a preset → creates the agent + its job. **Only beta presets start paused** (assisted autonomy); stable presets (e.g. Hype Man, Analyst) hire ACTIVE with autonomy=auto and `next_run_at` set — the job will run on schedule. Read back the actual job status after hiring; offer an explicit pause if the user wants to preview first. |
| `list-agents` | GET · RO | `workspace_id`* | Hired agents + ids. |
| `create-agent` | POST | `workspace_id`*, `name`*, `type`*, `role`, `description`, `avatar`, `config` | Create a custom agent from scratch (types: content_creator \| engagement \| acquisition \| reviewer \| analytics \| moderator \| custom). Free workspaces are capped at 1 agent (402 → explain the upgrade honestly). Prefer `hire-agent-preset` when a preset fits. |
| `get-agent` | GET · RO | `workspace_id`*, `agent_id`* | One agent's config/persona/status. |
| `update-agent` | PATCH | `workspace_id`*, `agent_id`*, `name`, `type`, `role`, `status`, `description`, `avatar`, `config` | Edit an agent. **Pause scope warning:** `status=paused` pauses the WHOLE agent and cascade-pauses ALL its active jobs (resume reverses exactly that cascade). If the user means one job/schedule, use `update-agent-job` instead; when ambiguous, list the jobs and ask. |
| `delete-agent` | DELETE · **DES** | `workspace_id`*, `agent_id`* | Irreversible — confirm first. Pauses its jobs, purges its service-account API keys, cascades its campaigns. Offer `update-agent status=paused` as the soft alternative. |
| `list-agent-jobs` | GET · RO | `workspace_id`*, `agent_id`* | An agent's jobs (schedule, status, `paused_by`). |
| `get-agent-job` | GET · RO | `workspace_id`*, `agent_id`*, `job_id`* | One job's full detail: schedule, status, voice, accounts, trigger_config, and `paused_by` (see below). Fetch this BEFORE any job edit. |
| `create-agent-job` | POST | `workspace_id`*, `agent_id`*, `name`*, `trigger`, `schedule`, `voice_profile_id`, `account_ids`, `trigger_config`, `run_instructions`, `max_retries`, `status`, `intended_platform` | Add a job to an agent. `status=paused` creates it dormant for config review; `intended_platform` steers platform-native style. Call `get-agent` first — config differs by type: content agents = `trigger=scheduled` + schedule + voice + accounts; engagement = on_new_mention/on_new_comment; acquisition (Hunter) = keyword_match + trigger_config keywords[]/subreddits[]; analytics/moderator may omit voice. Mirror a sibling job (`get-agent-job`) instead of guessing shapes. |
| `update-agent-job` | PATCH | `workspace_id`*, `agent_id`*, `job_id`*, `name`, `status`, `schedule`, `trigger`, `trigger_config`, `voice_profile_id`, `account_ids`, `run_instructions`, `max_retries` | Edit a job. `status=paused` = the **job-level pause** (agent + other jobs keep running); `status=active` resumes and `next_run_at` recalculates on schedule changes. **`trigger_config` and `schedule` are FULL-REPLACE:** to add one keyword, `get-agent-job` → modify the returned object → resend the WHOLE thing. A partial send silently wipes sibling keys. |
| `delete-agent-job` | DELETE · **DES** | `workspace_id`*, `agent_id`*, `job_id`* | **Soft delete** — the job is recoverable for 7 days via `list-recently-deleted` → `restore-deleted`, BUT its linked Hunter/Engager campaign is destroyed immediately and cannot be restored. Confirm first; offer `status=paused` as the soft alternative. |
| `run-agent-job-now` | POST | `workspace_id`*, `agent_id`*, `job_id`*, `run_instructions`, `account_id` | Trigger a job immediately (optional one-off instructions). |
| `list-agent-job-runs` | GET · RO | `workspace_id`*, `agent_id`*, `job_id`*, `limit` | Run history: status, tools used, tokens, cost, output. |
| `list-agent-runs` | GET · RO | `workspace_id`*, `agent_id`, `status`, `since`, `limit` | **Workspace-wide** run history across all agents (agent/job attribution per run), newest first, default last 7 days (`since` widens the window). Prefer this for "what did my agents do". |
| `get-agent-run` | GET · RO | `workspace_id`*, `run_id`* | Full detail for one run: status, timing, cost, tokens, tool calls, final output, and error (stage/code) on failure. Drill-down after `list-agent-runs`. |

### The full agent loop
`list-agent-presets` → `hire-agent-preset` → (verify) `list-agent-jobs` →
`run-agent-job-now` → `list-agent-job-runs` (watch it work) →
`list-recurring-reviews` (its drafts land here) → `approve-recurring-review` /
`reject-recurring-review`. This closes the loop: the agent proposes, the human approves,
and rejections/edits feed Bolta's voice learning so it gets better.

### `paused_by` — explaining WHY something is paused
Jobs expose a read-only `paused_by` when `status=paused`. Use it to explain honestly and
to decide whether resuming is even possible:

| Value | Meaning | Resume rule |
|-|-|-|
| `user` | The user paused it themselves | Only resume on the user's explicit ask |
| `agent` | Cascade from an agent-level pause | Resume the agent (`update-agent status=active`) or the job directly |
| `trial_quota` / `plan_gate` | Plan or credit limit hit | A status flip comes right back — an upgrade is required; say so |
| `backpressure` | Too many undecided drafts piled up | Clear the review queue first, then resume |
| `system` | Bolta paused it (e.g. errors) | Investigate the runs before resuming |

**Never blind-resume.** Read `paused_by` (via `get-agent-job`) before setting
`status=active`, and never resume a `user`-paused job as a side effect of another task.

\* = required parameter.
