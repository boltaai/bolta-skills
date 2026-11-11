# Different text and settings per network or account

One post can carry its own text and settings for each network, and for each account, Facebook Page or LinkedIn page on it. Set them with `platform_specific` on `create-post` or `update-post`. The keys each network reads, and what is saved but never used: [per-network keys](post-per-network-keys.md).

## The shape

```json
{"linkedin": {"text": "The longer story for LinkedIn",
              "accounts": {"<linkedin_org_ id from list-accounts>": {"text": "The company page's version"}}},
 "x": {"text": "One line for X", "reply_settings": "followers"},
 "instagram": {"content_type": "REELS"}}
```

- Keyed by network: `x`, `threads`, `instagram`, `facebook`, `linkedin`, `tiktok`, `youtube`, `pinterest`, `bluesky`, `mastodon`, `reddit`, `discord`, `wordpress`. Any other name ("twitter") is refused.
- `accounts` is keyed by the id from `list-accounts`: an account id, `facebook_page_<id>` for a Page, `linkedin_org_<id>` for a LinkedIn page. Bolta stores it under the account's or Page's name, so a read back shows the name, not the id.
- `text` on a network replaces the post's text there; on an account, for that account only. It changes the first part only: later parts of a thread go out as written.
- Which wins when it goes out: the account's entry, then the network's fields, then what `update-post-platform-details` set. TikTok and YouTube are stricter: an account with its own entry uses only that entry, so repeat any network field it needs.

## On create and on update

- `create-post`: send everything in the one call; no settings call after. The post is still a Draft.
- `update-post` merges into what is there: fields you send replace those fields, the rest stay; accounts merge one by one. `null` removes a network, a field or an account's entry: `{"x": {"text": null}}` puts X back on the main text.
- Unknown field names are saved and never used, with a success reply. Read back: `get-post` shows them under `metadata.platformSpecific`.

## When to use which

- **`platform_specific`**: a different text per network or per Page on one post; a setting for one account only; settings in the same call that saves the post; an Instagram trial reel.
- **`update-post-platform-details`**: one network's settings on a saved post, with keys from `get-post-platform-details`, and anything that needs Bolta's own ids: Reddit subreddit, Discord channel, Pinterest board, LinkedIn `selected_organization`.
- A key set in `platform_specific` wins over the same key set with `update-post-platform-details`. To change it, change it where it was set.
- Separate posts instead ([cross-posting](post-cross-posting.md)): different media, different times, or extra parts (a thread, a first comment) on one network only.

## Approval

- Changing any of these on an Approved or Scheduled post sends it back to waiting for a yes, and voids a client's yes. The reply carries `approval_reset` and a message. Say so before changing it: "Changing the X text sends this scheduled post back for your yes."
- Sending the same values again changes nothing and keeps the yes.
- A client reviewer can't edit the text of a post with its own text per network ([client details](review-client-details.md)).

## Showing it

Number each destination with its own text: "1. LinkedIn, Acme company page: (full text) 2. X, @acme: (full text). Replies: people it follows." One post, so one yes covers all of them.

## Always

- Follow the house rules in the Bolta skill.
- Show the full text each network or Page will get, never only the main text.
- Account ids come from `list-accounts`; never guess one.
- Say before changing settings on an approved or scheduled post that it needs a yes again.
