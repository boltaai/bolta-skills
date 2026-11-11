# Bolta routines that reply or report

Read after [routine-templates.md](routine-templates.md) for Outreach replies, Comment replies and Insights. Quotes and counts are Bolta's; "Fits" is advice.

## Outreach replies: join conversations

| `template_key` | Makes | Networks | Fits |
|-|-|-|-|
| `reddit_engagement` | "A few genuinely useful Reddit replies, waiting for your approval", each to a different thread, plus why others were skipped | Reddit | Brands whose buyers ask for help in subreddits |
| `cross_platform_engagement` | One pass across the connected networks, a handful of replies | Reddit, Threads, Bluesky, Mastodon | Brands present on several of these |
| `social_inbox_engagement` | Replies to recent mentions of the brand or its problem | Reddit, Threads, Bluesky, Mastodon | Brands people already talk about |

- **Premium only.** Without it the save, the switch on and every run are refused; say "Replies routines need the Premium plan" and link bolta.ai/pricing.
- **Bind the speaking account** in `source_bindings`.
- **Topics are required:** `output_config: {"artifact_type":"reply","count":3,"topics":[...],"communities":[...]}`. `topics`: up to 10 short phrases buyers use when they need the business ("best CRM for a 5-person agency"), in the user's words. `communities`: up to 10 subreddits, Reddit only. With none, switching on is refused here and every run is refused. Routines made on Bolta's web page start with none: check `get-routine`, add them with a yes.
- `count` 3 (most 8); weekly or a few weekdays (advice: replies go stale, daily is fine only if someone reviews daily). Never `auto`: ask me first or the brand setting.
- Drafts wait in `list-engagements` as `pending`, not in the review list. Sending them: [replies](replies.md).
- **The Outreach keyword monitor** (keywords, subreddits, networks, scored for buying interest) is made by Bolta's planner (`plan-routine`, then `revise-plan` `changes` with `keywords`, `subreddits`) or on Bolta's routines page (bolta.ai/dashboard/routines), never with `create-routine`. Its keywords are edited on that page.
- Seen: one reply routine in production, so no evidence yet on what works; start with 3 replies weekly.

## Comment replies: not yet

Comment replies on the brand's own posts can't be a routine yet ("Coming soon" in Bolta). For one comment: its link and `draft-inbound-reply`, in [replies](replies.md).

## Insights: reports

| `template_key` | Makes | Runs |
|-|-|-|
| `performance_digest` (beta) | "Your week's numbers, read for you, in your inbox": what carried the week and what to do more of | Weekly, Monday morning |
| `account_performance_deep_dive` (beta) | One account fully read, compared with last month | Monthly; one account in `source_bindings`; the first has no month to compare |
| `best_time_to_post_report` (beta) | The hours each account's audience shows up, with the evidence | Monthly ("audiences drift") |

- Reports post nothing: each run emails the brand's admins and saves to Reports. They cost no review time, so they fit beside 1-2 writing routines.
- `approval_policy: "inherit"` only; say first: "Reports post nothing, but Bolta's checks still ask before saving and switching on."
- `output_config: {"artifact_type":"report","count":1}`. No voice, no writing settings.
- Seen: reports barely ran in production; offer one when the user asks how things are going, or in place of more drafts when 10+ wait and there are published posts to read.

## Always

- Check Premium and gather topics before saving a reply routine.
- Say a report emails numbers and posts nothing.
