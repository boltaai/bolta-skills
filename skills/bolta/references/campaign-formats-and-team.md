# Formats, settings and the team side

Read for campaign formats and settings, or a team version: one idea written for each person. The employee Library and the idea bank: [library-and-ideas.md](campaign-library-and-ideas.md).

## Formats (`content_mix` keys, per week)

- `text`: words only. `still_image`: one generated image. `carousel`: a multi-slide deck.
- `feed_video`: a 16:9 feed video. `short_video`: a 9:16 vertical short for Reels, Shorts or TikTok.
- `blog`: a long-form article, written into Approvals. It publishes only to a connected WordPress site; with none, say "Connect your WordPress site first, or the article has nowhere to go."
- `email`: written into Approvals in the brand's voice; the user copies it into their mail tool. Say it as Bolta does: "Bolta writes these. Sending them is still yours." Bolta never sends email; never say it will.
- `story` and `avatar_video` are kept but never made. Don't send them. Say "Campaigns can't make stories yet." or "Bolta doesn't make avatar videos yet."
- Any other key drops silently. A theme ("behind the scenes", "tips") goes in the theme or notes, never the mix.
- **Video costs more:** each video draft runs a paid generation. Say before the yes, with no number: "Each video draft costs more credits than an image post." Worked example: [video-campaign](../examples/video-campaign.json).

## Accounts or days per format

The mix can't say which account or weekday a format goes to ("the carousel on LinkedIn, the shorts on TikTok"). That is the content plan, edited on the campaign page under "Content per week". Sending `content_mix` later rebuilds the plan with no accounts or days, so read `get-content-campaign` first ([two-ways.md](campaign-two-ways.md)).

## Planned posts and settings

- Each planned post (topic, format, accounts, time) is edited under "Post prompts" on the campaign page before its week is written; a written post is fixed.
- Tone, image quality, video style and length are under "Context Settings" on the campaign page (bolta.ai/dashboard/campaigns/<id>); post time and timezone on its "Schedule" row. I can't set them: send the user there. Post time applies to drafts written after the change.

## A team version

One idea written as a post for each person or function (2 to 6), each in their own voice, for the account that voice posts from, saved as one group in Approvals. Call it a team version, never a cascade. "Have David, Maria and Procurement each post about the new warehouse" is one.

1. `propose-cascade` with `idea` (the user's words, a sentence or two, at most 600 characters: facts, numbers and names in the drafts come only from here) and `participants` (only those the user named, such as `[{"name": "David"}, {"name": "Procurement"}]`), or `count` for the brand's person voices. A function like Procurement writes in the brand voice. It saves a plan only: nothing written, charged or scheduled.
2. Show the rows: who, voice, account, angle. A row Bolta couldn't place (a name matching several voices or none, a voice on several accounts) comes back unresolved with the choices: ask, never choose. Settle it with `update-cascade`, passing the `revision` the user saw.
3. On a yes, `start-cascade` with the id and revision. Drafts only, each charged only when approved.
4. `get-cascade` until rows show a saved draft; only then say they are written.

A person with no voice yet: [voice-brand-and-learning.md](voice-brand-and-learning.md). Bolta's own chat (bolta.ai/dashboard/hub) can also put the idea in the employee Library; these tools can't.

## Always

- Get a yes on a team version's plan before `start-cascade`.
- Never add a person or function the user didn't name.
- Never promise a format Bolta doesn't make, or an email it sends.
