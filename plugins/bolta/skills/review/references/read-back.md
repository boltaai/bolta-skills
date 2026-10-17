# The read-back, the learn line, legacy rows

Read when reporting decisions, or when a legacy row is on the list.

## The read-back

> Scheduled in Acme:
> - Mon Oct 19, 9:00 am (New York) · LinkedIn · "Most hiring advice…"
> - Wed Oct 21, 12:00 pm (New York) · X · "Paying for seats…"
>
> Removed post 5 (undo within 7 days). Bolta didn't record why.
> You decided 5 of 5.
> Post 2, new version: "…" Schedule this version?

- One line per scheduled post: day, time, city, network, first words.
- Decision rate: decided out of shown. "You decided 4 of 6. 2 still waiting."
- End with one question. A changed post comes first; otherwise the DON'T offer.

## Learning, honestly

- Learn line, once per conversation: "Every yes and edit is saved. After about 10 new ones, Bolta updates your DOs and DON'Ts overnight."
- Edits teach because Bolta keeps its first version next to the user's. A drop records nothing.
- A reason given ("drop 5, too salesy"), or the same change twice: offer once, "Add 'no hard sell' to your DON'Ts?" On yes: `get-voice-profile` (profile id from the voice read), then `update-voice-profile` with the full DON'T list plus the new rule. Saw "Bolta checks are on in this session" at the start? Its Bolta check is the confirmation. Otherwise get a yes in words first.
- If asked how to record why: "Tap No with a reason in your review list. I can't do that from here."

## Legacy rows (`source` recurring)

Older automations only; Bolta routines never land here. The row's `id` is the `review_id`.
- Yes: `approve-recurring-review` with `newScheduleTime` (wall clock) or `useSuggestedTime`. With neither, Bolta picks a slot.
- No: `reject-recurring-review` with `rejectionReason` in the user's words and only `rejectionCategories` that truly fit (too_salesy, too_long, wrong_tone, off_brand, factual_error, and the others listed for that call). This one records why. It can't be undone, so each gets its own Bolta check.
- `list-recurring-reviews` lists the same rows if you need more detail.
