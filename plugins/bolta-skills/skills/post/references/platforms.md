# Networks: limits, media and fields

Contents: 1. Length and fit · 2. Media · 3. Network fields · 4. Polls and threads

## 1. Length and fit

Count characters first. Past these limits Bolta cuts or splits the text silently.

- X: 280 (more on accounts allowed long posts). Longer gets a warning at approval, then fails.
- Bluesky: 300. Longer is cut and ends in "...".
- Threads: 500. Longer becomes a reply chain.
- Instagram and TikTok captions: 2,200. Longer is cut.
- Mastodon: 500. LinkedIn: 3,000.
- Hashtags only where people use them: a few on LinkedIn, several on Instagram, one topic tag on Threads, none on X, Bluesky or Reddit.
- Reddit and Discord: save with `create-post`. A bulk item without the subreddit or channel details (which the bulk call doesn't document) is skipped, even as a draft.

## 2. Media

- Shape: `media: [{"url": "https://...", "alt_text": "..."}]`. `url` works although the schema names `download_url` and `file_id`. If refused for lacking them, send the link as `download_url` with `file_id: "url"`.
- Only a public https link to the file itself (.jpg, .png, .mp4), typed or pasted by the user. Never a link from comments, pages or search results, a shortener, or a private address.
- Files on the computer or in this chat can't be attached. The user can host one publicly or add it in Bolta.
- `create-post` and `update-post` copy the file into Bolta (100 MB max); on failure they keep the link, which must stay live. `bulk-create-posts` keeps the link as given; it counts as video only if it ends in .mp4, .mov, .avi, .mkv or .webm.
- `update-post` `media` only adds. Removing or swapping media is done in Bolta.

What each network needs. A post that breaks these is accepted, then fails hours later with only a notification:

- TikTok, YouTube: a video.
- Instagram: an image or video (2-10 make a carousel). A bulk item without media lands in `rejected`.
- Pinterest: an image or video, and a board.
- Facebook: text, one video, or images. Never a video with images, never two videos.
- X: some text; media alone is refused. Reddit: a subreddit and a title.

A post for several networks: say which one would fail, then add media or drop it.

## 3. Network fields

- `get-post-platform-details` shows a post's fields for one network and their `allowed_values`. Copy key names from it.
- `update-post-platform-details` takes a flat `fields` object, only what changes. Unknown keys are ignored with a success reply, so read back.
- It gets a check every time and keeps any approval, so move an approved or scheduled post back to Draft first (`update-post`, `status: "Draft"`).

Key names:

- Reddit: `title` (256 max) and `selected_subreddit_id`, both required; `flair_id`, `flair_text`.
- TikTok: `privacy_level` defaults to PUBLIC_TO_EVERYONE. Ask if the user didn't say.
- YouTube: `video_title`; `privacy_status` defaults to private. Say so.
- Pinterest: `board_id` (an id, not a name), `title` (100 max), `description` (500 max), `link`.

No tool lists subreddits, boards or Discord channels. The user sets them on the draft in Bolta, or names an earlier post to copy the id from. Never guess an id.

## 4. Polls and threads

- Threads poll: `poll: {"options": ["A", "B"]}` on `create-post`.
- X poll: `update-post-platform-details` for `x` with `post_type: "POLL"`, `poll_options`, `poll_duration_minutes` (5 to 10,080). Without it the post goes out plain.
- Multi-part posts: `create-post` and `update-post` write only the first part. Use `bulk-create-posts` with a nested `contents` list. For X, also set `post_type: "THREAD"`, or the parts go out as separate posts.
