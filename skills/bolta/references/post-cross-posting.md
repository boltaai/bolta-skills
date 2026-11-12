# One idea on several networks

How one post reaches many networks and accounts, and when to write separate posts instead. The keys: [per network](post-per-network.md) · [which keys, from where](post-per-network-keys.md) · [every setting](post-settings.md).

## How Bolta holds it

- **One post, many destinations**: every account in `account_ids` (or an account group in `social_buckets`). A Facebook Page is its own row (`facebook_page_<id>`), a LinkedIn company page too (`linkedin_org_<id>`): read `list-accounts` once and use those ids.
- **One text by default**: every destination gets the post's text and media.
- **Its own text per network**: `platform_specific` `<network>.text`. **Per account, Page or LinkedIn page**: `<network>.accounts.<id from list-accounts>.text`. The account's text wins over the network's, which wins over the post's.
- **Settings**: some can differ per account (LinkedIn visibility, TikTok privacy, YouTube title), others are one value for every account of that network (Instagram reel or story, Mastodon visibility, Bluesky languages), and some go only in the settings row, `save-post` `platform_details`, in the saving call or later (X quote or reply, subreddit, Discord channel). The table: [which keys, from where](post-per-network-keys.md).
- **Media, time and parts are shared** by every destination on the post.

## One post or several

- **One post** (the usual case): same media, same time, one part each. Per-network text and settings in one `save-post`. One yes covers every destination; results stay together.
- **Separate posts** when one network needs:
  - different media (Instagram a video, LinkedIn an image), or a different time,
  - extra parts (an X or Threads thread, a Facebook first comment) ([post parts](post-parts.md)),
  - a different Instagram format per account, or a TikTok, YouTube, Pinterest or WordPress caption of its own beyond its own field.
- Several separate posts: one `bulk-create-posts`, each item with its own `account_ids`. A batch item carries no `platform_specific` and no poll; after it completes, one `save-post` with `post_id` (and `platform_specific` or `platform_details`) per post. Reddit and Discord items carry their details inside.

## Writing each version

Checks before writing, and how to write each network's version fresh: [writing per network](post-cross-posting-writing.md).

## Changing it later

- `save-post` with `post_id`: `platform_specific` merges: send only the network or account that changes; `null` removes an entry, putting it back on the text above it.
- Any real change to text or settings on an Approved or Scheduled post sends it back for a yes; on a Scheduled post, any edit at all (`sent_back_for_review` in the result). Say so before changing it ([changes](post-changes.md)).

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
