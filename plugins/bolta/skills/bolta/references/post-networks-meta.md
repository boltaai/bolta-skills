# Network settings: Threads, Instagram, Facebook

Set with `update-post-platform-details` (network `threads`, `instagram` or `facebook`), only the keys that change, or in the saving call with `platform_specific` ([per network](post-per-network.md)); read back with `get-post-platform-details`. Every network: [at a glance](post-networks-at-a-glance.md).

## Threads

- **Topic**: `topic_tag` (up to 30 characters; letters, numbers, spaces and underscores only; not only digits; a leading `#` is dropped) together with `use_topic_tag: true`. Without the second, the topic is saved and not sent. A tag with any other character is silently left off at publish. One topic per post.
- **Ghost post**: `is_ghost_post: true`. A text-only post that disappears after 24 hours. It applies only to one short text part with no image, video, poll or reply chain; with any of those the post goes out as a normal, lasting post. Say both things before saving: "This one disappears after a day."
- **Spoiler**: `is_spoiler_media: true` blurs the post's images and videos until tapped. No effect on a text-only post.
- **Location**: `location_id`, an id from Threads. Only set one the user gave.
- **Polls**: [platforms](post-platforms.md), section 4.
- Longer than 500 characters becomes a reply chain on its own; a ghost post can't be one.
- Who can reply (`reply_control`) is saved but not sent to Threads. Don't offer it.

## Instagram

- **Where it goes**: `content_type` `FEED` (the default), `REELS` or `STORY`.
  - One video always goes out as a reel, even on `FEED`. `REELS` with one image posts a plain image.
  - A story takes no caption; the text is not shown.
  - A story can't be a carousel (it fails). 2 to 10 images or videos make a carousel, whatever `content_type` says.
- **Trial reel**: `trial_reel_enabled: true` shows a reel to non-followers first. `trial_graduation_strategy`: `MANUAL` (the default; the user decides in Instagram) or `SS_PERFORMANCE` (Instagram shares it with followers if it does well). Only with `content_type` `REELS` and one video; otherwise it goes out as a normal post. On `create-post`: [per-network keys](post-per-network-keys.md).
- **Reel cover**: `cover_url` (a public image link) or `thumbnail_offset` (milliseconds into the video). One video only, not a carousel.
- **Tags and place**: `user_tags` (people in the image), `location_id`. Only ones the user gave. Not sent on a story.
- **Alt text**: on each media item, not here.
- Needs an image or video. A text-only Instagram post is refused.

## Facebook

- **The Page**: `list-accounts` lists each Page as its own row, id `facebook_page_<id>` with `is_page`, and `is_primary` on the default Page. Put that id in `create-post` `account_ids`, save it as a draft first, then schedule as a second call. Several Page ids post to several Pages: the first is the main Page, the rest get the same post as cross-posts.
- Before the yes, name the Page it will go to: "This goes to the Acme Bakery Page." Each Page can get its own text: `platform_specific` `facebook.accounts`, keyed by the `facebook_page_` id.
- `primary_page_id` and `cross_post_pages` (with `cross_post_enabled: true`) take internal Page ids, shown only by `get-post-platform-details`. Prefer `account_ids`.
- **First comment**: see [post parts](post-parts.md).
- Media: text, one video, or images. Never a video with images.
- Feeling, activity, place, privacy, post type, comment, sharing and reaction settings and the cross-post delay are saved but never sent. Don't offer them.

## Always

- Say every setting you changed in plain words, with the post it's on: "Threads post 2: topic set to Marketing; it disappears after 24 hours."
- A setting on an approved or scheduled post sends it back for review. Say so before changing it.
- Never invent an id (location, Page, person). Pages come from `list-accounts`.
