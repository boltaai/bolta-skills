# Best posts, live links and reports

Read for "which post did best", a link to a live post, a report Bolta made, or anything that lives only in Bolta on the web. Before quoting one network's numbers, or when numbers look stuck, read [results-posts-and-reports-fields.md](results-posts-and-reports-fields.md).

## Best posts

`list-workspace-posts` with `sort_by: "engagement"`, `sort_order: "desc"`, `status: "published"`, `include_metrics: true`, the window's `start_date` and `end_date`, a small `limit` (10) and `platform` for one network. It ranks the whole window: one page is enough.

- The order uses each post's `total_engagement` across all its networks: likes, comments, shares, quotes, reactions and awards (Reddit upvotes count as likes). Views, saves and clicks don't count. For "best LinkedIn post", re-rank posts that went to several networks by that network's block first.
- Posts with no numbers yet sort last: leave them out.
- `status: "published"` leaves out partially published posts (out on some accounts). If they matter, read `"partially published"` too and say so.
- Name the evidence: first words, network, day, and what the winners share.

Say it like this: "Your best post in the last 30 days: 'We almost shut down in March…' on LinkedIn, last Tuesday, 148 likes, comments and shares. The two best were both customer stories." Then one next step, such as "Make 3 more like it?"

## A link to the live post

- Any post, including Bolta routine and campaign drafts that went out: `get-post`, then `<network>_metrics.permalink`. X has none, and it may lag.
- Never build a link from an id. No link: say so plainly: "Bolta doesn't have a link for the X version; it went out on your X profile on <day>."

## Reports Bolta made

- `list-inbox-items` with `source: "report"` and `status: "approved"` gives finished reports: `title`, `created_at` and a 300-character `content_preview` of its description. `status: "pending"` lists reports still being made; `"rejected"` lists failed ones.
- Link `file_url` only when set. The full report is at bolta.ai/dashboard/reports or in the email.
- A PDF, CSV or TXT report file is made at bolta.ai/dashboard/reports. Research reports use credits.

Say it like this: "Your report '<title>' is ready. In short: <preview>. Full report: <file_url, or bolta.ai/dashboard/reports>."

## Only on the web

One line and one link each; you can't read these.

- **Competitors:** compare up to 4 Threads or X handles at Reports > Profile Discovery or bolta.ai/dashboard/explore. Needs a connected account on that network. Never estimate competitor numbers; check the handles resolved.
- **LinkedIn company page viewers** by country, industry, region and section (last 7 days; viewers, not followers; may ask to reconnect): bolta.ai/dashboard/analytics.
- **Team review stats:** Bolta does not measure approval speed; don't cite the Team Insights review panel. For what's waiting, use `total_team` from `list-inbox-items`.
- **Trending topics:** bolta.ai/dashboard/products/signals.

## Always

- Follow the house rules in the Bolta skill.
- Re-rank by one network before naming a best post on it.
- Leave unsynced and numberless posts out of rankings, and say how many.
- Never invent a link, a competitor number or an approval speed.
