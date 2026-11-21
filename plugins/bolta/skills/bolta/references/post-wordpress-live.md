# WordPress: the date, the featured image and a live article

Part of [WordPress articles](post-wordpress.md). The article comes first: optional fields (search details, excerpt, categories, an image) never hold back a publish the user asked for.

## The date the article shows

- `publication_date` on `create-wordpress-blog-post`, only when the user named a date: `"2024-03-05"` or `"2024-03-05T09:30"`, in the WordPress site's own clock (not the brand's), no Z, no offset. A date alone is stored as 12:00 site time.
- It must be now or earlier on the site: a future date is refused (`PUBLICATION_DATE_IN_FUTURE`). `SITE_TIMEZONE_UNAVAILABLE`: Bolta couldn't read the site's clock and the date is too recent to be safe; ask for an older date or leave it out.
- It is not when Bolta sends the article: that is `scheduled_time` (or `publish-post` `when`). An old article published today: publish now with `publication_date`.

## The featured image

- `featured_image_required` defaults to false: the hero is best effort. If it fails to upload, the article still goes out without it and the result says why (`publish_warnings`, stage `featured_media_upload`).
- True only when the user said the article must not go out without that image; then an image failure fails the publish.
- Where an image can come from: [media](post-media.md). A Bolta Library upload is not a WordPress attachment: the site's own copy is `wordpress_media_id`, set only when WordPress confirms it.

## Reporting what happened

Three answers, each from its own confirmed field:

- **Published:** only when `published` is true, or `get-post` says Published, with the link. `publication_state` `publishing_queued` (Queued, Processing), `scheduled`, `draft` or `awaiting_approval` (Pending Approval) is not published: say which.
- **Date:** `publication_date_confirmed` true, with the date WordPress returned. False: say the site shows another date.
- **Image:** `featured_media_confirmed` true, or that media item's `status` `confirmed_attached`. `uploaded_to_bolta` (kept in Bolta only) or `uploaded_to_wordpress` (on the site): not attached. `failed`: its `stage` and `reason`. Never say the theme shows it.
- Publishing runs in the background: check one article with `get-post` and its `post_id`, never by listing posts. Its date and image afterwards: `get-post` with `platform: "wordpress"`, `seo_metadata.publish_confirmation` (`featured_media_confirmed`, `publication_date.confirmed`, `warnings`); `featured_media_id` is set only once WordPress confirmed it.

## Changing an article already live

- `save-post` refuses a published post. `update-wordpress-article` with `post_id` edits the same article at the same address, never a new one; never pass a WordPress post number.
- Pass only what changes: `title` (the address stays), `content` (the WHOLE new body, Markdown), `publication_date`, `featured_image` (`{"url": "https://...", "alt_text": "..."}`). Everything else stays as it is.
- Lengthening or rewriting: `get-post` the body, write the whole new one, show it, send after the yes. No `# ` title line; never the featured image in the body; keep an inline image as a Markdown image.
- It needs the yes that publishing needs ([whose yes](review-authority.md)) and passes `publish-post`'s checks. A refusal (`approval_required`, Safe Mode, client sign-off, not published) is final: say why.
- Read back: `title.status`, `content.status` (`confirmed`, with `content.word_count`), `publication_date.confirmed`, `featured_image.status` (`failed` keeps the old image), `preserved` (false: say WordPress changed it). Give the `link`; `link_changed` true: give `previous_link` too.
- `retryable` true (no readback, or `bolta_sync.status` `failed`): call again with the same input. It never makes a second article.

## Which number is which

Keep them apart: `post_id` (Bolta's post), `wordpress_post_id` (the site's post), `wordpress_media_id` (the site's image), a Library media id, a chat file's `file_id`. The settings row `get-post` with `platform` returns is not a post: its id is never a `post_id`.

## Always

- Follow the house rules in the Bolta skill.
- Report published, date and image separately, each from its confirmed field.
