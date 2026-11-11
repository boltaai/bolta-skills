# Network settings: how to set them and which wins

Every setting on every network, one page per network: [X](post-settings-x.md) · [Threads](post-settings-threads.md) · [Instagram](post-settings-instagram.md) · [Facebook](post-settings-facebook.md) · [LinkedIn](post-settings-linkedin.md) · [TikTok](post-settings-tiktok.md) · [YouTube](post-settings-youtube.md) · [Pinterest](post-settings-pinterest.md) · [Bluesky and Mastodon](post-settings-bluesky-mastodon.md) · [Reddit and Discord](post-settings-reddit-discord.md) · [WordPress](post-settings-wordpress.md). One post on several networks: [cross-posting](post-cross-posting.md).

## Three ways to set one

1. **`platform_specific`** on `create-post` or `update-post`: per network, and per account under `accounts` ([per network](post-per-network.md)). Settings land in the same call that saves the post.
2. **`update-post-platform-details`**: one network on a saved post, a flat `fields` object, shared by all that network's accounts. Bad choice values are refused with the allowed list; unknown keys are ignored with a success reply.
3. **Inside a `bulk-create-posts` item**: only `reddit_post_details` and `discord_post_details`. A batch item carries no `platform_specific` and no poll: save the batch, then `update-post` each post.

`get-post-platform-details` shows a network's current values and `allowed_values`. Read it before setting any choice (privacy, visibility, reply settings) and copy the exact spelling.

## Which wins

Each network page marks every key with how it can be set:

- **Both, per account**: read from `platform_specific` when the post goes out. The account's entry wins, then the network's, then what `update-post-platform-details` saved.
- **Both, network only**: `platform_specific` at network level is copied into the network's settings when the post is saved, so the last save wins (Instagram differs: [Instagram](post-settings-instagram.md)). An account entry for these is ignored. A later `update-post` that names this network copies its values again over a details change: set each key in one place. One bad value here (a misspelled Mastodon `visibility`) is dropped silently, with the networks after it in that call.
- **Details only**: `update-post-platform-details` (or the batch details). In `platform_specific` it is saved and never used.

Not working yet: on a post with no X settings saved, a `platform_specific` naming `x` creates none, so no X setting goes out, and the network-only keys of Mastodon, Bluesky, Reddit and Discord sent in that same call are skipped. Set X with `update-post-platform-details` first, and those networks' keys in their own call.

`platform_specific` values are not checked (Instagram skips bad ones). Send real `true` or `false`: the text "false" counts as true. A wrong TikTok privacy there goes out as the first level the account allows, usually public. For a choice field, prefer the details call, which refuses a bad value, or copy from `allowed_values`.

Unknown or misspelled keys are kept quietly and never used, either way. Read back before saying a setting is set.

## Approval

Any real change to text or a setting on an Approved or Scheduled post, by either route, sends it back to waiting for a yes and voids a client's yes. The reply carries `approval_reset`. Sending the same values again keeps the yes. Say so before changing: "Changing YouTube to public sends this scheduled post back for your yes."

## Not sent yet

Some settings are saved and shown in Bolta but never reach the network. Each page lists them under "Saved, not sent yet". Bolta is fixing these; until a page says otherwise, never offer them and say plainly they can't be set yet.

## Only in Bolta's web app

Removing or swapping media, a Threads text spoiler (a hidden span of text), Reddit promotion across several subreddits, repeating, auto-repost and auto-plug ([repeating](post-repeating.md)), and picking a Pinterest board or Discord channel from a list.

## Always

- Follow the house rules in the Bolta skill.
- Read back with `get-post-platform-details` or `get-post` before saying a setting is set.
- Never offer a setting listed as saved, not sent yet.
