# Networks: what each one needs

Part of [networks: limits, media and settings](post-platforms.md). Live rules from `get-posting-rules` come first.

These are accepted, then fail when the post goes out, with only a notification in Bolta:

- TikTok, YouTube: a video. Instagram: an image or video (2-10 make a carousel; over 10 fails); a bulk item aimed at Instagram without media lands in `rejected`. Pinterest: an image or video, and a board ([Pinterest](post-settings-pinterest.md)).
- X: needs text (an image alone isn't supported) and takes images only; a video fails.

Refused at schedule or publish: Facebook with two videos or a video plus images; Reddit without a subreddit and title (approval refuses it too), or with a video; X media with no text.

Defaults to say out loud before the yes ([TikTok](post-settings-tiktok.md), [YouTube](post-settings-youtube.md)):

- TikTok goes out public to everyone unless `privacy_level` is set. The user didn't say? Ask.
- YouTube goes up private unless `privacy_status` is changed. Say so: "This video will go up private on YouTube unless you want it public."
- Pinterest needs a board, an id, not a board name; with none set the most recently updated board is used. Which id goes where: [Pinterest](post-settings-pinterest.md).

A post for several networks: say which one would fail and why, then add media or drop that network: "Instagram needs an image; add one, or I'll leave Instagram off."

## Always

- Name every network that would fail, and why, before saving.
- Say the TikTok and YouTube privacy out loud before the yes.
- Never guess a board, subreddit or channel.
