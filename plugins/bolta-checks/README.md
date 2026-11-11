# BOLTA checks

The local checks behind the `bolta` plugin, as a plugin of their own for Claude Code. Before anything public, approved, turned down or final, Claude Code shows you a Bolta check and waits for your yes. Drafts need none.

The checks are hooks (shell scripts Claude Code runs around Bolta's tool calls). Anthropic's plugin directory accepts such hooks only from Verified organizations, so they ship here, from GitHub, and not inside the directory listing.

## Install

Install `bolta` first, then add this:

```
/plugin marketplace add boltaai/bolta-skills
/plugin install bolta-checks@bolta-marketplace
```

Without it, Claude still asks in words before anything public; the skills are written for both.

## What Bolta checks, and where

The checks go by each tool's name, so any connection name works: the `bolta` plugin's own server, a server added with `claude mcp add`, or a claude.ai connector.

- Bolta asks before anything public (a post, a reply, a reaction), approving or turning down posts (once per batch per message), scheduling, running a Bolta routine now, switching on a plan as it is saved, applying or accepting one of Bolta's suggestions, starting or finishing a campaign, changing a running campaign, changing your voice or business details, and anything that can't be undone.
- **Bolta checks** `careful` in `/config` checks every approval, one at a time.
- A declined check is final for that call: Claude says so and never retries it.
- After a sign-in error, Claude tells you to reconnect instead of retrying.

Tested in Claude Code against a mock Bolta server and on a server added with `claude mcp add` under another name. A claude.ai connector is not tested end to end. Chat and Cowork run no plugin hooks.

## Limits

- Hooks need `sh` and `awk`. On Windows, install [Git for Windows](https://git-scm.com/downloads/win) first, or every Bolta save is blocked.
- The checks trust their marker files. Claude, if it may run shell commands unasked, could forge one.
- Another server's tool named like a Bolta one gets the same check, and a call the checks can't read gets one too.

## Sent and stored

The hooks keep marker files in `${TMPDIR:-/tmp}/bolta-plugin/` and make no network calls. They never see a password or a token.

v0.4.0 (beta). [Privacy](https://bolta.ai/privacy-policy) · [Terms](https://bolta.ai/tos) · [Support](https://bolta.ai/support) · MIT licence
