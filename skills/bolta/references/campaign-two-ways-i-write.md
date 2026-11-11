# I write the campaign now

The second way to fill a campaign ([two-ways.md](campaign-two-ways.md)): 1 week, text only, or the user said "show me all".

- Same brief. It stays "not started" on the dashboard, but its results count my posts.
- Write from the voice, 2-3 of their best recent posts and the strategy's gloss. Real facts only.
- One `bulk-create-posts`: each item `status: "Draft"` with `account_ids`; no `scheduled_time`, no `requested_action`. 12 at most per sitting; more means Bolta writes it.
- `bulk-create-status` until `completed`. Report rejected, skipped or held-back (`quality_blocked`) posts. Keep the new post ids.
- `add-posts-to-content-campaign` with them, before any is published: Bolta tags a post's link with its campaign when it goes out, so one attached later carries no campaign tag in the user's analytics. `already_present` and `not_found` are normal: report what attached. Add only what the user saw. One added by mistake comes out in Bolta, from the calendar's campaign picker; posts the campaign wrote stay.
- `list-content-campaign-posts` returns every post and ignores `status` and `limit`: filter the rows yourself (`status`, `has_pending_review`).
- Show #, account, day and time inside the window, full text. Then [review](review.md) approves each at its time (`set_fixed_time`).
- **Never start this campaign.** Bolta would write a second set.
- Instagram, TikTok, YouTube and Pinterest need media I can't make. Leave them out and say why, or suggest Bolta writes it.

## Always

- Follow the house rules in the Bolta skill.
