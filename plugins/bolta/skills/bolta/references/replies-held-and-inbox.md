# Held replies, Reddit safety and the web Inbox

## Reading a reply's status

`get-engagement-status(engagement_id, verify=true)`:

| Status | Means | Do |
|-|-|-|
| `sent` with `canonical_url` | posted | show the link |
| `pending`, `needs_approval` false | still queued | say queued, not confirmed; never resend |
| `pending`, `needs_approval` true, with an `error` | Bolta held it | quote the reason; a person approves it in Bolta |
| `failed` | it didn't go | give the reason as written (none given: say so); don't retry, a new draft is needed |

- No `verification_status`: it wasn't checked (only `sent` replies are). `published`: found. On X, Threads, Bluesky and Mastodon that only means the reply is still reachable.
- `missing_or_removed`: sent, then taken down. `verification_unavailable`: this network can't be checked (anything but Reddit, X, Threads, Bluesky and Mastodon). `verification_failed`: the check errored.
- Queued or throttled is not a failure. `list-engagements(status="failed")` lists failures.

## When it goes wrong

- The network can't do it: give the link; don't retry another way.
- Disconnected account: hand to [connect](connect.md).
- Not found: deleted, private or a wrong link. Ask for another.
- Timeout on a send: outcome unknown. Check `list-engagements` first, before any resend.
- A limit or "wait a moment": stop for now.

## Reddit safety

- **New or low-karma accounts** (under 30 days old, under 100 karma, or no verified email) are paced, even with a person's yes.
- **A suspended account** blocks sending ([connect](connect.md)).
- **Removed by Reddit:** a `failed` row whose reason starts `REMOVED_BY_PLATFORM` was taken down. Don't resend. Bolta then pauses unattended Reddit replies from that account for 72 hours (7 days after a second removal within 7 days, or a removal only the author can see), and skips that subreddit after an AutoModerator removal. Replies a person approves still go.
- **Locked or archived threads:** an unattended reply is dropped for good.
- A rate limit: stop. "Rate limited (conservative)": Bolta resends shortly, so report it queued. Banned, or below a community's posting requirements: not there for now. "Reddit refused this wording": Bolta holds the draft unchanged; the user rewords it and approves it in Bolta. Never resend the same text.
- **Warm-up rows:** `send-outreach-reply` returns `warmup_requires_human`. The person approves those in Bolta themselves; don't retry.

## Premium

Sending replies needs Premium. Without it, engagement tools refuse with `hunter_plan_required`, and an already-queued reply goes back to review with "Not sent: replying needs a Premium plan."

## Web Inbox, reply rules and monitors

Comments on the brand's own posts, standing reply rules, monitors and Auto Reply: [web Inbox](replies-held-and-inbox-web.md).

## Always

- A held reply waits for a person in Bolta. Never resend, reword or switch tools to get past a hold, a pause or a removal.
- Say queued until a status read shows it sent.
