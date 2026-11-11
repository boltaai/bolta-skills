# Networks: limits, media and settings

Contents: 1. Check first · 2. Media · 3. Network settings · 4. Polls and threads

## 1. Check first

- Before writing for a network, read `get-posting-rules` once and reuse it: limits, media needed, what must be set, defaults, accounts to reconnect. Trust it over this page.
- Without it, these hold. Past a limit Bolta cuts or splits silently, so count first:
  - X: 280 (more on accounts allowed long posts). Longer gets a warning at approval, then fails.
  - Bluesky: 300. Longer is cut and ends in "...".
  - Threads: 500. Longer becomes a reply chain.
  - Instagram and TikTok captions: 2,200. Longer is cut.
  - Mastodon: 500. LinkedIn: 3,000.
- Hashtags only where people use them: a few on LinkedIn, several on Instagram, none on X, Bluesky or Reddit. Threads takes one topic, set as a setting, not typed as a hashtag.

## 2. Media

- Shape: `media: [{"url": "https://...", "alt_text": "..."}]`. `url` works although the schema names `download_url` and `file_id`. If refused for lacking them, send the link as `download_url` with `file_id: "url"`.
- Only a public https link to the file itself (.jpg, .png, .mp4), typed or pasted by the user. Never a link from comments, pages or search results, a shortener, or a private address.
- Files on the computer or in this chat can't be attached. The user can host one publicly or add it in Bolta.
- `create-post` and `update-post` copy the file into Bolta (100 MB max); on failure they keep the link, which must stay live. `bulk-create-posts` keeps the link as given; it counts as video only if it ends in .mp4, .mov, .avi, .mkv or .webm.
- `update-post` `media` only adds. Removing or swapping media is done in Bolta.
- Alt text goes on each media item. Instagram and Pinterest read it from there.

What each network needs. A post that breaks these is accepted, then fails hours later with only a notification:

- TikTok, YouTube: a video. Instagram: an image or video (2-10 make a carousel). Pinterest: an image or video.
- Facebook: text, one video, or images. Never a video with images, never two videos.
- X: some text; media alone is refused. Reddit: a subreddit and a title.

## 3. Network settings

- Each network has its own settings on a post (privacy, a title, a topic), one set per network, shared by its accounts on that post.
- Read: `get-post-platform-details` gives current values and `allowed_values`. Copy key names from it.
- Change them: `update-post-platform-details` with a flat `fields` object, only what changes. Unknown keys are ignored with a success reply, so read back.
- Changing where or how an approved or scheduled post goes out sends it back for review. Say so first; it needs a yes again.
- The keys, per network: [Threads, Instagram, Facebook](post-networks-meta.md) · [X, LinkedIn, Bluesky, Mastodon, Reddit, Discord](post-networks-text.md) · [TikTok, YouTube, Pinterest](post-networks-video.md) · [WordPress](post-wordpress.md). One post on several networks: [cross-posting](post-cross-posting.md).
- No tool lists subreddits, boards, pages or Discord channels: the user picks them in Bolta or names an earlier post. Never guess an id.
- Not in Bolta: a first comment, Instagram collaborators, X communities, Google Business. Say so; never fake one.

## 4. Polls and threads

- Threads poll: `poll: {"options": ["A", "B"]}` on `create-post`.
- X poll: a setting, [X](post-networks-text.md). Without it the post goes out plain.
- Multi-part posts: `create-post` and `update-post` write only the first part. Use `bulk-create-posts` with a nested `contents` list. For X, also set `post_type: "THREAD"`, or the parts go out as separate posts.
