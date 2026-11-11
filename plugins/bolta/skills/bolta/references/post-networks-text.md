# Network settings: X, LinkedIn, Bluesky, Mastodon, Reddit, Discord

Set with `update-post-platform-details` (network `x`, `linkedin`, `bluesky`, `mastodon`, `reddit` or `discord`), only the keys that change; read back with `get-post-platform-details`. How settings work in general: [platforms](post-platforms.md).

## X

- **Kind of post**: `post_type` `TEXT`, `MEDIA`, `POLL`, `QUOTE`, `REPLY` or `THREAD`.
  - Poll: `poll_options` (2 to 4, 25 characters each) and `poll_duration_minutes` (5 to 10,080; one day if unset).
  - Quote: `quoted_tweet_id`. Reply: `in_reply_to_tweet_id`. Only ids the user gave.
  - Thread: the parts come from `bulk-create-posts` `contents`; without `THREAD` they go out as separate posts.
- **Who can reply**: `reply_settings` `everyone` (default), `mentioned_users` or `followers`.
- **Subscribers only**: `for_super_followers_only: true`, for accounts with subscriptions.
- Some text is required; media alone is refused.

## LinkedIn

- **Who sees it**: `visibility` `PUBLIC` (default) or `CONNECTIONS`.
- **As a company page**: `post_as_organization: true` with `selected_organization`, a page the account manages.
- **Also on other pages**: `cross_post_organizations` (a list) with `cross_post_enabled: true`.
- Up to 3,000 characters. A few hashtags at the end, at most.

## Bluesky

- `languages`: a list of language codes, such as `["en"]` or `["en", "es"]`.
- `include_facets` (default on): links, mentions and hashtags become tappable. Leave it on.
- 300 characters; longer is cut.

## Mastodon

- `visibility` `public`, `unlisted`, `private` (followers only) or `direct`.
- `sensitive: true` with `spoiler_text` hides the post behind a content warning.

## Reddit

- Both required: `title` (256 characters) and `selected_subreddit_id`. Without them it can't be approved or posted.
- `flair_id` or `flair_text` when the subreddit asks for flair. `nsfw`, `spoiler` as needed. `sendreplies` (default on) sends replies to the inbox.
- Write for the subreddit's rules: no hashtags, no sales pitch.

## Discord

- `selected_channel_id`: a channel in this brand's server. Required.
- An embed: `embed_enabled: true`, `embed_title`, `embed_description`, `embed_color` (a hex color like `#7B23CB`).

## Always

- No tool lists subreddits, LinkedIn pages or Discord channels. Copy from an earlier post or ask the user to pick it in Bolta. Never guess an id.
- Say every setting you changed in plain words, with the post it's on.
- A setting on an approved or scheduled post sends it back for review. Say so before changing it.
