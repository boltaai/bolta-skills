# Per-network keys: what each network reads

The keys `platform_specific` takes, per network, and what is saved but never used. How it works: [per network](post-per-network.md). What each setting means: [Threads, Instagram, Facebook](post-networks-meta.md) · [X, LinkedIn, Bluesky, Mastodon, Reddit, Discord](post-networks-text.md) · [TikTok, YouTube, Pinterest](post-networks-video.md) · [WordPress](post-wordpress.md).

## Keys, by network

| Network | `text` used | Other keys read (network or account) |
|-|-|-|
| X | Yes | `reply_settings`, `for_super_followers_only` |
| Threads | Yes | `topic_tag` (no `use_topic_tag` needed here), `is_ghost_post`, `is_spoiler_media`, `location_id` |
| Instagram | Yes | `content_type`, `location_id`, `cover_url`, `thumbnail_offset`; trial reel below |
| Facebook | Yes, per Page | none |
| LinkedIn | Yes, per profile and per page | `visibility` |
| Bluesky, Mastodon | Yes | none |
| Reddit | Yes | `title`, `flair_id`, `flair_text`, `nsfw`, `spoiler`, `sendreplies` |
| TikTok | No: the post's text is the caption | `privacy_level`, `disable_comments`, `disable_duet`, `disable_stitch`, `brand_organic_toggle`, `brand_content_toggle` |
| YouTube | No | `video_title`, `video_description`, `tags`, `category_id`, `privacy_status`, `self_declared_made_for_kids`, `allow_embedding`, `notify_subscribers` |
| Pinterest | No | `title`, `description`, `link`, `board_id` |
| WordPress | No | `title`, `excerpt`, `categories`, `tags`, `meta_title`, `meta_description`, `comment_status`, `sticky`, `format` |

A different caption for TikTok, YouTube, Pinterest or WordPress needs its own post, or the network's own field (`video_description`, `description`, `excerpt`).

## Instagram trial reel

`{"instagram": {"content_type": "REELS", "trialReelEnabled": true, "trialGraduationStrategy": "SS_PERFORMANCE"}}` on `create-post` (or `update-post`) makes a trial reel: shown to non-followers first; `SS_PERFORMANCE` shares it with followers if it does well, `MANUAL` (the default) leaves that to the user in Instagram.

- One setting for the whole post: every Instagram account on it gets the same.
- It needs `REELS` and one video. Without `REELS` the trial is switched off; with an image it goes out as a normal post. Any other strategy value becomes `MANUAL`.
- Bad Instagram values are skipped, not refused: read back with `get-post-platform-details` (network `instagram`) before saying it is set.

## Saved, never used

- Threads `reply_control`: who can reply is not sent to Threads. Don't offer it.
- Facebook `location`, `feeling`, `activity`: not sent.
- On an account's entry, `useMainMedia`, `hashtags` and `link` (except Pinterest's pin link): not read. Media and hashtags are the post's own.
- Any key not listed above.

## Pinterest board ids

`board_id` here is Pinterest's own board id. `update-post-platform-details` takes a different one, Bolta's id for the board, and `get-post-platform-details` shows that one. Never copy one into the other. No tool lists boards: the user picks in Bolta or names an earlier pin.

## WordPress

Article settings only; the text is the article. `wordpress_post_id` is ignored: an article is never pointed at an existing WordPress post from here. New category and tag names are created on the site when it goes out, so match the existing spelling.

## Always

- Never offer a key marked saved, never used; say plainly it isn't possible here.
- Read back before saying a setting is set: unknown keys and bad values are dropped quietly.
- Never invent an id (board, location, account).
