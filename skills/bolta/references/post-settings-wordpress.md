# WordPress settings

How to save an article: [WordPress articles](post-wordpress.md). How to set and which wins: [network settings](post-settings.md). Network `wordpress`. The post's text is the article body; a `text` key is ignored.

Change settings on a saved article with `save-post` `post_id` and `platform_details` `{"wordpress": {...}}` or `platform_specific` `{"wordpress": {...}}`. In `platform_specific` an account's entry merges with the network's, the account winning, and an empty `title` there doesn't wipe the saved one.

## Settings

All both, per account, unless marked.

- **Title**: `title`, up to 255 characters. Empty: the first line if under 100 characters (a leading `#` and all), else "Blog Post" and the date. Always set one.
- **Address**: `slug`, on `create-wordpress-blog-post` or in `platform_specific` (which wins). Empty: made from the title. Guidance: short, lowercase, the main search words ("sourdough-starter-guide"); change it only before the article goes out, since a live address change breaks links.
- **Search title and description**: `meta_title` (aim for 60 characters or fewer), `meta_description` (160 or fewer). Sent as the post's `title` and `description` meta keys; they show in search results only if the site's SEO plugin reads those keys. Never promise they appear.
- **Excerpt**: `excerpt`. Empty: about the first 155 characters of the article. Guidance: one or two sentences that make someone click from the blog index.
- **Categories and tags**: `categories`, `tags`, lists of names. A new name is created on the live site at publish, so match existing spelling; one that can't be created is dropped without a word. Guidance: one or two categories, a handful of tags.
- `post_type` takes `post` (default) or `page`, but `page` is not honoured yet: everything goes out as a blog post. Don't offer pages.
- **Comments and pingbacks**: `comment_status`, `ping_status`, `open` (default) or `closed`.
- **Pinned to the top**: `sticky` (default false). Guidance: one sticky article at a time, for a launch or an important notice.
- **Format**: `format` `standard` (default), `aside`, `chat`, `gallery`, `link`, `image`, `quote`, `status`, `video`, `audio`. Only matters if the site's theme uses formats; leave `standard` otherwise.
- **Featured image**: on save, `media_urls` with `role: "featured"` ([WordPress articles](post-wordpress.md)). `featured_media_id` (details only) takes the site's own media id; leave it to the save.

When it goes out it is published live on the site, never sent as a WordPress draft or for review there; `status` (`publish`, `draft`, `private`, `pending`, `future`, `trash`) can't be set.

## Not sent

`custom_fields`, `password`, `template`, `parent_id` (a parent page), `menu_order` and `status`: Bolta refuses them. Also never used: `post_type` `page`, and `seo_metadata` beyond the slug, meta title and description (canonical link, focus keyphrase, schema). Don't offer them.

## Not possible here

A standing page (About, Pricing), editing an article already on the site, choosing an author, scheduling inside WordPress, Markdown tables or code blocks, password-protected or private posts.

## Always

- Set a title and slug before the yes; say the address it will get.
- Category and tag names spelled as the site already has them.
- Going out is public and can't be undone from here: say so before the yes.
