# The yes move: reading the result

Read after an approval comes back. The order of calls: [review-yes-move.md](review-yes-move.md).

- Scheduled: read back the time, in the brand clock.
- "Ready for Scheduling" (typed in Bolta's composer, or no connected account): say it is approved but not scheduled. Account connected and review mode off: ask for a time, then `publish-post` with that `when`. Review mode on, `publish-post` sends it back to the review list: instead `save-post` with `post_id` and its unchanged `content` puts it back on the list (`sent_back_for_review`, new `content_fingerprint`); approve with `set_fixed_time`. More: [review-times.md](review-times.md).
- `already_decided`: approved before; nothing changed. Repeating a batch is safe.
- `warnings` (X length, Reddit): pass them on.
- Post now, check declined after approval: it stays scheduled at Bolta's time. Say the time; offer to pull it back ([fix](fix.md)).

## Always

- Follow the house rules in the Bolta skill.
- Read every time back from Bolta, never from memory.
