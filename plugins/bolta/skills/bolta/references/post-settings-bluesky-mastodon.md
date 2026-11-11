# Bluesky and Mastodon settings

How to set and which wins: [network settings](post-settings.md). Apart from `text`, every key on both is network only: an account entry for it is ignored.

## Bluesky

Network `bluesky`. 300 characters; each part over that is cut to 297 and "...". Parts from a batch go out as a reply thread, each answering the one before ([post parts](post-parts.md)).

- **Own text**: `text`. Both, per account.
- **Languages**: `languages`, a list of language codes such as `["en"]` or `["en", "es"]`. Both, network only. Default: none set.
  - Guidance: set it when the post isn't in English, or mixes two languages, so people filtering their feeds by language see it. Name only languages actually in the post.
- **Tappable links and mentions**: `include_facets` (default true). Both, network only. Leave it on; hashtags stay plain text either way.

Alt text: each image's `alt_text` is sent ([media](post-media.md)).

Not sent: `reply_settings` (who can reply: `everyone`, `mentioned`, `nobody`). Bolta refuses it; choosing who can reply isn't possible here.

## Mastodon

Network `mastodon`. 500 characters, or the server's own limit; longer is cut. Extra parts are not posted: only part 1's text goes out. Write one part.

- **Own text**: `text`. Both, per account.
- **Who sees it**: `visibility` `public` (default), `unlisted` (not on public timelines, still public by link), `private` (followers only) or `direct` (only people mentioned). Both, network only.
  - Guidance: `unlisted` for routine updates that shouldn't flood local timelines; `private` for follower-only notes. `direct` is a private message; never for a brand post.
- **Content warning**: `sensitive: true` with `spoiler_text` (the warning shown, up to 255 characters). Both, network only. The post's text is hidden behind the warning until tapped; `sensitive` also hides media.
  - Guidance: Mastodon communities expect a warning for spoilers, politics, health topics and flashing images; a short plain label ("Spoiler: season finale"). Not for ordinary marketing.

- **Language**: `language`, one two-letter code such as `"en"` or `"de"`. Both, network only. Set it when the post isn't in the account's usual language.
- **Poll**: `poll_options` (a list, 2 or more), `poll_expires_in` in seconds (300 to about a month; default 86,400, one day), `poll_multiple` (several answers), `poll_hide_totals` (results hidden until it ends). Both, network only. Never with images or video: Bolta refuses that, and a poll saved with media goes out without the poll.
  - Guidance: a real choice the audience cares about; a day or two is plenty.
- **Reply to a post**: `in_reply_to_id`, the id of a Mastodon post the user linked. Both, network only. Never guess one.

Not possible here: alt text (images go up without a description).

## Always

- Say the setting in plain words: "Mastodon: unlisted, behind the warning 'Spoiler: finale'."
- Never offer Bluesky reply settings; never a Mastodon poll with media.
- Language codes only for languages in the post.
