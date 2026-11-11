# Different text and settings per network or account

One post can carry its own text and settings per network, and per account, Facebook Page or LinkedIn page: `platform_specific` on `save-post`, new or with `post_id`. Which keys each network reads, network level or per account: [per-network keys](post-per-network-keys.md). Every setting in detail: [network settings](post-settings.md).

## The shape

```json
{"linkedin": {"text": "The longer story for LinkedIn",
              "accounts": {"<linkedin_org_ id from list-accounts>": {"text": "The company page's version"}}},
 "x": {"text": "One line for X"},
 "threads": {"topic_tag": "Coffee"},
 "instagram": {"content_type": "REELS"}}
```

- Keyed by network: `x`, `threads`, `instagram`, `facebook`, `linkedin`, `tiktok`, `youtube`, `pinterest`, `bluesky`, `mastodon`, `reddit`, `discord`, `wordpress`. Any other name ("twitter") is refused.
- `accounts` is keyed by the id from `list-accounts`: an account id, `facebook_page_<id>` for a Page, `linkedin_org_<id>` for a LinkedIn page. Bolta stores it under the account's or Page's name, so a read back shows the name, not the id.
- `text` on a network replaces the post's text there; on an account, for that account only. First part only: later parts of a thread go out as written. TikTok, YouTube, Pinterest and WordPress ignore `text`.

## Which wins

- For keys read per account: the account's entry, then the network's, then what `platform_details` saved. A later `platform_details` change rewrites a copy of the key here.
- TikTok and YouTube: an account with its own entry uses only that entry; repeat every key it needs there.
- Keys marked network only are copied into the network's settings when the post saves; an account entry for them is ignored, and the latest save wins.
- Keys marked details only do nothing here, though they are kept.

## On create and on update

- New (`save-post`, no `post_id`): send everything in the one call. The post is still a Draft.
- An edit (`save-post` with `post_id`) merges into what is there: fields sent replace those fields, the rest stay; accounts merge one by one. `null` removes a network, a field or an account's entry: `{"x": {"text": null}}` puts X back on the main text; `{"facebook": {"accounts": {"<facebook_page_ id>": null}}}` puts that Page back on the Facebook text.
- Send only what changes. Never resend other networks' values from memory.
- Unknown keys are saved and never used, with a success reply. Read back: `get-post` shows them under `metadata.platformSpecific`.
- A batch item carries no `platform_specific`: save the batch, then one `save-post` with `post_id` per post.

## When to use which

`platform_specific` or `platform_details`, key by key: [which way](post-per-network-which.md).

## Approval

- A real change on an Approved or Scheduled post sends it back to waiting for a yes and voids a client's yes. On a Scheduled post any `save-post` does, even with the same values; on an approved post not yet scheduled, the same values keep the yes. The reply carries `sent_back_for_review` and `approval_reset`. Say so first: "Changing the X text sends this scheduled post back for your yes."
- A client reviewer can't edit the text of a post with its own text per network ([client details](review-client-details.md)).

## Always

- Follow the house rules in the Bolta skill.
- Show the full text each network or Page will get, never only the main text.
- Account ids come from `list-accounts`; never guess one.
