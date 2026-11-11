# Instagram settings

How to set and which wins: [network settings](post-settings.md). Network `instagram`. Caption: keep it to 2,200 characters; Bolta doesn't check it, and Instagram may refuse a longer one when the post goes out. Needs an image or video: a text-only draft saves, then fails when it goes out.

Set Instagram settings for the whole network, never per account: an account entry is followed only in part. A story on one account and a reel on another are two posts.

Set each key one way and change it the same way: a value set in `platform_specific` beats a later `update-post-platform-details` for `content_type`, `cover_url`, `thumbnail_offset` and `location_id`. The details call takes snake case only and refuses a bad `content_type`.

## Where it goes

`content_type` `FEED` (default), `REELS` or `STORY`. Both, network only.

- **Feed**: one image, or 2 to 10 images or videos as a carousel (a carousel whatever `content_type` says). One video on `FEED` goes out as a reel.
- **Reel**: one video. `REELS` with an image posts a plain image.
- **Story**: one image or video, gone after 24 hours. The caption, place, tags and cover are dropped. Never two or more items: it fails, or only the first goes out.
- Guidance, which one:
  - Story: a time-bound offer, behind-the-scenes, "today only". No caption shows, so the offer must be in the image.
  - Reel: video meant to reach new people; evergreen.
  - Carousel: steps, before-and-after, a product range; one idea a slide.
  - Feed image: one strong picture; the caption does the work.

## Settings

- **Own caption**: `text`. Both, per account. Not shown on a story. Never `caption`: it sticks to the post, and later text edits no longer change what goes out.
- **Trial reel**: `trial_reel_enabled` true or false (default false) with `trial_graduation_strategy` `MANUAL` (default: the user decides in Instagram) or `SS_PERFORMANCE` (to followers if it does well). In `platform_specific` spell them `trialReelEnabled` and `trialGraduationStrategy` or snake case. Network only. Needs `REELS` and one video, or it is switched off. A misspelled strategy becomes `MANUAL`.
  - Guidance: test a hook or a format on non-followers before it reaches the feed. Not for time-bound news.
- **Reel cover**: `cover_url` (a public image link the user gave, 200 characters at most) or `thumbnail_offset` (milliseconds into the video). Single video only; a carousel gets none.
- **Place**: `location_id`, an Instagram place id the user gave. Not on stories.
- **People tags**: `user_tags`, a list of `{"username": "...", "x": 0.5, "y": 0.5}` (Instagram's own format, position 0 to 1; Bolta passes it on unchecked). Not on stories. Only accounts the user named.
- **Product tags**: `product_tags`, a list of `{"product_id": "...", "x": 0.5, "y": 0.5}`. Instagram Shopping accounts only; product ids from the user. Not on stories.
- **Alt text**: on each media item (`alt_text`), not here.
- `media_type` `IMAGE`, `VIDEO` or `CAROUSEL_ALBUM`: Bolta sets it from the attached media. Leave it.

In `platform_specific` a bad or over-long value is skipped, not refused: read back with `get-post-platform-details`. An image of the wrong shape is padded with white, never cropped.

## Not possible here

Collaborators, music, a first comment, keeping a reel out of the feed, a story link sticker, a text-only post, removing or reordering media (done in Bolta).

## Always

- Say which one it will be before the yes: "Instagram: a story, gone after 24 hours, and the caption won't show."
- Read back `content_type` before saying it is a reel, story or trial.
- Tags, places and product ids only from the user.
