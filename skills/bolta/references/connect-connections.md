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

- Add https://mcp.bolta.ai/mcp as "Bolta", sign in, tick the brands.
<!-- host-note -->
- In apps that have `/mcp` (for example Claude Code): `/mcp`, pick bolta. With Customize > Connectors (for example claude.ai or Cowork): Add custom connector. Team and Enterprise: only an Owner can add it. Free plan: one custom connector in all.
<!-- /host-note -->
- Then say what it reaches: "This connection reaches Acme and Beta."
- Several organizations: one connection each, with "bolta" in its name. Use the one reaching the named brand. Two Bolta entries on one organization (the plugin's and your own): keep one and remove the other.

## Reconnecting Bolta itself

"Invalid API key", "API key expired", "API key inactive" or "Not authenticated": this connection lapsed. Don't retry.
- Sign in again.
<!-- host-note -->
- In apps that have `/mcp` (for example Claude Code): pick Bolta. With Customize > Connectors (claude.ai or Cowork): Reconnect on Bolta.
<!-- /host-note -->
- Then read the brands and say their names.
- Sign-ins last 60 days and normally renew themselves.

## Sign-in versus a pasted API key

- Sign-in marks posts from this app as AI drafts, keeping the first version, so edits teach the voice; Bolta keeps them on the review list until approved.
- A pasted Bolta API key acts as the person directly: no AI-draft mark, so edits don't teach, and the sign-in hold is off: it can schedule or publish without an approval. Safe Mode and required client sign-off still apply, plus the plugin's checks.
- Used a key, or asking? Say this once; recommend sign-in.

## What this connection may do

`get-my-capabilities`: read it after a refusal, or when asked. For each "no", `denied_by` gives a reason:

| Reason | Say |
|-|-|
| `role` | "Your role can't do this." |
| `workspace_plan` | "Your plan doesn't include this." |
| `key_scope` | "This connection wasn't given that access." |
| `override` | "An owner or admin turned this off for you. Ask a brand admin; a new connection won't fix it." |

- On a sign-in connection, workspace settings always show as not given (`key_scope`), by design (Bolta Settings only). Don't flag it.
- Access follows the role of whoever signed in. A viewer's connection is read-only: no saves, nothing that uses credits. A client reviewer can't connect at all. A role change applies when the sign-in next renews; sign in again to apply it now.
- A role that can't connect accounts: a teammate whose role can does it.
- The read can say yes and Bolta still refuse. Give Bolta's sentence; don't try another way.
- Owners, admins and creators approve by default, but per-member permissions can change that: trust this read, never memory.

Clock, review mode and "Is everything set up?": [team-and-integrations](connect-team-and-integrations.md).
