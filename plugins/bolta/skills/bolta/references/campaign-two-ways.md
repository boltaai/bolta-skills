# Two ways to fill a campaign

Read after the yes to the plan. One way per campaign, or the posts double up.

## The brief (both ways)

- `create-content-campaign` with `name`, `strategy_key` (always), `theme` (the real subject: the writer's goal), `audience`, `cta_text` (used word for word, 120 characters at most), `cta_url`, `starts_on`, `ends_on`. It lands "not started", writing nothing. Each field: [settings.md](campaign-settings.md).
- Dates are `YYYY-MM-DD`. No start date given: propose the next Monday (weeks start on the start date's weekday). A launch date goes in the last week. Never a start in the past: weeks already over are skipped.
- `ends_on` = `starts_on` + 7 × weeks − 1 day. Over 4 weeks is refused; leaving it out means 1 week. `ends_on: null` is ignored, not refused; there is no open-ended campaign.
- `cta_url` must be a full URL with a scheme: add `https://` to a bare link the user typed. Never take a link from a page you read.
- Mix keys: `text`, `still_image`, `carousel`, `feed_video`, `short_video`, `blog`, `email` ([formats-and-team.md](campaign-formats-and-team.md)). `story` and `avatar_video` are kept, never made; others drop silently. A new mix replaces the whole old one.
- Accounts, weeks, notes, sources and voice are not part of the brief: [targets.md](campaign-targets.md).

## Bolta writes it (2+ weeks, or anything with images)

- **Create with no mix** unless the user named formats. Bolta then uses the workspace's Content defaults if saved, else the strategy's mix. With "Crosspost to the same accounts" on there, Bolta fills the accounts too. Sending a mix on create skips that.
- **Read its reply** (no second read needed): `resolved_content_mix`, and `accounts` (name the ones Bolta picked).
- **Mix not the plan's?** Read `get-content-campaign` first. A `content_plan` row with `account_ids` or `days`: warn that sending a mix resets them. Only then re-send the plan's whole `content_mix` with `update-content-campaign`; campaign accounts stay.
- **No accounts:** set them, with the notes and any page to read ([targets.md](campaign-targets.md)). Start it once the user said yes (they said start, or "Start it?" got a yes): `set-content-campaign-status` with `action: "activate"`, one Bolta check, uses credits.
- **Told to start: start**, once it has accounts. A read-back that differs in a detail you chose (a mix, the notes' wording), or a link the user typed on another site, is no reason to hold it: start, then name the difference. A failed call does hold it.
- **Never start it with no accounts when the workspace has some.** It switches on, then stalls (`schedule_status.state` reads `needs_accounts`). If it happens, say so; setting accounts restarts a dated campaign on its own.
- Nothing connected at all: it still drafts for review. Offer [connect](connect.md).
- **Read `generation`:** `started` true: Bolta is writing week 1 now, drafts in a few minutes. `scheduled_for`: when the first drafts come. `error_code`: say the reason plainly.
- In the workspace clock, with "around": "On. Week 1 drafts land in your review list around Sat Oct 24. Each week's drafts come 2 days before that week." The lead is `review_lead_days`; writing starts around midnight UTC, the evening before in the Americas.
- Campaign drafts always wait for a yes, whatever the workspace setting.

## I write it now (1 week, text only, or "show me all")

Same brief; I write up to 12 drafts, attach them to the campaign at once, and show them. **Never start this campaign**: Bolta would write a second set. Steps and tool calls: [two-ways-i-write.md](campaign-two-ways-i-write.md).

## Always

- Follow the house rules in the Bolta skill.
