# Connect

See which accounts are connected, connect or reconnect one, see account groups (made and changed in the Bolta web app), see or add the brands this connection reaches, or find out what this connection may do. Use for: connect Instagram, which accounts are connected, reconnect LinkedIn, make an account group, which brand is this, add a client, invite a teammate, is everything set up.

## Done when

Accounts are shown as connected, disconnected or added without connecting, with a link where needed. Or a group the user made or changed in Bolta is read back. Or the user knows, in one line, what this connection can't do and why.

## Know this

- **One connection is one organization**, reaching the brands ticked at sign-in (`list-workspaces`). Several: pass the brand's `workspace_id` on every call; unsure which, ask. A new brand needs a reconnect. Adding a client, reconnecting Bolta itself, a refusal: [references/connections.md](connect-connections.md).
- **Accounts:** valid means connected, invalid means disconnected, ghost means added without connecting: never disconnected, and connecting alone doesn't release its drafts ([ghost accounts](connect-ghost-accounts.md)). Facebook shows only Pages; LinkedIn adds a row per company page. Both copy the parent's status. A disconnected account is skipped when posts go out, even inside a group. Count by network.
- **Connect or reconnect:** one link per network, the same for both: `get-connect-link(platform)`, platform lower-case (instagram, linkedin, x). It finishes in the browser, on the brand selected there: ask them to check it shows "<brand>". On "done", read the accounts again.
  - Which networks open, WordPress, and what the page shows when it can't: read [references/networks.md](connect-networks.md) before sending a link.
- **Account groups:** read them with `list-accounts` and `groups: true`. Making, renaming or changing one happens only in the Bolta web app, in one line with one link: bolta.ai/dashboard/account/socials (the Social Buckets tab). Posts already in a group go to its new members. On "done", read the groups back. A post goes to a group with `social_buckets` on `save-post`. Read [references/accounts-and-groups.md](connect-accounts-and-groups.md) first.
- **What this connection may do:** nothing lists it ahead of time; a refusal names the role, plan or access that's missing. Say it plainly, in the words on [refusals](connect-refusals.md).
- **Brand settings** (clock, review mode, reviewers, `autonomy_mode`): read [references/brand-settings.md](connect-brand-settings.md). They change only in Bolta; never suggest turning review mode off to pass a refusal.
- **Teammates, roles, client links, reviewers, integrations, billing:** read [references/team-and-integrations.md](connect-team-and-integrations.md) and [people and roles](connect-people-and-roles.md).
- **Sign-in, not an API key.** Posts made here teach the voice either way: a yes, an edit or a no with a reason. Sign-in also keeps them on the review list until approved; a pasted Bolta API key can schedule or publish without a yes.

## Tools

- `list-workspaces`: the brands this connection reaches, with your role and organization; each row is the brand's full settings (clock, review mode, approval settings).
- `list-accounts`: accounts and their status; with `groups: true`, account groups and members; with `capabilities: true`, what each account can do for replies.
- `get-connect-link`: connect or reconnect link, per network.

## Hand off

[start](start.md): first-time set-up. [post](post.md): writing posts, including to a group (find it here, pass it whole). [fix](fix.md): a post that didn't go out. [review](review.md): approvals. [voice](voice.md): your voice. [today](today.md): what needs me.

## Always

- Follow the house rules in the Bolta skill.
- Never say an account is connected, or a fix worked, until a fresh read shows it.
- Show a group's members before and after a change made in Bolta, by name and network.
- Never guess the brand. The user's words decide; unsure, ask.
