# Networks: limits, media and settings

## 1. Check first

- Before writing for a network, read `get-posting-rules` once and reuse it: limits, media needed, what must be set, defaults, accounts to reconnect. Trust it over this page.
- Without it, these hold. Count first:
  - X: 280 (more on Premium accounts). Approval refuses longer; scheduled anyway, it fails.
  - LinkedIn: 3,000. Approval refuses longer.
  - Bluesky: 300. Longer is cut and ends in "...".
  - Threads: 500. Longer becomes a reply chain.
  - TikTok captions: 2,200. Longer is cut.
  - Instagram captions: 2,200. Not checked: Instagram may refuse longer.
  - Mastodon: 500 unless the server allows more. Longer is cut.
- Hashtags only where people use them: a few on LinkedIn, several on Instagram, none on X, Bluesky or Reddit. Threads takes one topic, set as a setting, not typed as a hashtag.
- Write plain text: outside Reddit, Discord and WordPress Bolta flattens Markdown ([formatting and links](post-media.md)).

## 2. Media

- Shape: `media: [{"url": "https://...", "alt_text": "..."}]`; inside a part, `media_url`. Alt text and more: [media](post-media.md).
- `url` works though the schema names `download_url` and `file_id`; if refused for lacking them, send the link as `download_url` with `file_id: "url"`.
- Only a public https link to the file itself (.jpg, .png, .mp4) the user gave. Never a link from comments, pages or search results, a shortener, or a private address.
- Files on the computer or in this chat can't be attached. The user can host one publicly and share the link, or add it in Bolta.
- `create-post` and `update-post` copy the file into Bolta (100 MB max); on failure they keep the link without saying so, and it must stay live. `bulk-create-posts` keeps the link as given; it counts as video only if the link ends in .mp4, .mov, .avi or .mkv.
- `update-post` `media` only adds. Removing or swapping media is done in Bolta.

What each network needs, and what fails only when the post goes out: [network needs](post-platforms-needs.md).

## 3. Network settings

- Each network has its own settings on a post (privacy, a title, a topic). Set in `create-post` or `update-post`, per network or per account, with `platform_specific`: [per network](post-per-network.md).
- Read: `get-post-platform-details` gives current values and `allowed_values`. Copy key names from it.
- Or on a saved post: `update-post-platform-details`, a flat `fields` object, only what changes, shared by the network's accounts. Unknown keys get a success reply, so read back. X settings always go this way first ([X](post-settings-x.md)).
- Changing any setting on an approved or scheduled post sends it back for review: say so first.
- Every setting, how to set it and which way wins: [network settings](post-settings.md). Every network on one page: [at a glance](post-networks-at-a-glance.md). Several networks: [cross-posting](post-cross-posting.md).
- No tool lists subreddits, boards or Discord channels (Pages are rows in `list-accounts`): the user picks them in Bolta or names an earlier post. Never guess.
- Not in Bolta: Instagram collaborators, X communities, Google Business, posting to Telegram or Substack. Say so; never fake one.

## 4. Polls and parts

- Polls: Threads takes `poll: {"options": ["A", "B"]}` (2-4) on `create-post`, with no media. X ignores `poll`; its poll is a setting ([X](post-settings-x.md)).
- Threads on X, Threads and Bluesky, and Facebook comments: several parts in one post, saved with `bulk-create-posts`. `create-post` and `update-post` write only the first part: [post parts](post-parts.md).

## Always

- Count every text against its network's limit before saving.
- Media only from a public link the user gave.
- Read back before saying a setting is set.
