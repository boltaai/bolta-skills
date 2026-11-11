# Network settings: X, LinkedIn, Bluesky, Mastodon, Reddit, Discord

Set with `update-post-platform-details` (network `x`, `linkedin`, `bluesky`, `mastodon`, `reddit` or `discord`), only the keys that change; read back with `get-post-platform-details`. How settings work in general: [platforms](post-platforms.md). Every network on one page: [at a glance](post-networks-at-a-glance.md).

## X

- **Several parts** (from `bulk-create-posts` `contents`: [post parts](post-parts.md)) always go out as a reply thread. In a thread a poll is dropped, a quote repeats on every part, and the first part can't be a reply.
- **Poll**: `post_type: "POLL"` with `poll_options` (2 to 4, 25 characters each) and `poll_duration_minutes` (5 to 10,080; one day if unset). Bolta doesn't check these; X refuses bad values.
- **Quote**: `quoted_tweet_id`. **Reply**: `in_reply_to_tweet_id`. Only ids the user gave.
- **Who can reply**: `reply_settings` takes only `everyone` (default), `mentioned_users` or `followers`. On X, `followers` means accounts it follows.
- **Subscribers only**: `for_super_followers_only: true`, for accounts that sell subscriptions.
- **Place**: `geo_place_id`, only an id the user gives.
- Images only: a video or GIF fails when the post goes out.
- Always write some text: media alone is refused (`schedule-post` turns away an X post with no text).

## LinkedIn

Company pages, posting to several pages, who sees it: [LinkedIn settings](post-networks-text-linkedin.md).

## Bluesky

- `languages`: a list of language codes, such as `["en"]` or `["en", "es"]`.
- `include_facets` (default on) makes links and @mentions tappable. Hashtags stay plain. Leave it on.
- 300 characters; longer is cut.
- Who can reply isn't sent to Bluesky from here yet. Don't offer it.

## Mastodon

- `visibility` `public`, `unlisted`, `private` (followers only) or `direct`.
- `sensitive: true` with `spoiler_text` hides the post behind a content warning.

## Reddit

- Both required: `title` (256 characters) and `selected_subreddit_id`. Without them it can't be approved or posted.
- `flair_id` or `flair_text` when the subreddit asks for flair. `nsfw`, `spoiler` as needed. `sendreplies` (default on) sends replies to the inbox. Don't offer `resubmit`: it's saved, not sent.
- Follow the subreddit's rules: no hashtags, no pitch.

## Discord

- `selected_channel_id`: a channel in this brand's server. Without one it schedules, then fails when it publishes: set it before the yes.
- An embed: `embed_enabled: true`, `embed_title`, `embed_description`, `embed_color` (a hex color like `#7B23CB`), `embed_footer`. A non-empty `embed_description` replaces the message text.
- Only Discord accounts connected before can be used; new ones can't be connected.
- In a `bulk-create-posts` item, a subreddit or channel name is accepted only if Bolta already synced it: [post parts](post-parts.md).

## Always

- No tool lists subreddits or Discord channels: copy from an earlier post or have the user pick in Bolta.
- LinkedIn pages come from `list-accounts`. Never guess an id.
- Name every setting you changed, with its post.
- A setting on an approved or scheduled post sends it back for review. Say so before changing it.
