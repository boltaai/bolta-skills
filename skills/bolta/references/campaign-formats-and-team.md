# Formats, settings and the team side

Read for campaign formats and settings, or a team version: one idea written for each person. The employee Library and the idea bank: [library-and-ideas.md](campaign-library-and-ideas.md).

## Formats (`content_mix` keys, per week)

`text`, `blog` (WordPress only), `email` (the user sends it): what a campaign made here sends. Which network takes which, the weekly caps, and changing a mix a campaign already has: [settings-formats.md](campaign-settings-formats.md). Pictures and video are chosen on the campaign page, bolta.ai/dashboard/campaigns/<id>, never from chat; a campaign with them is changed only there. Worked example: [campaign-webinar-countdown](../examples/campaign-webinar-countdown.json).

## Whose voice

One campaign writes in one voice: the brand's, or a person's set with `voice_profile_id` ([targets.md](campaign-targets.md)). Several people each posting about one idea is a team version, below.

## Accounts or days per format

The mix can't say which account or weekday a format goes to ("text on LinkedIn only, the blog on Tuesdays"). That is the content plan, edited on the campaign page under "Content per week". Sending `content_mix` later rebuilds the plan with no accounts or days, so a campaign with any set changes formats on its page ([settings-formats.md](campaign-settings-formats.md)).

## Planned posts and settings

- Each planned post (topic, format, accounts, time) is edited under "Post prompts" on the campaign page before its week is written; a written post is fixed.
- Tone, post time, and every picture or video setting: the campaign page only ([settings-web.md](campaign-settings-web.md)). Send the user there. Post time applies to drafts written after the change and overrides per-post times.

## A team version

One idea written as a post for each person or function (2 to 6), each in their own voice, is a team version, not a campaign. "Have David, Maria and Procurement each post about the new warehouse" is one. How to plan, start and read it back: [review-team-version.md](review-team-version.md).

## Always

- Never promise a format Bolta doesn't make, or an email it sends.
- Never set up pictures or video from chat.
- Follow the house rules in the Bolta skill.
