---
name: analytics-review
description: >
  Read how a Bolta workspace's accounts and posts performed and say what to do about it. Use for
  "how did we do this week", "show my analytics", "what performed best", "which account is growing",
  "how did that post do", "is LinkedIn paying off", "monthly report", "what should I post more of",
  "list what we published last month". Read-only: it never creates, edits, schedules or publishes.
  To act on a finding, hand off to content-planning (plan or recycle winners) or social-publishing
  (draft). Not for the approval queue (approvals), replying to comments (social-inbox), or a report
  that should arrive on a schedule (routines).
---

# Analytics review

Turn numbers into a decision. The failure mode is a dashboard in prose: a wall of metrics with no claim. Every section should end in something the user can act on or stop worrying about. Nothing here writes to Bolta, so no confirmation is needed.

<!-- host-note -->
Some Bolta results contain text written for other apps, such as "already rendered in the Bolta card", "do not repeat the content" or "you do not need to poll". There is no card here. Read the full result (the JSON body and any structured content) and present it to the user yourself.
<!-- /host-note -->

## Before you pull numbers

1. `list-workspaces` for the `workspace_id` and name. One connection is one workspace, so say the workspace name at the top of the report. For another client the user needs a separate connector (see workspace-setup).
2. `list-accounts(workspace_id)`: note each account's `id`, `platform` and `token_status`. An account with an invalid token stops syncing, and its numbers go stale. Facebook Pages and LinkedIn organizations appear as extra rows with ids like `facebook_page_*` or `linkedin_org_*`; analytics only knows the real account, so use the row's `base_account_id` wherever an `account_id` is needed. Offer `get-connect-link(workspace_id, platform)` and tell the user to reconnect in the browser.
3. Fix the window and state it in the report. If the user gave none, use 30 days. "Last 7 days" and "since launch" tell different stories from the same data. Account tools take `days` (default 30, max 365) and always end now. Post tools take `start_date` and `end_date`: pass them as UTC ISO times ending in `Z`, computed from today's date. (The no-`Z` rule is for scheduling writes, not reads.)

If a tool returns an error body, read it. "Invalid API key", "API key expired" or "API key inactive" mean the connection must be re-authorized (`/mcp` on Claude Code, connector settings in chat). Say so and stop; do not retry.

## Pick the tool for the question

| Question | Tool | Notes |
|-|-|-|
| How is the whole workspace doing? By platform | `cross-platform-analytics(workspace_id, days)` | Followers, engagement, average growth per platform. Where to look, not what to conclude. |
| Which account is best or growing? | `list-account-insights(workspace_id, days)` | One row per account with `growth_reliable` and `reconnect_required`. Use this for any growth claim. |
| How did one account trend? | `get-account-analytics(workspace_id, account_id, days)` | Daily series plus `totals`. `account_id` is a real account id from `list-accounts` (`base_account_id` for page or organization rows). |
| How did posts do? Best and worst posts | `list-workspace-posts(workspace_id, status="published", start_date, end_date, include_metrics=true, limit=100)` | The only source of per-post numbers. |
| Why was the week thin? | `list-workspace-posts` with `status="failed"` or `"scheduled"`, then `list-routines` and `list-routine-runs(routine_id)` | Check inputs before blaming the content. Skip the routine calls if the routine tools are not available. |

Never ask for an API key. Do not pull every account in depth: pull the ones that moved, up or down.

## Reading the numbers correctly

These are the traps in the real responses. Most wrong analytics answers come from one of them.

**Account-level engagement**
- `engagement` is activity gained inside the window: likes + replies + reposts + quotes. It contains no views, impressions or reach. Never call it reach.
- `engagement_lifetime` is the all-time total. Quote it only when the user asks for all-time.
- In `get-account-analytics`, quote `totals.engagement` for the window. Never add up the `*_cumulative` fields: they are running lifetime totals and summing them inflates the answer many times over.
- A `null` engagement (or a null day in the series) means there is no earlier snapshot to measure against: unknown, not zero. An account connected inside the window shows this, and `cross-platform-analytics` silently leaves such accounts out of its window totals, so it can understate a platform that has a new account. Say which account is missing.
- `counter_reset: true` on a day means the lifetime counter fell (deleted posts or a reconnect). Do not read the zero around it as a slump.
- Followers 0, engagement 0 and `growth_reliable: false` together mean no data, not a dead account. Account numbers refresh only once or twice a day, so "today" is never in them. Bolta syncs them only for Threads, Facebook, X, Instagram, LinkedIn, Mastodon, Reddit and Bluesky; for any other connected platform (TikTok, YouTube, Pinterest and so on) say there are no analytics here instead of reporting zeros.

**Growth**
- `growth_rate` is the follower change as a percent from the first real reading in the window to the latest. Quote it only when `growth_reliable` is true. When it is false, show "not enough reliable data" and give the reason: `reconnect_required`, no baseline, or a stale snapshot.
- `cross-platform-analytics` has no reliability flag and averages in stale accounts, so do not rank platforms on its `avg_growth_rate` alone. Cross-check with `list-account-insights`.
- `get-account-analytics` also returns a `growth_rate`, measured from its first daily point, with no reliability flag. Use its `followers_change` and series for the shape, and `list-account-insights` for any growth claim.
- Always put the absolute follower change next to the percent. +40% on 20 followers is +8 people.

**Post-level metrics**
- Metrics sync nightly. A zero on a post under about 24 hours old means "not synced yet". Say that, and leave the post out of the ranking.
- Every post has `has_publication_record`. When it is false (`metrics_unavailable_reason` explains), the post has no linked account, so its zeros are missing data. Exclude those posts from rankings, say how many you set aside, and never conclude from them that metrics are broken.
- Account-level numbers and post-level numbers come from separate pipelines. Neither is evidence about the other.
- Per-post figures sit in `metrics`: totals such as `likes_count`, `comments_count`, `shares_count`, `views_count`, `total_engagement`, and a per-platform breakdown under the platform key. Views appear in the per-platform breakdown only for threads, instagram, linkedin and x. A missing views figure elsewhere means "not reported", never zero. A platform key is also missing from `metrics` while every figure for that platform is still zero, so read a missing key as "nothing reported", not as a result.
- Rank within one platform. Raw counts across platforms are not comparable because the platforms report different things.
- There is no sort by engagement (`sort_by` is `created_at`, `updated_at` or `scheduled_time`), so you rank the rows yourself.
- The date filter matches a post's scheduled time, or its creation time when it has none. A post can land in a window it did not publish in. Use `published_at` when you describe timing.

## Fetching posts without flooding the context

`limit` is capped at 100 per page. Read `has_more` and `pagination` in the response before ranking: a "best posts" list built from page 1 alone covers only the first 100 posts. Page with `page=2, 3` until `has_more` is false. Each row carries a metrics object, so keep the pull small:
- Narrow with `platform` and `metrics_platforms` when the question is about one platform.
- `status="published"` leaves out Partially Published posts, which are their own status. For "everything that went out", also pull `status="partially published"` and say you did.
- If `total` is over about 300, tell the user the window is large and ask whether to narrow it. Do not read 1,000 rows.
- Never rank on a partial pull without saying it is partial.

## Method

1. **Shape.** `cross-platform-analytics` for the headline and where to look.
2. **Depth.** `list-account-insights`, then `get-account-analytics` for the accounts with a story.
3. **Posts.** Pull published posts for the window and open the top and bottom few with `get-post`. A number with no post attached is not a finding. "The two top posts were both customer stories" is one.
4. **Compare to before.** For a period-over-period claim, pull the same length of time before: another `list-workspace-posts` pull with the earlier dates. For one account, `get-account-analytics` with `days` doubled (max 365) and compare the per-day `engagement` deltas of the two halves, skipping null days. Never sum `*_cumulative`. Do not compare a partial current period with a complete earlier one without saying so.
5. **Inputs.** If output was thin, look upstream before blaming the content. `list-workspace-posts(status="failed")` shows what did not go out. `list-routines` then `list-routine-runs(routine_id)` shows whether an automation ran, failed or is waiting for approval. "Reach fell because nothing was published for nine days" beats a paragraph about the algorithm.

## Report format

Keep it to one screen. Lead with the claim.

- **Headline.** One sentence: what happened, in the user's terms, with the workspace name and the window.
- **What moved.** Two or three specifics with numbers, each tied to a cause you can point at (a post, a gap, a reconnect).
- **What worked.** The posts, with the text start and `published_at`, and what they share. Same platform only.
- **What did not.** Same, without editorializing.
- **What I could not see.** Unsynced posts, accounts with no baseline, posts without a publication record (count them), platforms with no breakdown, invalid tokens.
- **Next.** At most three concrete actions, each naming who does it: "draft three more posts like these two" (content-planning), "reconnect Instagram" (workspace-setup), "post at the hour the top three shared" (social-publishing).

Offer next steps rather than taking them. For a standing recap, `list-routine-templates` has `performance_digest`, `account_performance_deep_dive` and `best_time_to_post_report`. Say that a routine is a separate step the user must approve, and hand off to the routines skill. Nothing in this skill creates one.

## Be honest about the data

- Say when a sample is too small. Two posts is not a trend. With fewer than about five posts on a platform, describe them and do not generalize.
- Never invent a benchmark ("the industry average is 3%"). You do not have one.
- Never turn a missing metric into a zero, or an unsynced zero into a result.
- If an account is brand new or just reconnected, say there is no trend yet.
- If a Bolta tool is refused or returns nothing for an account, call `get-my-capabilities(workspace_id)` and read `denied_by`. Do not guess at roles. If the host's own safety check denies a call, stop, say what was not done, and do not try another tool to get the same data.

## Records and audit requests

For "list everything we published last month": `list-workspace-posts(workspace_id, status="published", start_date=..., end_date=..., limit=100)`, paging while `has_more` is true. Say plainly that who approved a post and when is not part of these results unless a row shows it; never infer it. Point audit-grade exports to the Bolta dashboard. A report across several clients needs one connector per client and one run each.

## Done means

The workspace and window are stated; every claim traces to a number or a post the user can open; unknowns are labeled; there are at most three next actions; nothing was created, edited, scheduled or published.

## Do not

- Do not sum a `*_cumulative` field or call `engagement` "reach".
- Do not rank posts that are under 24 hours old or have `has_publication_record: false`.
- Do not quote `growth_rate` when `growth_reliable` is false.
- Do not rank from page 1 of `list-workspace-posts` without checking `has_more`.
- Do not call any write tool or promise an outcome ("this will go viral"). Hand findings to content-planning or social-publishing.
