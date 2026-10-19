# WordPress articles

Bolta facts only. Write the article as usual.

- **Saving:** `create-wordpress-blog-post` with `title`, Markdown `content`, `seo` and an `idempotency_key`. It saves a draft, no check. Send no time or publish action; the yes belongs to `review`. Asked to send it for review? `requested_action: "submit_for_review"` does it here.
- **No WordPress connected** (`wordpress_connection_required`): give a `get-connect-link` link and offer the article as text. Never ask for a password. Several sites: the reply lists them; ask which, then resend with `wordpress_account_id`.
- **Markdown:** tables don't convert (rows run together) and nested lists flatten; the rest of basic Markdown does. The title is the page heading: start the body with the introduction and use `##` for sections.
- **Address:** `slug` has no effect; the address comes from the title. Leave out `content_format`.
- **Categories and tags** are names; a new one is created on the live site at publish, so match existing spelling.
- **Search details:** `seo.meta_title` and `seo.meta_description` go to WordPress. Keep them under 60 and 160 characters; longer is sent, with a warning in `seo_validation`. Other `seo` fields only feed those warnings, which never block.
- **Images:** `media: [{"url": "https://...", "role": "featured", "alt_text": "..."}]`, a public link the user gave. Images only, 25 MB max. It uploads to the site's media library when the draft saves, even if never published. Failures arrive in `media_warnings`; the draft still saves.
- **After saving:** `wordpress_post_id` and `preview_url` stay empty until it goes out. Going out is public and can't be undone from here.
- **Changes:** the body via `update-post` with `status: "Draft"`. Title, meta and excerpt with `update-post-platform-details` for `wordpress`, which gets a check every time.
- **Timeouts:** check recent WordPress drafts, then retry with the same `idempotency_key`.
- **Offer once:** "Want posts written from each new article?" A Bolta routine does that (`routine`) once the blog is connected in Bolta.
