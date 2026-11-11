# Formats, settings and the team side

Read for campaign formats and settings, or a team version: one idea written for each person. The employee Library and the idea bank: [library-and-ideas.md](campaign-library-and-ideas.md).

## Formats (`content_mix` keys, per week)

`text`, `still_image`, `carousel`, `feed_video` (16:9), `short_video` (9:16), `blog` (WordPress only), `email` (the user sends it). Which network takes which, the weekly caps, when to pick each and the video cost: [settings-formats.md](campaign-settings-formats.md). Say "Campaigns can't make stories yet." or "Bolta doesn't make avatar videos yet." for `story` and `avatar_video`. Worked example: [video-campaign](../examples/video-campaign.json).

## Whose voice

One campaign writes in one voice: the brand's, or a person's set with `voice_profile_id` ([targets.md](campaign-targets.md)). Several people each posting about one idea is a team version, below.

## Accounts or days per format

The mix can't say which account or weekday a format goes to ("the carousel on LinkedIn, the shorts on TikTok"). That is the content plan, edited on the campaign page under "Content per week". Sending `content_mix` later rebuilds the plan with no accounts or days, so read `get-content-campaign` first ([two-ways.md](campaign-two-ways.md)).

## Planned posts and settings

- Each planned post (topic, format, accounts, time) is edited under "Post prompts" on the campaign page before its week is written; a written post is fixed.
- Tone, image quality, video style and length, post time: the campaign page only ([settings-web.md](campaign-settings-web.md)). Send the user there. Post time applies to drafts written after the change and overrides per-post times.

## A team version

One idea written as a post for each person or function (2 to 6), each in their own voice, is a team version, not a campaign. "Have David, Maria and Procurement each post about the new warehouse" is one. How to plan, start and read it back: [review-team-version.md](review-team-version.md).

## Always

- Never promise a format Bolta doesn't make, or an email it sends.
- Follow the house rules in the Bolta skill.
