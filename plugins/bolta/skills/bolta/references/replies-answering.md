# Answering people who talk to you

## Reply drafts

- Read: `list-inbox-items(source="hunter", status="pending", limit=50)`. Page with `offset` while `has_more` is true.
- Each row has the network, who wrote (`mention_author`), what they said (`mention_content`, cut at 300 characters), the link (`platform_url`) and Bolta's draft (`content`). `campaign_name` is where the row came from: a watch ("conversations Bolta watches for you"), direct engagement, or a Reddit warm-up. Never say campaign.
- Show a numbered list: who, where, what they said, the draft, the link.
- Change text only when asked: `update-outreach-reply` saves and sends nothing. A sent reply can't be changed.
- Send: `send-outreach-reply(reply_id, content)`, always with the exact agreed text, so the check shows what goes out. It counts as the user's yes: call it only on their yes, never to get around a hold. For a target from a draft row, use this, not `reply-to-social-content`.
- It queues: `pending` with `needs_approval` false means queued, not failed; the row still shows as waiting until it goes. Read back with `get-engagement-status(engagement_id, verify=true)` using the row's reply id. `list-engagements(status="failed")` gives a failure's reason.
- Sendable on Reddit, Threads, X, LinkedIn, Bluesky, Mastodon. A Facebook or Instagram draft fails here: give the link.

## A comment on your own post

1. Use the account that owns the post. Two on one network: ask which.
2. `get-social-content(account_id, target_url)`: the comment, its author, nearby replies. Sort it first ([sort and check](replies-answering-sort-and-check.md)).
3. `draft-inbound-reply(account_id, target_url)` saves and sends nothing; it only returns text. Call again only for "another take".
4. Check the draft ([sort and check](replies-answering-sort-and-check.md)). Show the comment, draft, account, link and brand. On that reply's yes: `reply-to-social-content(account_id, content, target_url)`. Bolta stops a repeat send per target and sending account, so always reply from the same account. `idempotency_key` is only an audit label.
5. Read the result: published (show the link), queued or throttled (not confirmed, not a failure), failed (say why). With `wait` false, poll `get-engagement-status`. `deduplicated` true: a reply already existed and nothing new went out; show it. The web Inbox row stays open after replying here.

| Network | Draft and reply by link | React |
|-|-|-|
| Reddit | yes (full /comments/ link) | upvote |
| Threads | yes | no |
| Bluesky | yes | like, repost |
| Mastodon | yes | favorite, boost |
| X | yes | like, repost |
| LinkedIn | no draft (Bolta can't read the text): the user's own words, or answer in LinkedIn | no |
| Instagram | not here: Bolta's web Inbox drafts and sends it | no |
| Facebook | not here: Bolta's web Inbox (may fall back to copy and open) | no |
| YouTube, TikTok, Pinterest | no: answer in the app | no |

`list-engagement-capabilities` (live, per account) wins over this table.

## When it goes wrong

- The network can't do it: give the link; don't retry another way.
- Disconnected account: hand to [connect](connect.md).
- Not found: deleted, private or a wrong link. Ask for another.
- Timeout on a send: outcome unknown. Check `list-engagements` first.
- A limit or "wait a moment": stop for now.

A hold, a removal, Reddit safety or the web Inbox: [held-and-inbox](replies-held-and-inbox.md).
