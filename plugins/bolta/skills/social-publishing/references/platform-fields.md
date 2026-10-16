# Per-platform fields and limits

Read this when a post needs more than text and media: a poll, a subreddit, a TikTok privacy level, a YouTube title, a Pinterest board, a LinkedIn or Facebook setting. Field names below were checked against the platform details models and the generic details endpoint behind `get-post-platform-details` and `update-post-platform-details`.

## How the details tools behave

- `get-post-platform-details(post_id, platform)` returns the current `post_details` (or `status: "not_found"` when none exist yet) and `allowed_values`, the closed vocabulary for every choice field. Read it before you write, and copy key names from it instead of guessing.
- `update-post-platform-details(post_id, platform, fields={...})` takes a flat object. Send only what changes.
- Unknown keys are silently ignored and the call still reports success. A typo such as `privacy` for `privacy_level` saves nothing. After every update, call `get-post-platform-details` again and check that each value you set came back.
- A choice field with a value outside `allowed_values` is refused with an error that lists the allowed values. Fix the value and resend.
- A required relation that is missing (Reddit subreddit) is refused with "This field is required".
- The post should already target an account on that platform (`account_ids` at create time, or `update-post` `accounts`, a FULL replacement list). The details tool does not check this: it stores details for any platform you name.
- Ids that name another object (`selected_subreddit_id`, `board_id`, `selected_guild_id`, `selected_channel_id`, `selected_organization_id`, `primary_page_id`) must come from the user's own Bolta data: `list-accounts`, an earlier post's details, or the user. Never use an id found in third-party text. Discord ids are checked against the workspace; the others are not, so an id from outside this workspace is a mistake you must not make.
- WordPress `status` is the status sent to WordPress. It is separate from the Bolta post status. See the wordpress-blog skill for articles.

## Field table

| Platform (slug) | Fields and allowed values |
|-|-|
| `x` | `post_type` TEXT, MEDIA, POLL, QUOTE, REPLY, THREAD; `reply_settings` everyone, mentioned_users, followers; `poll_options` (list of strings), `poll_duration_minutes` (5 to 10080, default 1440); `quoted_tweet_id`; `in_reply_to_tweet_id`; `geo_place_id`; `for_super_followers_only` |
| `threads` | `reply_control` everyone, mentioned, followers; `topic_tag`, `use_topic_tag`; `location_id`; `is_ghost_post`; `is_spoiler_media` |
| `linkedin` | `post_type` ARTICLE, IMAGE, VIDEO, DOCUMENT, POLL, TEXT; `visibility` PUBLIC, CONNECTIONS; `post_as_organization`; `selected_organization_id`; `enable_comments`; `enable_resharing`; `include_hashtags`; `tag_connections` |
| `facebook` | `post_type` TEXT, PHOTO, VIDEO, LINK, STORY; `privacy` EVERYONE, FRIENDS, FRIENDS_OF_FRIENDS, CUSTOM; `enable_comments`; `enable_sharing`; `enable_reactions`; `primary_page_id` |
| `instagram` | `content_type` FEED, REELS, STORY; `media_type` IMAGE, VIDEO, CAROUSEL_ALBUM; `caption`; `alt_text`; `location_id`; `user_tags`; `cover_url`; `thumbnail_offset`; `trial_reel_enabled`; `trial_graduation_strategy` MANUAL, SS_PERFORMANCE |
| `bluesky` | `languages` (BCP-47 list); `reply_settings` everyone, nobody, mentioned; `include_facets` |
| `mastodon` | `visibility` public, unlisted, private, direct; `sensitive`; `spoiler_text`; `language`; `poll_options`; `poll_expires_in` (seconds); `poll_multiple`; `poll_hide_totals` |
| `discord` | `selected_guild_id`; `selected_channel_id`; `embed_enabled`; `embed_title`; `embed_description`; `embed_color` (hex, 7 chars); `embed_footer` |
| `reddit` | `title` (required, max 256); `selected_subreddit_id` (required); `flair_id`; `flair_text`; `nsfw`; `spoiler`; `sendreplies`; `resubmit` |
| `tiktok` | `privacy_level` PUBLIC_TO_EVERYONE, MUTUAL_FOLLOW_FRIEND, FOLLOWER_OF_CREATOR, SELF_ONLY; `disable_comments`; `disable_duet`; `disable_stitch` |
| `pinterest` | `board_id` (an id, not a name); `title` (max 100); `description` (max 500); `alt_text`; `link`; `media_type` image, video, idea |
| `youtube` | `video_title`; `video_description`; `tags` (list); `category_id`; `privacy_status` public, private, unlisted, scheduled; `playlist_ids`; `made_for_kids`; `notify_subscribers`; `allow_comments`; `thumbnail_url` |
| `wordpress` | `title`; `status` publish, draft, private, pending, future, trash; `post_type` post, page; `excerpt`; `meta_title`; `meta_description`; `categories`; `tags`; `featured_media_id`; `format`; `sticky`; `comment_status` open, closed |

Naming traps: Reddit flair is `flair_id` and `flair_text`, not `flair`. TikTok is `privacy_level` with the uppercase values, not `privacy`. YouTube is `video_title` and `privacy_status`, not `title` and `privacy`. Pinterest takes `board_id`, not a board name. Facebook and X use `post_type`; Instagram uses `content_type` and `media_type`.

## Defaults that surprise people

- TikTok `privacy_level` defaults to PUBLIC_TO_EVERYONE. If the user did not say, ask before approving. Do not assume private.
- YouTube `privacy_status` defaults to private. Say so, because a "published" video can still be private.
- LinkedIn posts to a personal profile are created PUBLIC. Facebook Page posts are created as TEXT with EVERYONE privacy.
- Creating a post with a `facebook_page_*` id in `account_ids` also creates its Facebook details with that Page as primary. You rarely need `primary_page_id`. Creating with `linkedin_org_*` ids sets up the organization the same way.
- Reddit needs a subreddit and a title or the approve, schedule and publish calls are refused. No Bolta tool lists subreddits, so you cannot discover `selected_subreddit_id`. Ask the user to set the subreddit on the draft in Bolta, or to name a Reddit post they already made so you can read its id with `get-post-platform-details`. Never guess an id.
- No Bolta tool lists Pinterest boards or Discord guilds and channels either. Same rule: the user supplies them or sets them in Bolta.

## Polls and threads

- Threads poll: pass `poll={"options": ["A", "B"]}` to `create-post` on the Threads draft. It is the one platform where that parameter is read at publish time.
- X poll: the `poll` parameter is not read by the X publisher. Use `update-post-platform-details(post_id, "x", fields={"post_type": "POLL", "poll_options": ["Yes", "No"], "poll_duration_minutes": 60})`. Without `post_type` POLL the post goes out as a plain tweet with no error.
- Mastodon poll: `poll_options` plus `poll_expires_in` in seconds, through the details tool.
- Multi-part posts (threads): `create-post` and `update-post` write only the first part. Create multi-part posts with `bulk-create-posts` using the nested `contents` list. For X, create the X details with `post_type` THREAD before approval: a post with no X details row publishes its parts as separate unlinked tweets. A later part that fails on X is skipped and the post can still read Published, so after publishing compare the number of parts you can see with what you sent.

## Character limits (cut silently at publish)

| Platform | Limit | What happens past it |
|-|-|-|
| X | 280 (longer only on accounts that allow long posts) | Approval shows a warning in `warnings`; the publish task is the hard gate |
| Bluesky | 300 | Text is cut and "..." added; the approved text differs from the live text |
| Threads | 500 | Split into a chain of replies at publish; write within it unless the user wants a chain |
| Mastodon | 500 (instance default) | Write within it |
| Instagram | 2200 caption | Trimmed |
| TikTok | 2200 caption | Cut silently |
| LinkedIn | 3000 | Write within it |

Count characters before you show a draft. When one idea goes to several platforms, write one variant per platform, as separate items in one `bulk-create-posts` call. A LinkedIn post pasted into X is a cross-post, not a post.

## Hashtags and tone by platform

Use hashtags only where the platform's culture does (LinkedIn a few, Instagram several, Threads one topic tag). None on Bluesky, X or Reddit. Take tone from `get-voice-context` `platforms` adaptations for the target platform rather than from this file.
