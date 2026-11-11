# Accounts and account groups

## Reading the accounts

- Show network, name and status. No ids. Filter by network (like linkedin or x) only when one is named. Filter by `token_status` yourself.
- valid: connected. invalid: disconnected; it is silently left out when a post goes out, even inside a group, and a post with only disconnected accounts doesn't go out.
- ghost: added without connecting. Its approved drafts are held. Connecting the real account doesn't release them: someone must also move its voice and drafts over in Bolta ([ghost accounts](connect-ghost-accounts.md)). Never call it disconnected or offer a reconnect.
- **Facebook shows only Pages**, one row each (`is_page`); `is_primary` marks the default Page. A Facebook sign-in with no Pages has no row, so "no Facebook" doesn't prove it's disconnected. Say you can't tell, and give bolta.ai/dashboard/account/socials.
- **LinkedIn** shows the personal profile plus one row per company page (`is_organization`). The personal row can be missing.
- Page and company-page rows copy the parent's status; reconnecting the parent fixes them all. Their `base_account_id` is the real account behind them.
- `count` counts rows, not sign-ins. Count by network and say what you counted: "LinkedIn: you and 2 company pages."
- The connect link's list of connected networks leaves Facebook out. Trust the accounts read.

Connecting: [networks](connect-networks.md).

## Account groups

Read them with `list-accounts` and `groups: true`. A post sent to a group goes to every member connected when it goes out, not when scheduled. Read groups and accounts fresh before talking about one.

- **Making, renaming or changing a group happens only in the Bolta web app:** bolta.ai/dashboard/account/socials (the Social Buckets tab). Say it in one line with that link, then on "done" read the groups back and compare with what they wanted.
- **Members are real accounts.** A Facebook Page or LinkedIn company page is not a member; its `base_account_id` is.
- **Several accounts match** ("my LinkedIn" with 2 company pages): ask which, offering the personal one.

**Make a group** ("a group called Launch Team with LinkedIn and X"):
- Compare the name with existing groups, ignoring case. Names match exactly, so "launch team" and "Launch Team" could both exist. Near match: offer to change that one instead.
- Then: "Make it in Bolta at bolta.ai/dashboard/account/socials, then tell me." Read back: "Acme's Launch Team = LinkedIn (Jane), X (@acme)."
- An empty group is allowed: confirm it.

**Change a group** ("add Instagram", "take X out", "rename it"):
- Show before and the after they want: "Launch Team now: LinkedIn, X. After: LinkedIn, X, Instagram. Posts already scheduled to it go to Instagram too." Then the link.
- On "done", read the groups back and show the members by name and network.

**Limits:**
- Deleting a group or changing its icon is also on that page. Offer a rename instead of a delete.
- A group holds the account, not a chosen Page or company page. Its posts go to that account's default (the primary Page; the LinkedIn personal profile). A company-page choice is set on that Bolta page; Facebook Page choices there aren't used. Never say a group "has the Acme Page" from this read.
- To post to a group: `social_buckets` with the group's id on `save-post`, passed whole ([post](post.md)).

## When something doesn't match

See [connect-accounts-and-groups-errors.md](connect-accounts-and-groups-errors.md) for what a missing group, a refused group on a post, or a refusal means and what to do next.

## Always

- Follow the house rules in the Bolta skill.
- Show a group's members before and after any change made in Bolta, by name and network.
