# Joining conversations

Two good replies and a list of skips is a good run; never pad to a number.

## Where it works

| Network | Find | Reply | React |
|-|-|-|-|
| Reddit | inside one subreddit | post or comment | upvote |
| Threads | keyword | yes | no |
| Bluesky | keyword | yes | like, repost |
| Mastodon | one hashtag | yes | favorite, boost |
| X | pasted link only | yes | like, repost |
| LinkedIn | pasted link only; no post text | yes | no |
| Facebook, Instagram, YouTube, TikTok, Pinterest | no | no | no |

`list-engagement-capabilities` is the live answer. Every action off means disconnected: hand to `connect`.

## The loop

1. **Account.** Two on one network: ask which one speaks. Check `list-engagements(account_id)`: skip threads already answered (one reply per post).
2. **Search** with `search-engagement-opportunities(account_id, platform, query, sort="new")`: one query per call, in words people type. Leave `campaign_id` out (despite the tool text, none is needed); keep the one it returns. Skip rows already replied to.
3. **Read** with `get-engagement-conversation(account_id, platform, target_id, target_type)`. Never judge from a title.
4. **Judge.** Skip if you'd only agree, it's answered well, all you'd add is the pitch, it's a rant or meme, it's old, or the community dislikes brands. Community rules can't be read from here: if unsure, ask. One line per skip.
5. **Bolta drafts** with `draft-engagement-reply(opportunity_id, account_id)`. Asking again returns the same draft; agreed changes go in the `content` sent.
6. **Check it.** Flag: restates the post, opens with praise, names the brand for no reason (the writer may slip one in), a link, a number or promise nobody gave, sounds like a company, too long.
7. **Show it** (below). On that reply's yes: `publish-engagement-reply(engagement_id, account_id, content)`, always with the exact text shown, so the check shows it. `account_id` makes a wrong identity fail instead of post.
8. **Verify** with `get-engagement-status(engagement_id, verify=true)`, up to 3 reads. Still pending: say queued, not confirmed; never resend.

```
Acme, as @handle on Reddit
Replying to <author> in <community>: <link>
They said: <two lines>
Reply:
> <exact text>
Public. It can't be edited or deleted from here. Send it?
```

## A pasted link

Read it with `get-social-content(account_id, target_url)`; its target id and type feed the next call. For Bolta to write, `create-engagement-opportunity` needs a `campaign_id` for that account and network: from a search with it, or a past reply in `list-engagements`. A fresh X or LinkedIn account has none: Bolta can't write this one yet; offer to send the user's own words as written, or skip. LinkedIn: pass the post text the user pastes as `content`, and say it's their paste.

## Status

published: live. missing_or_removed: sent, then taken down. verification_unavailable or verification_failed: couldn't check (always on LinkedIn). failed: give the reason as written; none given, say so and don't retry.

## Reddit

- `subreddit` (no "r/") is required. None in mind: suggest 2 or 3.
- Search finds posts only. For a comment, use its full /comments/ link; /s/ links don't resolve.
- A draft naming the product may need disclosure there: tell the user.
- Never downvote unless asked by name.
- A rate limit: stop. "Rate limited (conservative)": Bolta resends shortly, so report it queued. Banned, or below the community's posting requirements: not there for now. "Reddit refused this wording": the user rewrites it.

## Every week

A Bolta routine can find conversations and draft replies on a schedule (see `routine`). It never sends on its own.
