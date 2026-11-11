# Reddit: the limits on replies

Read before sending or promising any Reddit reply, or when one is queued, held or removed. Back to [held-and-inbox](replies-held-and-inbox.md).

## Whose yes counts

Bolta paces Reddit replies to protect the account, and skips most of that pacing for a person's approval. A yes in this chat is not always one:

- `send-outreach-reply` on a reply draft counts as the person's approval, except a warm-up row (`warmup_requires_human`): the person approves those in Bolta themselves.
- `reply-to-social-content` and `publish-engagement-reply` count as Bolta sending on its own, even after the user's yes here. Every limit below applies.

So say "queued" when a status read shows it queued, never "it's posting now".

## The limits

- **New or low-karma accounts** (under 30 days old, under 100 karma, or no verified email) are paced, even with a person's approval.
- **Unattended pacing** (the two sends above): a few replies a day by account age (2 a day from 30 days old, 4 from 90, 6 from 180), at least 45 minutes apart, one per subreddit a day. Over a limit Bolta holds the reply: `pending`, `needs_approval` true, with the reason. A person releases it in Bolta's Inbox; never resend it from here.
- **The subreddit's own rules** hold any reply, a person's approval included, in a community that bans bots or AI, has closed comments, or sets karma or age minimums the account doesn't meet. Quote the hold reason. Those rules can't be read from here.
- **Removed by Reddit:** a `failed` row whose reason starts `REMOVED_BY_PLATFORM` was taken down. Don't resend. Bolta pauses unattended Reddit replies from that account for 72 hours (7 days after a second removal within 7 days, or one only the author can see), and skips that subreddit after an AutoModerator removal.
- **A suspended or banned account** blocks every send ([connect](connect.md)).
- **Locked or archived threads:** an unattended reply is dropped for good.
- A rate limit: stop. "Rate limited (conservative)": Bolta resends shortly, so report it queued. "Reddit refused this wording": Bolta holds the draft unchanged; the user rewords it and approves it in Bolta. Never resend the same text.

## Checking it

`get-engagement-status(engagement_id, verify=true)`. `missing_or_removed` comes only from Reddit: sent, then taken down. On other networks a taken-down reply may show only `verification_failed`, so say "couldn't confirm it's still up", not "it failed".

## Always

- Follow the house rules in the Bolta skill.
- Never resend, reword or switch tools to get past a Reddit hold, pause or removal.
- Never call a chat yes sent with `reply-to-social-content` or `publish-engagement-reply` a person's approval.
