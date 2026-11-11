# TikTok settings

How to set and which wins: [network settings](post-settings.md). Network `tiktok`. Needs one video (a public https link); photo posts aren't supported. The post's text is the caption, up to 2,200 characters; longer is cut. A `text` in `platform_specific` is ignored here.

**Per-account entries replace, not merge**: an account with its own entry under `tiktok.accounts` uses only that entry, so repeat every TikTok setting it needs there. Where an entry or the network level lacks a key, Bolta falls back to what `update-post-platform-details` saved.

## Settings

- **Who sees it**: `privacy_level` `PUBLIC_TO_EVERYONE` (default), `MUTUAL_FOLLOW_FRIEND`, `FOLLOWER_OF_CREATOR` or `SELF_ONLY`. Both, per account.
  - If the account doesn't allow the level chosen, TikTok's first allowed level is used instead, which is usually public. Bolta says nothing.
  - Set it with `update-post-platform-details`, which refuses a misspelled level. In `platform_specific` a misspelling is kept and becomes that first allowed level at publish.
  - The user didn't say? Ask; never assume public. `SELF_ONLY` is the way to put a video up for a client or teammate to check in the app first.
- **Comments**: `disable_comments` true or false (default false). Both, per account.
- **Duet and stitch**: `disable_duet`, `disable_stitch` true or false (default false: allowed). Both, per account.
  - Guidance: keep duets and stitches on for trend, challenge and how-to content, since they spread it. Turn them off for a client testimonial, a person's face used with permission, or anything that could be remixed against the brand.
- **Promotes the user's own business**: `brand_organic_toggle: true`. `platform_specific` only.
- **Paid partnership or sponsored**: `brand_content_toggle: true`. `platform_specific` only. TikTok labels the video as branded content. It can't be private: with `SELF_ONLY` the label is dropped.
  - Guidance: TikTok asks creators to disclose promotion; when a video promotes a product, service or offer, ask which applies (own business, a paid partner, or neither) and set it before the yes; never decide for the user that no disclosure is needed. Both can be on.
  - `update-post-platform-details` can't set these two: it answers success and keeps nothing. Read back with `get-post` (`metadata.platformSpecific.tiktok`).

## Not possible here

An AI-generated content label, photo or carousel posts, sounds or music, a cover frame, a different caption from the post's text (give TikTok its own post).

`post` (the post the settings belong to) is Bolta's own; never send it.

## Always

- Name the privacy before the yes: "TikTok: public to everyone, comments on."
- Ask about paid or brand disclosure on any video that sells something.
- Read back the settings before saying they're set.
