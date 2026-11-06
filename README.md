# bolta-skills

Skills and plugins that let AI assistants work in a [Bolta](https://bolta.ai) workspace: write and schedule posts in your voice, keep posting every week with Bolta routines, run campaigns for launches, and read the results.

## Bolta plugin for Claude

```
/plugin marketplace add boltaai/bolta-skills
/plugin install bolta@bolta-marketplace
```

Then run `/mcp`, sign in to Bolta, and run `/bolta:start`. One plugin, no hooks: the skills ask for your yes in words before anything public or final, and Bolta's server enforces the same. (Anthropic's plugin directory accepts command hooks only from Verified organizations, so the plugin ships none.) The behavioural evals run in Claude Code against a mock Bolta server. A claude.ai connector, Cowork and claude.ai chat are not tested end to end. Drafts save freely; nothing is approved, scheduled or published until you say yes.

What users need to know (install per host, what Bolta checks, the limits, what is sent and stored) is in [`plugins/bolta/README.md`](plugins/bolta/README.md).

## What is in this repository

| Path | What it is |
|-|-|
| `plugins/bolta/` | The Claude plugin (v0.5): 12 skills, two read-only subagents (`clearing-house`, a first pass over a long review list, and `community-triage`, sorting comments and mentions), and the Bolta connection (`.mcp.json`). No commands, no hooks. |
| `.claude-plugin/marketplace.json` | Makes this repository a Claude marketplace that lists the plugin. |
| `plugin-skills/` | The skills pack for the ChatGPT app. Host-specific; kept separate on purpose. |
| `tools/` | The plugin checker, the eval runner and `tools/fixtures/` (the saved Claude tool list, see below). |
| `.github/workflows/` | CI: the checker on every pull request. The evals and `claude plugin validate` need the Claude CLI and run by hand. |
| `evals/claude-plugin/` | Behavioural evals for the plugin, kept outside the shipped folder. |
| `skills/`, `docs/`, `TOOLS-ALIGNMENT.md`, `V2-REVIEW-STATUS.md` | The earlier pre-v1 skills pack. Superseded; its tool names no longer exist. Kept for reference only. |

## Maintaining the Claude plugin

```
python3 -I tools/check_claude_plugin.py      # tool names and arguments vs the live tool list, skill shape and word budgets, plain words, directory file rules
claude plugin validate plugins/bolta --strict
claude plugin validate . --strict            # the marketplace
sh tools/run_plugin_evals.sh safety          # live behavioural checks against mocks; costs a few dollars (also: smoke, quiet, newtools, all)
```

- The checker fetches Bolta's public tool list and fails when a skill names a tool or argument the server does not have. The list depends on the caller's User-Agent: some assistants see fewer tools, and only a Claude one sees the tools made for Claude (`approve-many-posts`, `reject-post`, `set-content-campaign-targets`, `analyze-content-campaign-source`). The checker sends a Claude Code-like one (`--user-agent` changes it). Production does not list those four yet, so the checker takes their schemas from `tools/fixtures/claude_tools_list.json` (the Claude tool list of the server change that adds them) and says so in an INFO line: a plain run passes for anyone, and `--tools-json tools/fixtures/claude_tools_list.json` runs it offline (CI does). Once the server deploys them, run `--no-pending` (a missing tool is an error again), then delete `PENDING_TOOLS` and the fixture; a live schema that differs from the fixture is a warning in the meantime.
- The plugin carries no `hooks/`, no `scripts/` and only the file types Anthropic's directory accepts from an unverified organization (Markdown, text, JSON, YAML, PNG, JPEG, GIF, WebP, ICO); the checker fails on anything else, because the directory refuses the version.
- Skills use the tools made for Claude when they are offered and fall back when they are not (`approve-post` one at a time; a "no" and campaign accounts go to the dashboard). The evals run both ways: the suite offers the production tools, and the `newtools` cases opt in to the new ones.
- The checker also holds v0.2's house style: the twelve skills, each `SKILL.md` in five sections (Done when, Know this, Tools, Hand off, Always) and 500 words or fewer (`LC_ALL=C wc -w`, frontmatter excluded), each reference 600 or fewer, descriptions that start with a verb and say "Use when" once, no internal words in descriptions or quoted lines, and no citations of server code.
- Claude Code pins a plugin to its `version`. Bump `version` in `plugins/bolta/.claude-plugin/plugin.json` for every change that should reach users.
- Skills state facts about the Bolta server (what a tool really does, which errors it returns). When the server changes, re-verify the affected skill; the checker only catches names and arguments. The shipped files cite no server paths: this repository is public.
- The plugin folder must contain only what users need. Test fixtures live in `evals/`.

## Licence

MIT. See `LICENSE`.
