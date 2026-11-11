# Different text and settings per network or account

One post can carry its own text and settings per network, and per account, Facebook Page or LinkedIn page: `platform_specific` on `create-post` or `update-post`. Which keys each network reads, network level or per account: [per-network keys](post-per-network-keys.md). Every setting in detail: [network settings](post-settings.md).

## Which settings to set

- **Required, ask if unknown:** Reddit title and subreddit, Pinterest board, Discord channel, YouTube title.
- **Optional:** only when asked or clearly fitting; offer in one line, never set silently.
- **Routines and campaigns** carry only required basics; no per-routine network settings yet.

## The shape

```json
{"linkedin": {"text": "The longer story for LinkedIn",
              "accounts": {"<linkedin_org_ id from list-accounts>": {"text": "The company page's version"}}},
 "x": {"text": "One line for X"},
 "threads": {"topic_tag": "Coffee"},
 "instagram": {"content_type": "REELS"}}
```

- Keyed by network: `x`, `threads`, `instagram`, `facebook`, `linkedin`, `tiktok`, `youtube`, `pinterest`, `bluesky`, `mastodon`, `reddit`, `discord`, `wordpress`. Any other name ("twitter") is refused.
- `accounts` is keyed by the id from `list-accounts`: an account id, `facebook_page_<id>` for a Page, `linkedin_org_<id>` for a LinkedIn page. A read back shows the name, not the id.
- `text` on a network replaces the post's text there; on an account, for that account only. First part only: later parts of a thread go out as written. TikTok, YouTube, Pinterest and WordPress ignore `text`.

## Which wins

- For keys read per account: the account's entry, then the network's, then what `update-post-platform-details` saved. A later details call rewrites a copy of the key here.
- TikTok and YouTube: an account with its own entry uses only that entry; repeat every key it needs there.
- Keys marked network only are copied into the network's settings when the post saves; an account entry for them is ignored, and the latest save wins.
- Keys marked details only do nothing here, though they are kept.

## On create and on update

- `create-post`: send everything in the one call. The post is still a Draft.
- `update-post` merges into what is there: fields sent replace those fields, the rest stay; accounts merge one by one. `null` removes a network, a field or an account's entry: `{"x": {"text": null}}` puts X back on the main text.
- Send only what changes. Never resend other networks' values from memory.
- Unknown keys are kept, never used; `get-post` shows them under `metadata.platformSpecific`.
- A batch item carries no `platform_specific`: save the batch, then one `update-post` per post.

## When to use which

- **`platform_specific`**: text per network or Page; a setting for one account only; settings in the same call that saves the post; an Instagram trial reel; TikTok paid or brand disclosure; a Pinterest board (Pinterest's id, as a read shows it).
- **`update-post-platform-details`**: X quote, reply, place and image tags; one network's settings on a saved post when a bad value should be refused (TikTok or YouTube privacy), and anything that takes Bolta's own ids: Reddit subreddit, Discord channel, LinkedIn `selected_organization`, Facebook Pages.
- Set each key one way. To change it, change it where it was set.

## Approval

- A real change on an Approved or Scheduled post sends it back to waiting for a yes and voids a client's yes; the reply carries `approval_reset`. Same values again keep the yes. Say so first.
- A client reviewer can't edit the text of a post with its own text per network ([client details](review-client-details.md)).

## Always

- Follow the house rules in the Bolta skill.
- Show the full text each network or Page will get. Never guess an account id.
