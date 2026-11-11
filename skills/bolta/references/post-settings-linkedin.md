# LinkedIn settings

How to set and which wins: [network settings](post-settings.md). Network `linkedin`. Up to 3,000 characters; longer is refused at approval. A few hashtags at the end, at most.

## Profile or company page

- **By account id (preferred)**: `list-accounts` shows each company page as its own row, id `linkedin_org_<id>` with `is_organization`. Put it in `create-post` `account_ids`. The profile's id plus a page id posts to both. Several page ids: the first is the main page, the rest get the same post. Pages under different LinkedIn logins need separate posts.
- Save it as a draft first, then schedule or publish as a second call.
- **By setting**: `post_as_organization: true` with `selected_organization` set to the row's `organization_id` (a long id with dashes, never the number in `linkedin_org_`). Details only. Send both: `post_as_organization` alone posts to the personal profile.
- **Also on other pages**: `cross_post_organizations`, a list of `organization_id` values, with `cross_post_enabled: true`. Details only. Each page gets the post at the same time.
- No profile row means the profile is hidden for this brand: don't offer "the personal one". A post aimed at it with no page fails.
- Guidance: company news, hiring and product posts on the page; opinions, lessons and "I" stories on the founder's profile, often both in one post with different text.

## Settings

- **Own text**: `text` for LinkedIn, or under `linkedin.accounts` keyed by `linkedin_org_<id>` or the profile's account id. Both, per account. A page without its own entry gets the LinkedIn `text`, else the main text, never the profile's own text. Pages added by `cross_post_organizations` follow the same rule.
- **Who sees it**: `visibility` `PUBLIC` (default) or `CONNECTIONS`. Both, per account. `platform_specific` sends whatever is typed, so copy the exact capitals; the details call refuses a wrong value.
  - Guidance: `CONNECTIONS` only on a profile post meant for the person's own network (a personal ask, a job search). A company page post stays `PUBLIC`.
- `post_type` takes `TEXT`, `IMAGE`, `VIDEO`, `ARTICLE`, `DOCUMENT`, `POLL`; it only checks media is attached for `IMAGE` and `VIDEO`. It does not make a document or poll.
- **Media**: up to 20 images, or one video (a GIF counts as the video). Alt text is not sent.
- **Extra parts**: the text of part 2 onward is dropped. Write one part.
- The 3,000 check at approval doesn't read a company page's own `text`: count that one yourself.

## Saved, not sent yet

`enable_comments`, `enable_resharing` (resharing is always allowed), `include_hashtags`, `tag_connections`, `linkedin_specific_content`, `location`, `feeling`, `activity`, `cross_post_delay` (pages all post at once). Don't offer them.

## Not possible here

Document or PDF carousels, polls, a first comment, tagging people or pages so they're notified, LinkedIn articles or newsletters, Groups, a delay between pages.

## Always

- Page ids only from `list-accounts`; never guess one.
- Name every destination and its own text before the yes.
- Say which pages get the post: "LinkedIn: your profile and the Acme company page."
