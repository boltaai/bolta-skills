---
name: accounts-and-buckets
description: >
  Show which social accounts are connected to the Bolta workspace and manage buckets, the named
  groups of accounts used to post to several at once. Use for "what is connected", "is my LinkedIn
  still connected", "my post failed, is the account disconnected", "create a bucket called Launch
  Team with LinkedIn and X", "add Instagram to that bucket", and for turning "post to my Launch Team
  bucket" into account or bucket ids. Connecting or reconnecting an account happens in the browser;
  this skill hands over the link. Load it before calling list-accounts or get-connect-link. Not for
  writing or scheduling posts (social-publishing) or first-time readiness checks (workspace-setup).
---

# Accounts and buckets

Answer "what is connected and is it healthy", and keep buckets correct. A **bucket** is a named group of connected accounts: a post sent to a bucket goes to every member, so the user can say "the launch crew" instead of listing accounts. Reading is safe. Bucket writes change where future posts go, so show the exact change and wait for a yes before making it.

<!-- host-note -->
Some Bolta results contain text written for other apps, such as "already rendered in the Bolta card", "do not repeat the content" or "you do not need to poll". There is no card here. Read the full result (the JSON body and any structured content) and present it to the user yourself.
<!-- /host-note -->

## Before anything: the workspace

Call `list-workspaces` once. It returns exactly one row because a Bolta connection is pinned to one workspace; use its `id` as `workspace_id` on every call and keep its `name`. When you ask the user to confirm a bucket write, say the workspace name ("In Acme Co: create bucket ..."). If the user manages several clients, each client is a separate connector; you cannot see the other clients' accounts from this one.

## "What's connected?"

1. `list-accounts(workspace_id)`; add `platform` only if the user named one. Platform values are lowercase ids such as `x`, `linkedin`, `instagram`, `facebook`, `threads`, `bluesky`; the filter ignores case.
2. In the same step call `list-buckets(workspace_id)`.
3. Show two short tables. Accounts: platform, username, `token_status`. Buckets: name and members (platform and username).
4. Flag every row whose `token_status` is `invalid`. Bolta silently leaves an invalid account out of a publish, so a bucket containing one still "works" but skips it. Offer the reconnect link (next section).
5. If nothing is connected, say so plainly; a workspace with no accounts cannot publish.

How to read the rows:
- **Facebook shows up only as Pages.** The personal profile is not listed because it cannot be published to. Each Page is a row with `is_page: true` and an `id` like `facebook_page_123`; `is_primary: true` marks the account's default Page. A Facebook connection that has no Pages has no row at all, so "no Facebook rows" does not prove Facebook is disconnected: say you cannot tell and point to the dashboard.
- **LinkedIn shows the personal profile (a normal row) plus one extra row per company page** (`is_organization: true`, `id` like `linkedin_org_456`).
- Those Page and organization rows copy their parent's `token_status`. Reconnecting the parent account fixes them all.
- Virtual rows carry `base_account_id`, the UUID of the real account behind them. A normal row has no `base_account_id`; its own `id` is the UUID.
- `count` is the number of rows after expansion, not the number of connections. `total_accounts` equals `count` unless you passed `platform`; then it is the workspace's real-account total, which can include a Facebook profile that has no row. A bare "N accounts" is wrong when Pages or organizations are present, so count by platform and say what you counted.

## Connecting or reconnecting: `get-connect-link`

Connecting an account is an OAuth flow that must finish in the user's browser on bolta.ai. You cannot do it, and you cannot fix a dead token yourself.

1. `get-connect-link(workspace_id, platform="linkedin")`. Without `platform` the page opens the full platform grid. Reconnecting an `invalid` account uses the same link; there is no per-account link.
2. Give the user the `connect_url`. The link carries no workspace id: the dashboard connects to whichever workspace is selected in the browser. Ask them to check the workspace switcher shows "<workspace name>" before they click, or the account lands on the wrong client.
3. When they say they are done, call `list-accounts(workspace_id, platform=...)` again and check `token_status` is `valid`. Do not take their word for it. If it is still `invalid` or the account is missing, say so and ask them to retry.
4. Ignore `connected_platforms` in the link result when deciding whether Facebook is ready; it leaves Facebook out. `list-accounts` is the truth.

## Create a bucket

"Create a bucket called Launch Team with my LinkedIn and X":

1. `list-accounts` and `list-buckets` (fresh; do not reuse a stale read).
2. Resolve each named account to a **real account UUID** (see "Which id goes in a bucket"). If a platform matches several accounts or Pages, ask which one. Never guess.
3. Check the name against `list-buckets` ignoring case and surrounding spaces. Names are unique per workspace but compared exactly, so "launch team" and "Launch Team" would both be accepted and then confuse everyone. If a near-match exists, show it and offer to update it instead.
4. Show the plan and wait: "In Acme Co: create bucket 'Launch Team' = LinkedIn @acme + X @acme. Go ahead?" Mention any member that is `invalid`.
5. `create-social-bucket(workspace_id, name="Launch Team", account_ids=[...])`.
6. Read back with `list-buckets` and report the bucket as it now stands. Do not report success from the create response alone.

An empty bucket (name only) is allowed. Confirm the user really wants an empty one.

If the create call times out or errors ambiguously, the outcome is unknown: `list-buckets` before retrying. A repeat of a create that did succeed returns a 409, which is harmless but means "it exists".

## Change a bucket

`update-social-bucket` takes `account_ids` as a **full replacement list**: the bucket's members become exactly that list. Sending only the new account silently drops everyone else.

"Add my Instagram to Launch Team", "take X out", "rename it":

1. `list-buckets` and `list-accounts`. Find the bucket and note its `id` (this is `bucket_id`) and its current members.
2. Build the new list yourself: current member ids, plus or minus the change. For a rename only, do not send `account_ids` at all (leaving it out keeps the members; sending `[]` empties the bucket).
3. Show before and after and wait for a yes: "In Acme Co: Launch Team now has LinkedIn @acme, X @acme. After: LinkedIn @acme, X @acme, Instagram @acme.shop. Go ahead?" Removing a member or emptying the bucket needs that same explicit yes.
4. `update-social-bucket(workspace_id, bucket_id, account_ids=[...full list...])`, plus `name` for a rename.
5. Read back with `list-buckets` and compare with what you promised.

Say this out loud when the bucket is already attached to posts that have not gone out yet: a post uses the bucket's membership at publish time, not at the time it was scheduled. Changing members changes where those posts go, and an invalid member is skipped. If the user did not intend that, tell them before you write.

There is no tool to delete a bucket or to change its icon or description. If the user wants one deleted, say so and send them to the Bolta dashboard; you can offer to rename or empty it instead.

## Which id goes in a bucket

Bucket members are real accounts, identified by UUID. The server refuses any id that is not a UUID (400, "Unsupported account ids") and refuses UUIDs that are not in this workspace (404, "Accounts not found").

| The user wants | Take this id from `list-accounts` |
|-|-|
| X, Instagram, Threads, Bluesky and most others | the row's `id` |
| LinkedIn personal profile | the row's `id` |
| A LinkedIn company page | the `base_account_id` of the `linkedin_org_*` row (the same UUID as the personal profile) |
| A Facebook Page | the `base_account_id` of the `facebook_page_*` row |

Never put a `facebook_page_*` or `linkedin_org_*` id in `account_ids`.

Consequence to tell the user when they ask for a Page or a company page: a bucket you create here holds only the underlying account. It cannot record which Facebook Page or LinkedIn organization it targets. A post to the bucket goes to the account's default destination for that platform (for Facebook the primary Page, for LinkedIn the personal profile) unless the post itself names another target; Page and organization choices stored on a bucket are set in the Bolta dashboard. `list-buckets` shows only the underlying account for such a member (for Facebook, the personal profile's name rather than the Page name), so do not tell the user a bucket "contains the Acme Page" from what you can read. If the destination matters, say what you can and cannot see, and ask them to check in the dashboard.

## "Post to my Launch Team bucket"

This skill resolves, social-publishing acts.
1. `list-buckets`, find the bucket by name (ignore case). If it does not exist, show the buckets that do and offer to create it. Never pick the closest name silently.
2. Check the members' `token_status` in `list-accounts` and say which will be skipped.
3. Hand off to the drafting flow in social-publishing with the bucket's `id`: `create-post(..., social_buckets=["<bucket id>"])`, or `social_buckets` on each item of `bulk-create-posts`. Passing the bucket id keeps the group as the user thinks of it; do not expand it into `account_ids` yourself unless the user wants a subset. Use `account_ids` only when the user names individual accounts.
4. The argument is `social_buckets` (snake_case, a list of bucket ids). `selected_accounts_or_buckets` and camelCase variants are not arguments of `create-post` or `bulk-create-posts`.
5. Drafts first: the post is created as a Draft and moved by the publishing ladder in social-publishing, never from here.

## Errors and what to do

Read the result body (`ok`, `error`, `next_step`); the envelope's `isError` flag is unreliable.

| Result | Do |
|-|-|
| 409 "A bucket named ... already exists" on create | Show the existing bucket and offer to update it. If `list-buckets` does not show that name, a deactivated bucket still holds it (the list shows only active buckets): ask for another name or send them to the dashboard. |
| 409 on rename | Same: the new name is taken. |
| 400 "Unsupported account ids" | You sent a virtual id. Re-resolve through `base_account_id`. Nothing was changed, including the name. |
| 404 "Accounts not found in this workspace" | An id from another workspace or an old read. Re-run `list-accounts`. |
| 404 "Bucket not found" | Re-run `list-buckets`; the id is stale or from another workspace. |
| Permission refusal on a bucket write | Call `get-my-capabilities(workspace_id)` and report the entry in `denied_by`. Do not state a role requirement from memory and do not retry. |
| "Invalid API key", "API key expired", "API key inactive" | The connection is dead. Tell the user to reconnect the Bolta connector (`/mcp` on Claude Code, connector settings in chat). Do not retry. |
| User declines the safety prompt, or the call comes back denied | Stop. Say what was not done. Do not try another tool for the same effect. |

## Do not

- Do not send a partial `account_ids` list to `update-social-bucket`; it is a full replacement. Send the whole list or omit it.
- Do not pass `facebook_page_*` or `linkedin_org_*` ids as bucket members; use `base_account_id`.
- Do not write a bucket without showing the resolved members and the workspace name and getting a yes.
- Do not treat an `invalid` account as connected, and do not claim a reconnect worked until `list-accounts` shows `valid`.
- Do not claim a bucket targets a specific Facebook Page or LinkedIn company page from what `list-buckets` returns.
- Do not guess account or bucket ids, or silently pick the nearest bucket name.
