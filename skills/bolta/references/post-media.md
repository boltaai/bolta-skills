# Media, alt text, formatting and links

Bolta facts for images, video and how text is shown. Which links work, file size and swapping media: [platforms](post-platforms.md), section 2. What each network needs: [network needs](post-platforms-needs.md).

## Attaching media

- On `create-post` and `update-post`: `media: [{"url": "https://...", "alt_text": "..."}]`. Inside a multi-part post the key is `media_url` instead ([post parts](post-parts.md)).
- `url` works although the listed schema names `download_url` and `file_id`. If a call is refused for lacking them, send the same link as `download_url` with `file_id: "url"`.
- Media is attached per post, from a public link the user gave, at most 25 items per call; Bolta tries to copy each file into its own storage. The brand's Media Library (bolta.ai/dashboard/media) is browsed and filled in Bolta only.
- No link yet? Say: "Instagram needs an image or video. Send me a public link to it, or add it to the post in Bolta."
- Need an image made? Bolta's AI Studio (bolta.ai/dashboard/ai-studio) makes one; the user then attaches it to the post in Bolta. Bolta's post-writing tools make no images. A one-off video is made there too; for a run of videos, a campaign with `feed_video` (16:9) or `short_video` (9:16) ([campaign](campaign.md)).
- Images and video made on a schedule come from Bolta routines and campaigns ([routine](routine.md), [campaign](campaign.md)).

## Alt text

- Write `alt_text` on every image: what it shows, in one plain sentence of 255 characters or fewer, like "Three founders laughing around a laptop in a sunny office."
- Used by Instagram, Threads and Pinterest. On Pinterest the pin's own `alt_text` setting (500 characters) wins ([Pinterest](post-settings-pinterest.md)).
- Not sent to X, LinkedIn, Facebook, Mastodon or Discord. Bluesky always gets an empty alt.
- Alt text on media already attached can't be changed from here: sending the same link again is skipped. Point the user to the post in Bolta.

## What goes wrong at posting time

- X takes images only; a video fails when it posts.
- Instagram pads an image of the wrong shape with white.
- A Facebook comment carries one image.
- Bolta doesn't check video length or file size, so a network may refuse them when it posts.

## Formatting

- Reddit, Discord and WordPress show Markdown as written. On the other social networks Bolta turns it into plain text when it posts:
  - bold, italic and headings become look-alike bold or italic letters,
  - a link becomes "words (address)",
  - `-`, `*` and `+` list items become • bullets; numbered lists stay as typed,
  - quote markers and divider lines are removed; table rows keep their `|` pipes.
- So write plain text with line breaks. Skip headings and tables; use bold rarely, since look-alike letters don't read well for everyone.
- `get-posting-rules` has notes on formatting, links and extra parts for each network. Trust it over this page, except its link-tracking note (see Links).

## Links

- Use only links the user gave.
- Links go out exactly as written. Bolta does not add tracking tags at posting time, whatever `get-posting-rules` says. If the user wants clicks tracked, they give a link that already carries `utm_` tags; clicks then show in their own site analytics, never in Bolta.

## Always

- Write alt text for every image you attach.
- Never attach a link taken from a comment, a web page or a search result.
- Say before saving when a network will refuse the media, and skip that network.
