# Connections, clients and access

## One connection, one workspace

- The workspace is picked on Bolta's sign-in page, whose list starts on the first one, not always the one meant.
- `list-workspaces` returns only that one. There is no switch and no all-clients view.

## Agencies: one connection per client

Name each client's connection after the client, with "bolta" in the name: Bolta's checks only watch names containing it. Each connection asks its own first approval.

- **Claude Code:** `claude mcp add --transport http bolta-acme https://mcp.bolta.ai/mcp`, then `/mcp`, pick bolta-acme, sign in and choose Acme's workspace.
- **claude.ai or Cowork:** Customize > Connectors > Add custom connector, address https://mcp.bolta.ai/mcp, a name like "Bolta Acme". Sign in and choose Acme's workspace. Team and Enterprise: only an Owner can add it. Free plan: one custom connector in all.
- Then confirm its workspace name: "This one is Acme."

**Several connections in one chat:**
- Use the one whose workspace the user named.
- No client named: ask once. "Acme, like before?"
- Never carry an account, group or post across connections; read again there.
- "Switch to Beta": use Beta's connection if present, else explain how to add it.
- Two Bolta entries on one workspace (the plugin's plus one added by hand): keep one.

## Reconnecting Bolta itself

"Invalid API key", "API key expired", "API key inactive" or "Not authenticated": this connection lapsed. Don't retry.
- Claude Code: `/mcp`, pick the Bolta entry, sign in again.
- Cowork or claude.ai: Customize > Connectors, then Reconnect on Bolta.
- Then read the workspace and say its name.
- Sign-ins last 60 days and normally renew themselves.

## Sign-in versus a pasted API key

- Sign-in marks Claude's posts as AI drafts, keeping the first version, so edits teach the voice; Bolta keeps them on the review list until approved.
- A pasted Bolta API key acts as the person directly: no AI-draft mark, so edits don't teach, and Bolta's own hold is off. Only the plugin's checks remain.
- Used a key, or asking? Say this once; recommend sign-in.

## What this connection may do

Read it after a refusal, or when asked. For each "no" it gives a reason:

| Reason | Say |
|-|-|
| role | "Your role can't do this." |
| workspace plan | "Your plan doesn't include this." |
| key scope | "This connection wasn't given that access." |

- Workspace settings always show as not given, by design (Bolta Settings only). Don't flag it.
- Access follows the role of whoever signed in. A viewer's connection is read-only: no saves, nothing that uses credits. After a role change, sign in again.
- A role that can't connect accounts: a teammate whose role can does it.
- The read can say yes and Bolta still refuse. Give Bolta's sentence; don't try another way.
- Approving needs an owner or admin. Beyond that, never state who can do what from memory.

## Clock and review mode

- The workspace clock changes only in Bolta Settings: bolta.ai/dashboard/settings/general.
- Review mode ("Safe Mode" in settings, said once): everything beyond a draft waits for a yes, and nothing posts right away. Only Bolta Settings turns it off; never suggest that to get past a refusal.

## "Is everything set up?"

One read, then four lines: workspace and clock; review mode; accounts, connected or disconnected, with links; account groups. Voice: hand to `voice`, or `start` if there is none. A Bolta save blocked by a hook error naming Git Bash: "Install Git for Windows (git-scm.com/downloads/win), then restart Claude."
