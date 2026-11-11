# Networks at a glance

One row per network. The live limits come first; trust them over this page. Where extra parts are blank or dropped, write one part. Every setting: [network settings](post-settings.md).

"Not sent" means Bolta keeps the setting but never passes it to the network, and refuses it from here.

| Network | Length, and past it | Media needed | Extra parts become | Worth asking about | Not possible here |
|-|-|-|-|-|-|
| LinkedIn | 3,000; longer is refused at approval | None | Text dropped | Personal profile or company page (`list-accounts`), `visibility` | Polls, documents; comments, resharing (not sent) |
| X | 280 (more on X Premium); longer is refused at approval | Images only; a video fails at publish | Replies, in a thread | Poll, quote, `reply_settings`, subscribers only | A poll inside a thread; video |
| Threads | 500; longer splits into a reply chain | Optional | Replies to the first post, not a chain; a later part over 500 is cut | Topic, ghost post, spoiler, who can reply (`reply_control`) | Quoting a post |
| Bluesky | 300; cut with "..." | Optional | Replies, in a thread | `languages`, alt text | Reply settings (not sent) |
| Mastodon | 500, or the server's own; cut | Optional | Text dropped | `visibility`, content warning, poll, `language` | A poll with media |
| Facebook | | Text, one video, or images; never a video with images | Comments by the Page, each with at most one image | Which Page (`list-accounts`) | Feeling, activity, place, privacy, comment settings (not sent) |
| Instagram | 2,200; not checked, may be refused | Image or video; 2 to 10 make a carousel | | Feed, reel or story; trial reel; cover | Text only; collaborators; per-account format |
| TikTok | 2,200; cut | One video | | `privacy_level` (public if unset; ask), comments, duet, stitch, brand disclosure | |
| YouTube | Title unchecked; blank uses the text's start | One video | | Title, `privacy_status` (default private), made for kids, thumbnail, language | Playlists, comments, chapters (not sent) |
| Pinterest | Title 100, description 500 | One image or one video | | Board (`board_id` from an earlier pin's read, or picked in Bolta), link, alt text | Listing boards from here |
| Reddit | Title 256 | None | Joined into the body | Subreddit and title (both required), flair | Video (images only); text beside images (only the title goes out) |
| Discord | 2,000; cut | None | Joined | Channel (required; missing fails at publish), embed | Connecting a new Discord account |
| WordPress | Meta title 60, description 160; longer is sent with a warning | Images only, 25 MB | One article | Categories, tags, featured image | Markdown tables, pages |

## Ask before the yes

- Which account or Page: read `list-accounts` and name it ("This goes to the Acme company page").
- Anything required: Reddit subreddit and title, Discord channel, a video for TikTok and YouTube.
- YouTube title and kids answer (unset: title from the text, not for kids).

## Always

- Read the live limits once per brand before writing for a network ([platforms](post-platforms.md), section 1), and reuse them.
- Never offer a setting marked not sent; Bolta refuses it. Say plainly it isn't possible here.
- Never invent a Page, board, subreddit, channel or place id.
- Say every setting you changed, with the post it's on.
