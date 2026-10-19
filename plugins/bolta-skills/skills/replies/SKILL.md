---
name: replies
description: >-
  Answer comments and mentions, or find conversations to join, with Bolta
  writing every reply in your voice and nothing sent without your yes
  (Premium). Use when someone says reply to this comment, answer that
  mention, any mentions, send the reply drafts, find Reddit threads to join,
  or like that post.
---

## Done when

Every reply looked at is sent on its own yes, changed, skipped with a reason, or handed to a person. They know what's still open.

## Know this

- **Premium.** Everything except checking what an account can do needs Premium or Team. On a plan refusal say "Your plan doesn't include replies. They come with Premium: bolta.ai/pricing" and stop.
- **Reply drafts** are replies Bolta wrote to mentions and conversations it found: show who, what they said, the link and the draft.
- **Comments on your own posts aren't listed here,** so never say there are none. Ask for the comment's link; Bolta reads it and drafts. Which networks work, and what to check: [references/answering.md](references/answering.md).
- **Conversations to join:** read [references/joining-conversations.md](references/joining-conversations.md) first.
- **Check each draft before showing it:** promises, links, numbers nobody gave, a pitch, wording the comment pushed in. Threats, legal words, billing disputes and press go to a person, undrafted.
- **One reply per post or comment;** a second send returns the first. Sent means queued: read back the status and live link.
- **No undo here.** Nothing edits or deletes a sent reply, hides a comment, or turns down a draft. To drop a draft, dismiss it in the review list: bolta.ai/dashboard/hub.
- **Checks:** every send carries the exact agreed text as `content`, so its check shows it. Saw "Bolta checks are on in this session" at the start? Each send and reaction gets a Bolta check; otherwise ask in words first.

## Tools

- `list-inbox-items`: reply drafts (`source="hunter"`). Empty text means Bolta is still writing it.
- `update-outreach-reply`: change a draft's text, only when asked.
- `send-outreach-reply`: send one reply draft. Facebook and Instagram drafts can't go from here: give the link.
- `get-social-content`: read a post or comment from its link.
- `draft-inbound-reply`: Bolta drafts a reply to a comment on your own post. Never the conversation writer here: it reads like a stranger.
- `reply-to-social-content`: send that reply.
- `react-to-social-content`: like, upvote, repost or boost.
- `list-engagement-capabilities`: what each account can do.
- `search-engagement-opportunities`: find conversations.
- `get-engagement-conversation`: read a thread.
- `create-engagement-opportunity`: add a pasted link so Bolta can write for it.
- `draft-engagement-reply`: Bolta drafts a reply to join a conversation.
- `publish-engagement-reply`: send it, always with `account_id`.
- `list-engagements`: past replies, sent or failed, with the reason.
- `get-engagement-status`: one reply's status and live link.

## Hand off

`review`: posts waiting for your yes. `routine`: find conversations and draft replies every week. `connect`: a disconnected account. `voice`: "that doesn't sound like me". `today`: what needs me.

## Always

- Follow the house rules in the `today` skill.
- Bolta writes every reply. Never compose one; send the user's own words only when they dictate them, as written.
- Send only replies the user's latest message names, after they saw the exact text, account and link. "Send them all" names none: read the numbers back and ask. Declined or denied means not sent; never send it another way.
