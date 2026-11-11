# Reddit and Discord settings

How to set and which wins: [network settings](post-settings.md). Both show Markdown as written. No tool lists subreddits or channels: copy from an earlier post's `get-post-platform-details`, or the user picks in Bolta. Never guess.

## Reddit

Network `reddit`. Both required, or it can't be approved or posted:

- **Subreddit**: `selected_subreddit_id`, Bolta's id for a subreddit already synced. Details only (or `reddit_post_details` in a batch item, where `subreddit_name` also works) ([post parts](post-parts.md)). The user names a subreddit: save a one-item batch with `subreddit_name`. They point at an earlier post: copy its id.
- **Title**: `title`, up to 256 characters. Must be saved with the details (or the batch item); `platform_specific` `title` can then give one account a different title.

The rest, all both, per account:

- **Own body**: `text`.
- **Flair**: `flair_id` or `flair_text`, when the subreddit requires flair. Only flair the user or an earlier post gave.
- **NSFW**: `nsfw` (default false). **Spoiler**: `spoiler` (default false). Guidance: set them whenever the content is either; many subreddits remove unmarked posts.
- **Replies to inbox**: `sendreplies` (default true). Guidance: leave on, so replies can be answered.

What goes out: no media is a text post; one image an image post; 2 or more a gallery. With images only the title goes out, not the body. A video is refused. Links go in the body text.

- Guidance: read the subreddit's rules first; no hashtags, no pitch, a title that states the point, and give before asking. One subreddit per post.

Not sent: `resubmit` (Bolta refuses it); the composer's brand-affiliate tag. `scheduling_metadata` belongs to the web app's promotion mode; never send it.

Not possible here: video, link posts with a preview, crossposting to several subreddits from one post (Bolta's web app has a promotion mode for that), polls.

## Discord

Network `discord`. Only Discord accounts already connected can be used; new ones can't be connected.

- **Channel (required)**: `update-post-platform-details` `selected_channel_id` takes Bolta's id for the channel; `platform_specific` `channel` (with `guild`) takes Discord's own ids and wins. `selected_guild_id` (or `selected_guild`) is the server, Bolta's id; `channel_name` and `guild_name` are labels only. In a batch item, `discord_post_details` with `selected_channel_id` or `channel_name`. Without a channel it schedules, then fails when it goes out: set it before the yes.
- **Own message**: `text`. Both, per account. Up to 2,000 characters; longer is cut.
- **Embed**: a boxed message with a colored edge.
  - `embed_enabled: true`, `embed_title` (256), `embed_description`, `embed_color` (a hex color like `#7B23CB`; a malformed one fails the post): both, network only. `embed_footer` (256): details only. A batch item takes only the first three.
  - With `embed_description` set, the message text is replaced by the embed. Without it, the post's text shows twice: in the message and in the embed. Always set a description with an embed.
  - Guidance: an embed for release notes, announcements and events with a title; plain text for chat-style updates and questions.

Not possible here: mentions or pinging roles, an image or link inside the embed, threads, buttons.

## Always

- Never guess a subreddit, flair or channel id.
- Say where it goes: "Reddit: r/smallbusiness, titled '...'" or "Discord: #announcements, as an embed."
- Ask about NSFW and spoiler marks when the content could be either.
