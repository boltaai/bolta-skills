---
name: social-inbox
description: >
  Work the inbound side — comments and mentions on the brand's own content across
  every connected platform — and reply to them. Use this skill when the user asks
  "any comments?", "what did people say", "reply to my mentions", "who replied to
  my post", "clear the inbox", "anyone talking to us", or wants inbound
  conversations triaged and answered. Inbound only: for replying to strangers'
  posts the brand did not start, use reddit-engagement or
  cross-platform-engagement. For approving drafted content use bolta-review-queue.
---

# Social Inbox

Answer the people who are already talking to you. Inbound replies are a different
writing task from outbound engagement — someone came to your post, so the reply
is a response, not an entrance — and Bolta uses a different server-side writer
for each. Keeping them separate is the point of this skill.

## When to use
Someone commented on the brand's post, mentioned the brand, or replied to a
reply. The user wants to see it and respond.

## Tools this skill uses
| Tool | Why |
|-|-|
| `list-workspaces` | Resolve `workspace_id` once. |
| `list-inbox-items` | The unified inbox. Every source in one call; filter with `source`. |
| `get-social-content` | Pull the full item and its thread when a preview is not enough. |
| `reply-to-social-content` | Reply to a comment or mention on a target you have. |
| `send-hunter-reply` | Send a hunter-drafted reply (optional `content` edits in the same call). |
| `update-hunter-reply` | Edit a hunter draft without sending it. |
| `draft-inbound-reply` | Draft a reply in the brand voice. Reads the comment AND the post it is on, then routes through the INBOUND writer. Creates and sends nothing. |
| `get-voice-context` | Load the voice before drafting anything. |
| `react-to-social-content` | Optional — like a comment instead of replying. |
| `list-engagement-capabilities` | Confirm the platform supports replying before promising it. |
| `get-my-capabilities` | Diagnose a permission refusal. |

## Prerequisites
- `workspace_id` via `list-workspaces`; auth is automatic, never ask for a key.
- Sending replies needs owner/admin/creator.
- Facebook and Instagram comments can be **read** but not replied to through
  Bolta today (Meta Advanced Access). Say so and offer the permalink instead of
  attempting a send.

## Workflow

### 1. Pull the inbox
`list-inbox-items(workspace_id)`. Each row carries a `source`:
- `comment` — someone commented on our post;
- `hunter` — an outbound reply draft awaiting a decision (that belongs to
  bolta-review-queue, but surface it so nothing is invisible);
- `recurring` / `team` — content drafts pending approval, not inbound;
- `report` — an agent report, read-only.

Filter to the inbound sources when the user asked about comments and mentions,
but tell them what else is waiting.

### 2. Summarize before acting
Group by platform and by post. For each item give one line: who, what they said,
and which of the brand's posts it is on. A list of twenty raw comments is not a
summary — say "eight comments on the launch post, mostly asking about pricing;
two on Threads about the integration".

### 3. Triage
Not every comment needs a reply. Sort into:
- **Answer** — a real question, a misunderstanding worth correcting, or someone
  who took the time to write something substantive.
- **React** — appreciation, agreement, a compliment. A like is the honest
  response; a written reply to "nice!" is filler.
- **Leave** — spam, bait, or an argument that a reply will only extend.
- **Escalate** — an angry customer, a factual complaint, anything legal or
  safety-adjacent. Do not draft a reply; tell the user it needs them.

Present the triage and let the user adjust it before you send anything.

### 4. Read the full context when replying
`get-social-content(workspace_id, account_id, platform, target_id)` for the
thread. A comment often makes sense only against what was said above it, and a
reply written from the snippet alone is how you answer a question nobody asked.

### 5. Draft
**Always draft through a tool. Never compose the reply yourself.** Reading the
comment — with `list-inbox-items`, `get-social-content`, whatever — is the INPUT
to drafting, not a substitute for it. A reply you write directly is in your
voice, not the workspace's, and it silently bypasses the Voice Profile and
Business DNA that are the whole reason the customer connected Bolta. Having read
the row, the next call is a drafting tool.

Prefer the tool that matches the row:
- **Hunter draft** → it already has text. `update-hunter-reply` to revise,
  `send-hunter-reply` to send (optionally with `content` to do both at once).
- **Comment on our post** → draft first with
  `draft-inbound-reply(account_id, target_url)` (or `platform` + `target_id`).
  It reads the comment and the post it was left on, routes through the inbound
  writer, and returns text — it creates nothing and sends nothing. Then send the
  approved text with `reply-to-social-content(account_id, platform, target_id,
  content)`.

  Use `draft-inbound-reply`, never `draft-engagement-reply`, for anything on our
  own content. They route to different server-side writers and picking the wrong
  one is silent: the reply comes back on-brand and reads as though a stranger
  wandered into the thread.

Inbound replies are short and direct. Answer the question in the first sentence.
Do not thank people for engaging, do not restate their comment back to them, and
do not turn a one-line answer into a paragraph.

### 6. Approve and send
Show the user each reply next to the comment it answers. Get an explicit
go-ahead — these are public and attached to the brand's account. Batches are
fine, but say how many are going out and to which platforms.

### 7. Verify
Confirm each send landed. For hunter replies, double-send is prevented
server-side, so a retry after a timeout is safe. Report anything that failed and
why, rather than reporting the batch as sent.

## Definition of done
- Every inbound item is answered, reacted to, left with a reason, or escalated.
- Nothing was sent without approval.
- Items on platforms Bolta cannot reply to were handed over as permalinks, not
  silently dropped.
- The user knows what is still waiting.

## Failure handling
- `unsupported_platform` on reply → Bolta cannot post there (Facebook,
  Instagram). Give the permalink; do not retry.
- `credentials_expired` → reconnect required; report and stop.
- 409 on `update-hunter-reply` → the reply was already sent. Do not resend; show
  its current state.
- Permission error → `get-my-capabilities`, name the missing role, do not retry.
- Empty inbox → say it is clear, and say when it was last checked.

## Save this as a routine
For "check this every morning":
1. `list-routine-templates()` → `social_inbox_engagement`.
2. `create-routine(...)` with a schedule and the accounts to watch bound as
   `source_bindings`.
3. `activate-routine(...)`.

Scheduled runs draft only and never send. Every reply lands in the review queue
for a human — this template does not permit `auto` approval, and that is
deliberate.
