# What a Bolta routine makes: pictures, the client, stories, Library posts

All live in `output_config`; read `get-routine` first.

## Pictures and video

Set up on the routine's page in Bolta, never from here.

- A routine made here writes text posts. Asked for pictures or video: save it as text, then say in one line that they are added on the routine's page: bolta.ai/dashboard/routines.
- Instagram, TikTok, YouTube and Pinterest refuse text-only posts: never plan a text draft to them. Leave that network off and say its pictures or video are added on the routine's page.
- Never write picture ideas, image prompts, video scripts or scene descriptions for Bolta to draw, in `instructions` or anywhere.
- A routine already set on its page to make pictures or video keeps them. Never switch them on, off or to another kind; resend them unchanged on updates (below).
- A draft that should carry a picture or video and came back without it is not ready: don't approve it.

## Straight to the client

`review: {"to_client": true, "bank_target": 20}` sends each run's drafts to the brand's client reviewers with no team pass; leave `recipient_ids` out (every client reviewer): picking some is on the routine's page. Teammate reviewers: `default_reviewer_ids` ([routine-settings.md](routine-settings.md)).

- Works only on a post routine, ask me first (not `auto`), story off, with at least one client reviewer. Otherwise nothing is sent; with no reviewer, `review.last_status` is `no_reviewer`.
- `bank_target` (1-200, optional): how many to keep waiting. Below it, Bolta runs again on its own to fill the bank (more credits) while runs add drafts and the idea bank has ideas. Scheduled runs skip once that many wait or 8 weeks are approved ahead; run now always runs.
- The client gets one notice per fill; the team a daily summary. A client yes takes the next open slot. Drafts reach the client unseen by the team: say so.
- Check `get-routine` `review.waiting` and `review.last_status`.

## One idea, several formats

`story: {"enabled": true, "post": 1, "article": 0-1, "library": 0-4, "send_to_client": false}`, on post routines. Its `carousel` piece is pictures: set on the routine's page; when changing a story, resend `carousel` as `get-routine` shows it. Each run takes one unused idea from the brand's idea bank and writes those pieces, overriding `count` and switching off client sending and Library posts alongside. With no ideas left it runs normally (`story.last_status: "no_ideas_ran_normal_run"`). Run now returns `run: null` with a `story` block: not a failure. `send_to_client` covers its Library posts only.

## Library posts alongside

`library: {"enabled": true, "voice_profile_ids": [...], "send_to_client": false}` on a post routine (voices from `get-voice-context` with `all_profiles: true`): up to 4 Library posts a run, at most once a day, reviewed first, skipped while a story is on. A routine that only makes Library posts is set up in Brand > Library (bolta.ai/dashboard/knowledge-base?tab=library); `list-routine-runs` stays empty for it, so read `get-routine` `library.last_status`.

Best posts again (`repurposing`): [routine-settings-writing.md](routine-settings-writing.md).

## Changing these

On `update-routine`, `review`, `story` and `library` are kept when left out; to turn one off, send it with `enabled` or `to_client` false. Every other `output_config` key is replaced whole: read `get-routine` and resend every key it shows, unchanged, beside the one that changes.

That includes every picture and video setting made on the routine's page, whatever its name. Left out, the routine loses its pictures: copy them back exactly as read; never drop, clear or change them.

## Always

- Get a yes before anything goes to a client.
- Never set up pictures or video from here; keep every picture setting a routine already has.
