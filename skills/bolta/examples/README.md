# Worked examples

Each file is one ask from start to finish: the calls in order, why each one is shaped that way, what to say at the end and what never to do. Routines and campaigns come first, because a few Bolta routines plus one campaign is what keeps a brand running; one-off posts follow. Values in `<angle brackets>` come from an earlier read; never send them as written. The brand in every example is Acme.

| File | The ask | Playbook |
|-|-|-|
| [weekly-routine.json](weekly-routine.json) | A Bolta routine: create, switch on, read back | [routine](../references/routine.md) |
| [routine-with-images.json](routine-with-images.json) | Weekly posts with an image each | [routine](../references/routine.md) |
| [routine-to-client.json](routine-to-client.json) | Send a routine's drafts straight to the client, keeping about 20 waiting | [routine](../references/routine.md) |
| [fix-a-failed-run.json](fix-a-failed-run.json) | A skipped run: one instructions change, then run now | [routine](../references/routine.md) |
| [launch-campaign.json](launch-campaign.json) | A 3-week launch: brief, accounts, a page to read, start | [campaign](../references/campaign.md) |
| [video-campaign.json](video-campaign.json) | A campaign with two short videos a week, its higher cost said first | [campaign](../references/campaign.md) |
| [first-voice.json](first-voice.json) | A first voice from a site and a writing sample | [start](../references/start.md) |
| [person-voice.json](person-voice.json) | A voice for the founder, writing as "I" | [voice](../references/voice.md) |
| [voice-generate-batch.json](voice-generate-batch.json) | A batch in the trained voice (1 credit a post written), then the status poll | [voice](../references/voice.md) |
| [decide-in-one-message.json](decide-in-one-message.json) | "1 and 3 yes, 2 too salesy, drop 4" | [review](../references/review.md) |
| [schedule-my-text.json](schedule-my-text.json) | The user's own text with a day and time | [review](../references/review.md) |
| [waiting-on-the-client.json](waiting-on-the-client.json) | A yes where one post still needs the client | [review](../references/review.md) |
| [move-a-time.json](move-a-time.json) | Move a scheduled post's time, keeping its yes | [review](../references/review.md) |
| [settings-change-needs-yes.json](settings-change-needs-yes.json) | Change one network's text on a scheduled post: it needs a yes again | [review](../references/review.md) |
| [approve-library-post.json](approve-library-post.json) | A yes to a Library post, which takes no time | [review](../references/review.md) |
| [one-post.json](one-post.json) | One LinkedIn post, saved as a draft | [post](../references/post.md) |
| [week-of-posts.json](week-of-posts.json) | A week of posts in one batch, then the status poll | [post](../references/post.md) |
| [reddit-post.json](reddit-post.json) | A network with its own fields: title and subreddit | [post](../references/post.md) |
| [instagram-with-image.json](instagram-with-image.json) | A post with media, for two networks | [post](../references/post.md) |
| [threads-topic-and-ghost.json](threads-topic-and-ghost.json) | Threads: a topic, and a post that disappears after 24 hours | [post](../references/post.md) |
| [x-poll.json](x-poll.json) | An X poll | [post](../references/post.md) |
| [linkedin-company-page.json](linkedin-company-page.json) | LinkedIn as the company page, by its page id from the account list | [post](../references/post.md) |
| [youtube-video.json](youtube-video.json) | A YouTube video: title, privacy, the self-declared kids flag, a thumbnail | [post](../references/post.md) |
| [tiktok-video.json](tiktok-video.json) | A TikTok video: privacy and duets | [post](../references/post.md) |
| [one-idea-three-networks.json](one-idea-three-networks.json) | One idea on four networks as separate posts, because Facebook gets a first comment | [post](../references/post.md) |
| [one-post-text-per-network.json](one-post-text-per-network.json) | One post, its own text on LinkedIn, X and Threads | [post](../references/post.md) |
| [text-per-page.json](text-per-page.json) | Its own text for a LinkedIn company page and one Facebook Page | [post](../references/post.md) |
| [instagram-trial-reel.json](instagram-trial-reel.json) | An Instagram trial reel, set when it is saved | [post](../references/post.md) |
| [x-thread.json](x-thread.json) | An X thread: parts in one batch item, an image on part 3 | [post](../references/post.md) |
| [facebook-first-comment.json](facebook-first-comment.json) | A Facebook Page post with the link as its first comment | [post](../references/post.md) |
| [undo-a-delete.json](undo-a-delete.json) | Bring a deleted post back | [fix](../references/fix.md) |
| [how-did-it-do.json](how-did-it-do.json) | The last 30 days' results, read honestly | [results](../references/results.md) |
| [best-posts.json](best-posts.json) | The best LinkedIn post, on LinkedIn's own numbers, with its link | [results](../references/results.md) |

## Which tool, which playbook

Two tools with no row in the playbook table, and where they belong:

| Tool | Playbook | When |
|-|-|-|
| `voice-generate` | [voice](../references/voice.md) | A batch in the trained voice, after saying it costs 1 credit a post and getting a yes |
| `list-reviews` | [review](../references/review.md) | "What's waiting on me": the posts assigned to this person |

## The shape

- `ask`: what the user typed. `before`: what the earlier reply already showed, when the ask is a yes.
- `steps`: calls in order, each with `tool`, `arguments` and `why`.
- `say`: the closing line, in the plain words.
- `never`: the mistakes this ask invites.

An example shows the shape of the calls. The playbook decides; when they differ, follow the playbook.
