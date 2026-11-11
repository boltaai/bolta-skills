# One idea on several networks

How a post reaches several networks, and when to write separate posts instead.

## How Bolta holds it

- One post can go to many accounts: list them all in `account_ids` (or an account group in `social_buckets`). Every account gets the same text and media.
- Each network's settings live once on the post and apply to all of that network's accounts on it ([platforms](post-platforms.md), section 3). Two Instagram accounts on one post share one Reel-or-feed choice.
- Text that differs per network can't be set from here yet; Bolta's composer can. So:
  - **Same words fit everywhere** (an announcement, a short line): one post, all the accounts. Count against the shortest limit among them.
  - **Each network wants its own shape** (the usual case): one post per network, each written fresh. Save them together with one `bulk-create-posts`, each item with its own `account_ids`.

## Before writing

1. Read `get-posting-rules` for every network named: limits, media needed, what must be set.
2. Check each network against the media the user has. Name any that would fail and why before writing: "TikTok needs a video; skip it, or do you have one?"
3. Pick a shape per network: LinkedIn a short story, X one line or a short thread, Threads conversational with one topic, Instagram the caption under an image, Bluesky plain and short, Reddit a title and a post that fits the subreddit's rules.

## Writing

- Write each version fresh. Same point, different first line; never paste one and trim it.
- Leave out networks that don't fit, and say so once: "Skipped Pinterest: no image."
- Then set each post's network settings ([Threads, Instagram, Facebook](post-networks-meta.md) · [X, LinkedIn, Bluesky, Mastodon, Reddit, Discord](post-networks-text.md) · [TikTok, YouTube, Pinterest](post-networks-video.md)). One `update-post-platform-details` per post and network.

## Showing it

Number every saved post with its network and account, full text, and any settings in plain words:

> 1. LinkedIn, Acme: (full text)
> 2. Threads, @acme: (full text). Topic: Small Business.
> 3. Instagram, @acme: (full text). A Reel, with the video you sent.

End as the post playbook says: saved as drafts, nothing goes out yet.

## When they say yes

- Each post is approved, scheduled or posted on its own; one message can cover all ("all three yes"). [review](review.md) has the moves.
- Several posts at one time: the same time unless the user asks otherwise.

## Always

- Never claim the same post will look the same everywhere: say what each network will show.
- A network whose account needs reconnecting: say so before writing for it ([connect](connect.md)).
