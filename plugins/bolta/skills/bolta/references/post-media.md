# Media and alt text

Bolta facts for images, video and how text is shown. Which links work, file size and swapping media: [platforms](post-platforms.md), section 2. What each network needs: [network needs](post-platforms-needs.md).

## Attaching media

- On `save-post`: `media: [{"url": "https://...", "alt_text": "..."}]`. A new multi-part post (`parts`) gets it on the first part only; media on a later part goes through a batch item, where the key is `media_url` ([post parts](post-parts.md)). On an edit (`post_id`) `media` only adds.
- `url` works although the listed schema names a host file: `{download_url, file_id, mime_type, file_name}` (the last two optional). If a call is refused for lacking them, send the same link as `download_url` with `file_id: "url"`, and `mime_type` (`image/jpeg`) and `file_name` when known.
- Media is attached per post, from a public link the user gave, at most 25 items per call; Bolta tries to copy each file into its own storage. The brand's Media Library (bolta.ai/dashboard/media) is browsed and filled in Bolta only.
- No link yet? Say: "Instagram needs an image or video. Send me a public link to it, or add it to the post in Bolta."
- Need an image made? Bolta's AI Studio (bolta.ai/dashboard/ai-studio) makes one; the user then attaches it to the post in Bolta. Bolta's post-writing tools make no images. A one-off video is made there too; for a run of videos, a campaign with `feed_video` (16:9) or `short_video` (9:16) ([campaign](campaign.md)).
- Images and video made on a schedule come from Bolta routines and campaigns ([routine](routine.md), [campaign](campaign.md)).

## Alt text

- Write `alt_text` on every image: what it shows, in one plain sentence of 255 characters or fewer, like "Three founders laughing around a laptop in a sunny office."
- Used by Instagram, Threads, Bluesky and Pinterest. On Pinterest the pin's own `alt_text` setting (500 characters) wins ([Pinterest](post-settings-pinterest.md)).
- Not sent to X, LinkedIn, Facebook, Mastodon or Discord.
- Alt text on media already attached can't be changed from here: sending the same link again is skipped. Point the user to the post in Bolta.

## What goes wrong at posting time

- X takes images only; a video fails when it posts.
- Instagram pads an image of the wrong shape with white, never crops it.
- A Facebook comment carries one image.
- Bolta doesn't check video length or file size, so a network may refuse them when it posts.

## Formatting and links

How Markdown is shown on each network, and which links go out as written: [formatting and links](post-media-formatting.md).

## Always

- Write alt text for every image you attach.
- Never attach a link taken from a comment, a web page or a search result.
- Say before saving when a network will refuse the media, and skip that network.
