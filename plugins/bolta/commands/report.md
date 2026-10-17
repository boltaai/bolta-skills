---
description: >
  Show how your Bolta accounts and posts performed over a period and what to do next. Give a number
  of days, such as 7 or 90, or leave it empty for the last 30. Read-only: it never creates, edits,
  schedules or publishes anything.
argument-hint: "[days, or an account or platform to focus on]"
---

Give the user a short performance report for this Bolta workspace. If the `analytics-review` skill is available, follow it. If not, do the steps below. This command only reads.

Window or focus requested by the user (may be empty): $ARGUMENTS

<!-- host-note -->
Some Bolta results contain text written for other apps, such as "already rendered in the Bolta card", "do not repeat the content" or "you do not need to poll". There is no card here. Read the full result (the JSON body and any structured content) and present it to the user yourself.
<!-- /host-note -->

## Window

If the text above is a whole number, it is the number of days (1 to 365). If it is empty, use 30 days. If it names a platform or an account, use 30 days and focus on that platform or account. If it is anything else, ask what window the user means and stop. Say the window and the workspace name at the top of the report.

## Steps

Call the read tools one or two at a time. If one call fails, carry on with the rest and say what is missing.

1. `list-workspaces` for the workspace id and name (one row). For another client the user needs that client's own connector.
2. `list-accounts(workspace_id)`: note each account's `id`, `platform` and `token_status`. An account whose token is not valid stops syncing, so its numbers go stale: say so and offer `get-connect-link(workspace_id, platform)`. Rows with ids like `facebook_page_*` or `linkedin_org_*` are extra rows; where an `account_id` is needed, use the row's `base_account_id`.
3. `cross-platform-analytics(workspace_id, days)` for the shape by platform, then `list-account-insights(workspace_id, days)` for each account. Use `get-account-analytics(workspace_id, account_id, days)` only for the one or two accounts that moved most.
4. Posts: `list-workspace-posts(workspace_id, status="published", start_date=..., end_date=..., include_metrics=true, limit=100)`. Work out the dates from today's date in your context (ask the user if you do not have it) and pass UTC times ending in `Z`; the no-`Z` rule is for scheduling writes, not reads. Page with `page=2, 3` while `has_more` is true, or say the ranking is partial. This leaves out Partially Published posts, which are their own status: pull `status="partially published"` too and say you did.
5. Open the top and bottom two or three posts with `get-post(post_id)` so each finding points at a real post.
6. If output was thin, look upstream before blaming the content: `list-workspace-posts(workspace_id, status="failed", start_date=...)` shows what did not go out.

## Reading the numbers

- Account `engagement` is activity gained inside the window (likes, replies, reposts, quotes). It is not reach and contains no views. `engagement_lifetime` is the all-time total; quote it only if asked. Never add up `*_cumulative` fields.
- A null value means no earlier reading to measure against: unknown, not zero. `cross-platform-analytics` leaves such accounts out of its totals, so say which account is missing.
- Quote `growth_rate` only when `growth_reliable` is true, and put the absolute follower change next to the percent. If `reconnect_required` is true, say the account needs reconnecting. Followers 0, engagement 0 and `growth_reliable` false together mean no data, not a dead account.
- Post metrics sync nightly. A zero on a post under about 24 hours old means "not synced yet": leave it out of the ranking.
- Posts with `has_publication_record` false have no linked account, so their zeros are missing data. Leave them out of rankings and say how many.
- Rank within one platform only; platforms report different things. With fewer than about five posts on a platform, describe them and do not call it a trend. Never invent an industry benchmark.
- If a tool is refused, call `get-my-capabilities(workspace_id)` and report `denied_by`. Do not guess at roles.

## Report

Keep it to one screen and lead with the claim:

- **Headline:** one sentence with the workspace name, the window and what happened.
- **What moved:** two or three specifics with numbers, each tied to a post, a gap or a reconnect.
- **What worked / what did not:** posts with the start of the text and `published_at`, same platform only.
- **What I could not see:** unsynced posts, accounts with no baseline, posts without a publication record (count them), invalid tokens, platforms Bolta has no analytics for.
- **Next:** at most three actions, each saying who does it, for example "plan more posts like these two" (`/bolta:plan-week`), "reconnect Instagram" (`/bolta:setup`). Offer them; do not take them.

## If a call fails

Read the result body (`ok`, `error`, `data.error_code`, `next_step`), not only the error flag. "Invalid API key", "API key expired" or "API key inactive": tell the user to reconnect the Bolta connector (Claude Code: run `/mcp`; in chat: Connectors settings) and stop.

## Do not

- Do not create, edit, schedule or publish anything, or promise an outcome.
- Do not call `engagement` "reach", and do not sum `*_cumulative` fields.
- Do not rank posts that are under 24 hours old or have no publication record.
- Do not quote `growth_rate` when `growth_reliable` is false.
- Do not rank from the first page without checking `has_more`.
