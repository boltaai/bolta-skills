# Account group write failures

What to do when making or changing an account group is refused. Back to [connect-accounts-and-groups.md](connect-accounts-and-groups.md).

- "Already exists": show that group, offer to change it. Not in the list? A retired group holds the name: pick another.
- "Unsupported account ids": a Page or company-page id was sent. Use `base_account_id`.
- "Accounts not found" or "Bucket not found": a stale read, or another client's connection. Read again.
- A create timed out: read groups before retrying, so you don't make it twice.
- A permission refusal: see [connect-connections.md](connect-connections.md).
