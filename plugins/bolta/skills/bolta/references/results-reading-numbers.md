# Reading the numbers

Read before quoting any account or post number. Best posts, fields per network, freshness, live links and reports: [results-posts-and-reports.md](results-posts-and-reports.md).

## Account numbers

From `cross-platform-analytics`, `list-account-insights` and `get-account-analytics`. They take `days` (default 30, max 365), counted back from now. Account snapshots sync at least once a day (LinkedIn, Mastodon, Reddit and Bluesky only once), so the newest activity may not be in them yet.

- On `cross-platform-analytics` and `list-account-insights`, `engagement` is what the posts published in the window earned. `impressions` is on the same basis, for Instagram, X, Threads and LinkedIn only; `null` means not reported. `engagement_lifetime` is all-time: quote it only when asked.
- On `cross-platform-analytics`, `likes`, `replies` and `reposts` per network are activity gained in the window, so they need not add up to `engagement`.
- On `cross-platform-analytics`, Facebook's `accounts` counts Pages, not logins.
- An `engagement` of 0 where `impressions` is null may be unknown: check that account in `list-account-insights`, where unknown shows as `null`.
- `null` means no earlier reading to compare with, or a network that reports none: unknown, not zero. The network summary leaves such accounts out of its window totals, so name the missing account.
- `get-account-analytics` totals are still differences between snapshots. Quote `totals.engagement` and `followers_change`; never add up the daily series. Each day is that day's change, and the `*_cumulative` fields are running totals. `counter_reset: true` marks a day the lifetime count fell (deleted posts or a reconnect), not a slump.

Reconnect, stale, growth, and which networks have account numbers at all: [results-reading-numbers-account-status.md](results-reading-numbers-account-status.md).

## Post numbers

From `list-workspace-posts` with `status: "published"`, `start_date`, `end_date`, `include_metrics: true` and `limit: 100`.

- Page with `page` while `has_more` is true. A total from page 1 alone is partial: say so.
- `status` is exact. "published" leaves out "partially published" (out on some accounts). For everything that went out, read both and say so.
- Dates match a post's scheduled time, or its creation time. `published_at` is when it went out.
- Totals sit in `metrics` (`total_engagement`, `likes_count`, `comments_count`, `shares_count`, `views_count`), plus a breakdown per network. Never compare totals across networks. Views come only from Threads, Instagram, LinkedIn and X: on other networks `views_count` is 0 because they don't report views, so say "not reported", never "0 views".
- To rank posts, sort with `sort_by: "engagement"` as in [results-posts-and-reports.md](results-posts-and-reports.md); never rank across networks.
- One network only: add `platform` and `metrics_platforms`, and read that network's breakdown; totals still span every network. Over about 300 posts: ask to narrow it.

## Comparing two periods

- Posts: two reads with date ranges of equal length.
- One account: read again with `days` doubled (max 365), then subtract the first read's `totals.engagement` and `followers_change`. Say you worked it out that way. Growth rates and lifetime figures don't subtract.
- Say so if the current period isn't over. Name what else changed: a paused Bolta routine, a launch, a reconnect.

## Claims

- Fewer than about 5 posts on a network: describe them, don't call it a trend.
- Correlation, not cause: "posts that opened with a question averaged 41 (6 posts)", not "questions win".
- Name the evidence: "the two best were both customer stories". Show each post's first words, network and day.
- Never invent a benchmark ("the average is 3%") or promise a result. A new or just-reconnected account has no trend yet.

## Always

- Follow the house rules in the Bolta skill.
