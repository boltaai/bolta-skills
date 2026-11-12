# Accounts added without connecting

A person's account added by name, before anyone hands over a login, so Bolta can learn their voice from pasted posts and write drafts for them. In `list-accounts` its `token_status` is `ghost`. Worked: [ghost-account-connect](../examples/ghost-account-connect.json).

## What it does and doesn't

- Bolta writes for it, and its drafts can be approved, but it never posts: an approved draft waits for a connection.
- It is not disconnected. Never call it that and never offer a "reconnect".
- Adding one, replacing its pasted posts and removing it happen in Bolta only: Brand > Accounts, "Connect account" menu, "Add without connecting" (bolta.ai/dashboard/knowledge-base?tab=accounts). Nothing here creates one.

## Connecting is not enough

Connecting the real account leaves the drafts with the added one. They move only when someone hands them over:

1. Best: on that Accounts tab, the added account's row has "Connect <network>". Connecting from there brings the person back to the tab and offers "Move <name>'s voice and drafts to @handle?". Yes moves the voice, the drafts and every other link to the real account, and the added row disappears.
2. Already connected some other way (for example with `get-connect-link`): the row's "Already connected?" button does the same move.

Say: "Connect it from the Accounts tab in Bolta, then say yes to moving <name>'s voice and drafts: bolta.ai/dashboard/knowledge-base?tab=accounts." The person who owns the login connects it; a client connect-only link works for a client ([team-and-integrations](connect-team-and-integrations.md)).

## After the move

- Read `list-accounts` again: the `ghost` row is gone and the real one is valid. Until then, say it hasn't moved.
- Held drafts bind to the real account and go out the way drafts made before a connection do: at their chosen time if still ahead, else the next free slot. A draft still waiting for a yes, or for a client, keeps waiting.
- Re-read with `list-workspace-posts` and the account's id in `account_ids` before saying when anything goes out.

## Always

- Follow the house rules in the Bolta skill.
- Never say drafts will post because the account was connected; only the move releases them.
- Never offer a reconnect for an account added without connecting.
