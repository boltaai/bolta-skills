# Pinterest settings

How to set and which wins: [network settings](post-settings.md). Network `pinterest`. Needs exactly one image or one video (a public https link). A `text` in `platform_specific` is ignored; the pin's words are its own settings. Here an account's entry merges with the network's, the account winning.

## The board

Every pin goes to a board. Bolta picks it in this order:

1. `board_id` in `platform_specific`: **Pinterest's own board id**, a long number (not the board's name or web address). `get-post-platform-details` on any earlier pin shows its board this way, as `board_id`.
2. A board set with `update-post-platform-details` `board` (or `board_id`): there both take **Bolta's id for the board**, which no read here shows. Don't use this route.
3. None set: the account's most recently updated board, which may be the wrong one. No boards at all: the pin fails when it goes out.

Same key name, two different ids: never send a read's `board_id` to `update-post-platform-details`. No tool lists boards: read an earlier pin on the board the user means and put its `board_id` in `platform_specific`, or the user picks the board in Bolta. Say which board will be used before the yes, or ask.

## Settings

All both, per account, unless marked.

- **Title**: `title`, up to 100 characters; longer is cut. Empty: the description is used, cut to 100.
  - Guidance: what someone would type into Pinterest search ("Easy sourdough for beginners"), not a slogan.
- **Description**: `description`, up to 500 characters; longer is cut. Empty: the post's text (first part).
- **Link**: `link`, the page the pin opens. Only a link the user gave.
  - Guidance: link every pin to the page that matches it (the recipe, the product), never a homepage. A pin without a link gets saves, not visits.
- **Alt text**: `alt_text`, up to 500 characters. Empty: the image's own alt text, else its file name. Pinterest is one of the few networks that receives alt text: always write it.
- **Video cover**: `cover_image_url`, a public JPEG or PNG link the user gave. A video pin needs one; an image pin ignores it.
- `media_url` adds a second file to the attached one, and a pin with two is refused; `media_type` (`image` or `video`) must match the file. Leave both out. `idea` saves, then fails when it goes out.

## Saved, not sent yet

`scheduled_publish_time`: schedule the post instead.

## Not possible here

Listing or creating boards, board sections, Idea pins, several images in one pin, tagging products.

`post` (the post the settings belong to) is Bolta's own; never send it.

## Always

- Never guess a board id; say which board the pin goes to.
- Link and alt text on every pin, from what the user gave.
- One image or one video per pin.
