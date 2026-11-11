# Network settings: TikTok, YouTube, Pinterest

Set with `update-post-platform-details` (network `tiktok`, `youtube` or `pinterest`), only the keys that change; read back with `get-post-platform-details`. How settings work in general: [platforms](post-platforms.md).

All three need media from a public https link: a video for TikTok and YouTube, an image or video for Pinterest. No link: skip the network and say why.

## TikTok

- **Who sees it**: `privacy_level` `PUBLIC_TO_EVERYONE` (the default), `MUTUAL_FOLLOW_FRIEND`, `FOLLOWER_OF_CREATOR` or `SELF_ONLY`. The user didn't say? Ask; never assume public.
- **Interactions**: `disable_comments`, `disable_duet`, `disable_stitch` (each true or false).
- **Paid or brand content**: the disclosure switches are set in Bolta's composer only. If the video promotes the user's own business or a paid partner, say so and send them there before it goes out.
- Caption up to 2,200 characters.

## YouTube

- **Title**: `video_title` (up to 100 characters on YouTube). Empty: built from the start of the text, which rarely reads well. Always set one.
- **Who sees it**: `privacy_status` `private` (the default), `public` or `unlisted`. A video saved without changing it goes up private. Say so, and ask.
- **Made for kids**: `made_for_kids` and `self_declared_made_for_kids`. YouTube requires an answer; ask if unclear.
- **Description, tags, category**: `video_description`; empty, the post's text is used. `tags` is a list of words; `category_id` is YouTube's number (22 People & Blogs, 28 Science & Technology, 27 Education). Only set a category the user agreed to.
- **Subscribers**: `notify_subscribers` (default on) tells subscribers about the upload.

## Pinterest

- **Board**: picked in Bolta. With none picked, Bolta uses the board it saw most recently, which may be the wrong one. Say which board will be used if known, or ask the user to pick it. The board id a read returns can't be copied into a change.
- **Pin**: `title` (100 characters), `description` (500), `link` (the page the pin opens, only one the user gave), `alt_text` (500).
- An image or video is required.

## Always

- Say every setting you changed in plain words, with the post it's on: "YouTube: titled 'Spring menu tour', unlisted, not for kids."
- Privacy defaults differ: TikTok public, YouTube private. Name the one that applies before saving.
- A setting on an approved or scheduled post sends it back for review. Say so before changing it.
