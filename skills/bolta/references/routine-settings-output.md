# Bolta routine settings: what each run makes

`output_config` on `create-routine` and `update-routine`. The tool describes it only as "platforms, counts"; every key below is real. Writing settings: [routine-settings-writing.md](routine-settings-writing.md). Pictures, the client, stories, Library posts: [routine-outputs.md](routine-outputs.md). Labels as in [routine-settings.md](routine-settings.md).

## Always sent

- `artifact_type`: `post`, `article` (weekly article), `reply` (reply routines) or `report` (reports). Required whenever `output_config` is sent, or the save is refused.
- `count`: posts per run. One post everywhere (`"cross-platform"`): each goes to every bound account. One per network (`"platform-specific"`): `count` ideas, each written once per account ([weekly-networks](routine-weekly-networks.md)). Send it every time. Sent without it, Bolta uses its writer's default, not the routine's: founder stories, customer wins and LinkedIn positions jump from 2 to 4 (Bolta). Most per run:

| Makes | Most |
|-|-|
| Weekly posts, founder, customer wins, LinkedIn positions, Square | 10 |
| Best posts again, threads; replies | 8 |
| Each new article, a Drive file | 6 |
| Research series | 5 |
| Merged pull requests | 4 |
| A meeting | 3 |
| Weekly article, HubSpot win | 2 |
| Reports | 1 |

These are limits per run, not per week: a daily routine at 10 is 70 drafts a week. Size to what gets decided, 3-6 a week for most people (advice; seen: weekly at 3 is what people keep, and one daily 10-a-run routine wrote 167 drafts, most never decided).

## Only when it fits

- `platforms`: only when the user limits networks ("LinkedIn only"). Left out, Bolta takes them from the bound accounts, so an account added later is used. Values: `x`, `threads`, `linkedin`, `facebook`, `instagram`, `reddit`, `bluesky`, `mastodon`, `tiktok`, `youtube`, `pinterest`, `wordpress`.
- `source_urls`: exactly one public page Bolta reads at every run ("from my blog page", a changelog, a newsletter archive). On weekly posts, research series and weekly articles. A page that changed nothing since the last run skips that scheduled run; one that can't be read refuses the run. A page that never changes skips every week: use it only for pages that change.
- `topics` (reply routines, required, up to 10 phrases of 120 characters): what people say when they need the business, in the user's words. `communities` (up to 10 subreddits, Reddit only). A reply routine made on Bolta's web page has no topics, so every run fails: read `get-routine` `output_config.topics` and, with a yes, add them with `update-routine`.
- `cta`: `{"text":"Book a free consult","url":"https://..."}`, text up to 200 characters, written exactly as it should read; a link only the user gave. On weekly posts and its siblings, best posts again and the weekly article. One call to action, not every post a pitch (advice).

## Where ideas come from

Most post routines and the weekly article take one unused idea per piece from the brand's documents (bolta.ai/dashboard/knowledge-base?tab=references). A `source_urls` page, an app source, best posts and threads turn that off: they write from their source only. Adding documents is the lasting way to steer topics.

## Changing it

`update-routine` replaces `output_config` whole, except `review`, `story` and `library`, which are kept when left out. Read `get-routine`, change one key, resend all the rest, `artifact_type` and `count` included. Sending only `{"count":2}` is refused for a missing `artifact_type`, and drops media, settings and topics.

## Always

- Send `artifact_type` and `count` together, every time `output_config` is sent.
- Never send a key the routine doesn't take: `topics` on a post routine, `source_urls` on a best-posts routine, `time_window` anywhere are refused.
