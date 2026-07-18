---
name: bolta-accounts-and-buckets
description: >
  Inspect connected social accounts and manage social buckets — named groups of accounts
  for one-shot multi-account publishing. Use this skill when the user asks "what's
  connected", "which accounts do I have", "show my social accounts", "create a bucket",
  "make a Launch Team bucket with my LinkedIn and X", "add my Instagram to the launch
  bucket", "rename that bucket", or says "post to my <bucket> bucket" and you need to
  resolve the bucket's member accounts. Not for connecting new accounts (done in the
  Bolta app), drafting content (use bolta-draft-post), or analytics (use
  bolta-analytics-report).
---

# Bolta Accounts & Buckets

Answer "what's connected" and turn natural phrases like "create a bucket called Launch
Team with my LinkedIn and X" into the right tool calls. A **bucket** is a named group of
connected accounts — publishing to a bucket hits every member at once, so buckets are how
users say "post this to the launch crew" without listing UUIDs. The connected-accounts
card these tools render has **Socials** and **Buckets** tabs — accounts on one, buckets
(with their members) on the other.

## When to use
Any question about which social accounts are connected, plus creating, renaming, or
re-membering buckets — or resolving a bucket name into account ids for another skill.

## Tools this skill uses
| Tool | Why |
|-|-|
| `list-workspaces` | Resolve `workspace_id` if unknown. |
| `list-accounts` | Connected accounts + their UUIDs — the ONLY source of `account_ids`. Optional `platform` filter. Renders the accounts card (Socials tab). |
| `list-buckets` | The workspace's buckets with member accounts (id, platform, username). Renders the accounts card (Buckets tab). |
| `create-social-bucket` | Create a bucket: `name` (unique per workspace) + `account_ids`. |
| `update-social-bucket` | Rename a bucket and/or replace its members (`account_ids` is a FULL replacement list). |
| `get-my-capabilities` | Diagnose permission errors on bucket writes (needs accounts:write). |

## Prerequisites
- `workspace_id` — resolve once via `list-workspaces`, reuse for every call. Auth is automatic
  via the Bolta connector's OAuth grant — never ask for an API key.
- Reads need any role; creating/updating buckets needs **accounts:write** (editor+).
  (Elsewhere, default new content to Draft; confirm before publish/delete.)

## Workflow

### 1. Resolve the workspace
Call `list-workspaces` and use the active workspace's `id`. Never guess a UUID.

### 2. "What's connected?"
Call `list-accounts(workspace_id)` (add `platform` if the user named one) and, in parallel,
`list-buckets(workspace_id)`. Present both halves the way the card does — Socials: each
account's platform + username + status; Buckets: each bucket's name and members. If nothing
is connected, say so and point the user to the Bolta app to connect accounts (there is no
connect tool here).

### 3. Create a bucket
"Create a bucket called Launch Team with my LinkedIn and X":
1. `list-accounts(workspace_id)` → match the named platforms/usernames to accounts and take
   their **base account UUIDs** (never virtual `linkedin_org_` / `facebook_page_` ids).
   If a platform matches several accounts, ask which one.
2. Confirm the resolved members with the user ("Launch Team = LinkedIn @acme + X @acme — 
   create it?").
3. `create-social-bucket(workspace_id, name="Launch Team", account_ids=[…])`.
Bucket names are unique per workspace — an exact duplicate 409s (see failures).

### 4. Update a bucket
"Add my Instagram to the Launch Team bucket" / "rename it":
1. `list-buckets(workspace_id)` → find the bucket, note its `bucket_id` AND current members.
2. Build the new membership: current member ids ± the change (ids from `list-accounts`).
   `account_ids` is a **full replacement** — sending only the new account would drop the rest.
3. `update-social-bucket(workspace_id, bucket_id, account_ids=[…full new list…])`; pass
   `name` for renames. Repeating the same update is safe (idempotent).

### 5. "Post to my <bucket> bucket"
This skill resolves; drafting skills act. Call `list-buckets`, find the bucket by name, and
hand its member `account_ids` to **bolta-draft-post** / `create-post` (or use the bucket with
`voice-generate`'s `selectedAccountsOrBuckets`). If the named bucket doesn't exist, show the
buckets that do and offer to create it.

## Failure handling
- Bucket name already exists (409 on create) → show the existing bucket and offer to update
  it instead of creating a duplicate.
- Permission error on create/update → run `get-my-capabilities`, report the missing
  accounts:write role plainly, don't retry.
- Named account not found → show `list-accounts` output and ask; never guess an id, and never
  pass virtual `linkedin_org_` / `facebook_page_` ids as bucket members.
- Empty bucket request (no resolvable accounts) → create with `name` only is allowed, but
  confirm the user really wants an empty bucket.

## Example
User: "What's connected? And make a bucket called Launch Team with LinkedIn and X."
1. `list-workspaces` → workspace_id.
2. `list-accounts(workspace_id)` + `list-buckets(workspace_id)` → LinkedIn @acme,
   X @acme, IG @acme.shop; no buckets yet.
3. "3 accounts connected (LinkedIn, X, Instagram), no buckets. Create Launch Team =
   LinkedIn @acme + X @acme?" → yes.
4. `create-social-bucket(workspace_id, name="Launch Team", account_ids=[li_id, x_id])`.
5. "Launch Team created with 2 members — say 'post to my Launch Team bucket' any time to
   hit both at once."
