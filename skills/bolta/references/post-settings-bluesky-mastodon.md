# Bluesky and Mastodon settings

How to set and which wins: [network settings](post-settings.md). Apart from `text`, every key on both is network only: an account entry for it is ignored.

## Bluesky

Network `bluesky`. 300 characters; each part over that is cut to 297 and "...". Parts from a batch go out as a reply thread, each answering the one before ([post parts](post-parts.md)).

- **Own text**: `text`. Both, per account.
- **Languages**: `languages`, a list of language codes such as `["en"]` or `["en", "es"]`. Both, network only. Default: none set.
  - Guidance: set it when the post isn't in English, or mixes two languages, so people filtering their feeds by language see it. Name only languages actually in the post.
- **Tappable links and mentions**: `include_facets` (default true). Both, network only. Leave it on; hashtags stay plain text either way.

Saved, not sent yet: `reply_settings` (who can reply: `everyone`, `mentioned`, `nobody`). Don't offer it.

Not possible here: alt text (Bluesky always gets an empty one), choosing who can reply.

## Mastodon

Network `mastodon`. 500 characters, or the server's own limit; longer is cut. Extra parts are not posted: only part 1's text goes out. Write one part.

- **Own text**: `text`. Both, per account.
- **Who sees it**: `visibility` `public` (default), `unlisted` (not on public timelines, still public by link), `private` (followers only) or `direct` (only people mentioned). Both, network only.
  - Guidance: `unlisted` for routine updates that shouldn't flood local timelines; `private` for follower-only notes. `direct` is a private message; never for a brand post.
- **Content warning**: `sensitive: true` with `spoiler_text` (the warning shown, up to 255 characters). Both, network only. The post's text is hidden behind the warning until tapped; `sensitive` also hides media.
  - Guidance: Mastodon communities expect a warning for spoilers, politics, health topics and flashing images; a short plain label ("Spoiler: season finale"). Not for ordinary marketing.

Saved, not sent yet: `language`, `poll_options`, `poll_expires_in`, `poll_multiple`, `poll_hide_totals` (polls), `in_reply_to_id`. Bolta's composer shows some; none reaches Mastodon. Don't offer them.

Not possible here: polls, alt text (images go up without a description), replying to a post, choosing the post's language.

## Always

- Say the setting in plain words: "Mastodon: unlisted, behind the warning 'Spoiler: finale'."
- Never offer a Mastodon poll or language, or Bluesky reply settings.
- Language codes only for languages in the post.
