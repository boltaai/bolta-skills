# Networks at a glance

One row per network. The live limits come first; trust them over this page. A blank cell is not checked here: for extra parts, write one post. Every setting in detail, and how to set it: [network settings](post-settings.md).

"Saved, not sent" means Bolta keeps the setting but never passes it to the network.

| Network | Length, and past it | Media needed | Extra parts become | Worth asking about | Not possible here |
|-|-|-|-|-|-|
| LinkedIn | 3,000; longer is refused at approval | None | | Personal profile or company page (`list-accounts`), `visibility` | Polls, documents; comments, resharing (saved, not sent) |
| X | 280 (more on X Premium); longer is refused at approval | Images only; a video fails at publish | Replies, in a thread | Poll, quote, `reply_settings`, subscribers only | A poll inside a thread; video |
| Threads | 500; longer splits into a reply chain | Optional | Replies to the first post, not a chain; a later part over 500 is cut | Topic, ghost post, spoiler | Reply control (saved, not sent) |
| Bluesky | 300; cut with "..." | Optional | Replies, in a thread | `languages` | Reply settings (saved, not sent) |
| Mastodon | 500, or the server's own; cut | Optional | Joined into one post | `visibility`, content warning | Polls, language (saved, not sent) |
| Facebook | | Text, one video, or images; never a video with images | Comments by the Page, each with at most one image | Which Page (`list-accounts`) | Feeling, activity, place, privacy, comment settings (saved, not sent) |
| Instagram | 2,200; cut | Image or video; 2 to 10 make a carousel | | Feed, reel or story; trial reel; cover | Text only; collaborators; per-account format |
| TikTok | 2,200; cut | One video | | `privacy_level` (public if unset; ask), comments, duet, stitch, brand disclosure | |
| YouTube | Title unchecked; blank uses the text's start | One video | | Title, `privacy_status` (default private), made for kids, thumbnail | Made-for-kids except `self_declared_made_for_kids`; playlists, comments, chapters, language (saved, not sent) |
| Pinterest | Title 100, description 500 | One image or one video | | Board (`board_id`, Pinterest's id from an earlier pin's read, or picked in Bolta; else latest synced), link, alt text | Listing boards from here |
| Reddit | Title 256 | None | | Subreddit and title (both required), flair | Video (images only); text beside images (only the title goes out) |
| Discord | 2,000; cut | None | | Channel (required; missing fails at publish), embed | Connecting a new Discord account |
| WordPress | Meta title 60, description 160; longer is sent with a warning | Images only, 25 MB | One article | Categories, tags, featured image | Markdown tables |

## Ask before the yes

- Which account or Page: read `list-accounts` and name it ("This goes to the Acme company page").
- Anything required: Reddit subreddit and title, Discord channel, a video for TikTok and YouTube.
- YouTube title and kids answer (unset: title from the text, not for kids).

## Always

- Read the live limits once per brand before writing for a network ([platforms](post-platforms.md), section 1), and reuse them.
- Never offer a setting marked saved, not sent; say plainly it isn't possible here.
- Never invent a Page, board, subreddit, channel or place id.
- Say every setting you changed, with the post it's on.
