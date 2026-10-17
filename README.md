# bolta-skills

Skills and plugins that let AI assistants work in a [Bolta](https://bolta.ai) workspace: plan, draft, review, schedule, engage and measure social content.

## Bolta plugin for Claude

```
/plugin marketplace add boltaai/bolta-skills
/plugin install bolta@bolta-marketplace
```

Then run `/mcp`, sign in to Bolta, and run `/bolta:setup`. Tested in Claude Code; Cowork and Claude chat are supported by the plugin format but not yet tested end to end. Drafts first; it publishes only when you say so for that exact post.

Everything a user needs to know (install per host, how confirmations work, what data is sent, the limits) is in [`plugins/bolta/README.md`](plugins/bolta/README.md).

## What is in this repository

| Path | What it is |
|-|-|
| `plugins/bolta/` | The Claude plugin: 13 skills, 7 commands, 4 subagents, 2 safety hooks. This is the only folder users install. |
| `.claude-plugin/marketplace.json` | Makes this repository a Claude marketplace that lists the plugin above. |
| `plugin-skills/` | The skills pack for the ChatGPT app. Host-specific; kept separate on purpose. |
| `tools/` | Checks for the Claude plugin (see below). |
| `evals/claude-plugin/` | Behavioural evals for the plugin, kept outside the shipped folder. |
| `skills/`, `docs/`, `TOOLS-ALIGNMENT.md`, `V2-REVIEW-STATUS.md` | The earlier pre-v1 skills pack. Superseded; its tool names no longer exist. Kept for reference only. |

## Maintaining the Claude plugin

```
python3 -I tools/check_claude_plugin.py      # tool names and arguments vs the live tool list, file rules, host-neutral wording
sh tools/test_hooks.sh                       # the two hook scripts, 50+ cases
claude plugin validate plugins/bolta --strict
sh tools/run_plugin_evals.sh safety          # live behavioural checks against mocks; costs a few dollars
```

- The checker fetches Bolta's public tool list and fails when a skill names a tool or argument the server does not have. The list depends on the caller's User-Agent (some assistants see fewer tools); the checker sends a neutral one. Use `--tools-json` to run offline.
- Claude Code pins a plugin to its `version`. Bump `version` in `plugins/bolta/.claude-plugin/plugin.json` for every change that should reach users.
- Skills state facts about the Bolta server (what a tool really does, which errors it returns). When the server changes, re-verify the affected skill; the checker only catches names and arguments.
- The plugin folder must contain only what users need. Test fixtures live in `evals/`.

## Licence

MIT. See `LICENSE`.
