# Network settings: how to set them and which wins

Every setting on every network, one page per network: [X](post-settings-x.md) · [Threads](post-settings-threads.md) · [Instagram](post-settings-instagram.md) · [Facebook](post-settings-facebook.md) · [LinkedIn](post-settings-linkedin.md) · [TikTok](post-settings-tiktok.md) · [YouTube](post-settings-youtube.md) · [Pinterest](post-settings-pinterest.md) · [Bluesky and Mastodon](post-settings-bluesky-mastodon.md) · [Reddit and Discord](post-settings-reddit-discord.md) · [WordPress](post-settings-wordpress.md). One post on several networks: [cross-posting](post-cross-posting.md). Approval, settings never sent, and what only the web app does: [approval and limits](post-settings-approval.md).

## Three ways to set one

1. **`save-post` `platform_specific`**, on a new post (no `post_id`) or an edit (`post_id`): per network, and per account under `accounts` ([per network](post-per-network.md)). Settings land in the same call that saves the post.
2. **`save-post` `platform_details`**: each network's settings row, `{"<network>": {"<field>": value}}`, shared by all that network's accounts. Several networks in one call. On a new post it can ride the creating call (no `post_id`) and is applied after the save; on a saved post send `post_id`. Bad choice values are refused with the allowed list; unknown keys are ignored with a success reply.
   - The result's `platform_details` reports each network (`ok`, or `error` with `details`). A refused network does not stop the others, and the post is still saved: read every network's entry, not just `ok` on the call. On a create, fix a refused network with `post_id` on the draft just made, never a second create.
3. **Inside a `bulk-create-posts` item**: only `reddit_post_details` and `discord_post_details`. A batch item carries no `platform_specific` and no poll: save the batch, then `save-post` with `post_id` for each post.

`get-post` with `post_id` and `platform: "<network>"` shows that network's current values, `allowed_values` and `not_sent_fields` (status `not_found` when nothing is saved yet). Read it before setting any choice (privacy, visibility, reply settings) and copy the exact spelling.

## Which wins

Each network page marks every key with how it can be set. "Details" means `save-post` `platform_details`:

- **Both, per account**: read from `platform_specific` when the post goes out. The account's entry wins, then the network's, then what `platform_details` saved. A later `platform_details` change rewrites any copy of the same setting in `platform_specific`, so its value wins.
- **Both, network only**: `platform_specific` at network level is copied into the network's settings when the post is saved, so the last save wins (Instagram differs: [Instagram](post-settings-instagram.md)). An account entry for these is ignored. One bad value here (a misspelled Mastodon `visibility`) is dropped silently for that network; the other networks in the call still save.
- **Details only**: `platform_details` (or the batch details). In `platform_specific` it is saved and never used.

`platform_specific` values are not checked (Instagram skips bad ones), except Threads `reply_control`: a bad one there refuses the whole call, naming it. Send real `true` or `false`: the text "false" counts as true. A wrong TikTok privacy there goes out as the first level the account allows, usually public. For a choice field, prefer `platform_details`, which refuses a bad value, or copy from `allowed_values`.

A saved setting the network can't take when the post goes out (a bad poll, an unknown Threads `reply_control` saved in Bolta, X image tags with no image) is left out and the post still goes out. Bolta records it on the post in `metadata.publish_setting_warnings` (`get-post`): read it when a setting didn't apply.

Unknown or misspelled keys are kept quietly and never used, either way. Read back before saying a setting is set.

## Always

- Follow the house rules in the Bolta skill.
- Read back with `get-post` (with `platform`, or the post's `metadata.platformSpecific`) before saying a setting is set.
- Never offer a setting listed as not sent.
