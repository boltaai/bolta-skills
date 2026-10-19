# BOLTA skills

The same twelve skills and checks as the `bolta` plugin, with no connection of its own. Tell Claude what you want to post about. Bolta writes it in your voice every week, and nothing goes out until you say yes.

## Which one to install

- **bolta** brings its own Bolta connection. Pick it if Bolta is not connected yet.
- **bolta-skills** (this one) brings none. Pick it if you already added Bolta in claude.ai (Customize > Connectors), in Cowork, or with `claude mcp add`.
- Never both: every skill and check would run twice.

Claude Code connects an address once, and your own `claude mcp add` server wins over the plugin's.

## Install

```
/plugin marketplace add boltaai/bolta-skills
/plugin install bolta-skills@bolta-marketplace
```

Then `/mcp`: Bolta should show as connected. Start with `/bolta-skills:start` or "set me up".

## What Bolta checks, and where

The checks go by each tool's name, so any connection name works. Call yours "Bolta" anyway: checks show it.

- **A server you added with `claude mcp add`:** tested. In a real Claude Code session with it named "social", a post-now call asked first and never reached the server.
- **A claude.ai, desktop or Cowork connector: not tested.** The checks are written for its tool names, but nobody has run them on a real connector. Claude asks in words first before anything public, a reply or a voice change. In the connector's settings, keep approve, schedule, publish and reject on "Needs approval".
- **Chat runs no plugin checks at all.** Posts stay on your review list until you say yes.
- Where checks run, Bolta asks before anything public, approving or turning down posts (once per batch per message), running a Bolta routine now, starting or finishing a campaign, changing a running campaign, and changing your voice or business details. Drafts need none.

## Limits

- Hooks need `sh` and `awk`. On Windows, install [Git for Windows](https://git-scm.com/downloads/win) first.
- The checks trust their marker files. Claude, if it may run shell commands unasked, could forge one.
- One connection is one workspace.
- Another server's tool named like a Bolta one gets the same check, and a call the checks can't read gets one too.

## Sent and stored

Bolta (mcp.bolta.ai) gets your requests and decisions. Claude handles sign-in; the plugin never sees a password. Hooks keep marker files in `${TMPDIR:-/tmp}/bolta-plugin/` and make no network calls.

v0.2.0 (beta). [Privacy](https://bolta.ai/privacy-policy) · [Terms](https://bolta.ai/tos) · [Support](https://bolta.ai/support) · MIT licence
