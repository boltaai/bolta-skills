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

`list-engagement-capabilities` is the live answer. `credential_ready` false (every action off) means reconnect: hand to [connect](connect.md).

## The loop

1. **Account.** Two on one network: ask which one speaks. Check `list-engagements(account_id)`: skip threads already answered (one reply per post).
2. **Search** with `search-engagement-opportunities(account_id, platform, query, sort="new")`: one query per call, in words people type. Leave `campaign_id` out; keep the one it returns. Skip rows already replied to.
3. **Read** with `get-engagement-conversation(account_id, platform, target_id, target_type)`. Never judge from a title.
4. **Judge.** Skip if you'd only agree, it's answered well, all you'd add is the pitch, it's a rant or meme, it's old, or the community dislikes brands. Community rules can't be read from here: if unsure, ask. One line per skip.
5. **Bolta drafts** with `draft-engagement-reply(opportunity_id, account_id)`. `tone` and `voice_profile_id` shape the first draft only, and `tone` "professional" or "helpful" changes nothing. Asking again returns the same draft: to change it, rewrite it with the user, then save with `update-outreach-reply` (its `reply_id` is the `engagement_id`) or send the agreed text as `content`.
6. **Check it.** Flag: restates the post, opens with praise, names the brand for no reason, a link, number or promise nobody gave, sounds corporate, too long.
7. **Show it** (below). On that reply's yes: `publish-engagement-reply(engagement_id, account_id, content)`, always with the exact text shown, so the check shows it. `account_id` makes a wrong identity fail instead of post.
8. **Verify** with `get-engagement-status(engagement_id, verify=true)`, up to 3 reads. `pending`, `needs_approval` false: queued, not confirmed; never resend. `needs_approval` true with an `error`: Bolta held it; quote the reason, a person approves it in Bolta. Statuses, holds and Reddit removals: [held-and-inbox](replies-held-and-inbox.md).

```
Acme, as @handle on Reddit
Replying to <author> in <community>: <link>
They said: <two lines>
Reply:
> <exact text>
Public. It can't be edited or deleted from here. Send it?
```

## A pasted link

Read it with `get-social-content(account_id, target_url)`; its target id and type feed the next call. For Bolta to write, `create-engagement-opportunity` needs a `campaign_id` for that account and network: from a search with it, or a past reply in `list-engagements`. A fresh X or LinkedIn account has none: offer to send the user's own words as written with `reply-to-social-content`, or skip. LinkedIn: pass the post text the user pastes as `content`, and say it's their paste.

## Reddit

- `subreddit` (no "r/") is required. None in mind: suggest 2 or 3.
- Search finds posts only. A comment: its full /comments/ link (/s/ links don't resolve).
- A draft naming the product may need disclosure there: tell the user.
- Never downvote unless asked by name.
- Limits, rules, holds and removals, and why a chat yes is still paced: [replies-reddit.md](replies-reddit.md).

## Every week

A Bolta routine ([reply templates](routine-templates-replies-reports.md)) finds conversations and drafts replies on a schedule ([routine](routine.md)). Drafts wait in `list-engagements(status="pending")` until a person approves them.

## Always

- Follow the house rules in the Bolta skill.
