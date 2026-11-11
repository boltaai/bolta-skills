# Connect

See which accounts are connected, connect or reconnect one, set up account groups, see or add the brands this connection reaches, or find out what this connection may do. Use for: connect Instagram, which accounts are connected, reconnect LinkedIn, make an account group, which brand is this, add a client, invite a teammate, is everything set up.

## Done when

Accounts are shown as connected, disconnected or added without connecting, with a link where needed. Or a group change is saved and read back. Or the user knows, in one line, what this connection can't do and why.

## Know this

- **One connection is one organization**, reaching the brands ticked at sign-in (`list-workspaces`). Several: pass the brand's `workspace_id` on every call; unsure which, ask. A new brand needs a reconnect. Adding a client, reconnecting Bolta itself, a refusal: [references/connections.md](connect-connections.md).
- **Accounts:** valid means connected, invalid means disconnected, ghost means added without connecting: never disconnected, and connecting alone doesn't release its drafts ([ghost accounts](connect-ghost-accounts.md)). Facebook shows only Pages; LinkedIn adds a row per company page. Both copy the parent's status. A disconnected account is skipped when posts go out, even inside a group. Count by network.
- **Connect or reconnect:** one link per network, the same for both: `get-connect-link(platform)`, platform lower-case (instagram, linkedin, x). It finishes in the browser, on the brand selected there: ask them to check it shows "<brand>". On "done", read the accounts again.
  - Which networks open, WordPress, and what the page shows when it can't: read [references/networks.md](connect-networks.md) before sending a link.
- **Account groups:** creating one needs no check. Changing one gets a Bolta check every time (no "Bolta checks are on" at the start: ask in words), since posts already in it go to the new members. Members are replaced whole. Read [references/accounts-and-groups.md](connect-accounts-and-groups.md) before any group write.
- **What this connection may do:** read `get-my-capabilities` only after a refusal, or when asked; say the reason plainly: "Your role can't do this", "Your plan doesn't include this" or "This connection wasn't given that access." Workspace settings always show as not given: by design.
- **Brand settings** (clock, review mode, reviewers, `autonomy_mode`): read [references/brand-settings.md](connect-brand-settings.md). They change only in Bolta; never suggest turning review mode off to pass a refusal.
- **Teammates, roles, client links, reviewers, integrations, billing:** read [references/team-and-integrations.md](connect-team-and-integrations.md) and [people and roles](connect-people-and-roles.md).
- **Sign-in, not an API key.** Posts made here teach the voice either way: a yes, an edit or a no with a reason. Sign-in also keeps them on the review list until approved; a pasted Bolta API key can schedule or publish without a yes.

## Tools

- `list-workspaces`: the brands this connection reaches, with your role and organization.
- `get-workspace`: a brand's clock, review mode and approval settings.
- `list-accounts`: accounts and their status.
- `get-connect-link`: connect or reconnect link, per network.
- `list-buckets`: account groups and members.
- `create-social-bucket`: make an account group.
- `update-social-bucket`: rename a group or change its members (checked).
- `get-my-capabilities`: what this connection may do.

## Hand off

[start](start.md): first-time set-up. [post](post.md): writing posts, including to a group (find it here, pass it whole). [fix](fix.md): a post that didn't go out. [review](review.md): approvals. [voice](voice.md): your voice. [today](today.md): what needs me.

## Always

- Follow the house rules in the Bolta skill.
- Never say an account is connected, or a fix worked, until a fresh read shows it.
- Show a group's members before and after any change, by name and network.
- Never guess the brand. The user's words decide; unsure, ask.
