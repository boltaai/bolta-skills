# X settings

How to set and which wins: [network settings](post-settings.md). Network `x`. Text: 280 characters (more on Premium accounts); longer is refused at approval.

Set X on the saving call: `platform_specific` `{"x": {...}}` on `create-post` works for every key marked both, on a new post too. Keys marked details only take `update-post-platform-details` after the save.

## Settings

- **Own text**: `text`. Both, per account. Replaces the post's text on X, first part only.
- **Who can reply**: `reply_settings` `everyone` (default), `mentioned_users` or `followers` (on X this means accounts the brand follows). Both, per account.
  - Guidance: `followers` on a launch, price change or anything likely to draw spam or a pile-on; `mentioned_users` for a post addressed to named partners. Leave `everyone` on posts meant to start conversation.
- **Subscribers only**: `for_super_followers_only` true or false (default false). Both, per account. Only for accounts that sell X subscriptions.
- **Poll**: `create-post` `poll: {"options": ["A", "B"]}` (the same poll goes to Threads if the post is there too), or `post_type: "POLL"` with `poll_options` and `poll_duration_minutes` (both, network only; without `post_type` POLL the options are not sent). 2 to 4 options, each 1 to 25 characters; 5 to 10,080 minutes (default 1,440, one day).
  - `create-post` and the details call refuse a bad poll with the reason. In `platform_specific` a bad one is left out when the post goes out.
  - Guidance: a poll for a real choice the brand will act on; one day for quick pulse checks, up to 7 days for a decision.
- **Quote a post**: `quoted_tweet_id`, the number at the end of a post link the user gave. Details only.
  - Guidance: quote to add the brand's take on a customer's or press post; a bare repost isn't possible here.
- **Reply to a post**: `in_reply_to_tweet_id`, same kind of id. Details only. For answering a specific post as the brand, not for starting a conversation.
- **Place**: `geo_place_id`, an X place id the user gave. Details only. Never look one up or guess.
- **Tag people in the images**: `media_tagged_user_ids`, up to 10 numeric X user ids the user gave (not @handles). Details only; only on a post with images, never on a thread.
- `post_type` takes `TEXT`, `MEDIA`, `POLL`, `QUOTE`, `REPLY`, `THREAD`; only `POLL` changes what goes out.

## Threads on X

- Parts come only from `bulk-create-posts` `contents` ([post parts](post-parts.md)); each part replies to the one before.
- A part that fails stops the thread; the parts already out stay up and nothing retries. Say so and point to the post in Bolta.
- A thread takes no poll (refused) and no image tags. A quote repeats on every part, and `in_reply_to_tweet_id` is replaced by the part before.
- Guidance: 3 to 6 parts that each stand alone; the hook in part 1, a link in the last part.

## Not sent

`auto_publish`: Bolta refuses it. `is_thread` and `thread_position` are Bolta's own; never send them.

## Not possible here

Video or GIF (images only; a video fails when it goes out), media with no text (refused at scheduling), Communities, editing a later part of a thread, a repost without comment.

## Always

- Ids (quoted post, reply, place) only from a link or id the user gave.
- Say every setting in plain words: "X: only accounts you follow can reply."
- Tag people only by numeric ids the user gave.
