# Connections, clients and access

## One connection, one organization

- At sign-in you pick the organization and tick the brands (workspaces) it may reach. `list-workspaces` returns them, each with your role.
- A brand added later isn't included. To add it: reconnect and tick it.

## Several brands

- Pass the brand's `workspace_id` on every call. One brand only: it may be left out.
- A call without it errors with the list of brands. Ask which; never pick one or retry with a guess.
- Pick per action; unsure: "Acme or Beta?" Never carry an account, group, voice or post across brands.

## Agencies

One connection for the agency's organization; tick the client brands.

- **Claude Code:** `/mcp`, pick bolta, sign in, tick the brands.
- **claude.ai or Cowork:** Customize > Connectors > Add custom connector, address https://mcp.bolta.ai/mcp, name "Bolta". Sign in, tick the brands. Team and Enterprise: only an Owner can add it. Free plan: one custom connector in all.
- Then say what it reaches: "This connection reaches Acme and Beta."
- Several organizations: one connection each, with "bolta" in its name. Use the one reaching the named brand. Two Bolta entries on one organization (the plugin's and your own): keep your own and install `bolta-skills` instead.

## Reconnecting Bolta itself

"Invalid API key", "API key expired", "API key inactive" or "Not authenticated": this connection lapsed. Don't retry.
- Claude Code: `/mcp`, pick the Bolta entry, sign in again.
- Cowork or claude.ai: Customize > Connectors, then Reconnect on Bolta.
- Then read the brands and say their names.
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

One read, then four lines per brand: brand and clock; review mode; accounts, connected or disconnected, with links; account groups. Voice: hand to [voice](voice.md), or [start](start.md) if there is none. A Bolta save blocked by a hook error naming Git Bash: "Install Git for Windows (git-scm.com/downloads/win), then restart Claude."
