# Instagram settings

How to set and which wins: [network settings](post-settings.md). Network `instagram`. Caption: 2,200 characters; longer is cut. Needs an image or video; text alone is refused.

Set Instagram settings for the whole network, never per account: several of them are read only from the network's settings, so an account entry is followed only in part. A story on one account and a reel on another are two posts.

## Where it goes

`content_type` `FEED` (default), `REELS` or `STORY`. Both, network only.

- **Feed**: one image, or 2 to 10 images or videos as a carousel (a carousel whatever `content_type` says). One video on `FEED` goes out as a reel.
- **Reel**: one video. `REELS` with an image posts a plain image.
- **Story**: one image or video, gone after 24 hours. The caption, place and tags are dropped. Two or more items fail.
- Guidance, which one:
  - Story: a time-bound offer or code, behind-the-scenes, "today only". No caption is shown, so the offer must be in the image.
  - Reel: video meant to reach new people; evergreen.
  - Carousel: steps, a how-to, before-and-after, a product range; each slide one idea, alt text on each.
  - Feed image: one strong picture with a caption that does the work.

## Settings

- **Own caption**: `text` (or `caption`). Both, per account. Not shown on a story.
- **Trial reel**: `trial_reel_enabled` true or false (default false) with `trial_graduation_strategy` `MANUAL` (default: the user decides in Instagram) or `SS_PERFORMANCE` (shared with followers if it does well). In `platform_specific` spell them `trialReelEnabled` and `trialGraduationStrategy` or snake case. Network only. Needs `REELS` and one video, or it is switched off.
  - Guidance: test a hook or a format on non-followers before it reaches the feed. Not for time-bound news.
- **Reel cover**: `cover_url` (a public image link the user gave) or `thumbnail_offset` (milliseconds into the video). Single video only; a carousel gets none.
- **Place**: `location_id`, an Instagram place id the user gave. Not on stories.
- **People tags**: `user_tags`, a list of `{"username": "...", "x": 0.5, "y": 0.5}` (passed to Instagram as given, in Instagram's format: position in the image, 0 to 1). Not on stories. Only accounts the user named.
- **Product tags**: `product_tags`, a list of `{"product_id": "...", "x": 0.5, "y": 0.5}`. Only for accounts with Instagram Shopping, with product ids the user gave. Not on stories.
- **Alt text**: on each media item (`alt_text`), not here.
- `media_type` `IMAGE`, `VIDEO` or `CAROUSEL_ALBUM`: Bolta sets it from the attached media. Leave it.

Choice values not in the list are skipped in `platform_specific`, not refused: read back with `get-post-platform-details`.

## Not possible here

Collaborators, music, a first comment, choosing whether a reel also shows in the feed, a story with a link sticker, a text-only post, removing or reordering media after saving (done in Bolta).

## Always

- Say which one it will be before the yes: "Instagram: a story, gone after 24 hours, and the caption won't show."
- Read back `content_type` before saying it is a reel, story or trial.
- Tags, places and product ids only from the user.
