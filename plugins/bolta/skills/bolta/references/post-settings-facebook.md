# Facebook settings

How to set and which wins: [network settings](post-settings.md). Network `facebook`. Bolta posts to Facebook Pages, never to a personal profile.

## Which Page

- **By account id (preferred)**: `list-accounts` lists each Page as its own row, id `facebook_page_<id>` with `is_page`; `is_primary` marks the default Page. Put the ids in `create-post` `account_ids`. Several Page ids: the first is the main Page, the rest get the same post.
- **By setting**: `primary_page` plus `cross_post_pages` with `cross_post_enabled: true`. Details only, and they take Bolta's internal Page ids, which only `get-post-platform-details` shows. Use only to change Pages on a saved post.
- No Page chosen: Bolta uses the brand's first Page, which may be the wrong one. Always name the Page before the yes.
- Save a Page post as a draft first; schedule or publish is a second call.

## Settings

- **Own text per Page**: `text` in `platform_specific` `facebook` (all Pages) or under `facebook.accounts` keyed by the `facebook_page_<id>` (one Page). Both, per account. Bolta stores the key as the Page's name; a read back shows the name.
  - Guidance: an agency posting the same news to several local Pages gives each Page its own line ("our Lisbon team...") in one post, so one yes covers all.
- **First comment**: part 2 of a post saved with `bulk-create-posts` `contents` goes out as a comment from the Page, one image at most ([post parts](post-parts.md)). Parts are shared by every account on the post, so a Facebook-only comment needs a post aimed only at the Page.
  - Guidance: put the link in the first comment when the post should read as a story, not an ad. A comment that fails is skipped silently: check the live post before saying it is there.
- **Media**: text alone, one video, or images. A video with images, or two videos, is refused at schedule. Alt text is not sent to Facebook.

## Saved, not sent yet

`privacy` (`EVERYONE`, `FRIENDS`, `FRIENDS_OF_FRIENDS`, `CUSTOM`), `post_type` (`TEXT`, `PHOTO`, `VIDEO`, `LINK`, `STORY`), `enable_comments`, `enable_sharing`, `enable_reactions`, `cross_post_delay`, `location`, `feeling`, `activity`. Bolta's composer shows some of them; none reaches Facebook. Don't offer them.

## Not possible here

Reels, Stories, posting to a personal profile or a Group, events, tagging people or Pages, boosting, a delay between Pages.

## Always

- Page ids only from `list-accounts`; never a Page name in place of an id.
- Name every Page and the text it gets before the yes.
- Never say a first comment is live without checking the live post.
