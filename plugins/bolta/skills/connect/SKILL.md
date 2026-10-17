---
name: connect
description: >-
  See which accounts are connected, connect or reconnect one, set up account
  groups, add Bolta for another client, or find out what this connection may
  do. Use when someone says connect Instagram, which accounts are connected,
  reconnect LinkedIn, make an account group, which workspace is this, add
  another client, or is everything set up.
---

## Done when

Accounts are shown as connected or disconnected, with a link where needed. Or a group change is saved and read back. Or the user knows, in one line, what this connection can't do and why.

## Know this

- **One connection is one workspace**, picked at sign-in. Nothing here switches workspace or sees another client. Agencies add one connection per client, with "bolta" in its name, so Bolta's checks watch it. Several in one chat: use the one whose workspace the user named; ask once if unclear. Read [references/connections.md](references/connections.md) when adding a client, reconnecting Bolta itself, or after a refusal.
- **Accounts:** valid means connected, invalid means disconnected. A disconnected account is skipped when posts go out, even inside a group. Facebook shows only Pages; LinkedIn adds a row per company page; both copy the parent's status. Count by network and say what you counted.
- **Connect or reconnect:** one link per network, the same for both. It finishes in the browser, on whichever workspace the browser has selected: ask them to check it shows "<workspace>". On "done", read the accounts again.
- **Account groups:** creating one needs no check. Changing one gets a Bolta check every time (no "Bolta checks are on" at the start: ask in words), since posts already in it go to the new members. Members are replaced whole. Use real account ids, never Page or company-page rows. Nothing here deletes a group. Read [references/accounts-and-groups.md](references/accounts-and-groups.md) before any group write.
- **What this connection may do:** read it only after a refusal, or when asked. Say the reason plainly: role, "Your role can't do this"; plan, "Your plan doesn't include this"; connection, "This connection wasn't given that access." Workspace settings always show as not given: by design.
- **Clock and review mode** change only in Bolta Settings: bolta.ai/dashboard/settings/general for the time zone. Never suggest turning review mode off to get past a refusal.
- **Sign-in, not an API key.** The sign-in connection marks Claude's posts as AI drafts, so edits teach the voice, and Bolta keeps them on the review list until approved. A pasted Bolta API key does neither.

## Tools

- `list-workspaces`: this connection's workspace.
- `get-workspace`: clock and review mode.
- `list-accounts`: accounts, connected or disconnected.
- `get-connect-link`: connect or reconnect link, per network.
- `list-buckets`: account groups and members.
- `create-social-bucket`: make an account group.
- `update-social-bucket`: rename a group or change its members (checked).
- `get-my-capabilities`: what this connection may do.

## Hand off

`start`: first-time set-up. `post`: writing posts, including to a group (find it here, pass it whole). `fix`: a post that didn't go out. `review`: approvals. `voice`: your voice. `today`: what needs me.

## Always

- Follow the house rules in the `today` skill.
- Never say an account is connected, or a fix worked, until a fresh read shows it.
- Show a group's members before and after any change, by name and network.
- Never guess the client. The workspace name decides.
