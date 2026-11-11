# The read-back, the learn line, legacy rows

Read when reporting decisions, or when a legacy row is on the list.

## The read-back

> Scheduled in Acme:
> - Mon Oct 19, 9:00 am (New York) · LinkedIn · "Most hiring advice…"
> - Wed Oct 21, 12:00 pm (New York) · X · "Paying for seats…"
>
> Turned down post 2: "too salesy". Bolta saved your reason. It stays in your list as Rejected.
> Removed post 5 (undo within 7 days). Bolta didn't record why.
> You decided 5 of 5.
> Post 2, new version: "…" Schedule this version?

- One line per scheduled post: day, time, city, network, first words.
- Library posts never get a time: "Live on your Library link" or "Sent to your client".
- Decision rate: decided out of shown. "You decided 4 of 6. 2 still waiting."
- End with one question. A changed post comes first; otherwise the DON'T offer.

## Learning, honestly

- Learn line, once per conversation: "Every yes and edit is saved. After about 10 new ones, Bolta updates your DOs and DON'Ts overnight."
- Edits teach because Bolta keeps its first version next to the user's. A drop records nothing. A no sent with `reject-post` saves the user's reason; say "Bolta saved your reason", and promise nothing beyond the learn line. On a post Bolta doesn't count as its own writing (saved with `create-post` over a pasted API key, or typed in Bolta), skip the learn line: nothing is learned ([saying no](review-saying-no.md)).
- A reason given ("drop 5, too salesy"), or the same change twice: offer once, "Add 'no hard sell' to your DON'Ts?" On yes: `get-voice-profile` (profile id from the voice read), then `update-voice-profile` with the full DON'T list plus the new rule. Saw "Bolta checks are on in this session" at the start? Its Bolta check is the confirmation. Otherwise get a yes in words first.
- The same reason on several no's for one Bolta routine's drafts: read Bolta's recommendation first (`list-routine-recommendations`, `list-bolta-suggestions`), name the pattern, offer the fix and apply it only on a yes ([routine](routine.md)). Those not on this app: propose one `update-routine` change yourself, or "Bolta's suggestions are in Bolta's Inbox: bolta.ai/dashboard/inbox."
- No `reject-post` here, and asked how to record why: "Tap the X (Dismiss) on that post at bolta.ai/dashboard/approvals and give your reason. I can't do that from here."

## Legacy rows (`source` recurring)

Older automations only; Bolta routines never land here. The row's `id` is the `review_id`.
- Yes: `approve-recurring-review` with `newScheduleTime` (wall clock) or `useSuggestedTime`. With neither, Bolta picks a slot.
- No: `reject-recurring-review` with `rejectionReason` in the user's words and only `rejectionCategories` that truly fit (too_salesy, too_long, wrong_tone, off_brand, factual_error, and the others listed for that call). This one records why. It can't be undone, so each gets its own Bolta check.
- `list-recurring-reviews` lists the same rows if you need more detail.

## Always

- Follow the house rules in the Bolta skill.
- Read every time back from Bolta, never from memory.
