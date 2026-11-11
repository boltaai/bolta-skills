# Held replies, Reddit safety and the web Inbox

## Reading a reply's status

`list-engagements(engagement_id, verify=true)`:

| Status | Means | Do |
|-|-|-|
| `sent` with `canonical_url` | posted | show the link |
| `pending`, `needs_approval` false | still queued | say queued, not confirmed; never resend |
| `pending`, `needs_approval` true, with an `error` | Bolta held it | quote the reason; a person approves it in Bolta |
| `failed` | it didn't go | give the reason as written (none given: say so); don't retry, a new draft is needed |

- No `verification_status`: it wasn't checked (only `sent` replies are). `published`: found. On X, Threads, Bluesky and Mastodon that only means the reply is still reachable.
- `missing_or_removed`: sent, then taken down. `verification_unavailable`: this network can't be checked (anything but Reddit, X, Threads, Bluesky and Mastodon). `verification_failed`: the check errored; off Reddit a removed reply can look like this too.
- Queued or throttled is not a failure. `list-engagements(status="failed")` lists failures.

## When it goes wrong

- The network can't do it: give the link; don't retry another way.
- Disconnected account: hand to [connect](connect.md).
- Not found: deleted, private or a wrong link. Ask for another.
- Timeout on a send: outcome unknown. Check `list-engagements` first, before any resend.
- A limit or "wait a moment": stop for now.

## Reddit

Pacing, whose yes counts, subreddit rules, removals and warm-up rows: [replies-reddit.md](replies-reddit.md). Read it before sending or promising any Reddit reply.

## Premium

Sending replies needs Premium. Without it, engagement tools refuse with `hunter_plan_required`, and an already-queued reply goes back to review with "Not sent: replying needs a Premium plan."

## Web Inbox, reply rules and monitors

Comments on the brand's own posts, standing reply rules, monitors and Auto Reply: [web Inbox](replies-held-and-inbox-web.md).

## Always

- Follow the house rules in the Bolta skill.
- A held reply waits for a person in Bolta. Never resend, reword or switch tools to get past a hold, a pause or a removal.
- Say queued until a status read shows it sent.
