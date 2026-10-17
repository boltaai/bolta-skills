# bolta-skills

Skills and plugins that let AI assistants work in a [Bolta](https://bolta.ai) workspace: write and schedule posts in your voice, keep posting every week with Bolta routines, run campaigns for launches, and read the results.

## Bolta plugin for Claude

```
/plugin marketplace add boltaai/bolta-skills
/plugin install bolta@bolta-marketplace
```

Then run `/mcp`, sign in to Bolta, and run `/bolta:start`. The hooks and the behavioural evals run in Claude Code against a mock Bolta server; Cowork and claude.ai chat are supported by the plugin format but not yet tested end to end. Drafts save freely; nothing is approved, scheduled or published until you say yes.

What users need to know (install per host, what Bolta checks, the limits, what is sent and stored) is in [`plugins/bolta/README.md`](plugins/bolta/README.md).

## What is in this repository

| Path | What it is |
|-|-|
| `plugins/bolta/` | The Claude plugin (v0.2): 12 skills, the hooks behind the Bolta checks (a write guard, a batch-window marker, a per-message reset, the house rules at session start, a reconnect notice). No commands or subagents. This is the only folder users install. |
| `.claude-plugin/marketplace.json` | Makes this repository a Claude marketplace that lists the plugin above. |
| `plugin-skills/` | The skills pack for the ChatGPT app. Host-specific; kept separate on purpose. |
| `tools/` | Checks for the Claude plugin (see below). |
| `evals/claude-plugin/` | Behavioural evals for the plugin, kept outside the shipped folder. |
| `skills/`, `docs/`, `TOOLS-ALIGNMENT.md`, `V2-REVIEW-STATUS.md` | The earlier pre-v1 skills pack. Superseded; its tool names no longer exist. Kept for reference only. |

## Maintaining the Claude plugin

```
python3 -I tools/check_claude_plugin.py      # tool names and arguments vs the live tool list, skill shape and word budgets, plain words, hook wiring
sh tools/test_hooks.sh                       # the hook scripts, 500+ cases, under every awk found
claude plugin validate plugins/bolta --strict
claude plugin validate . --strict            # the marketplace
sh tools/run_plugin_evals.sh safety          # live behavioural checks against mocks; costs a few dollars
```

- The checker fetches Bolta's public tool list and fails when a skill names a tool or argument the server does not have. The list depends on the caller's User-Agent (some assistants see fewer tools); the checker sends a neutral one. Use `--tools-json` to run offline.
- The checker also holds v0.2's house style: the twelve skills, each `SKILL.md` in five sections (Done when, Know this, Tools, Hand off, Always) and 500 words or fewer (`LC_ALL=C wc -w`, frontmatter excluded), each reference 600 or fewer, descriptions that start with a verb and say "Use when" once, no internal words in descriptions or quoted lines, no citations of server code, and a guard whose tool list matches the hook matcher.
- Claude Code pins a plugin to its `version`. Bump `version` in `plugins/bolta/.claude-plugin/plugin.json` for every change that should reach users.
- Skills state facts about the Bolta server (what a tool really does, which errors it returns). When the server changes, re-verify the affected skill; the checker only catches names and arguments. The shipped files cite no server paths: this repository is public.
- The plugin folder must contain only what users need. Test fixtures live in `evals/`.

## Licence

MIT. See `LICENSE`.
