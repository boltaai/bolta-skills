# X settings

How to set and which wins: [network settings](post-settings.md). Network `x`. Text: 280 characters (more on Premium accounts); longer is refused at approval.

**Set X settings with `update-post-platform-details`.** Nothing but text and images reaches X until the post has X settings saved, and on a new post `platform_specific` saves none (its `text` still works). After one details call, `platform_specific` works for the keys marked both.

## Settings

- **Own text**: `text`. Both, per account. Replaces the post's text on X, first part only.
- **Who can reply**: `reply_settings` `everyone` (default), `mentioned_users` or `followers` (on X this means accounts the brand follows). Both, per account.
  - Guidance: `followers` on a launch, price change or anything likely to draw spam or a pile-on; `mentioned_users` for a post addressed to named partners. Leave `everyone` on posts meant to start conversation.
- **Subscribers only**: `for_super_followers_only` true or false (default false). Both, per account. Only for accounts that sell X subscriptions.
- **Poll**: `post_type: "POLL"` with `poll_options` (2 to 4 options, each 1 to 25 characters) and `poll_duration_minutes` (5 to 10,080; default 1,440, one day). Both, network only. Without `post_type` POLL the options are not sent.
  - The details call refuses a bad option or duration with the reason. In `platform_specific` a bad poll is dropped without a word.
  - `create-post` `poll` is for Threads only; X ignores it.
  - Guidance: a poll for a real choice the brand will act on; one day for quick pulse checks, up to 7 days for a decision.
- **Quote a post**: `quoted_tweet_id`, the number at the end of a post link the user gave. Details only.
  - Guidance: quote to add the brand's take on a customer's or press post; a bare repost isn't possible here.
- **Reply to a post**: `in_reply_to_tweet_id`, same kind of id. Details only. For answering a specific post as the brand, not for starting a conversation.
- **Place**: `geo_place_id`, an X place id the user gave. Details only. Never look one up or guess.
- `post_type` takes `TEXT`, `MEDIA`, `POLL`, `QUOTE`, `REPLY`, `THREAD`; only `POLL` changes what goes out.

## Threads on X

- Parts come only from `bulk-create-posts` `contents` ([post parts](post-parts.md)). They chain as replies **only when the post has X settings saved**: a batch never makes them, so follow with one X setting (for example `reply_settings`) by `update-post-platform-details`. Without it, parts 2 onward go out as separate posts.
- A part that fails stops the thread; the parts already out stay up and nothing retries. Say so and point to the post in Bolta.
- In a thread a poll is dropped, a quote repeats on every part, and `in_reply_to_tweet_id` is replaced by the part before.
- Guidance: 3 to 6 parts that each stand alone; the hook in part 1, a link in the last part.

## Saved, not sent yet

`media_tagged_user_ids` (tagging people in images), `auto_publish`, `is_thread`, `thread_position`. Don't offer them.

## Not possible here

Video or GIF (images only; a video fails when it goes out), media with no text (refused at scheduling), Communities, editing a later part of a thread, a repost without comment.

## Always

- Ids (quoted post, reply, place) only from a link or id the user gave.
- Say every setting in plain words: "X: only accounts you follow can reply."
- A thread needs one X setting saved after the batch, or it goes out as separate posts.
