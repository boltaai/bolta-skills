# Multi-part posts in a batch

Part of [post parts](post-parts.md): what a `bulk-create-posts` item needs, and how to read what saved.

## Reddit and Discord in a batch

An item aimed at Reddit or Discord is skipped (in `bulk-create-status`, not `rejected`) unless it carries the details:

- Reddit: `reddit_post_details: {"title": "...", "selected_subreddit_id": "..."}`, or `subreddit_name` in place of the id. Optional: `nsfw`, `spoiler`, `sendreplies`, `flair_id`, `flair_text`.
- Discord: `discord_post_details: {"selected_channel_id": "..."}`, or `channel_name`. Optional: `embed_enabled`, `embed_title`, `embed_description`.
- Names match only subreddits or channels already synced in Bolta. Never guess an id.

An item aimed straight at Instagram (not through an account group) with no media is refused.

## Reading what saved

- The `bulk-create-posts` reply lists refused items in `rejected`, each with a reason. Those posts don't exist.
- Poll `bulk-create-status` until `completed`. `skipped_count` and `skip_reasons` say how many were skipped and why; each item in `items` carries its own `reason` and `error`. Report `quality_blocked` too.
- Name every item that didn't save and what to add.

## Always

- Say the refused and skipped items in plain words, never as raw reasons.
- Never guess a subreddit or channel id.
