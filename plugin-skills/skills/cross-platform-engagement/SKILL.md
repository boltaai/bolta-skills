---
name: cross-platform-engagement
description: >
  Run one outbound engagement pass across Threads, Bluesky, Mastodon, X and
  LinkedIn — discover conversations where discovery exists, read them, draft
  native replies, publish after approval, verify. Use this skill when the user
  asks to "engage across my networks", "find conversations on Threads/Bluesky/
  Mastodon", "reply to this X post", "comment on that LinkedIn post", "join
  relevant discussions", or names a platform other than Reddit. For Reddit
  specifically use reddit-engagement (it has the richest adapter); for comments
  on OUR OWN posts use social-inbox. To make this recurring, see "Save this as a
  routine".
---

# Cross-Platform Engagement

The same loop as reddit-engagement, run across the other networks — with one
difference that shapes everything: **platforms differ in what Bolta can do**, and
pretending otherwise is the main way this goes wrong.

## The capability matrix, honestly
| Platform | Keyword discovery | Read a conversation | Reply |
|-|-|-|-|
| Threads | Yes | Yes | Yes |
| Bluesky | Yes | Yes | Yes |
| Mastodon | Yes (hashtag) | Yes | Yes |
| X | **No** — needs elevated API access | Yes | Yes |
| LinkedIn | **No** — no public search | Yes (by post URN) | Yes |
| Facebook / Instagram | No | Read-only | **No** — needs Meta Advanced Access |

For X and LinkedIn the user must supply a URL or post id; you cannot go looking.
Say that plainly rather than searching and returning nothing. Never claim a
platform works because it appears in this table — always confirm with
`list-engagement-capabilities`, which reports the live per-account state.

## Tools this skill uses
| Tool | Why |
|-|-|
| `list-workspaces` / `list-accounts` | Resolve the workspace and the connected accounts. |
| `list-engagement-capabilities` | The authoritative per-account matrix. Call it first, every time. |
| `get-voice-context` | Load the voice; needed to judge relevance. |
| `list-engagements` | Avoid re-engaging something already handled. |
| `search-engagement-opportunities` | Discovery — Threads, Bluesky, Mastodon only. |
| `create-engagement-opportunity` | Register a target the user supplied by URL (the X/LinkedIn path). No `campaign_id` needed. |
| `get-engagement-conversation` | Read the target and its replies. Works everywhere reply does. |
| `draft-engagement-reply` | Draft. Server-side writer, per-platform norms applied for you. |
| `publish-engagement-reply` | Publish after approval; optional `content` edits in the same call. |
| `get-engagement-status` | Verify the canonical URL. |
| `react-to-social-content` | Optional — like / repost / boost / upvote where supported. Confirm first; it is a public action. |

## Prerequisites
- `workspace_id` via `list-workspaces`; auth is automatic, never ask for a key.
- At least one connected account on the target platform.
- Publishing needs owner/admin/creator. On a permission error run
  `get-my-capabilities` and report the missing role rather than retrying.

## Workflow

### 1. Resolve and confirm
`list-workspaces` → `list-accounts` →
`list-engagement-capabilities(workspace_id)`.

Show the user which of their platforms can be engaged and which cannot, before
doing anything. If they asked for a platform with no discovery, say so now and
ask for a URL instead of failing later.

### 2. Load the voice and prior work
`get-voice-context(workspace_id)`, then
`list-engagements(workspace_id)` to see what has already been drafted or sent.

### 3. Find targets

**Where discovery exists (Threads, Bluesky, Mastodon):**
`search-engagement-opportunities(workspace_id, account_id, platform, query,
sort="new")`. One query at a time. `campaign_id` is optional; omit it.

**Where it does not (X, LinkedIn):** ask the user for the URL or post id, then
`create-engagement-opportunity(account_id, platform, target_id)` to register it.
That returns an `opportunity_id` the rest of the flow uses, so a user-supplied
URL reaches the same voice-aware drafting pipeline as a discovered one.

No Hunter campaign is needed — omit `campaign_id` and the target is filed in the
account's own engagement container. Pass one only when the user is deliberately
working inside an existing campaign.

### 4. Read every candidate
`get-engagement-conversation(...)`. Same rule as Reddit: judging from a preview
is how a brand ends up replying to a thread it misread.

### 5. Judge
Skip when you have nothing specific to add, when the point is already made, when
the only available contribution is the pitch, or when the thread is not a
conversation (a poll, a meme, an announcement). Fewer, better replies. Report
what you passed on.

Per-platform instincts worth carrying into the judgement:
- **Threads** — casual, one thought. A long reply is out of place.
- **Bluesky** — dry and skeptical of marketing language; 300 characters hard.
- **Mastodon** — earnest and technical, and openly hostile to promotion. The
  bar for a brand account replying at all is higher here than anywhere else.
- **X** — terse. One clause of substance beats a paragraph.
- **LinkedIn** — resist the platform's own cadence. No one-line-per-sentence
  formatting, no comment-farming question at the end.

### 6. Draft
`draft-engagement-reply(workspace_id, opportunity_id, account_id)`. The
server-side writer applies the platform's norms and length budget along with the
brand voice — you do not need to (and should not) restate them in a prompt.

### 7. Check, approve, publish, verify
Same as reddit-engagement: read the draft critically, show the user the reply
**and the thread**, wait for explicit approval, `publish-engagement-reply`, then
`get-engagement-status` for the canonical URL. Not done until you have a link.

### 8. Reactions (optional)
`react-to-social-content(workspace_id, account_id, platform, target_id,
reaction)` — `like` / `repost` on Bluesky and X, `favourite` / `boost` on
Mastodon, `upvote` on Reddit. These are public actions under the user's account:
ask first. They are idempotent, so a retry is safe.

## Definition of done
- Every platform the user asked about was either engaged or explained.
- Every published reply has a verified canonical URL.
- Nothing published without explicit approval.
- Platforms without discovery were named as such, not silently skipped.

## Failure handling
- `unsupported_platform` on search → that platform has no discovery adapter.
  Offer the supply-a-URL path; do not retry the search.
- `unsupported_platform` on reply → Bolta cannot post there at all (Facebook,
  Instagram today). Say so; offer copy-and-open instead.
- `credentials_expired` → reconnect required. Report, do not retry.
- `target_not_found` → deleted between discovery and drafting; drop it.
- Character-limit surprises → the server enforces platform limits on the draft,
  so a returned reply already fits. If one looks truncated, redraft rather than
  editing it into a fragment.

## Save this as a routine
1. `list-routine-templates()` → `cross_platform_engagement`.
2. `create-routine(...)` with `template_key="cross_platform_engagement"`, a
   schedule, one `source_bindings` entry per account to engage as, and
   `output_config={artifact_type: "reply", count: 3, topics: [...]}`.
3. `activate-routine(...)`.

Bind only accounts on platforms that actually support discovery — a routine
bound to an X account has nothing to search for. `approval_policy` cannot be set
to `auto` on this template; every scheduled reply waits for a human.
