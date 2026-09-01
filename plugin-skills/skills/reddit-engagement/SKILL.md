---
name: reddit-engagement
description: >
  Find Reddit threads this brand can genuinely help with, read them, draft native
  replies, publish them after approval, and verify the canonical URL. Use this
  skill when the user asks to "reply on Reddit", "find Reddit conversations",
  "engage on Reddit", "who's talking about this on Reddit", "join that thread",
  "comment on Reddit for me", or wants outbound participation in subreddit
  discussions. For the same loop across Threads/Bluesky/Mastodon use
  cross-platform-engagement; for replying to comments left on OUR OWN posts use
  social-inbox; for writing a new post use social-publishing. To make this run on
  a schedule instead of now, see "Save this as a routine" at the end.
---

# Reddit Engagement

Join conversations other people are already having, usefully. The whole skill is
one loop — discover, read, judge, draft, approve, publish, verify — and the
hardest step is the judging, not the writing.

## When to use
The user wants to participate in Reddit threads the brand did not start. One
pass produces a small number of replies (two or three is a good outing), each to
a different thread, each adding something specific.

## Tools this skill uses
| Tool | Why |
|-|-|
| `list-workspaces` | Resolve `workspace_id` once and reuse it. |
| `list-accounts` | Find the connected Reddit account and its UUID. |
| `list-engagement-capabilities` | Confirm Reddit discovery/reply are actually available for that account before trying. |
| `get-voice-context` | Load the brand's voice and what it actually does — you cannot judge relevance without it. |
| `list-business-dna` | Optional; find the DNA entry when voice context is thin. |
| `get-business-dna` | Optional; read that entry — it needs a `dna_id`, so list first. |
| `list-engagements` | See what has already been drafted or sent, so you do not reply twice. |
| `search-engagement-opportunities` | Find recent submissions. Synchronous — results come back in the call. |
| `get-engagement-conversation` | Read the submission and its comments before deciding. |
| `draft-engagement-reply` | Draft the reply. The writer is server-side; you do not write the text. |
| `publish-engagement-reply` | Publish after the user approves. Optional `content` sends an edited version in the same call. |
| `get-engagement-status` | Verify: did it land, and at what canonical URL. |
| `create-engagement-opportunity` | Only when the user supplies a specific Reddit URL instead of asking you to search. No `campaign_id` needed. |

## Prerequisites
- `workspace_id` — resolve once via `list-workspaces`. Auth is automatic through
  the Bolta connector's OAuth grant; never ask for an API key.
- A connected Reddit account. If none exists, use `get-connect-link` with
  `platform="reddit"` and stop — you cannot engage without an identity.
- Publishing a reply needs an **owner/admin/creator** role. If a call returns a
  permission error, run `get-my-capabilities`, say which role is missing, and do
  not retry.

## Workflow

### 1. Resolve workspace and account
`list-workspaces` → `list-accounts(workspace_id)`. Pick the Reddit account. If
there are several, ask which identity to speak as — this is a public reply under
somebody's username.

### 2. Confirm the capability
`list-engagement-capabilities(workspace_id, platform="reddit")`. Check
`discover`, `reply_to_post` and `reply_to_comment` for the chosen account. An
account whose credentials need reconnecting is reported with its capabilities
downgraded — say so and stop rather than failing later at publish time.

### 3. Load the voice
`get-voice-context(workspace_id)`. You need this to judge relevance, not to
write: the reply text is generated server-side. What you are looking for is what
the brand actually does, who it is for, and what it would never say.

`get-voice-context` already returns the resolved Business DNA context, so it is
usually enough on its own. If you need the deeper DNA record, take the id from
its provenance — or call `list-business-dna` — and then `get-business-dna(dna_id)`.
`get-business-dna` requires a `dna_id`; there is no workspace-wide form of it.

### 4. Check what has already been done
`list-engagements(workspace_id, platform="reddit")`. Replying twice to the same
thread, or re-engaging a thread from last week's run, is the most visible way to
look automated.

### 5. Search
`search-engagement-opportunities(workspace_id, account_id, platform="reddit",
query=..., subreddit=..., sort="new", time_filter="week")`.

Search one term at a time, and use terms people would actually type. Derive them
from the voice context and the user's ask, not from product marketing language.
`campaign_id` is optional — omit it unless the user is working inside a specific
Hunter campaign.

### 6. Read before judging
For each candidate that looks plausible, `get-engagement-conversation(...,
target_id=..., comment_limit=20)`. Read the submission AND the comments. This is
not optional: most of the value of this skill is in the threads you skip, and
you cannot skip well from a title.

### 7. Judge — this is the actual work
**Skip the thread when:**
- you have nothing specific to add beyond agreement;
- the question is already answered well in the comments;
- the only thing you could say is a version of the product pitch;
- it is a rant, a poll, a meme, or a support request for somebody else's tool;
- it is old enough that a new comment reads as thread necromancy;
- the subreddit's rules or culture clearly do not welcome a brand account.

Two good replies and an explanation of why you passed on the rest is a
**successful** run. Padding to a number with weak replies is a failed one. Tell
the user what you skipped and why — that judgement is the thing they are
trusting you with.

### 8. Draft
`draft-engagement-reply(workspace_id, opportunity_id, account_id)`.

You are not writing the reply. Bolta's outbound engagement writer produces it
server-side and already enforces the brand voice, Reddit's conventions, and the
rules that matter here — no summarizing the OP, no generic praise opener, one
specific contribution, participant not commentator, no forced slang, no
thought-leadership cadence, and no brand mention unless the context genuinely
calls for one. Your job is picking the right target and giving the writer the
conversation.

Calling it twice for the same opportunity returns the existing draft rather than
producing a second one.

### 9. Check the draft before showing it
Read what came back and sanity-check it against the same bar:
- Does it add something, or does it restate the post?
- Is it short — usually under 80 words for Reddit?
- Does it mention the brand for no reason? (It should not.)
- Would it read as a person in that subreddit, or as a company?

If it fails, say so plainly and offer to redraft with a different angle, or drop
the thread. Do not silently publish a reply you would not have written.

### 10. Approve
Show the user the reply **and the thread it is going into**, with the permalink.
Wait for an explicit go-ahead. A Reddit comment is public and attached to a real
username; this is not a step to infer consent for.

If they want a change, pass the edited text as `content` to
`publish-engagement-reply` — one call edits and sends.

### 11. Publish
`publish-engagement-reply(workspace_id, engagement_id, content?)`. Idempotent by
construction: one reply per target, so a retry after a network failure returns
the original rather than double-posting.

### 12. Verify
`get-engagement-status(workspace_id, engagement_id)`. **Not done until this
returns a real canonical URL** or an explicit pending/failed state. Report the
URL to the user. A reply you cannot link to has not been verified, whatever the
publish call returned.

## Definition of done
- Every thread you engaged has a canonical Reddit URL reported back.
- Every thread you skipped has a one-line reason.
- Nothing was published without an explicit approval.
- No thread received two replies.

## Failure handling
- `unsupported_platform` on search → discovery is not available; stop, do not
  retry with different parameters.
- `account_missing` → no Reddit account attached; `get-connect-link` and stop.
- `credentials_expired` → the account needs reconnecting. Say so; do not retry.
- `target_not_found` / `target_deleted` → the submission went away between
  discovery and drafting. Drop it and move on; this is normal.
- `invalid_subreddit` → the campaign has no configured subreddits and none was
  given. Ask the user which subreddit.
- Permission error on publish → `get-my-capabilities`, report the missing role,
  do not retry.
- Rate limiting → report it and stop. Reddit rate limits are per-account and
  waiting is the only fix.

## Save this as a routine
When the user wants this to keep happening — "do this every weekday morning" —
do not build an agent. Create a routine:

1. `list-routine-templates()` → find `reddit_engagement`.
2. `create-routine(template_key="reddit_engagement", name=...,
   goal=<the user's own words>, trigger_type="schedule",
   schedule={"cron": "0 10 * * 1-5"}, timezone=<their zone>,
   instructions=<their steer>, source_bindings=[{provider: "social_account",
   ref: <reddit account id>}], output_config={artifact_type: "reply", count: 3,
   topics: [...], communities: [...]})`.
3. `activate-routine(routine_id)` — it is a draft until you do.

Notes:
- The schedule vocabulary is `daily` / `weekly` / `monthly` plus `cron`.
  "Weekdays at 10am" is `{"cron": "0 10 * * 1-5"}`.
- Times are wall-clock in the routine's timezone. Never send a UTC offset and
  never convert the user's stated time yourself.
- `approval_policy` defaults to `review_every_artifact` and this template does
  **not** allow `auto`. Every scheduled reply waits for a human. Say that out
  loud — it is the reassurance the user actually wants.
- Scheduled runs draft only; the drafts land in the review queue
  (`list-inbox-items`) and are published from there.
