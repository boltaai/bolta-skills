# Network settings: TikTok, YouTube, Pinterest

Set with `update-post-platform-details` (network `tiktok`, `youtube` or `pinterest`), only the keys that change; read back with `get-post-platform-details`. How settings work in general: [platforms](post-platforms.md). Every network on one page: [at a glance](post-networks-at-a-glance.md).

All three need media attached to the post (a public https link): a video for TikTok and YouTube, exactly one image or one video for Pinterest. No media: skip the network and say why.

## TikTok

- **Who sees it**: `privacy_level` `PUBLIC_TO_EVERYONE` (the default), `MUTUAL_FOLLOW_FRIEND`, `FOLLOWER_OF_CREATOR` or `SELF_ONLY`. TikTok may narrow it to what the account allows. The user didn't say? Ask; never assume public.
- **Interactions**: `disable_comments`, `disable_duet`, `disable_stitch` (each true or false).
- **Paid or brand content**: the disclosure switches are set in Bolta's composer only. If the video promotes the user's own business or a paid partner, say so and send them there before it goes out.
- Caption up to 2,200 characters; longer text is cut off at that point.

## YouTube

- **Title**: `video_title`. Empty: built from the first 95 characters of the text, which rarely reads well. Always set one. Bolta doesn't check YouTube's own title limit, so keep it short.
- **Who sees it**: `privacy_status` `private` (the default), `public` or `unlisted` (don't use `scheduled`). A video saved without changing it goes up private. Say so, and ask.
- **Made for kids**: `self_declared_made_for_kids` (true or false) is the only kids answer sent; `made_for_kids` is ignored. Not set, Bolta tells YouTube "not made for kids", so ask if unclear.
- **Description, tags, category**: `video_description`; empty, the post's text is used. `tags` is a list of words; `category_id` is YouTube's number (22 People & Blogs, 28 Science & Technology, 27 Education). Only set a category the user agreed to.
- **Thumbnail**: `thumbnail_url`, a public https image the user gave. Best effort: if it fails, the video still publishes.
- **Embedding**: `allow_embedding` (default on) lets other sites show the video.
- **Subscribers**: `notify_subscribers` (default on) tells subscribers about the upload.
- Leave `publish_at` out; schedule the post instead.
- Playlists, comments, chapters and language are saved but never sent. Don't offer them.

## Pinterest

- **Board**: picked in Bolta. With none picked, Bolta uses the most recently synced board, which may be the wrong one; with no board at all the pin fails. Say which board will be used if known, or ask the user to pick it. The board id a read returns can't be copied into a change.
- **Pin**: `title` (100 characters; empty, the description is used), `description` (500; empty, the post's text), `link` (the page the pin opens, only one the user gave), `alt_text` (500).

## Having Bolta make the video

No tool here makes a video for a single post. For a run of videos, use a campaign with `feed_video` (16:9) or `short_video` (9:16): [campaign](campaign.md). A one-off video is made in Bolta's AI Studio (bolta.ai/dashboard/ai-studio).

## Always

- Options set earlier in Bolta's composer for that account win over the same keys set here (except YouTube's thumbnail, where this tool wins). Read back with `get-post-platform-details` and say what will actually be used.
- Say every setting you changed in plain words, with the post it's on: "YouTube: titled 'Spring menu tour', unlisted, not for kids."
- Privacy defaults differ: TikTok public, YouTube private. Name the one that applies before saving: "On YouTube this goes up private unless you say otherwise. Public or unlisted?"
- A setting on an approved or scheduled post sends it back for review. Say so before changing it.
