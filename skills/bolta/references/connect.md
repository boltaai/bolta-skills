# Connect

See which accounts are connected, connect or reconnect one, set up account groups, see or add the brands this connection reaches, or find out what this connection may do. Use when someone says connect Instagram, which accounts are connected, reconnect LinkedIn, make an account group, which brand is this, add another client, invite a teammate, or is everything set up.

## Done when

Accounts are shown as connected, disconnected or added without connecting, with a link where needed. Or a group change is saved and read back. Or the user knows, in one line, what this connection can't do and why.

## Know this

- **One connection is one organization**, reaching the brands ticked at sign-in (`list-workspaces`). Several: pass the brand's `workspace_id` on every call; unsure which, ask. A new brand needs a reconnect. Read [references/connections.md](connect-connections.md) when adding a client, reconnecting Bolta itself, or after a refusal.
- **Accounts:** valid means connected, invalid means disconnected, ghost means added without connecting (never call it disconnected). Facebook shows only Pages; LinkedIn adds a row per company page. Both copy the parent's status. A disconnected account is skipped when posts go out, even inside a group. Count by network and say what you counted.
- **Connect or reconnect:** one link per network, the same for both: `get-connect-link(platform)`, platform lower-case (instagram, linkedin, x). It finishes in the browser, on the brand selected there: ask them to check it shows "<brand>". On "done", read the accounts again.
  - Which networks open, WordPress, and what the page shows when it can't: read [references/networks.md](connect-networks.md) before sending a link.
- **Account groups:** creating one needs no check. Changing one gets a Bolta check every time (no "Bolta checks are on" at the start: ask in words), since posts already in it go to the new members. Members are replaced whole. Use real account ids, never Page or company-page rows. Nothing here deletes a group. Read [references/accounts-and-groups.md](connect-accounts-and-groups.md) before any group write.
- **What this connection may do:** read `get-my-capabilities` only after a refusal, or when asked; say the reason plainly: role, "Your role can't do this"; plan, "Your plan doesn't include this"; connection, "This connection wasn't given that access." Workspace settings always show as not given: by design.
- **Brand settings** (clock, review mode, reviewers, `autonomy_mode`): read [references/brand-settings.md](connect-brand-settings.md). They change only in Bolta Settings; never suggest turning review mode off to get past a refusal.
- **Teammates, client links, reviewers, Dropbox, Slack, billing:** read [references/team-and-integrations.md](connect-team-and-integrations.md).
- **Sign-in, not an API key.** Sign-in marks posts made here as AI drafts, so edits teach the voice, and Bolta keeps them on the review list until approved. A pasted Bolta API key does neither.

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
