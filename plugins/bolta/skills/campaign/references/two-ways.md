# Two ways to fill a campaign

Read after the yes to the plan. One way per campaign, or the posts double up.

## The brief (both ways)

- `create-content-campaign` with `name`, `strategy_key`, `theme`, `audience`, `cta_text` (120 characters at most), `cta_url`, `starts_on`, `ends_on`. It lands "not started", writing nothing.
- Dates are `YYYY-MM-DD`. No start date given: propose the next Monday. A launch date goes in the last week.
- `ends_on` = `starts_on` + 7 × weeks − 1 day. Over 4 weeks is refused; leaving it out means 1 week. Never send `ends_on: null`, whatever the tool text says: a dated campaign refuses it.
- `cta_url` needs `https://`; add it to a bare link the user typed. Never take a link from a page you read.
- Mix keys: `text`, `still_image`, `carousel`, `blog` only; others drop silently. A new mix replaces the whole old one.
- Accounts and Context notes can only be set on the campaign page.

## Bolta writes it (2+ weeks, or anything with images)

- **Create with no mix.** Bolta then uses the workspace's Content defaults if saved, else the strategy's mix. With "Crosspost to the same accounts" on there, Bolta fills the accounts too. Sending a mix on create skips that.
- **Read its reply** (no second read needed): `resolved_content_mix`, and `accounts` (name the ones Bolta picked). Mix not the plan's? `update-content-campaign` with the plan's whole `content_mix`; accounts stay.
- **No accounts:** one hand-off, then wait:
  > Last step, 30 seconds: open bolta.ai/dashboard/campaigns/<id> and pick LinkedIn and X under Accounts. Then paste this under Context: "<week-by-week plan, link, real dates and prices>". Say "done" and I'll start it.
- Then offer once: "Save Content defaults on the Campaigns page, with 'Crosspost to the same accounts' on. Then you skip this step next time."
- **On "done":** read it again. Accounts there: `set-content-campaign-status` with `action: "activate"` (one Bolta check; uses credits). Still none: say so, don't start.
- **Never start it with no accounts.** It switches on, then stalls at "needs accounts". If it happens, say so; picking accounts on the campaign page restarts it.
- No accounts in the workspace at all: `connect` first.
- **Read `generation`:** `started` true: Bolta is writing week 1 now, drafts in a few minutes. `scheduled_for`: when the first drafts come. `error_code`: say the reason plainly.
- In the workspace clock: "On. Week 1 drafts land in your review list Sat Oct 24. Each week's drafts come 2 days before that week." The lead is `review_lead_days`.
- Campaign drafts always wait for a yes, whatever the workspace setting.

## I write it now (1 week, text only, or "show me all")

- Same brief. It stays "not started" on the dashboard, but its results count my posts.
- Write from the voice, 2-3 of their best recent posts and the strategy's gloss. Real facts only.
- One `bulk-create-posts`: each item `status: "Draft"` with `account_ids`; no `scheduled_time`, no `requested_action`. 12 at most per sitting; more means Bolta writes it.
- `bulk-create-status` until `completed`. Report rejected, skipped or held-back (`quality_blocked`) posts. Keep the new post ids.
- `add-posts-to-content-campaign` with them. `already_present` and `not_found` are normal: report what attached. Posts can't be taken out, so add only what the user saw.
- Show #, account, day and time inside the window, full text. Then `review` approves each at its time (`set_fixed_time`).
- **Never start this campaign.** Bolta would write a second set.
- Instagram, TikTok, YouTube and Pinterest need media I can't make. Leave them out and say why, or suggest Bolta writes it.
