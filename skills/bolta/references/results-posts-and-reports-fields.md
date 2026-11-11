# Post fields by network, and how fresh they are

Read with [results-posts-and-reports.md](results-posts-and-reports.md) before quoting one network's numbers on a post, or when numbers look stuck.

## Fields by network

Top-level `*_count` fields add up all networks. Each post's `metrics` also has a block per network (`facebook`, `threads`, `instagram`, `linkedin`, `reddit`, `bluesky`, `mastodon`, `x`), only when that network has a non-zero number. Blocks carry `likes`, `comments`, `shares` and `total`, plus:

- Instagram: `saves`, `views`, `reach`, `impressions`. Its block `total` also counts saves, which `total_engagement` doesn't.
- Facebook: `reactions`.
- Threads, X: `quotes`, `views`. Bluesky: `quotes`.
- Reddit: `upvotes`, `downvotes`, `comments`, `awards` (no likes or shares).
- LinkedIn: `views`, `clicks`.

`impressions_count` and `reach_count` are Instagram only: use `views_count`. A 0 in a field that network doesn't report means "not reported", never "0 views". Say it like this: "1,200 views on Threads; Facebook doesn't report views."

## How fresh

- Threads numbers are fetched about every 12 hours. Other networks re-sync about once a week (early Sunday, UTC). The weekly LinkedIn sync doesn't update counts: LinkedIn numbers move only when refreshed.
- Post totals are rebuilt daily for posts under 14 days old, weekly up to 90 days, monthly after that.
- Zeros on a post under about a week old mean "not synced yet": leave it out of rankings and say so: "3 posts from this week aren't counted yet."
- The user can refresh one post: the refresh icon by Results on that post in Bolta's Inbox, once a minute. You can't refresh it. Say: "Want fresher numbers on that one? Hit refresh by Results on the post in Bolta."

## Always

- Follow the house rules in the Bolta skill.
