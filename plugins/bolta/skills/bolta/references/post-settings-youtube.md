# YouTube settings

How to set and which wins: [network settings](post-settings.md). Network `youtube`. Needs one video (a public https link). A `text` in `platform_specific` is ignored; the description is its own setting.

**Per-account entries replace, not merge**: a channel with its own entry under `youtube.accounts` uses only that entry, so repeat every setting it needs there. Missing keys fall back to what `save-post` `platform_details` saved.

## Settings

- **Title**: `video_title`. Both, per account. Empty: the first 95 characters of the post's text, which rarely reads well. Always set one, short and searchable; Bolta doesn't check YouTube's own title limit.
- **Description**: `video_description`. Both, per account. Empty: the post's text.
- **Who sees it**: `privacy_status` `private` (default), `unlisted` or `public`. Both, per account. Never `scheduled`: schedule the post instead.
  - Guidance: `unlisted` to let a client or teammate watch it by link before it is public, then change to `public` (on a scheduled post that needs a new yes). `private` only for the owner's eyes. Say the default out loud: a video saved without a choice goes up private.
- **Made for kids**: `self_declared_made_for_kids` true or false (default false); `made_for_kids` is the same setting. Both, per account. Ask when the content could be aimed at children: YouTube's rules make the uploader answer.
- **Tags**: `tags`, a list of words. **Category**: `category_id`, YouTube's number (22 People & Blogs, 27 Education, 28 Science & Technology). Both, per account. Only a category the user agreed to.
- **Thumbnail**: `thumbnail_url`, a public https image the user gave. Best effort: if it fails, the video still goes up. Here `platform_details` wins over `platform_specific`.
- **Language**: `default_language`, the video's language code such as `"en"` or `"es"`. Both, per account. Set it when the video isn't in the channel's usual language.
- **Embedding**: `allow_embedding` (default true) lets other sites show the video.
- **Tell subscribers**: `notify_subscribers` (default true). Guidance: turn off for a re-upload, a client preview or a minor clip so subscribers aren't pinged.
- `publish_at`: details only; leave it out and schedule the post.

## Shorts

Bolta has no Shorts switch. YouTube itself decides whether an upload shows as a Short, from the video's shape and length. A vertical, short clip usually does; never promise it.

- Guidance: a vertical clip made for Reels or TikTok goes to YouTube as is and may land in Shorts; a horizontal video with a real title and description is a normal video. For a Short, keep the title short and the description to a line or two.

## Not sent

`playlist_ids` (adding to a playlist), `allow_comments`, `enable_auto_chapters`: Bolta refuses them. Don't offer them.

## Not possible here

Playlists, turning comments off, chapters, captions or subtitles, end screens, a premiere, choosing Short or long yourself.

`post` and `video_id` (filled in after upload) are Bolta's own; never send them.

## Always

- Say the title, privacy and kids answer before the yes: "YouTube: 'Spring menu tour', unlisted, not for kids."
- Privacy defaults to private: name it and ask.
- Read back before saying a setting is set.
