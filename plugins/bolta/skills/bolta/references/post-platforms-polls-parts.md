# Networks: polls and parts

Part of [networks: limits, media and settings](post-platforms.md), section 4.

- Polls: `poll: {"options": ["A", "B"]}` (2-4) on `save-post`, with no media, goes to Threads and X (on X each option 25 characters at most; never on an X thread) ([X](post-settings-x.md)).
- Threads on X, Threads and Bluesky, and Facebook comments: several parts in one post, `save-post` `parts` (media on part 1 only) or `bulk-create-posts` `contents`. An edit writes only the first part: [post parts](post-parts.md).

## Always

- Count each option and each part against its network's limit.
- Never put a poll on an X thread.
