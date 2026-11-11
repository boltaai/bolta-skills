# What needs me

## Look once (first Bolta ask in a conversation)

- `list-workspaces`: every brand on the connection; keep each id and name. Several: the reads below per brand, with its `workspace_id`, one section each.
- Each `list-workspaces` row is that brand's full settings: `name`, `timezone`, `audience_timezone`, `safe_mode` (review mode: everything waits for a yes). Typed and shown times use `timezone`; times Bolta picks may follow `audience_timezone` (both in Settings, under Brand timezone). `UTC` is often unset: if a time matters, ask their city once.
- `list-accounts`: `platform`, `username`, `token_status`. `invalid`: disconnected; posts skip it until reconnected. `ghost`: added without connecting. Say "not connected yet", never "broken"; its drafts wait for a connection.
- `get-voice-context`: `writing.feedback_count`, `knowledge.available`, `missing_fields`. "No voice profile" means none yet.

## The reads (fresh every time, all at once)

- **Waiting for your yes:** `list-inbox-items(status="pending", limit=20)`. Count `total_team` plus `total_recurring` (workspace-wide). Routine and campaign drafts are team rows. `total_hunter` is reply drafts ([replies](replies.md)). Unsent drafts aren't counted; mention only ones this conversation saved. A row's `expires_at` within a week: flag "expires Oct 30". Null isn't never: untimed drafts expire after 30 days unchanged.
- **Reports:** `list-inbox-items(source="report", status="approved")`. Keep only rows whose `source` is `report`; ignore that call's totals. Show the newest `title` and date: "Report ready: Weekly performance (Oct 16), at bolta.ai/dashboard/reports".
- **Going out this week:** `list-workspace-posts(account_ids=[<every id from list-accounts>], start_date="<now>", end_date="<now + 7 days>")`, as UTC times ending in `Z`. Count `total_count`; show the next one.
- **Didn't go out:** `list-workspace-posts(status="failed", start_date="<7 days ago>")`.
- **Bolta routines:** `list-routines(status="active,paused")`. Per row: `name`, `display_state`, `pause_reason`, `next_run_at`, `attention_count` (drafts waiting), `blocked`.
- **Campaigns:** `list-content-campaigns(status="draft,scheduled,active,paused,completed")`. Per row: `status`, `starts_on`, `ends_on`, `window_closed`, and `schedule_status` (`state`, `week.index` of `week.total`, `posts_to_review`, `last_error`).

## Reading it

- **Running:** each Bolta routine whose `display_state` is `on_track`, `waiting` or `running`, with its next drafts; each campaign that is on, with its week and drafts waiting. Before its start date: "starts Mon Oct 26". Paused: "(paused)" and the reason in plain words. Leave out not-started campaigns with no dates.
- **Ended:** Bolta finishes a campaign that is on the day after its end date. Show "ended" for one finished in the last 14 days, or a not-started one with `window_closed` true (its window passed). Its verdict: [campaign](campaign.md).
- **Broke**, most urgent first: see [today-what-needs-me-broke.md](today-what-needs-me-broke.md) for each case and what to say.
- Times in the workspace clock: "Mon Oct 19, 9:00 am (New York)".
- A read failed: show the rest, name the missing line, never "all clear".
- Nothing anywhere: "Nothing needs you right now." Then the next step ([today](today.md)).

## Example

> **Acme** · Sat Oct 17 (New York time)
> Waiting for your yes: 6 (4 from Bolta routine "Weekly LinkedIn"; 1 expires Oct 20) · 2 reply drafts
> Going out this week: 3. Next: Mon Oct 19, 9:00 am, LinkedIn (Jane)
> Running: Bolta routine "Weekly LinkedIn" (next drafts Mon Oct 19, 8:00 am) · campaign "New pricing" (week 2 of 3, 2 waiting)
> Ended: campaign "Spring sale" ended Oct 12.
>
> Want to go through the 6 waiting?

## Always

- Follow the house rules in the Bolta skill.
