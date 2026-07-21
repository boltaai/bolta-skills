---
name: bolta-platform-tailoring
description: >
  Set per-platform options on a Bolta post — polls, flair, titles, privacy, boards. Use this
  skill when the user asks to "add a poll to the Threads post", "set the Reddit flair", "set the
  YouTube title and privacy", "add Pinterest board and link", "pick TikTok privacy", "add a
  poll to the X post", or otherwise wants platform-specific fields beyond plain text and media.
  Covers X, Threads, LinkedIn, Facebook, Instagram, Bluesky, Mastodon, Discord, Reddit, TikTok,
  Pinterest, YouTube, and WordPress.
---

# Bolta — Platform Tailoring

Add the platform-specific extras a post needs: a poll, a subreddit flair and title, a video
privacy setting, a Pinterest board, a YouTube title. Threads polls have a dedicated `poll`
param on `create-post`; everything else — including X polls — goes through the
platform-details tools.

## When to use
The user wants fields that are specific to one platform — not just text (bolta-draft-post) or
media (bolta-post-media).

## Tools this skill uses
| Tool | Why |
|-|-|
| `list-workspaces` | Resolve `workspace_id` if unknown. |
| `get-post` | Read the current post before editing per-platform details. |
| `create-post` | Create a post; supports a `poll` object at creation (Threads only). |
| `get-post-platform-details` | Read current per-platform fields for a post + platform. |
| `update-post-platform-details` | Set per-platform `fields` (poll, flair, title, privacy…). |

## Prerequisites
- `workspace_id` — resolve once via `list-workspaces`, reuse. Auth is automatic via the Bolta
  connector's OAuth grant — never ask for an API key. Default new content to Draft; confirm
  before publish/delete.
- The `post_id` for an existing post (or create one first with `create-post`).
- The exact platform slug: one of `x`, `threads`, `linkedin`, `facebook`, `instagram`,
  `bluesky`, `mastodon`, `discord`, `reddit`, `tiktok`, `pinterest`, `youtube`, `wordpress`.

## Critical: unknown keys are silently dropped

The server ignores any `fields` key it doesn't recognize and **still returns success**. A typo
(`privacy` instead of `privacy_level`) is a reported-success no-op — nothing saved, no error.
So after every `update-post-platform-details`, ALWAYS do a verify-read:
call `get-post-platform-details(post_id, platform)` and confirm each value you set actually
came back changed. If a value didn't stick, the key name was wrong — use the table below.

## Workflow

### Polls
- **Threads:** pass a `poll` object to `create-post`:
  `poll = { "options": ["Ship it", "Wait"], "duration_minutes": 1440 }`.
- **X:** the `create-post` `poll` param does NOT work for X — the X publisher only reads
  `XPostDetails.poll_options`, and nothing syncs the two. An X poll set via `create-post`
  publishes as a plain tweet with no poll and no error. Route X polls through
  `update-post-platform-details(post_id, "x", fields={"post_type": "POLL",
  "poll_options": ["Yes", "No"], "poll_duration_minutes": 60})`. `post_type` must be
  `"POLL"` or the options are ignored at publish time.
- **Mastodon:** `poll_options` (list) + `poll_expires_in` (seconds, not minutes) via
  `update-post-platform-details`.

### Richer per-platform fields
1. Resolve `post_id` (create the post first if needed).
2. Read current values: `get-post-platform-details(post_id, platform)`.
3. Set values: `update-post-platform-details(post_id, platform, fields={...})`. `fields` is an
   object of platform-specific keys — set only what you're changing. Use the exact key names
   below; anything else is silently dropped.
4. Verify-read: `get-post-platform-details` again and compare against what you sent.
5. Confirm back what was set. Keep new content as a Draft unless the user asked to publish.

### Field names by platform (verified against the server)
| Platform | Fields |
|-|-|
| `x` | `post_type` (`TEXT`/`MEDIA`/`POLL`/`QUOTE`/`REPLY`/`THREAD`), `reply_settings` (`everyone`/`mentioned_users`/`followers`), `poll_options` (list of strings), `poll_duration_minutes`, `quoted_tweet_id`, `in_reply_to_tweet_id` |
| `threads` | `topic_tag`, `use_topic_tag`, `location_id`, `reply_control` (`everyone`/`mentioned`/`followers`), `is_ghost_post`, `is_spoiler_media` — poll goes via `create-post` |
| `linkedin` | `post_type`, `visibility` (`PUBLIC`/`CONNECTIONS`), `post_as_organization`, `selected_organization_id`, `enable_comments`, `enable_resharing` |
| `facebook` | `primary_page_id` (**required** on first-time creation), `post_type` (`TEXT`/`PHOTO`/`VIDEO`/`LINK`/`STORY`), `privacy` (`EVERYONE`/`FRIENDS`/…), `enable_comments`, `enable_sharing` |
| `instagram` | `content_type` (`FEED`/`REELS`/`STORY`), `media_type` (`IMAGE`/`VIDEO`/`CAROUSEL_ALBUM`), `caption`, `alt_text`, `location_id`, `user_tags`, `cover_url`, `thumbnail_offset` |
| `bluesky` | `languages` (BCP-47 list), `reply_settings` (`everyone`/`nobody`/`mentioned`), `include_facets` |
| `mastodon` | `visibility` (`public`/`unlisted`/`private`/`direct`), `sensitive`, `spoiler_text`, `language`, `poll_options`, `poll_expires_in` (seconds), `poll_multiple`, `poll_hide_totals` |
| `discord` | `selected_guild_id`, `selected_channel_id`, `embed_enabled`, `embed_title`, `embed_description`, `embed_color` (hex), `embed_footer` |
| `reddit` | `title`, `selected_subreddit_id` (**required** on first-time creation — a missing subreddit 400s), `flair_id`, `flair_text`, `nsfw`, `spoiler`, `sendreplies` |
| `tiktok` | `privacy_level` (`PUBLIC_TO_EVERYONE`/`MUTUAL_FOLLOW_FRIEND`/`FOLLOWER_OF_CREATOR`/`SELF_ONLY`), `disable_comments`, `disable_duet`, `disable_stitch` |
| `pinterest` | `board_id` (board **ID**, not name — a name string won't resolve), `title`, `description`, `alt_text`, `link`, `media_type` (`image`/`video`/`idea`) |
| `youtube` | `video_title`, `video_description`, `tags` (list), `category_id`, `privacy_status` (`public`/`private`/`unlisted`), `playlist_ids`, `made_for_kids`, `notify_subscribers`, `thumbnail_url` |
| `wordpress` | `title`, `status`, `excerpt`, `meta_title`, `meta_description`, `categories` (list), `tags` (list), `featured_media_id`, `format`, `sticky`, `comment_status` |

Note the naming traps: Reddit flair is `flair_id`/`flair_text` (not `flair`), TikTok is
`privacy_level` with the enum values above (not `privacy: "public"`), YouTube is
`video_title`/`privacy_status` (not `title`/`privacy`), Pinterest takes a `board_id` FK
(not a board name). When in doubt, call `get-post-platform-details` first and mirror the
key names it returns — don't invent field names.

## Failure handling
- Unknown platform slug → confirm the exact platform; only the 13 listed above are valid.
- Verify-read shows a value didn't stick → the key was silently dropped; fix the key name
  from the table above and resend.
- Required-relation 400 (Reddit `selected_subreddit_id`, Facebook `primary_page_id`) → the
  first-time save needs that ID; look it up before creating details.
- Poll with fewer than 2 options or an invalid duration → fix before sending.
- Setting details on a post not connected to that platform → the post's `account_ids` must include
  an account for that platform; add it via bolta-draft-post/update first.
- Permission error → report the missing role/scope; leave the post as-is.

## Example
User: "Set the Reddit post's flair to Discussion and give it a title."
1. `list-workspaces` → workspace_id; resolve `post_id`.
2. `get-post-platform-details(post_id, "reddit")` → current values; note whether
   `selected_subreddit_id` is already set (required on first-time creation).
3. `update-post-platform-details(post_id, "reddit", fields={"flair_text":"Discussion","title":"How we cut build times 40%"})`.
4. `get-post-platform-details(post_id, "reddit")` → confirm `flair_text` and `title` stuck.
5. "Reddit flair set to Discussion with that title. It's still a Draft — schedule or publish?"
