# Multi-part posts and first comments

A thread on X, a reply chain on Threads or Bluesky, or a Facebook post with a comment underneath: one post with several parts.

## Saving parts

- One multi-part post: `save-post` with `parts`, an array of strings in order, instead of `content`: `{"parts": ["Part 1 text", "Part 2 text"], "account_ids": [...]}`. A `poll` goes on the first part (never on an X thread). `media_urls` (a link) goes on the first part only: `save-post` has no media per part.
- Media on a later part: `bulk-create-posts`, where each item carries a nested `contents` list instead of `content`:
  `{"account_ids": [...], "status": "Draft", "contents": [{"content": "...", "index": 0}, {"content": "...", "index": 1, "media": [{"media_url": "https://...", "alt_text": "..."}]}]}`. Or the user adds it to that part in Bolta.
- Media inside a part must use `media_url`. A `url` key there is dropped silently.
- `save-post` with `post_id` changes part 1 only (its `content`). To change a later part, save a new post with all parts and, after a yes, delete the old draft; or edit it in Bolta.
- The gap between parts can't be chosen.
- A batch item carries no `platform_specific` and no poll: set settings after, one `save-post` with `post_id` per post. A single `save-post` with `parts` takes them in the same call.

## What each network does with parts

- **X, Threads, Bluesky:** every part after the first goes out as a reply, whatever `post_type` says.
  - X: each part replies to the one before ([X](post-settings-x.md)). A failed part stops it.
  - Threads: each part replies to the first post, so they read as answers to it, not a chain. Only part 1's text past 500 characters is split into a chain of replies; a later part over 500 is cut short. For a long Threads thread, put all the text in one long first part.
  - Bluesky: each part replies to the one before.
- **Facebook:** part 2 and later become comments from the Page, a few seconds after the post, one image each. A comment that fails is skipped silently, so check the live post before saying the comment is there.
- **LinkedIn, Mastodon:** only part 1's text goes out. **Reddit, Discord:** parts are joined. Write single-part posts for these and every other network.

## A Facebook first comment

- Parts are shared by every account on the post. A comment meant only for Facebook needs a post aimed only at the Page: use the Page's id from `list-accounts`.
- Save it as a Draft, show both parts, and say the second goes out as a comment. Never say it is live until the live post shows it.

## Reddit, Discord and what saved in a batch

Which details a Reddit or Discord item needs, and how to read what a batch saved: [batch parts](post-parts-batch.md).

## Always

- Show every part in full, numbered, and say what each becomes: "part 2 goes out as a reply" or "as a comment from the Page".
- Count each part against its network's limit ([platforms](post-platforms.md)).
- Never promise a reply or comment is live without checking the published post.
