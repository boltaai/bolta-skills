# bolta-skills

One skill that lets an AI assistant run a brand's social media in [Bolta](https://bolta.ai): write posts in your voice, decide what goes out from one review list, keep posting every week with Bolta routines, run campaigns for launches, answer comments and read the results. Drafts save freely. Nothing is approved, scheduled or published until you say yes.

Two parts, and every client needs both:

- **The Bolta connection**: a hosted server at `https://mcp.bolta.ai/mcp`. You sign in to Bolta in the browser the first time; there is no key to paste.
- **The Bolta skill**: [`skills/bolta/`](skills/bolta/SKILL.md). One entry point, twelve playbooks and [worked examples](skills/bolta/examples/README.md) with the exact calls.

## Choose your client

| Client | Connection | Skill | Status |
|-|-|-|-|
| Claude Code | the plugin brings it | the plugin brings it | Checked in CI; behavioural evals run against a mock Bolta |
| claude.ai, Claude desktop, Cowork | Customize > Connectors | install the plugin, or upload the skill | Not tested end to end |
| Cursor | `mcp.json` in this repository | `skills/bolta` | Manifest follows Cursor's plugin docs; not tested |
| Gemini CLI | `gemini-extension.json` | `skills/bolta` | Manifest follows the extension docs; not tested |
| Codex CLI | `~/.codex/config.toml` | `npx skills add` | Not tested |
| Grok Build | `grok mcp add` | reads this repository as a Claude Code marketplace | Not tested |
| VS Code, Windsurf, anything else | its own config file | `npx skills add` | Not tested |

"Not tested" means nobody has run a full draft, review and schedule there yet. Clients differ in what Bolta offers them: the batch approval, the "no" with a reason and campaign set-up from chat reach Claude and Cursor today. Elsewhere the skill falls back to one approval at a time and a link to Bolta, and says so.

### Claude Code

```
/plugin marketplace add boltaai/bolta-skills
/plugin install bolta@bolta-marketplace
```

Then `/mcp`, sign in, tick your brands, and say "set me up". Already connected Bolta yourself (a connector, or `claude mcp add`)? Keep that connection and add only the skill: `npx skills add boltaai/bolta-skills --skill bolta`. Add `bolta-checks@bolta-marketplace` for a check you answer before anything public or final. More in [`plugins/bolta/README.md`](plugins/bolta/README.md).

### Cursor

Add the server to `.cursor/mcp.json` (or `~/.cursor/mcp.json`), then install the skill:

```json
{ "mcpServers": { "bolta": { "url": "https://mcp.bolta.ai/mcp" } } }
```

```
npx skills add boltaai/bolta-skills --skill bolta
```

This repository is also a Cursor plugin (`.cursor-plugin/plugin.json`, `mcp.json`, `skills/`) for a team marketplace import.

### Gemini CLI

```
gemini extensions install https://github.com/boltaai/bolta-skills
```

`gemini-extension.json` carries the connection (`httpUrl`) and the extension ships `skills/bolta`. Sign in with `/mcp auth bolta`.

### Codex CLI

```toml
# ~/.codex/config.toml
[mcp_servers.bolta]
url = "https://mcp.bolta.ai/mcp"
```

```
codex mcp login bolta
npx skills add boltaai/bolta-skills --skill bolta
```

### Grok Build

```
grok mcp add --transport http bolta https://mcp.bolta.ai/mcp
```

Grok Build reads Claude Code marketplaces and skills as they are, so the plugin above installs there too.

### VS Code and others

```json
{ "servers": { "bolta": { "type": "http", "url": "https://mcp.bolta.ai/mcp" } } }
```

That is `.vscode/mcp.json`. Any other client: point it at the same address over HTTP, then `npx skills add boltaai/bolta-skills --skill bolta`, or copy `skills/bolta` into the folder your client reads skills from.

## What is in this repository

| Path | What it is |
|-|-|
| `plugins/bolta/` | The Claude plugin and **the source of truth**: the skill (`skills/bolta/`: `SKILL.md`, `references/`, `examples/`), two read-only subagents and the Bolta connection (`.mcp.json`). Edit the skill here and nowhere else. |
| `skills/bolta/` | The skill on its own, for every other client. **Generated**; never edit it by hand. |
| `plugins/bolta-checks/` | The hooks behind the Bolta checks, for Claude Code. A plugin of its own because Anthropic's directory accepts command hooks only from Verified organizations. |
| `.claude-plugin/marketplace.json` | Makes this repository a Claude marketplace listing the two plugins. |
| `.cursor-plugin/plugin.json`, `mcp.json`, `gemini-extension.json` | The same skill and connection for Cursor and Gemini CLI. |
| `tools/` | The checker, the generator, the hook tests, the eval runner and the saved tool list. |
| `evals/claude-plugin/` | Behavioural evals, kept outside the shipped folders. |

## How the skill is laid out

```
skills/bolta/
  SKILL.md          house rules, how Bolta is built, the look-once reads, which playbook an ask goes to
  references/
    today.md  start.md  post.md  review.md  routine.md  campaign.md
    results.md  voice.md  replies.md  connect.md  fix.md  my-workflow.md      the twelve playbooks
    <playbook>-<topic>.md                                                     detail a playbook sends you to
  examples/
    README.md       the index
    *.json          one ask each: the calls in order, why, what to say, what never to do
```

An assistant reads `SKILL.md`, picks one playbook, and reads it before acting. The examples are checked against Bolta's tool list on every pull request, so an argument that does not exist fails the build.

## Maintaining it

```
python3 -I tools/sync_skill.py      # regenerate skills/bolta after any change under plugins/bolta
python3 -I tools/check_claude_plugin.py      # both plugins: tool names and arguments vs the live tool list, skill shape and word budgets, plain words, hook wiring, directory file rules, skills/bolta in sync
python3 -I tools/sync_skill.py --check   # skills/bolta is what the generator writes now (also part of the checker)
sh tools/test_hooks.sh                       # the hook scripts, 800+ cases, under every awk found (3 minutes)
claude plugin validate plugins/bolta --strict
claude plugin validate plugins/bolta-checks --strict
claude plugin validate . --strict            # the marketplace
sh tools/run_plugin_evals.sh safety          # live behavioural checks against mocks; costs a few dollars (also: smoke, quiet, newtools, all)
```

- The checker fetches Bolta's public tool list and fails when a skill names a tool or argument the server does not have. The list depends on the caller's User-Agent: some assistants see fewer tools, and only a Claude one sees the tools made for Claude (`approve-many-posts`, `reject-post`, `set-content-campaign-targets`, `analyze-content-campaign-source`). The checker sends a Claude Code-like one (`--user-agent` changes it). Production does not list those four yet, so the checker takes their schemas from `tools/fixtures/claude_tools_list.json` (the Claude tool list of the server change that adds them) and says so in an INFO line: a plain run passes for anyone, and `--tools-json tools/fixtures/claude_tools_list.json` runs it offline (CI does). Once the server deploys them, run `--no-pending` (a missing tool is an error again), then delete `PENDING_TOOLS` and the fixture; a live schema that differs from the fixture is a warning in the meantime.
- The listed plugin (`bolta`) carries no `hooks/`, no `scripts/` and only the file types Anthropic's directory accepts from an unverified organization (Markdown, text, JSON, YAML, PNG, JPEG, GIF, WebP, ICO); the checker fails on anything else, because the directory refuses the version. `userConfig` lives in `bolta-checks` with the guard that reads it.
- The checks' hook matchers cover Bolta under any server name: the plugin's own (`mcp__plugin_bolta_bolta__<tool>`), a claude.ai connector (`mcp__claude_ai_<name>__<tool>`) and a server added with `claude mcp add` (`mcp__<name>__<tool>`), without matching tools Bolta does not have. A matcher that only fit names with "bolta" in them would leave a Bolta added as "social" with no check while the session start line says checks are on. A tool of another server that shares a Bolta tool's name gets the same check, by design. The reconnect-notice matcher lists tools by name; `python3 -I tools/sync_skill.py --sync-hooks` rewrites it from the skills.
- `skills/bolta` is byte for byte what the generator writes now. The session-start hook in `bolta-checks` ends with "Bolta checks are on in this session"; a skill that sees it lets a check stand in for asking in words, and otherwise asks in words first.
- Skills use the tools made for Claude when they are offered and fall back when they are not (`approve-post` one at a time; a "no" and campaign accounts go to the dashboard). The evals run both ways: the suite offers the production tools, and the `newtools` cases opt in to the new ones.
- The checker also holds the house style: one skill, `bolta`. Its `SKILL.md` has eight fixed sections and 1,600 words or fewer (`LC_ALL=C wc -w`, frontmatter excluded), holds the ten house rules word for word as the session-start hook prints them, and links every playbook. The twelve playbooks (`references/<name>.md`) keep five sections (Done when, Know this, Tools, Hand off, Always); every reference is 600 words or fewer and belongs to a playbook (`<playbook>-<topic>.md`). Every `examples/<name>.json` is checked against the tool list: real tools, real argument names, every required argument, no draft saved with a time or an action. The description starts with a verb and says "Use when" once; no internal words in descriptions or quoted lines, no citations of server code, and a guard whose tool list matches the hook matcher.
- Claude Code pins a plugin to its `version`. Bump `version` in `plugins/bolta/.claude-plugin/plugin.json` and in `plugins/bolta-checks/.claude-plugin/plugin.json` for every change that should reach users; `tools/test_hooks.sh` keeps the two equal.
- Skills state facts about the Bolta server (what a tool really does, which errors it returns). When the server changes, re-verify the affected skill; the checker only catches names and arguments. The shipped files cite no server paths: this repository is public.
- The plugin folder must contain only what users need. Test fixtures live in `evals/`.

## Licence

MIT. See `LICENSE`.
