# bolta-skills

Skills and plugins that let AI assistants work in a [Bolta](https://bolta.ai) workspace: write and schedule posts in your voice, keep posting every week with Bolta routines, run campaigns for launches, and read the results.

## Bolta plugin for Claude

```
/plugin marketplace add boltaai/bolta-skills
/plugin install bolta@bolta-marketplace
```

Then run `/mcp`, sign in to Bolta, and run `/bolta:start`. Already connected Bolta yourself (a connector in claude.ai, the desktop app or Cowork, or `claude mcp add`)? Install `bolta-skills@bolta-marketplace` instead: the same skills and checks with no Bolta connection of its own, so Bolta's tools are not registered twice. The hooks and the behavioural evals run in Claude Code against a mock Bolta server. The checks were also seen working on a server added with `claude mcp add` under another name. A claude.ai connector, Cowork and claude.ai chat (which runs no hooks) are not tested end to end, and the bundle says so. Drafts save freely; nothing is approved, scheduled or published until you say yes.

What users need to know (install per host, what Bolta checks, the limits, what is sent and stored) is in [`plugins/bolta/README.md`](plugins/bolta/README.md).

## What is in this repository

| Path | What it is |
|-|-|
| `plugins/bolta/` | The Claude plugin (v0.3): 12 skills, two read-only subagents (`clearing-house`, a first pass over a long review list, and `community-triage`, sorting comments and mentions), the hooks behind the Bolta checks (a write guard, a batch-window marker, a per-message reset, the house rules at session start, a reconnect notice), and the Bolta connection (`.mcp.json`). No commands. This is the source of truth. |
| `plugins/bolta-skills/` | The skills-only bundle for people who already connected Bolta themselves: the same skills, hooks and scripts, no `.mcp.json`, and one session-start line that says its checks may not run. **Generated** from `plugins/bolta` by `tools/build_skills_bundle.py`; never edit it by hand. |
| `.claude-plugin/marketplace.json` | Makes this repository a Claude marketplace that lists both plugins. |
| `plugin-skills/` | The skills pack for the ChatGPT app. Host-specific; kept separate on purpose. |
| `tools/` | Checks for the Claude plugins, the bundle generator, the eval runner and `tools/fixtures/` (the saved Claude tool list, see below). |
| `.github/workflows/` | CI: the checker, the hook tests and the bundle sync on every pull request. The evals and `claude plugin validate` need the Claude CLI and run by hand. |
| `evals/claude-plugin/` | Behavioural evals for the plugin, kept outside the shipped folder. |
| `skills/`, `docs/`, `TOOLS-ALIGNMENT.md`, `V2-REVIEW-STATUS.md` | The earlier pre-v1 skills pack. Superseded; its tool names no longer exist. Kept for reference only. |

## Maintaining the Claude plugin

```
python3 -I tools/build_skills_bundle.py      # regenerate plugins/bolta-skills after any change under plugins/bolta
python3 -I tools/check_claude_plugin.py      # both plugins: tool names and arguments vs the live tool list, skill shape and word budgets, plain words, hook wiring, bundle in sync
python3 -I tools/build_skills_bundle.py --check   # the bundle is what the generator writes now (also part of the checker)
sh tools/test_hooks.sh                       # the hook scripts, 800+ cases, under every awk found (3 minutes)
claude plugin validate plugins/bolta --strict
claude plugin validate plugins/bolta-skills --strict
claude plugin validate . --strict            # the marketplace
sh tools/run_plugin_evals.sh safety          # live behavioural checks against mocks; costs a few dollars (also: smoke, quiet, newtools, all)
```

- The checker fetches Bolta's public tool list and fails when a skill names a tool or argument the server does not have. The list depends on the caller's User-Agent: some assistants see fewer tools, and only a Claude one sees the tools made for Claude (`approve-many-posts`, `reject-post`, `set-content-campaign-targets`, `analyze-content-campaign-source`). The checker sends a Claude Code-like one (`--user-agent` changes it). Production does not list those four yet, so the checker takes their schemas from `tools/fixtures/claude_tools_list.json` (the Claude tool list of the server change that adds them) and says so in an INFO line: a plain run passes for anyone, and `--tools-json tools/fixtures/claude_tools_list.json` runs it offline (CI does). Once the server deploys them, run `--no-pending` (a missing tool is an error again), then delete `PENDING_TOOLS` and the fixture; a live schema that differs from the fixture is a warning in the meantime. `--no-bundle` checks the full plugin only.
- Both plugins' hook matchers cover Bolta under any server name: the plugin's own (`mcp__plugin_bolta_bolta__<tool>`), a claude.ai connector (`mcp__claude_ai_<name>__<tool>`) and a server added with `claude mcp add` (`mcp__<name>__<tool>`), without matching tools Bolta does not have. A matcher that only fit names with "bolta" in them would leave a Bolta added as "social" with no check while the session start line says checks are on. A tool of another server that shares a Bolta tool's name gets the same check, by design. The reconnect-notice matcher lists tools by name; `python3 -I tools/build_skills_bundle.py --sync-hooks` rewrites it from the skills.
- The bundle checks: no `.mcp.json`, and byte for byte what the generator writes now. Its one difference from the full plugin is the last session-start line: the full plugin says "Bolta checks are on in this session" (the skills then let a check stand in for asking in words); the bundle says they may not run, because nobody has run its checks on a real claude.ai connector. Remove that swap in the generator only after a real connector session shows the ask.
- Skills use the tools made for Claude when they are offered and fall back when they are not (`approve-post` one at a time; a "no" and campaign accounts go to the dashboard). The evals run both ways: the suite offers the production tools, and the `newtools` cases opt in to the new ones.
- The checker also holds v0.2's house style: the twelve skills, each `SKILL.md` in five sections (Done when, Know this, Tools, Hand off, Always) and 500 words or fewer (`LC_ALL=C wc -w`, frontmatter excluded), each reference 600 or fewer, descriptions that start with a verb and say "Use when" once, no internal words in descriptions or quoted lines, no citations of server code, and a guard whose tool list matches the hook matcher.
- Claude Code pins a plugin to its `version`. Bump `version` in `plugins/bolta/.claude-plugin/plugin.json` for every change that should reach users.
- Skills state facts about the Bolta server (what a tool really does, which errors it returns). When the server changes, re-verify the affected skill; the checker only catches names and arguments. The shipped files cite no server paths: this repository is public.
- The plugin folder must contain only what users need. Test fixtures live in `evals/`.

## Licence

MIT. See `LICENSE`.
