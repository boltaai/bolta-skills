# Threads settings

How to set and which wins: [network settings](post-settings.md). Network `threads`. Text: 500 characters; longer becomes a reply chain on its own.

## Settings

- **Own text**: `text`. Both, per account.
- **Topic**: `topic_tag`. Both, per account. Letters, numbers, spaces and underscores, up to 30 characters, not only digits; a leading `#` is dropped and `SmallBusiness` becomes `Small Business`. One per post. A tag breaking these rules is left off when it goes out, without an error.
  - In `platform_specific` the tag is enough. With `update-post-platform-details` also send `use_topic_tag: true`, or the tag is saved and not sent.
  - Guidance: the community people browse ("Small Business", "Coffee"), never the brand's own name. Not typed as a hashtag in the text.
- **Ghost post**: `is_ghost_post` true or false (default false). Both, per account. The post disappears after 24 hours. It works only on one text part with no image, video or poll; otherwise it goes out as a normal, lasting post.
  - Guidance: a flash sale, a code that expires today, a live moment ("we're on stage now"). Never for evergreen posts, announcements people will look for later, or anything with an image. Keep the link out: the point is the moment, and a ghost post must stay one short part.
- **Spoiler media**: `is_spoiler_media` true or false (default false). Both, per account. Blurs the post's images and videos until tapped; no effect on a text-only post.
  - Guidance: reveals, before-and-after, a finale, results people may not want to see yet.
- **Location**: `location_id`, a Threads place id the user gave. Both, per account. Never guess one.
- **Poll**: `create-post` `poll: {"options": ["A", "B"]}`, 2 to 4 options (extras and blanks are dropped; Bolta doesn't stop a 1-option poll, so always give 2 or more). Change it with `update-post` `poll`. Only on a text post: with media the poll is not sent. Never on a reply part.
  - Guidance: polls draw replies on Threads; ask something the audience has an opinion on, with short options. A batch item can't carry a poll: save it with `create-post`.

## Parts

From `bulk-create-posts` `contents` ([post parts](post-parts.md)). Each part replies to the first post; a later part over 500 is cut. For a long post, put all the text in one long first part.

## Saved, not sent yet

`reply_control` (who can reply: `everyone`, `mentioned` or `followers`): the tool's own example shows it, but it never reaches Threads. Don't offer it. `auto_publish` changes nothing for the user.

## Only in Bolta's web app

A text spoiler (hiding a phrase inside the text) is marked in Bolta's composer; plain text sent from here can't mark one.

## Not possible here

Choosing who can reply, quoting a Threads post, a ghost post with media.

## Always

- Say what each setting does to this post: "Threads: topic Small Business; it disappears 24 hours after it goes out."
- A ghost post is one short text part; say it disappears before the yes.
- Never invent a topic the user would not recognise, or a place id.
