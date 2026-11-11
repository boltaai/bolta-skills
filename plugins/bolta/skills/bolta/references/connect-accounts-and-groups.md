# Accounts and account groups

## Reading the accounts

- Show network, name and status. No ids. Filter by network (like linkedin or x) only when one is named. Filter by `token_status` yourself.
- valid: connected. invalid: disconnected; it is silently left out when a post goes out, even inside a group, and a post with only disconnected accounts doesn't go out.
- ghost: added without connecting. Drafts for it are held and it never publishes until connected. Never call it disconnected; offer the connect link.
- **Facebook shows only Pages**, one row each (`is_page`); `is_primary` marks the default Page. A Facebook sign-in with no Pages has no row, so "no Facebook" doesn't prove it's disconnected. Say you can't tell, and give bolta.ai/dashboard/account/socials.
- **LinkedIn** shows the personal profile plus one row per company page (`is_organization`). The personal row can be missing.
- Page and company-page rows copy the parent's status; reconnecting the parent fixes them all. Their `base_account_id` is the real account behind them.
- `count` counts rows, not sign-ins. Count by network and say what you counted: "LinkedIn: you and 2 company pages."
- The connect link's list of connected networks leaves Facebook out. Trust the accounts read.

## Connecting

- Say: "Connecting happens in your browser. Check the workspace switcher shows Acme first." The link carries no brand; the browser's selection picks it.

## Account groups

A post sent to a group goes to every member connected when it goes out, not when scheduled. Read groups and accounts fresh before any write.

- **Members are real accounts.** Most rows: the row's own id. A Facebook Page or LinkedIn company page: its `base_account_id`. A Page or company-page id is refused, and nothing changes, not even a rename.
- **Several accounts match** ("my LinkedIn" with 2 company pages): ask which, offering the personal one.

**Make a group** ("a group called Launch Team with LinkedIn and X"):
- Compare the name with existing groups, ignoring case. Names match exactly, so "launch team" and "Launch Team" could both exist. Near match: offer to change that one instead.
- No check. Read the groups back, then: "Saved to Acme: Launch Team = LinkedIn (Jane), X (@acme)."
- An empty group is allowed: confirm it.

**Change a group** ("add Instagram", "take X out", "rename it"):
- The members you send become the whole group. Send current members plus or minus the change. Sending only the new one removes everyone else.
- Rename only: leave members out. An empty list empties the group.
- Show before and after: "Launch Team now: LinkedIn, X. After: LinkedIn, X, Instagram. Posts already scheduled to it go to Instagram too."
- Saw "Bolta checks are on in this session" at the start? The Bolta check is the ask; otherwise get a yes in words.
- Read the groups back and compare with what you promised.

**Limits:**
- Nothing here deletes a group or changes its icon: bolta.ai/dashboard/account/socials (the Social Buckets tab). Offer a rename instead.
- A group made here holds the account, not a chosen Page or company page. Its posts go to that account's default (the primary Page; the LinkedIn personal profile). A company-page choice is set on that Bolta page; Facebook Page choices there aren't used. Never say a group "has the Acme Page" from this read.

## When a write fails

See [connect-accounts-and-groups-errors.md](connect-accounts-and-groups-errors.md) for what each refusal means and what to do next.
