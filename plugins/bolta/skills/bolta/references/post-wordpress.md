# WordPress articles

Bolta facts only. Write the article as usual.

- **Saving:** `create-wordpress-blog-post` with `title`, Markdown `content`, `seo` and an `idempotency_key`. With no `requested_action` it saves a draft, no check. `requested_action: "publish"` (or `"schedule"` with `scheduled_time`) only on a yes that covers it: to the saved draft, or to the whole task ("write and publish this article") ([whose yes](review-authority.md)). Asked to send it for review? `requested_action: "submit_for_review"`. A date the article should show, its featured image, what to report: [the live article](post-wordpress-live.md).
- **No WordPress connected** (`wordpress_connection_required`): offer the article as text, and send a `get-connect-link` with no platform: on that page the user opens View More, then WordPress (site address, username and an application password). Or Settings > Integrations > WordPress in Bolta. Never ask for passwords in chat. Several sites: the reply lists them; ask which, then resend with `wordpress_account_id`.
- **Markdown:** tables don't convert (rows run together), nested lists flatten and fenced code blocks come out mangled; the rest of basic Markdown converts. The title is the page heading: start the body with the introduction and use `##` for sections.
- **Address:** `slug` on this tool sets it (short, lowercase, the main search words); without one it comes from the title. Change it later with `save-post` `post_id` and `platform_specific` `{"wordpress": {"slug": "..."}}` ([settings](post-settings-wordpress.md)). Leave out `content_format`.
- **Categories and tags** are names; a new one is created on the live site at publish, so match existing spelling.
- **Search details:** `seo.meta_title` (defaults to the title) and `seo.meta_description` are sent at publish as post meta keys `title` and `description`; WordPress keeps them only if the site registers those keys (SEO plugins such as Yoast use their own), so never promise they show in search results. Keep them under 60 and 160 characters; longer is sent, with a warning in `seo_validation`. Other `seo` fields are never sent; only `focus_keyphrase` adds a warning (missing from the title and opening). Warnings never block.
- **Images:** `media_urls: [{"url": "https://...", "role": "featured", "alt_text": "..."}]` (also `filename`, `caption`), a public link the user gave or the `url` from `upload-library-image`; a file attached in the chat goes in `media` with its `download_url` ([media](post-media.md)). `role` defaults to `inline` (added at the end unless `placement` says otherwise); with no `featured` image, the first image becomes the featured one at publish. Images only, 25 MB max. It uploads to the site's media library when the draft saves, even if never published. Failures arrive in `media_warnings`; the draft still saves.
- **After saving:** `wordpress_post_id` and `preview_url` stay empty until it goes out. Going out is public; only its date and featured image can be fixed from here.
- **Changes:** `save-post` with `post_id`: the body as `content`; title, meta and excerpt as `platform_details` `{"wordpress": {"title": "...", "meta_description": "..."}}`, or as `platform_specific` the same shape ([keys](post-per-network-keys.md)); never a `wordpress_post_id`, which is ignored. Every change gets a check. Going out later, now or at a time: `publish-post` after the yes ([review](review.md)). Already live: `save-post` refuses it; `update-wordpress-article` edits the same article in place: headline, body, date, featured image ([the live article](post-wordpress-live.md)).
- **Timeouts:** check with `get-post` (or recent WordPress drafts), then retry with the same `idempotency_key`.
- **Offer once:** "Want posts written from each new article?" A Bolta routine does that ([routine](routine.md)) once the blog is connected in Bolta.

## Always

- No time or publish action in the saving call without a yes that covers it.
- Never promise search details show in results, or ask for a password in chat.
- Say before the yes that going out is public on the site.
