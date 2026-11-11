# Reading the numbers

Read before quoting any account or post number.

## Account numbers

From `cross-platform-analytics`, `list-account-insights` and `get-account-analytics`. They take `days` (default 30, max 365), always ending now. They refresh at least once a day (LinkedIn, Mastodon, Reddit and Bluesky only once), so the latest hours aren't in them.

- `engagement` is likes, replies, reposts and quotes gained in the window. It is not reach and has no views. `engagement_lifetime` is all-time: quote it only when asked.
- One account: quote `totals.engagement` and `followers_change`. Never add up the daily series. Each day is that day's change, and the `*_cumulative` fields are running totals.
- `null` means no earlier reading to compare with: unknown, not zero. The network summary leaves such accounts out of its window totals, so name the missing account.
- `counter_reset: true` marks a day the lifetime count fell (deleted posts or a reconnect). Not a slump.
- **Growth:** quote `growth_rate` only from `list-account-insights`, and only where `growth_reliable` is true. Otherwise say "not enough reliable data" and why: disconnected (`reconnect_required`), no starting count, or a stale reading. The network summary's `avg_growth_rate` has no such check: never rank networks on it.
- Put people next to the percent: "+40% (8 people)".
- Followers 0, engagement 0 and `growth_reliable` false together mean no data, not a dead account.
- Bolta has account numbers for LinkedIn, X, Instagram, Facebook, Threads, Bluesky, Mastodon and Reddit only. For any other network, say there are none; never report zeros.
- Facebook Page and LinkedIn company rows: where an account is needed, use the row's `base_account_id`.
- Account numbers come from the networks; post numbers come from Bolta's own records. Neither is evidence about the other.

## Post numbers

From `list-workspace-posts` with `status: "published"`, `start_date`, `end_date`, `include_metrics: true` and `limit: 100`.

- Page with `page` while `has_more` is true. A ranking from page 1 alone is partial: say so.
- `status` is exact. "published" leaves out "partially published", which went out on some accounts. For everything that went out, read both and say so.
- Dates match a post's scheduled time, or its creation time if it has none. Use `published_at` for when it actually went out.
- Totals sit in `metrics`: `total_engagement`, `likes_count`, `comments_count`, `shares_count`, `views_count`, plus a breakdown per network. Views come only from Threads, Instagram, LinkedIn and X. `views_count` is 0 on Facebook, Bluesky, Mastodon and Reddit because they don't report views: say "not reported", never "0 views".
- There is no sort by engagement: rank the rows yourself, within one network. Networks count different things, so never rank across them.
- One network only: add `platform` and `metrics_platforms`.
- Over about 300 posts in the window: ask to narrow it.
- Name the evidence: "the two best were both customer stories". Show each post's first words, network and day.

## Comparing two periods

- Posts: two reads with date ranges of equal length.
- One account: read again with `days` doubled, then subtract the first read's `totals.engagement` and `followers_change`. Say you worked it out that way. Growth rates and lifetime figures don't subtract.
- Say so if the current period isn't over yet.
- Name what else changed: a paused Bolta routine, a launch, a reconnect.

## Claims

- Fewer than about 5 posts on a network: describe them, don't call it a trend.
- Correlation, not cause: "posts that opened with a question averaged 41 (6 posts)", not "questions win".
- Never invent a benchmark ("the average is 3%") or promise a result.
- A new or just-reconnected account has no trend yet. Say so.
