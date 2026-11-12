# Account group problems

What to do when a group read or a post to a group doesn't match. Groups are made and changed only in the Bolta web app (bolta.ai/dashboard/account/socials). Back to [connect-accounts-and-groups.md](connect-accounts-and-groups.md).

- A name "already exists" in Bolta: show that group, offer to change it there. Not in the list? A retired group holds the name: pick another.
- A Page or company page can't be a member: in Bolta, pick the real account (its `base_account_id` here).
- A group "not found" on a post, or accounts missing from it: a stale read, or another client's connection. Read groups again with `list-accounts` and `groups: true`.
- They say it's done but the read doesn't show it: the change went to another brand, or wasn't saved. Ask them to check the brand switcher in Bolta.
- A permission refusal: see [connect-connections.md](connect-connections.md).

## Always

- Follow the house rules in the Bolta skill.
- Read the groups again before any retry.
