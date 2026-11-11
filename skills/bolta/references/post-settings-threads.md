# Threads settings

How to set and which wins: [network settings](post-settings.md). Network `threads`. Text: 500 characters; a longer first part is split into a reply chain.

Bolta removes everything after a `?` or `#` in each Threads link (tracking tags are lost; say so), and skips a post whose first 100 characters match one the account posted in the last 30 minutes, while reporting success.

## Settings

- **Own text**: `text`. Both, per account.
- **Topic**: `topic_tag`. Both, per account. English letters, numbers, spaces and underscores (no accents, hyphens, emoji, `.` or `&`), up to 30 characters, not only digits; a leading `#` is dropped. One per post. A tag breaking these rules is left off silently.
  - In `platform_specific` the tag is enough. With `update-post-platform-details` also send `use_topic_tag: true`, or the tag is saved and not sent.
  - Guidance: the community people browse ("Small Business", "Coffee"), never the brand's name. Not a hashtag in the text.
- **Ghost post**: `is_ghost_post` true or false (default false). Both, per account. The post disappears after 24 hours. Only on one text part of 500 characters or fewer with no image, video or poll; otherwise it goes out as a normal, lasting post, without an error.
  - Guidance: a flash sale, a code that expires today, a live moment. Never for evergreen posts or announcements people will look for later.
- **Spoiler media**: `is_spoiler_media` true or false (default false). Both, per account. Blurs the first part's images and videos until tapped; no effect on a text-only post.
  - Guidance: reveals, before-and-after, a finale.
- **Who can reply**: `reply_control` `everyone` (default), `followers` (only the brand's followers) or `mentioned` (only accounts tagged in the post). Both, per account. Use these words, not Threads' `followers_only` or `mentioned_only`.
  - "Only accounts we follow" is Threads' `accounts_you_follow`: `platform_specific` only, in a call naming only `threads` (a Threads-only save, or `update-post` after saving). Bolta can't keep it as a saved setting, so in a bigger call later networks' settings are lost, and `get-post-platform-details` still shows `everyone`: read it back in `get-post` (`metadata.platformSpecific`).
  - Guidance: limit replies on a post likely to draw spam; keep `everyone` to start conversation.
- **Location**: `location_id`, a Threads place id (digits only) the user gave. Both, per account. A bad one is left off silently. Never guess one.
- **Poll**: `create-post` `poll: {"options": ["A", "B"]}`, 2 to 4 options (extras and blanks are dropped; always give 2 or more). Change it with `update-post` `poll`. Only on a text post: with media the poll is not sent.
  - Guidance: polls draw replies on Threads; ask something the audience has an opinion on, with short options. A batch item can't carry a poll: save it with `create-post`. The same `poll` goes to X if the post is there too (X's limits apply: [X](post-settings-x.md)).

## Parts

From `bulk-create-posts` `contents` ([post parts](post-parts.md)). Each part replies to the first post; a later part over 500 is cut. For a long post, put all the text in part 1. A reply that fails is not retried: the post shows as partly published.

`auto_publish` changes nothing; leave it out.

## Only in Bolta's web app

A text spoiler (hiding a phrase inside the text).

## Not possible here

Quoting a Threads post, a ghost post with media.

## Always

- Say what each setting does to this post: "Threads: topic Small Business; it disappears 24 hours after it goes out."
- A ghost post is one short text part; say it disappears before the yes.
- Never invent a topic the user would not recognise, or a place id.
