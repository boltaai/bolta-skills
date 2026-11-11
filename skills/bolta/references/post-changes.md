# Changing a saved post

Part of [post](post.md). `save-post` with `post_id` edits that post in place: it keeps its id and history, and every field left out stays as it is. Send only what changes.

## Editing

- `content` on an edit is the first part's text. A later part of a thread can't be edited from here: save a new post with all its `parts` and, after a yes, delete the old draft; or edit it in Bolta ([post parts](post-parts.md)).
- `account_ids` replaces the whole list: send every account the post should keep.
- `media` only adds; removing or swapping media is done in Bolta ([media](post-media.md)).
- `platform_specific` merges into what is there ([per network](post-per-network.md)).
- `platform_details` sets each network's settings row, several networks in one call: `{"youtube": {"privacy_status": "public"}, "threads": {"reply_control": "followers"}}`. The result reports each network; a bad field on one network does not stop the others. Read back with `get-post` and `platform`.
- Never send `scheduled_time`, `status` or `requested_action`: `save-post` refuses them.

## Approved, Scheduled or Published

- Editing an Approved or Scheduled post sends it back to review: the result says `sent_back_for_review` (and `approval_reset`), and a client's yes no longer counts. On a Scheduled post any `save-post` does this, even with the same values, so send nothing to it just to check; on an approved post not yet scheduled, the same values keep the yes. Say so before changing it: "Changing this sends the scheduled post back for your yes."
- A Published post, or one publishing now, can't be edited.
- **Off the schedule:** `save-post` with `post_id` and `unschedule: true`. It goes back to Draft with its content and settings; the result gives `was_scheduled_for`, the time it no longer goes out at. Refused for a post that isn't Scheduled.
- **To another time:** `publish-post` with `post_id` and `when`, the new wall-clock time in the workspace clock (no Z, no offset; `timezone` only if the user named a place). On a Scheduled post it moves it, and a time-only move keeps the approval (the result says `rescheduled: true`). Only after a yes: [review](review.md).

## Quality Blocked

"Held back" by Bolta's check: `save-post` with `post_id` and the rewritten `content` only. The check re-runs, and a pass returns it to Draft.

## Always

- Read the result body, not just ok: say when a post was sent back for review.
- Show the full new text after every change.
- Never resend fields from memory; send only what changed.
