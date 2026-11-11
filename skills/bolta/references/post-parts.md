# Multi-part posts and first comments

A thread on X, a reply chain on Threads or Bluesky, or a Facebook post with a comment underneath: one post with several parts.

## Saving parts

- Only `bulk-create-posts` takes parts. Each item carries a nested `contents` list instead of `content`:
  `{"account_ids": [...], "status": "Draft", "contents": [{"content": "...", "index": 0}, {"content": "...", "index": 1, "media": [{"media_url": "https://...", "alt_text": "..."}]}]}`
- Media inside a part must use `media_url`. A `url` key there is dropped without a word.
- `create-post` has no parts. `update-post` changes part 1 only. To change a later part, save a new post with all parts and, after a yes, delete the old draft; or edit it in Bolta.
- Bolta spaces the parts itself; the gap between them can't be chosen.
- A batch item carries no `platform_specific` and no poll: set settings after, one `update-post` per post.

## What each network does with parts

- **X, Threads, Bluesky:** every part after the first goes out as a reply, whatever `post_type` says.
  - X: each part replies to the one before, **only once the post has an X setting saved**, which a batch never does: after it, set one (`reply_settings` is enough) with `update-post-platform-details`, or parts 2 onward go out as separate posts ([X](post-settings-x.md)). A failed part stops it.
  - Threads: each part replies to the first post, so they read as answers to it, not a chain. Only part 1's text past 500 characters is split into a chain of replies; a later part over 500 is cut short. For a long Threads thread, put all the text in one long first part.
  - Bluesky: each part replies to the one before.
- **Facebook:** part 2 and later become comments from the Page, a few seconds after the post, one image each. A comment that fails is skipped silently, so check the live post before saying the comment is there.
- Other networks: say nothing about what they do with extra parts. Write single-part posts for them.

## A Facebook first comment

- Parts are shared by every account on the post. A comment meant only for Facebook needs a post aimed only at the Page: use the Page's id from `list-accounts`.
- Save it as a Draft, show both parts, and say the second goes out as a comment. Never say it is live until the live post shows it.

## Reddit and Discord in a batch

An item aimed at Reddit or Discord is skipped before any post exists unless it carries the details:

- Reddit: `reddit_post_details: {"title": "...", "selected_subreddit_id": "..."}`, or `subreddit_name` in place of the id. Optional: `nsfw`, `spoiler`, `sendreplies`, `flair_id`, `flair_text`.
- Discord: `discord_post_details: {"selected_channel_id": "..."}`, or `channel_name`. Optional: `embed_enabled`, `embed_title`, `embed_description`.
- Names match only subreddits or channels already synced in Bolta. Never guess an id.

An item aimed straight at Instagram (not through an account group) with no media is refused.

## Reading what saved

- The `bulk-create-posts` reply lists refused items in `rejected`, each with a reason. Those posts don't exist.
- Poll `bulk-create-status` until `completed`. `skipped_count` and `skip_reasons` say how many were skipped and why; each item in `items` carries its own `reason` and `error`. Report `quality_blocked` too.
- Name every item that didn't save and what to add.

## Always

- Show every part in full, numbered, and say what each becomes: "part 2 goes out as a reply" or "as a comment from the Page".
- Count each part against its network's limit ([platforms](post-platforms.md)).
- Never promise a reply or comment is live without checking the published post.
