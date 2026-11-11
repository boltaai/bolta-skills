# One idea on several networks

How a post reaches several networks, and when to write separate posts instead.

## How Bolta holds it

- One post can go to many accounts: list them all in `account_ids` (or an account group in `social_buckets`). Without more, every account gets the same text and media.
- One post can also carry its own text per network, and per Facebook Page or LinkedIn page: `platform_specific` on `create-post` ([per network](post-per-network.md)). Settings can differ per account the same way.
- So, pick one:
  - **Same media, same time, one part each** (the usual case): one post, a fresh `text` per network in `platform_specific`. One yes covers it; results stay together. Count each text against its own network's limit.
  - **Different media or times, or extra parts on one network** (an X or Threads thread, a Facebook first comment): one post per network, saved together with one `bulk-create-posts`, each item with its own `account_ids`. A Reddit or Discord item carries its details inside it ([post parts](post-parts.md)).
  - **TikTok, YouTube, Pinterest or WordPress** with its own words: these ignore `text`. Give it its own post, or use its own field (`video_description`, `description`).
- Parts are shared by every account on a post ([post parts](post-parts.md)).

## Before writing

1. Read `get-posting-rules` for every network named: limits, media needed, what must be set.
2. Check each network against the media the user has. Name any that would fail and why before writing: "TikTok needs a video; skip it, or do you have one?"
3. Pick a shape per network: LinkedIn a short story, X one line or a short thread, Threads conversational with one topic, Instagram the caption under an image, Bluesky plain and short, Reddit a title and a post that fits the subreddit's rules.

## Writing

- Write each version fresh. Same point, different first line; never paste one and trim it.
- Leave out networks that don't fit, and say so once: "Skipped Pinterest: no image."
- Settings go in the same `platform_specific` ([keys](post-per-network-keys.md)). For separate posts, or keys that need Bolta's ids (subreddit, channel, board): one `update-post-platform-details` per post and network ([Threads, Instagram, Facebook](post-networks-meta.md) · [X, LinkedIn, Bluesky, Mastodon, Reddit, Discord](post-networks-text.md) · [TikTok, YouTube, Pinterest](post-networks-video.md)).

## Showing it

Number every destination with its network and account, its full text, and any settings in plain words, whether it is one post or several:

> 1. LinkedIn, Acme: (full text)
> 2. Threads, @acme: (full text). Topic: Small Business.
> 3. Instagram, @acme: (full text). A Reel, with the video you sent.

End as the post playbook says: saved as drafts, nothing goes out yet.

## When they say yes

- One post with per-network text takes one yes. Separate posts are approved, scheduled or posted on their own; one message can cover all ("all three yes"). [review](review.md) has the moves.
- Several posts at one time: the same time unless the user asks otherwise.

## Always

- Never claim the same post will look the same everywhere: say what each network will show.
- A network whose account needs reconnecting: say so before writing for it ([connect](connect.md)).
