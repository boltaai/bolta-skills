# Per-network keys: per account, network only, or details only

Which keys each network reads, and from where. How `platform_specific` works: [per network](post-per-network.md). What each key does, its values and when to use it: [network settings](post-settings.md).

- **Per account**: works in `platform_specific` at network level or under `accounts`, and with `update-post-platform-details`.
- **Network only**: works at network level in `platform_specific` (copied when the post saves) and with `update-post-platform-details`; an account entry is ignored.
- **Details only**: `update-post-platform-details` (or a batch item's details). In `platform_specific` it is kept and never used.

| Network | Per account | Network only | Details only |
|-|-|-|-|
| X (settings need one details call first: [X](post-settings-x.md)) | `text`, `reply_settings`, `for_super_followers_only` | `post_type`, `poll_options`, `poll_duration_minutes` | `quoted_tweet_id`, `in_reply_to_tweet_id`, `geo_place_id` |
| Threads | `text`, `topic_tag`, `is_ghost_post`, `is_spoiler_media`, `location_id` | | `use_topic_tag` (needed only here) |
| Instagram | `text` | `content_type`, `trialReelEnabled`, `trialGraduationStrategy`, `cover_url`, `thumbnail_offset`, `location_id`, `user_tags`, `product_tags` | |
| Facebook | `text`, per Page | | `primary_page`, `cross_post_pages`, `cross_post_enabled` |
| LinkedIn | `text`, `visibility`, per profile or page | | `post_as_organization`, `selected_organization`, `cross_post_organizations`, `cross_post_enabled` |
| TikTok | `privacy_level`, `disable_comments`, `disable_duet`, `disable_stitch`, `brand_organic_toggle`*, `brand_content_toggle`* | | |
| YouTube | `video_title`, `video_description`, `tags`, `category_id`, `privacy_status`, `self_declared_made_for_kids`, `allow_embedding`, `notify_subscribers`, `thumbnail_url` | | `publish_at` |
| Pinterest | `board_id` (Pinterest's id), `title`, `description`, `link`, `alt_text`, `cover_image_url` | | `board` (Bolta's id; no read shows it, so use `board_id`) |
| Bluesky | `text` | `languages`, `include_facets` | |
| Mastodon | `text` | `visibility`, `sensitive`, `spoiler_text` | |
| Reddit | `text`, `title`, `flair_id`, `flair_text`, `nsfw`, `spoiler`, `sendreplies` | | `selected_subreddit_id`; `title` must be saved here too |
| Discord | `text`, `channel`, `guild` (Discord's ids) | `embed_enabled`, `embed_title`, `embed_description`, `embed_color` | `selected_channel_id` (Bolta's id), `embed_footer` |
| WordPress | `title`, `slug`, `excerpt`, `categories`, `tags`, `meta_title`, `meta_description`, `comment_status`, `ping_status`, `sticky`, `format` | | `featured_media_id` |

\* `platform_specific` only: `update-post-platform-details` answers success and keeps nothing.

## Notes

- Instagram: keep every key at network level. A few read an account's entry for a single image or video, but a story or carousel check uses the network value, so mixed entries misbehave. Bad Instagram values are skipped, not refused.
- TikTok and YouTube: an account's entry replaces the network's keys entirely.
- Pinterest and WordPress: an account's entry merges with the network's.
- `text` is ignored by TikTok, YouTube, Pinterest and WordPress: a different caption there needs the network's own field (`video_description`, `description`, `excerpt`) or its own post.
- `slug` works only in `platform_specific`; `use_topic_tag` only matters with the details call.

## Saved, never used

Every network page lists its settings that are saved but not sent yet. Also never read on an account's entry: `useMainMedia`, `hashtags`, and `link` (except Pinterest's). Media and hashtags are the post's own. Any key not in the table above.

## Always

- Never offer a key listed as saved, not sent yet; say plainly it isn't possible here.
- Read back before saying a setting is set: unknown keys and bad values are dropped quietly.
- Never invent an id (board, channel, subreddit, location, account).
