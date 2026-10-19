# What needs me

## Look once (first Bolta ask in a conversation)

- `list-workspaces`: one row (a connection can't switch). Keep its id and name.
- `get-workspace`: `name`, `timezone`, `safe_mode` (review mode: everything waits for a yes). `UTC` is often unset: if a time matters, ask their city once.
- `list-accounts`: platform, name, `token_status`. Not `valid`: disconnected; posts skip it until reconnected.
- `get-voice-context`: `writing.feedback_count`, `knowledge.available`, `missing_fields`. "No voice profile" means none yet.

## The reads (fresh every time, all at once)

- **Waiting for your yes:** `list-inbox-items(status="pending", limit=20)`. Count the workspace-wide totals: `total_team` plus `total_recurring`. Drafts from Bolta routines and campaigns arrive as team rows. `total_hunter` is reply drafts (`replies`); `total_report` is reports, mention only. Drafts never sent for review aren't counted; mention them only if this conversation saved some.
- **Going out this week:** `list-scheduled-posts(start_date="<now>", end_date="<now + 7 days>")`, as UTC times ending in `Z`. Count `total_count`; show the next one.
- **Didn't go out:** `list-workspace-posts(status="failed", start_date="<7 days ago>")`.
- **Bolta routines:** `list-routines(status="active,paused")`. Per row: `name`, `status`, `next_run_at`, `attention_count` (its drafts waiting), `blocked`, `last_run.status`.
- **Campaigns:** `list-content-campaigns(status="draft,scheduled,active,paused,completed")`. Per row: `status`, `starts_on`, `ends_on`, `window_closed`, and `schedule_status` (`state`, `week.index` of `week.total`, `posts_to_review`, `last_error`).

## Reading it

- **Running:** each active Bolta routine with its next drafts; each campaign that is on, with its week and drafts waiting. Before its start date: "starts Mon Oct 26". Paused ones get "(paused)". Leave out not-started campaigns with no dates.
- **Ended:** Bolta finishes a campaign that is on the day after its end date. Show "ended" for one finished in the last 14 days, or a not-started one with `window_closed` true (Claude wrote it). Its verdict: `campaign`.
- **Broke**, most urgent first:
  - Disconnected account: "LinkedIn is disconnected. Reconnect: <link>" (`get-connect-link` with that platform).
  - A post that didn't go out: day, account, and "Want the reason?" (`fix`).
  - Routine `blocked`: "Bolta routine 'X' can't run: its writer is paused. Resume it at bolta.ai/dashboard/agents."
  - Routine `last_run.status` is `failed`: its explanation, in plain words (`routine`).
  - Campaign `state` is `needs_accounts`: "Campaign 'X' is on but has no accounts, so nothing gets written." Campaign `last_error`: say it plainly (`campaign`).
- Show every time in the workspace clock: "Mon Oct 19, 9:00 am (New York)".
- One read failed: show the rest, say which line is missing, never "all clear".
- Nothing anywhere: "Nothing needs you right now." Then one next step.

## The one next step

Pick the first that applies. It is the only question.

1. Something broke: fix that.
2. Posts waiting: "Want to go through the 6 waiting?" (`review`)
3. A campaign ended: "Want the verdict on Spring sale?" (`campaign`)
4. Nothing going out this week: "What do you want to post about this week? I'll write the posts." (`post`; skip if they said).
5. No Bolta routine on: "Want Bolta to write 5 LinkedIn and X drafts every Monday at 8 am, about what Acme does? They wait for your yes, and it uses credits each run." (`routine`; name the networks they post on).

In a scheduled run, the summary is the whole job; the next step is a suggestion.

## Example

> **Acme** · Sat Oct 17 (New York time)
> Waiting for your yes: 6 (4 from Bolta routine "Weekly LinkedIn") · 2 reply drafts
> Going out this week: 3. Next: Mon Oct 19, 9:00 am, LinkedIn (Jane)
> Running: Bolta routine "Weekly LinkedIn" (next drafts Mon Oct 19, 8:00 am) · campaign "New pricing" (week 2 of 3, 2 waiting)
> Ended: campaign "Spring sale" ended Oct 12.
>
> Want to go through the 6 waiting?
