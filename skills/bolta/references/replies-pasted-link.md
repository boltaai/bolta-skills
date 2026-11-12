# Replies: a pasted link

Read from [joining conversations](replies-joining-conversations.md) when the user pastes a post's link.

Read it with `get-social-content(account_id, target_url)`; its target id and type feed the next call. For Bolta to write, register it first: `draft-engagement-reply` without `opportunity_id`, with `account_id`, `campaign_id`, `platform`, `target_id` and `target_type`, returns an `opportunity_id`; call it again with that id to draft. It needs a `campaign_id` for that account and network: from a search with it, or a past reply in `list-engagements`. A fresh X or LinkedIn account has none: offer to send the user's own words as written with `reply-to-social-content`, or skip. LinkedIn: pass the post text the user pastes as `content`, and say it's their paste.
