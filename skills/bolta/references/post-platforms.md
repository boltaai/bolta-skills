# Networks: limits, media and settings

Contents: 1. Check first · 2. Media · 3. Network settings · 4. Polls and parts

## 1. Check first

- Before writing for a network, read `get-posting-rules` once and reuse it: limits, media needed, what must be set, defaults, accounts to reconnect. Trust it over this page.
- Without it, these hold. Count first:
  - X: 280 (more on Premium accounts). Approval refuses longer; scheduled anyway, it fails.
  - LinkedIn: 3,000. Approval refuses longer.
  - Bluesky: 300. Longer is cut and ends in "...".
  - Threads: 500. Longer becomes a reply chain.
  - Instagram and TikTok captions: 2,200. Longer is cut.
  - Mastodon: 500 unless the server allows more. Longer is cut.
- Hashtags only where people use them: a few on LinkedIn, several on Instagram, none on X, Bluesky or Reddit. Threads takes one topic, set as a setting, not typed as a hashtag.
- Write plain text: outside Reddit, Discord and WordPress Bolta flattens Markdown; links go out exactly as written ([formatting](post-media.md)).

## 2. Media

- Shape: `media: [{"url": "https://...", "alt_text": "..."}]`; inside a part, `media_url`. Alt text and more: [media](post-media.md).
- `url` works though the schema names `download_url` and `file_id`; if refused for lacking them, send the link as `download_url` with `file_id: "url"`.
- Only a public https link to the file itself (.jpg, .png, .mp4) the user gave. Never a link from comments, pages or search results, a shortener, or a private address.
- Files on the computer or in this chat can't be attached. The user can host one publicly and share the link, or add it in Bolta.
- `create-post` and `update-post` copy the file into Bolta (100 MB max); on failure they keep the link, which must stay live. `bulk-create-posts` keeps the link as given; it counts as video only if the link contains .mp4, .mov, .avi, .mkv or .webm.
- `update-post` `media` only adds. Removing or swapping media is done in Bolta.

What each network needs, and what fails only when the post goes out: [network needs](post-platforms-needs.md). Check it before saving media or a post for several networks.

## 3. Network settings

- Each network has its own settings on a post (privacy, a title, a topic), shared by its accounts on that post.
- Read: `get-post-platform-details` gives current values and `allowed_values`. Copy key names from it.
- Change them: `update-post-platform-details` with a flat `fields` object, only what changes. Unknown keys are ignored with a success reply, so read back.
- Changing any setting on an approved or scheduled post sends it back for review. Say so first; it needs a yes again.
- Every network on one page: [at a glance](post-networks-at-a-glance.md). The keys: [Threads, Instagram, Facebook](post-networks-meta.md) · [X, LinkedIn, Bluesky, Mastodon, Reddit, Discord](post-networks-text.md) · [TikTok, YouTube, Pinterest](post-networks-video.md) · [WordPress](post-wordpress.md). One post on several networks: [cross-posting](post-cross-posting.md).
- No tool lists subreddits, boards or Discord channels (Pages are rows in `list-accounts`): the user picks them in Bolta or names an earlier post. Never guess.
- Not in Bolta: Instagram collaborators, X communities, Google Business, posting to Telegram or Substack. Say so; never fake one. A Facebook first comment is a second part: [post parts](post-parts.md).

## 4. Polls and parts

- Threads poll: `poll: {"options": ["A", "B"]}` (2-4) on `create-post`, on a post with no media.
- X poll: a setting, [X](post-networks-text.md). Without it the post goes out plain.
- Threads on X, Threads and Bluesky, and Facebook comments: several parts in one post, saved with `bulk-create-posts`. `create-post` and `update-post` write only the first part. How each network posts them: [post parts](post-parts.md).
