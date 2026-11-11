# Credits on approval

Read when an approval spends credits, is refused for credits, or someone asks what a yes costs. Back to [review-more-decisions.md](review-more-decisions.md).

## What a yes costs

- Charged at approval, from the brand owner's balance: drafts written in Bolta's own chat (and their AI images or video), versions a cascade wrote, a story routine's post, carousel posts and Library entries, and Library posts Bolta wrote (one sent to the client is charged when the client approves). Posts saved here with `create-post` cost nothing on approval. Other routine and campaign drafts, and a story's article, were paid when the run wrote them.
- Out of credits (`INSUFFICIENT_CREDITS`) refuses before anything changes, with `credits_needed` and `credits_remaining` (in a batch, the numbers are in that item's `error` text). Say the numbers, send them to bolta.ai/dashboard/settings/billing, then approve again. The other items in a batch stand.
- `BILLING_UNAVAILABLE`: Bolta couldn't check the balance, so nothing was approved. Try once more shortly.
- When credits were spent, `approve-post` gives `credits_charged`: say it, for example "Approved and scheduled for Tuesday 9:00. That used 2 credits."
