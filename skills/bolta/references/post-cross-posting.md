# One idea on several networks

How one post reaches many networks and accounts, and when to write separate posts instead. The keys: [per network](post-per-network.md) · [which keys, from where](post-per-network-keys.md) · [every setting](post-settings.md).

## How Bolta holds it

- **One post, many destinations**: every account in `account_ids` (or an account group in `social_buckets`). A Facebook Page is its own row (`facebook_page_<id>`), a LinkedIn company page too (`linkedin_org_<id>`): read `list-accounts` once and use those ids.
- **One text by default**: every destination gets the post's text and media.
- **Its own text per network**: `platform_specific` `<network>.text`. **Per account, Page or LinkedIn page**: `<network>.accounts.<id from list-accounts>.text`. The account's text wins over the network's, which wins over the post's.
- **Settings**: some can differ per account (X reply settings, LinkedIn visibility, TikTok privacy, YouTube title), others are one value for every account of that network (Instagram reel or story, Mastodon visibility, Bluesky languages, an X poll), and some need `update-post-platform-details` (subreddit, Discord channel, X quote). The table: [which keys, from where](post-per-network-keys.md).
- **Media, time and parts are shared** by every destination on the post.

## One post or several

- **One post** (the usual case): same media, same time, one part each. Per-network text and settings in one `create-post`. One yes covers every destination; results stay together.
- **Separate posts** when one network needs:
  - different media (Instagram a video, LinkedIn an image), or a different time,
  - extra parts (an X or Threads thread, a Facebook first comment) ([post parts](post-parts.md)),
  - a different Instagram format per account, or a TikTok, YouTube, Pinterest or WordPress caption of its own beyond its own field.
- Several separate posts: one `bulk-create-posts`, each item with its own `account_ids`. A batch item carries no `platform_specific` and no poll; after it completes, `update-post` (or `update-post-platform-details`) each post. Reddit and Discord items carry their details inside.

## Before writing

1. `get-posting-rules` for every network named: limits, media needed, what must be set.
2. Check each network against the media the user has; name any that would fail and why: "TikTok needs a video; skip it, or do you have one?"
3. Pick a shape per network: LinkedIn a short story, X one line, Threads conversational, Instagram the caption, Reddit what fits the subreddit.

## Writing

- Write each version fresh: same point, different first line; never paste one and trim it. Count each against its own limit.
- Leave out networks that don't fit, and say so once: "Skipped Pinterest: no image."
- Guidance: per-Page text for agencies and multi-location brands, so each Page sounds local; a founder's profile in "I", the company page in "we".

## Changing it later

- `update-post` `platform_specific` merges: send only the network or account that changes; `null` removes an entry, putting it back on the text above it.
- Any real change to text or settings on an Approved or Scheduled post sends it back for a yes. Say so before changing it.

## Showing it

Number every destination with its account, full text and settings in plain words:

> 1. LinkedIn, you: (full text)
> 2. LinkedIn, Acme company page: (full text)
> 3. X, @acme: (full text). Replies: accounts you follow.

End as the post playbook says: saved as drafts, nothing goes out yet. One post takes one yes; separate posts can share one message ("all three yes").

## Always

- Never claim the same post will look the same everywhere: say what each destination gets.
- A network whose account needs reconnecting: say so before writing for it ([connect](connect.md)).
- Ids only from `list-accounts`.
