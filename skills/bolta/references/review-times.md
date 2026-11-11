# Times: moving them, and where Bolta puts them

Read when a yes names no time, when someone wants a scheduled post moved, or when a time looks wrong. How Bolta picks a time on its own, and the posting schedule: [review-times-auto.md](review-times-auto.md).

## Move a scheduled post

- For a post already Scheduled: `update-post` with `post_id` and only `scheduled_time` (wall clock, no Z, no offset; `timezone` only if the user named a place). No `status`, no text, no media, no accounts. It must be in the future.
- The post stays Scheduled, keeps its approval and keeps the client's sign-off. Only the time moves.
- Any change to text, media or accounts sends an approved post back for a new yes, and voids a client's sign-off too.
- Still show the new time and get a yes first: "Move LinkedIn 'Most hiring advice…' to Thu Nov 19, 2:00 pm (New York)?"
- Read the result's `status` and time back. A refusal says why (a time in the past, a format problem): say it plainly.
- Still waiting for a yes? Don't move it: name the time in the approval (`set_fixed_time`).
- Approved with no time, or "Ready for Scheduling": `update-post` stores a time but does not schedule it.
  - Review mode off: `schedule-post` with the time.
  - Review mode on: `schedule-post` sends it back to the review list. Instead: `update-post` with `status: "Draft"`, `submit-for-review`, then approve with `set_fixed_time`.

## When nothing names a time

- Say it before the yes: "Bolta picks exact times from your posting schedule unless you name one."
- After the yes, read back the time Bolta picked, in the brand's clock. "Best time" means `use_suggested_time`.
- A day alone ("Tuesday") is not a time. Ask the hour: "Tuesday at what time?" Without one, Bolta picks, and it may not land on Tuesday.
- Approved but "Ready for Scheduling" has no time yet. Say so and ask: "Approved, but not scheduled yet. What time should it go out?" Then follow "Move a scheduled post" above.

## Time zones

- Every time you send is read in the brand's time zone (`get-workspace` `timezone`).
- A brand's time zone is `UTC` until someone changes it, and often nobody has. If it reads `UTC` and a time matters, ask once: "Your brand's clock is set to UTC. Which city should I use for times?" Then send that city's zone as `timezone` on each time. That covers only those posts; the brand's own zone changes only in Bolta Settings, so offer that once.
- `get-workspace` `audience_timezone`, when set, steers the hours Bolta picks itself. Mention it if a picked time looks odd for the brand.
- `approve-post` and `list-scheduled-posts` give times in UTC. Show them in the brand clock with the city: "Tue Nov 17, 9:07 am (Chicago)".

## "Changed after approval"

- `schedule-post` or `publish-post` can answer that the post changed since it was approved (`approval_reset` true). It is back waiting for a yes.
- That is not an error to retry. Show the current text, say what changed if the result names it, and get a new yes: "This post changed since you approved it. Here's the current version. Still yes?"
- A time-only move never causes it.

## Always

- Follow the house rules in the Bolta skill.
- Read every time back from Bolta's answer, in the brand's clock.
