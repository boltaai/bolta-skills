# What a Bolta routine makes: pictures, the client, stories, Library posts

All in `output_config`; read `get-routine` first.

## Pictures and video

- **Has pictures:** `get-routine` `output_config` has a picture, video, slide or visual setting that is on or filled in (a flag ending in `_supported` is not one), or its `story` has `image`, `video` or `carousel` above 0. Here: read, list runs, review drafts, pause. Anything else (a change, run now, switching on, a copy, a suggestion for it), and any picture request: one line, "That's done on its page in Bolta: bolta.ai/dashboard/routines/<id>."
- A routine made here writes text. Pictures, video, and Instagram, TikTok, YouTube and Pinterest (they refuse text-only posts) stay out of the plan. Asked for them, after saving: "Pictures and Instagram are added on its page: bolta.ai/dashboard/routines/<id>."
- Only those networks wanted, or none named and only those connected: save nothing: "Instagram needs a picture on every post, so this routine is set up in Bolta: bolta.ai/dashboard/routines. Here I can write single posts for a photo you attach."
- Never write picture ideas, image prompts or video scripts, anywhere.
- A draft missing the picture or video it should carry is not ready to approve.

## Straight to the client

`review: {"to_client": true, "bank_target": 20}` sends each run's drafts to the brand's client reviewers with no team pass; leave `recipient_ids` out (every client reviewer): picking some is on the routine's page. Teammate reviewers: `default_reviewer_ids` ([routine-settings.md](routine-settings.md)).

- Works only on a post routine, ask me first (not `auto`), story off, with at least one client reviewer. Otherwise nothing is sent; with no reviewer, `review.last_status` is `no_reviewer`.
- `bank_target` (1-200, optional): how many to keep waiting. Below it, Bolta runs again on its own to fill the bank (more credits) while runs add drafts and the idea bank has ideas. Scheduled runs skip once that many wait or 8 weeks are approved ahead; run now always runs.
- The client gets one notice per fill; the team a daily summary. A client yes takes the next open slot. Drafts reach the client unseen by the team: say so.
- Check `review.waiting` and `review.last_status`.

## One idea, several formats

`story: {"enabled": true, "post": 1, "article": 0-1, "library": 0-4, "send_to_client": false}`, on post routines. Never switch on its `image`, `video` or `carousel` pieces here: switching a story on, leave them out (they stay 0). To change one story setting, resend the whole `story` as read, only that one changed; a piece left out is switched off. Each run takes one unused idea from the brand's idea bank and writes those pieces, overriding `count` and switching off client sending and Library posts alongside. With no ideas left it runs normally (`story.last_status: "no_ideas_ran_normal_run"`). Run now returns `run: null` with a `story` block: not a failure. `send_to_client` covers its Library posts only.

## Library posts alongside

`library: {"enabled": true, "voice_profile_ids": [...], "send_to_client": false}` on a post routine (voices from `get-voice-context` with `all_profiles: true`): up to 4 Library posts a run, at most once a day, reviewed first, skipped while a story is on. A routine that only makes Library posts is set up in Brand > Library (bolta.ai/dashboard/knowledge-base?tab=library); `list-routine-runs` stays empty for it; read `get-routine` `library.last_status`.

Best posts again (`repurposing`): [routine-settings-writing.md](routine-settings-writing.md).

## Changing these

Text routines only (pictures: above). On `update-routine`, `review`, `story` and `library` are kept when left out; to turn one off, send it with `enabled` or `to_client` false. Every other `output_config` key is replaced whole: resend every key `get-routine` shows, unchanged, beside the one that changes.

## Always

- Get a yes before anything goes to a client.
