# Bolta MCP Tools — Canonical Reference

The single source of truth for every tool the Bolta plugin exposes. Skills MUST use
these exact tool ids and parameter names. The server is **mcp.bolta.ai/mcp** (StreamableHTTP,
stateless). **68 tools** are exposed. Any tool name not on this list does not exist — do not
call it. In particular the Agent / Job / Run / Preset tools and `start-workflow` /
`get-workflow-run` were **removed from the MCP surface** (SERVER:
`resources/architecture/SKILLS_FIRST_ARCHITECTURE_AUDIT_2026-08.md`): their REST endpoints
still exist for the Bolta dashboard, but they are not tools any more. Automation is
Routines, and only Routines.

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
| `approve-post` | POST | `workspace_id`*, `post_id`*, `schedule_mode`, `expected_fingerprint`, `fixed_time`, `timezone`, `comments` | Approve a post in review. **Pass `expected_fingerprint`** — the `content_fingerprint` from your most recent read of the item (`list-inbox-items` / `list-reviews`) — to guarantee you approve exactly the revision reviewed. A **409 `stale_review`** means the post changed since review; the 409 deliberately carries no fingerprint, so NEVER blindly retry — re-read the item, show the user the current content, get a fresh decision, then retry with the fresh fingerprint. Review rows with status `autonomous` were scheduled by autonomy policy, not human-approved. |
| `list-reviews` | GET · RO | `workspace_id`*, `reviewer_id`, `workflow_type`, `limit`, `page` | Standard review queue. |
| `list-recurring-reviews` | GET · RO | `workspace_id`*, `status`, `template_id`, `agent_creator_id`, `limit`, `page` | **Pending drafts produced by automation** (routine runs). This is the routine → human queue; `agent_creator_id` is the producer id echoed on inbox rows. |
| `list-inbox-items` | GET · RO | `workspace_id`*, `source` (team\|recurring\|hunter\|report), `status`, `agent_id`, `limit`, `offset` | **Unified inbox** of everything pending review — team posts, recurring drafts, hunter reply drafts (with the mention/lead context they respond to), and reports (with download links). Pass `agent_id` (the producer id echoed on rows) to answer "what did that routine produce that needs me?". Prefer this for "what's waiting for me". Team rows carry `content_fingerprint` (echo as `expected_fingerprint` on `approve-post`) and, for run-produced drafts, `workflow_run_id` (group them as one batch). |
| `approve-recurring-review` | POST | `review_id`*, `approvalComments`, `approveWithSchedule`, `useSuggestedTime`, `newScheduleTime`, `account_ids` | Approve an agent-produced draft. `newScheduleTime` (ISO8601) = "approve it but post Friday 9am" in one call; `account_ids` retargets at approval time. |
| `reject-recurring-review` | POST | `review_id`*, `rejectionReason`, `rejectionCategories` | Reject an agent-produced draft (feeds voice learning). ALWAYS pass `rejectionCategories` when the objection fits a code — structured categories train the voice far better than free text. Valid codes: too_casual, too_formal, wrong_tone, off_brand, too_long, too_short, wrong_format, factual_error, spelling_grammar, missing_cta, wrong_cta, wrong_emoji, wrong_hashtag, not_engaging, platform_mismatch, too_salesy, off_topic, repetitive, other (invalid codes are silently dropped). |
| `send-hunter-reply` | POST | `workspace_id`*, `reply_id`*, `content` | Approve + send a hunter reply draft (from `list-inbox-items`, `source=hunter`). Optional `content` overrides the draft text in the same call. Double-send is prevented server-side. |
| `update-hunter-reply` | PATCH | `workspace_id`*, `reply_id`*, `content`* | Edit a hunter reply draft **without sending** (already-sent replies 409). Send later via `send-hunter-reply`. |

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

## Routines (the automation surface)

A **Routine** is what a customer configures: a repeatable outcome + a trigger + an execution
policy. It binds to a **WorkflowDefinition** (the server-enforced runtime contract — objective
schema, execution modes, and a hard tool allowlist that is never exposed over MCP) and is
usually created from a **RoutineTemplate** (the user-facing behavior description and its
compatibility matrix). The execution principal a run borrows is provisioned server-side;
there is nothing for the user to hire and no lower level to drop to.

| Tool | Method | Params | Notes |
|-|-|-|-|
| `list-routine-templates` | GET · RO | `workspace_id`*, `outcome_goal`, `source` | The first-party template library: what outcome each produces, which triggers/sources/approval policies are legal, and the instructions it seeds. **Start here** when the user describes something they want happening repeatedly. Templates with `available_in_workspace: false` cannot be created yet — say so rather than trying. |
| `list-workflow-definitions` | GET · RO | `workspace_id`* | The runtime contracts a routine can bind to. Use it to discover valid `workflow_definition_key` values instead of guessing. |
| `list-routines` | GET · RO | `workspace_id`*, `status`, `template_key`, `limit` | The workspace's routines and their state. |
| `get-routine` | GET · RO | `workspace_id`*, `routine_id`* | One routine in full: trigger, schedule, timezone, instructions, approval policy, sources. Read this BEFORE any edit. |
| `create-routine` | POST | `workspace_id`*, `name`*, `goal`*, `template_key`, `workflow_definition_key`, `outcome_category`, `trigger_type`, `schedule`, `timezone`, `instructions`, `approval_policy` | Save a repeatable outcome. Pass a `template_key` from `list-routine-templates` (recommended) or a `workflow_definition_key`. **The routine is created as a DRAFT and never fires until `activate-routine`** — creating is not arming. `approval_policy` may only ever TIGHTEN the workspace policy: `review_every_artifact` always forces human approval, `auto` is honoured only where the workspace already allows it. Ask whether posts need approval; don't assume. |
| `update-routine` | PATCH | `workspace_id`*, `routine_id`*, `name`, `goal`, `trigger_type`, `schedule`, `timezone`, `instructions`, `approval_policy`, `capability_keys`, `output_config`, `source_bindings` | Edit a routine. `get-routine` first — nested objects (`schedule`, `source_bindings`, `output_config`) replace wholesale, so resend the whole object rather than one key. |
| `activate-routine` | POST · **OW** | `workspace_id`*, `routine_id`* | Arm it. The server re-validates the whole definition against current workspace state here, so activation can fail with a typed reason (missing source, disconnected account, plan gate) even though saving succeeded. Tell the user what will now happen and when the first run is due. |
| `pause-routine` | POST | `workspace_id`*, `routine_id`* | Stop the trigger firing; the routine keeps its config. |
| `resume-routine` | POST · **OW** | `workspace_id`*, `routine_id`* | Re-arm a paused routine. Never resume one the user paused themselves without an explicit ask. |
| `archive-routine` | POST · **DES** | `workspace_id`*, `routine_id`* | **Terminal** — an archived routine can only be duplicated, not revived. Confirm first; offer `pause-routine` as the soft alternative. |
| `run-routine-now` | POST · **OW** | `workspace_id`*, `routine_id`* | Fire it once, immediately, outside its schedule. Idempotent: an in-flight run is returned rather than a second one started (`started: false`). |
| `list-routine-runs` | GET · RO | `workspace_id`*, `routine_id`*, `limit` | One routine's run history: status, timing, and what each run produced. |

### The full routine loop
`list-routine-templates` → `create-routine` → `activate-routine` → (`run-routine-now` to see
it work immediately) → `list-routine-runs` → `list-inbox-items` (its drafts land here) →
`approve-post` / `approve-recurring-review` / `reject-recurring-review`. This closes the
loop: the routine proposes, the human approves, and rejections/edits feed Bolta's voice
learning so it gets better.

### Three things worth saying every time
- **A new routine is a draft.** It does not fire until `activate-routine`.
- **Schedule times are wall clock** in the routine's timezone. Never send a UTC offset and
  never convert the user's stated time yourself.
- **Approval policy can tighten but never loosen** the workspace's own safety posture.

### Explaining WHY something is paused
A paused routine may have been paused by the user or by Bolta. Read `get-routine` before
resuming and explain honestly:

| Cause | Resume rule |
|-|-|
| The user paused it | Only resume on the user's explicit ask |
| Plan or credit limit hit | A status flip comes right back — an upgrade is required; say so |
| Backpressure (too many undecided drafts) | Clear the review queue first, then `resume-routine` |
| Bolta paused it after errors | Read `list-routine-runs` before resuming |

**Never blind-resume,** and never resume a user-paused routine as a side effect of another
task.

\* = required parameter.
