# Network settings: Threads, Instagram, Facebook

Set with `update-post-platform-details` (network `threads`, `instagram` or `facebook`), only the keys that change; read back with `get-post-platform-details`. How settings work in general: [platforms](post-platforms.md).

## Threads

- **Topic**: `topic_tag` (30 characters, no `#`, `.` or `&`, not only digits) together with `use_topic_tag: true`. Without the second, the topic is saved and not sent. One topic per post; it replaces hashtags.
- **Ghost post**: `is_ghost_post: true`. A text-only post that disappears after 24 hours. It applies only to one short text part with no image, video, poll or reply chain; with any of those the post goes out as a normal, lasting post. Say both things before saving: "This one disappears after a day."
- **Spoiler**: `is_spoiler_media: true` blurs the post's images until tapped.
- **Location**: `location_id`, an id from Threads. Only set one the user gave.
- **Polls**: see [platforms](post-platforms.md), section 4.
- Longer than 500 characters becomes a reply chain on its own; a ghost post can't be one.
- Who can reply isn't sent to Threads from here yet. Don't offer it.

## Instagram

- **Where it goes**: `content_type` `FEED` (the default), `REELS` or `STORY`.
  - A reel needs one video.
  - A story takes no caption; the text is not shown.
  - A story can't be a carousel. 2 to 10 images or videos on the feed make a carousel.
- **Trial reel**: `trial_reel_enabled: true` shows a reel to non-followers first. `trial_graduation_strategy`: `MANUAL` (the user decides in Instagram) or `SS_PERFORMANCE` (Instagram shares it with followers if it does well). Video only.
- **Reel cover**: `cover_url` (a public image link) or `thumbnail_offset` (milliseconds into the video).
- **Tags and place**: `user_tags` (people in the image), `location_id`. Only ones the user gave.
- **Alt text**: on each media item, not here.
- Needs an image or video. A text-only Instagram post is refused.

## Facebook

- **The page**: by default the post goes to the page the Facebook account is connected with. To pick another page that account manages: `primary_page_id`. No tool lists pages; the user picks it in Bolta or names an earlier post.
- **More pages**: `cross_post_pages` (a list) with `cross_post_enabled: true` posts the same text to the account's other pages too.
- **Feeling, activity, place**: `feeling`, `activity`, `location`, only when the user asked.
- Media: text, one video, or images. Never a video with images.

## Always

- Say every setting you changed in plain words, with the post it's on: "Threads post 2: topic set to Marketing; it disappears after 24 hours."
- A setting on an approved or scheduled post sends it back for review. Say so before changing it.
- Never invent an id (location, page, person).
