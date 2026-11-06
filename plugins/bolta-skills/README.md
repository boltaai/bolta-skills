# BOLTA skills

The same twelve skills as the `bolta` plugin, with no connection of its own. Tell Claude what you want to post about. Bolta writes it in your voice every week, and nothing goes out until you say yes.

## Which one to install

- **bolta** brings its own Bolta connection. Pick it if Bolta is not connected yet.
- **bolta-skills** (this one) brings none. Pick it if you already added Bolta in claude.ai (Customize > Connectors), in Cowork, or with `claude mcp add`.
- Never both: every skill would run twice.
- **bolta-checks** adds the Bolta checks in Claude Code (see below). Install it next to either.

Claude Code connects an address once, and your own `claude mcp add` server wins over the plugin's.

## Install

```
/plugin marketplace add boltaai/bolta-skills
/plugin install bolta-skills@bolta-marketplace
```

Then `/mcp`: Bolta should show as connected. Start with `/bolta-skills:start` or "set me up".

## What Bolta checks, and where

Nothing is approved, scheduled, published or switched on until you say yes: Claude asks in words first, and posts stay on your review list until then. In the connector's settings, keep approve, schedule, publish and reject on "Needs approval".

In Claude Code, `bolta-checks` turns that into a Bolta check you answer before anything public, approving or turning down posts (once per batch per message), running a Bolta routine now, starting or finishing a campaign, changing a running campaign, and changing your voice or business details. Drafts need none. The checks go by each tool's name, so any connection name works. Chat and Cowork run no plugin hooks.

## Limits

- One connection is one organization and reaches the brands you ticked. A new brand needs a reconnect.
- No media upload: Instagram, TikTok, YouTube and Pinterest need a public link.

## Sent and stored

Bolta (mcp.bolta.ai) gets your requests and decisions. Claude handles sign-in; the plugin never sees a password. The plugin makes no network calls of its own.

v0.4.0 (beta). [Privacy](https://bolta.ai/privacy-policy) · [Terms](https://bolta.ai/tos) · [Support](https://bolta.ai/support) · MIT licence
