# Changing a post, moving a time, posting now, and Bolta checks

Read before editing a post that waits or is scheduled, moving a time, posting now, or when a Bolta check is declined. Back to [review](review.md).

## Change the text

1. `update-post` with the new text and `status: "Draft"`. Show the new version in full.
2. `submit-for-review`, then ask: "Schedule this version?"
3. On that yes, the yes move ([yes move](review-yes-move.md)).

- A yes given to the old text never covers the new one.
- Pull an approved or scheduled post back to Draft only for a real edit: it loses its time and needs a new yes.
- A post the client has, or has approved: an edit voids their answer. Say so first ([sign-off](review-client-signoff.md)).

## Move a time

- Already Scheduled: `update-post` with only `scheduled_time`. It keeps its approval ([times](review-times.md)).
- A client request still waiting does not survive a new time: the client saw the old one, so it has to be sent again ([sign-off](review-client-signoff.md)). Say that before moving, and move only on a yes.
- Still waiting for a yes: don't move it. Name the time in the approval (`set_fixed_time`).
- Show the new time and get a yes first; read the saved time back.

## Post now

- "Post it now" is a yes only for the posts it names, after the user saw their exact text.
- The yes move first, then `publish-post`.
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
