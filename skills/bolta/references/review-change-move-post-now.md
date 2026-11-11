# Changing a post, moving a time, posting now, and Bolta checks

Read before editing a post that waits or is scheduled, moving a time, posting now, or when a Bolta check is declined. Back to [review](review.md).

## Change the text

1. `save-post` with `post_id` and the new `content` (the first part's text; a later part of a thread can't be edited from here: offer Bolta). Show the new version in full.
2. Approved or Scheduled before: the result says `sent_back_for_review` true; it is back on the review list and won't go out until approved again. Already waiting: it stays waiting. Either way, approve with the result's `content_fingerprint`. A Draft (`post_status`): `submit-for-review` first. Then ask: "Schedule this version?"
3. On that yes, the yes move ([yes move](review-yes-move.md)).

- A yes given to the old text never covers the new one.
- Edit an approved or scheduled post only for a real change: any edit needs a new yes. A Published or publishing post can't be edited.
- A post the client has, or has approved: an edit voids their answer. Say so first ([sign-off](review-client-signoff.md)).

## Move a time

- Already Scheduled: `publish-post` with `post_id` and the new `when` (wall clock). A time-only move keeps its approval; the result says `rescheduled: true` ([times](review-times.md)). Never `save-post` to move a time.
- A client request still waiting does not survive a new time: the client saw the old one, so it has to be sent again ([sign-off](review-client-signoff.md)). Say that before moving, and move only on a yes.
- Off the schedule instead: `save-post` with `post_id` and `unschedule: true`. It goes back to Draft with its text; `was_scheduled_for` is the time it no longer goes out at.
- Still waiting for a yes: don't move it. Name the time in the approval (`set_fixed_time`).
- Show the new time and get a yes first; read the saved time back.

## Post now

- "Post it now" is a yes only for the posts it names, after the user saw their exact text.
- The yes move first, then `publish-post` with `when: "now"`.
- Review mode on: nothing posts right away. Offer a time a few minutes away instead (`set_fixed_time`, at least 2 minutes ahead).
- It can't be recalled once out ([fix](fix.md)): read the account and first words back before the call.

## Bolta checks

Only in a session that began with "Bolta checks are on in this session". Without that line, ask in words first.

- One check covers the batch approval. After it passes, this reply's other approvals, no's, schedules and deletes pass without another.
- Posting now always asks, every time.
- Declined means not done: say so, don't retry, and never reach it another way.
- A check declined after the approval went through: the post stays scheduled at Bolta's time. Say the time; offer to pull it back ([fix](fix.md)).

## Always

- Follow the house rules in the Bolta skill.
- Never post now on a yes that only said "schedule" or "approve".
- Read every time back from Bolta, never from memory.
