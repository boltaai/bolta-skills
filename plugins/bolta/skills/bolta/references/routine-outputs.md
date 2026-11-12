# What a Bolta routine makes: pictures, the client, stories, Library posts

All live in `output_config`; read `get-routine` first.

## Pictures and video

- Only `weekly_social_posts`, `founder_story_series`, `customer_win_social_proof`, `linkedin_thought_leadership` and the Square ones take media (and older `writing_to_posts_weekly`, `company_page_posts` routines); never promise it on others.
- Keep routines text-first unless the user asks or the network needs pictures (Instagram, TikTok, YouTube). Seen: of 17 image-routine drafts, none approved yet.
- `media_mode`: `none`, `image`, `video` or `carousel`. `media_prompt`: what to show, up to 500 characters, required for video; an image without one is made from the post and the brand's look. `visual_style`: 120 at most.
- `image_model` (image only): `fal-ai/nano-banana-2`, `openai/gpt-image-2.5/flare` or `openai/gpt-image-2.5/sunburst`. Omit for automatic.
- `reference_media_id` (image only): a picture every image follows. Use only an id the user gives or one `get-routine` already shows; nothing here lists the Media Library.
- Carousel: `carousel_config: {"slideCount": 2-10, "visualStyle": "auto"|"bold"|"minimal"|"editorial"|"photographic", "aspectRatio": "portrait_4_5"|"square_1_1", "continuity": "brand_lock"|"chain", "useBrand": true}`. `library_media: {"enabled": true, "mix": "library_only"}` builds each deck from the brand's own photos instead (carousel only). Every network must take them.
- Video is refused if every network is text-only (WordPress, Reddit, Discord, Slack, Mastodon).
- Switching format: send `carousel_config` and `library_media` cleared, or the change is refused.
- Pictures cost credits. Short of them, a run steps down instead of failing (video to image, image to text posts); a carousel is never swapped for another format.

## Straight to the client

`review: {"to_client": true, "bank_target": 20}` sends each run's drafts to the brand's client reviewers with no team pass; leave `recipient_ids` out (every client reviewer): picking some is on the routine's page. Teammate reviewers: `default_reviewer_ids` ([routine-settings.md](routine-settings.md)).

- Works only on a post routine, ask me first (not `auto`), story off, with at least one client reviewer. Otherwise nothing is sent; with no reviewer, `review.last_status` is `no_reviewer`.
- `bank_target` (1-200, optional): how many to keep waiting. Below it, Bolta runs again on its own to fill the bank (more credits) while runs add drafts and the idea bank has ideas. Scheduled runs skip once that many wait or 8 weeks are approved ahead; run now always runs.
- The client gets one notice per fill; the team a daily summary. A client yes takes the next open slot. Drafts reach the client unseen by the team: say so.
- Check `get-routine` `review.waiting` and `review.last_status`.

## One idea, several formats

`story: {"enabled": true, "post": 1, "carousel": 0-1, "article": 0-1, "library": 0-4, "send_to_client": false}`, on post routines. Each run takes one unused idea from the brand's idea bank and writes those pieces, overriding `count` and switching off client sending and Library posts alongside. With no ideas left it runs normally (`story.last_status: "no_ideas_ran_normal_run"`). Run now returns `run: null` with a `story` block: not a failure. `send_to_client` covers its Library posts only.

## Library posts alongside

`library: {"enabled": true, "voice_profile_ids": [...], "send_to_client": false}` on a post routine (voices from `get-voice-context` with `all_profiles: true`): up to 4 Library posts a run, at most once a day, reviewed first, skipped while a story is on. A routine that only makes Library posts is set up in Brand > Library (bolta.ai/dashboard/knowledge-base?tab=library); `list-routine-runs` stays empty for it, so read `get-routine` `library.last_status`.

Best posts again (`repurposing`): [routine-settings-writing.md](routine-settings-writing.md).

## Changing these

On `update-routine`, `review`, `story` and `library` are kept when left out; to turn one off, send it with `enabled` or `to_client` false. Every other `output_config` key is replaced whole: resend them all.

## Always

- Get a yes before anything goes to a client.
- Say pictures cost credits before switching them on (decks of the brand's own photos use none).
