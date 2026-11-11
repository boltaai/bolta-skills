# Network settings: approval and limits

How to set a setting and which wins: [network settings](post-settings.md).

## Approval

Any real change to text or a setting on an Approved or Scheduled post, by `platform_specific` or `platform_details` on `save-post`, sends it back to waiting for a yes and voids a client's yes. The result says `sent_back_for_review`. On a Scheduled post any `save-post` sends it back, even one sending the same values; on an approved post that isn't scheduled yet, the same values again keep the yes. Say so before changing: "Changing YouTube to public sends this scheduled post back for your yes."

## Not sent

Some settings are stored in Bolta but never reach the network; each page lists them under "Not sent". Bolta refuses them from here, naming the setting (`get-post` with `platform` lists them as `not_sent_fields`; in `platform_details` only that network is refused). Never offer one; say plainly it can't be set.

## Only in Bolta's web app

Removing or swapping media, a Threads text spoiler (a hidden span of text), Reddit promotion across several subreddits, repeating, auto-repost and auto-plug ([repeating](post-repeating.md)), and picking a Pinterest board or Discord channel from a list.

## Always

- Say a change sends an approved or scheduled post back before making it.
- Never offer a setting listed as not sent.
