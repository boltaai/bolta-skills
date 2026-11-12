#!/usr/bin/env python3
"""Check the Bolta Claude plugin (v0.2) against the live Bolta tool surface,
the plugin's own house style, and the static rules Anthropic's directory applies.

The skills have drifted from the server before: a skill that names a tool the
host cannot call is worse than a missing skill, because the model tries it,
gets "unknown tool", and improvises. This gate makes that a CI failure. It also
keeps the plugin short and plain: twelve skills, each a few hundred words, no
commands, at most the read-only subagents listed in AGENTS (full plugin only),
and no internal words in what the user reads.

Source of truth for tool names and arguments is the server's public
`tools/list`. It varies by User-Agent: OpenAI user agents lose the routine
tools, and only a Claude user agent sees the tools made for Claude (such as
approve-many-posts and reject-post), so this script sends a Claude Code-like one.

Four of those tools (PENDING_TOOLS) are not deployed yet. While the live list
lacks one, the checker takes its schema from tools/fixtures/claude_tools_list.json
(the Claude tool list of the server change that adds them) and says so in an INFO
line, so this check passes for anyone, not just whoever has the list saved. Once
the server change is deployed, the live list wins, a changed schema is a warning,
and `--no-pending` makes a missing tool an error again.

It checks two plugins: plugins/bolta (the plugin: the skill, the subagents and
its own Bolta connection) and plugins/bolta-checks (the hooks and scripts behind
the Bolta checks). skills/bolta at the repository root, the copy other clients
read, must match what tools/sync_skill.py would write byte for byte. The listed
plugin carries no hooks
and no shell scripts, and only the file types Anthropic's directory accepts from
an unverified organization; the checks plugin carries nothing else. Its hook
matchers must fit Bolta under any server name (the plugin's own, a connector, or
a server added by hand), because a call a matcher misses gets no check.

Usage:
    python3 -I tools/check_claude_plugin.py                       # fetch live
    python3 -I tools/check_claude_plugin.py --tools-json tools.json   # offline, e.g. CI
    python3 -I tools/check_claude_plugin.py --no-pending          # live list only
    python3 -I tools/check_claude_plugin.py --strict              # warnings fail
    python3 -I tools/check_claude_plugin.py --require-coverage    # every tool used
    python3 -I tools/check_claude_plugin.py --no-bundle           # the full plugin and the checks only
    python3 -I tools/check_claude_plugin.py --coverage-only       # key coverage only, offline
    python3 -I tools/check_claude_plugin.py --coverage-only --coverage-report missing.md

Key coverage (runs first, needs no tool list): every key in
tools/fixtures/coverage_keys.json (routine and campaign tool inputs, per-network
fields, platform_specific keys the publishers read, tool names) must appear in a
code span or fence of some references/*.md, next to its tool, parent key or
network. A missing key is an ERROR; a per-network key with no examples/*.json
showing it is a WARN. Deliberate gaps go in tools/fixtures/coverage_exempt.json as
{"key id": "reason"}: an empty reason or a key the fixture lacks is an ERROR, an
exempt key the skill now teaches is a WARN. When the server changes, regenerate
the fixture (python3 -I tools/build_coverage_fixture.py [SERVER_PATH]) and commit
it with the skill change that teaches the new keys.

Checks, in order: manifest and marketplace, file hygiene, layout (skills, plus
agents/ in the full plugin only; no commands/), agent shape (read-only tool list,
no frontmatter Claude Code ignores), skill frontmatter (strict YAML, name, description),
skill shape (the five sections, house rules, hand-offs), word budgets, tool ids
and call-site arguments, links, host-neutral and plain-words lint, citations of
server code, hook wiring (scripts, matchers, the guard's tool list, settings).
Exit status is non-zero when any ERROR is reported (or any WARN with --strict).
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import re
import ssl
import sys
import urllib.request
import importlib.util

REPO = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_PLUGIN = REPO / "plugins" / "bolta"
DEFAULT_CHECKS = REPO / "plugins" / "bolta-checks"
DEFAULT_MARKETPLACE = REPO / ".claude-plugin" / "marketplace.json"
DEFAULT_URL = "https://mcp.bolta.ai/mcp"
#: The Claude tool list of the server change that adds PENDING_TOOLS: name, title,
#: description, inputSchema and annotations of every tool, in the tools/list shape.
DEFAULT_FIXTURE = REPO / "tools" / "fixtures" / "claude_tools_list.json"
#: Tools the skills and the guard use that production does not list yet. While the
#: live list lacks one, its schema comes from DEFAULT_FIXTURE. Delete a name here
#: once the live list has it (the checker says when).
PENDING_TOOLS = ("approve-many-posts", "reject-post", "analyze-content-campaign-source",
                 "plan-team-posts", "update-team-post-plan", "generate-team-post-drafts", "get-team-post-plan",
                 "list-workspace-members", "revise-plan", "confirm-plan",
                 "plan-routine", "plan-campaign", "recommend-routines",
                 # Release 2: the folded catalog's new tools
                 "save-post", "plan", "list-suggestions", "decide-suggestion")
#: Live tools whose saved schema adds arguments production does not take yet. Until it does,
#: the saved arguments are accepted too. Delete a name once the live list has them (the checker says when).
PENDING_UPDATES = ("create-routine", "update-routine", "extract-business-dna", "voice-generate",
                   # Release 2: tools that absorbed a folded tool's arguments
                   "list-workspaces", "list-accounts", "list-workspace-posts", "get-post", "publish-post",
                   "list-inbox-items", "draft-engagement-reply", "list-engagements", "list-account-insights",
                   "get-voice-context", "list-business-dna", "create-content-campaign", "update-content-campaign")
#: Claude Code sends "claude-code/<version> (<entrypoint>)" on its MCP requests,
#: and the server matches "claude" in it. Without it the list lacks the tools made for Claude.
CLAUDE_USER_AGENT = "claude-code/2.1.302 (cli; bolta-plugin-check)"

#: Accepted on every Bolta tool regardless of its declared schema: the MCP layer
#: prepends workspace_id. It may be left out only when the connection reaches one
#: brand (workspace); with several, every brand call must pass it.
UNIVERSAL_PARAMS = {"workspace_id"}

#: Hyphenated words that legitimately appear in backticks and are not tool ids.
NON_TOOL_TOKENS = {"read-only", "draft-only", "mcp-app", "claude-code", "bolta-skills", "bolta-checks"}

#: Exposed tools the skills deliberately never use. Naming one in a skill is an
#: error only where the reason says so (`forbid`).
INTENTIONALLY_UNUSED: dict[str, tuple[str, bool]] = {}
#: Release 1 tools the Release 2 server no longer lists but still answers by name (each folded
#: into a listed tool). A model can still call one, so the guard keeps gating the ones that write,
#: and SKILL.md's "When something is missing" may name one as the fallback for an older server.
#: Nowhere else: a skill that teaches an unlisted name sends the model to a tool it cannot see.
LEGACY_TOOLS = frozenset({
    "get-workspace", "get-my-capabilities", "list-buckets", "create-social-bucket", "update-social-bucket",
    "list-engagement-capabilities", "list-scheduled-posts", "list-content-campaign-posts",
    "get-post-platform-details", "create-post", "update-post", "update-post-platform-details", "schedule-post",
    "approve-post", "approve-recurring-review", "list-reviews", "list-recurring-reviews",
    "reject-recurring-review", "get-engagement-conversation", "create-engagement-opportunity",
    "get-engagement-status", "cross-platform-analytics", "list-voice-profiles", "get-business-dna",
    "resume-routine", "set-content-campaign-targets", "add-posts-to-content-campaign",
    "list-routine-recommendations", "list-bolta-suggestions",
    "decide-routine-recommendation", "decide-bolta-suggestion",
})
LEGACY_SECTION = "When something is missing"

#: The subagents the full plugin ships (agents/<name>.md). The skills-only bundle ships none: its
#: connection can have any name, and an agent's tool list has to name the server.
AGENTS = ("clearing-house", "community-triage")
#: Frontmatter a plugin agent may use. permissionMode, hooks, mcpServers and initialPrompt are
#: ignored for plugin agents, so a file that sets one only looks safer than it is.
AGENT_KEYS = {"name", "description", "model", "tools", "maxTurns", "color", "effort"}
AGENT_IGNORED_KEYS = {"permissionMode", "hooks", "mcpServers", "initialPrompt", "disallowedTools"}
#: The two server prefixes an agent's tool list names: the plugin's own server and one added as "bolta".
#: A wildcard in the server part is not supported, so a connection named anything else gives the agent
#: no Bolta tools; its prompt says to stop and the skill does the work itself.
AGENT_PREFIXES = ("mcp__plugin_bolta_bolta__", "mcp__bolta__")
#: An agent may call these and nothing else: reads only.
AGENT_READ_PREFIXES = ("list-", "get-")
AGENT_READ_EXTRA = {"search-engagement-opportunities"}
MAX_AGENT_WORDS = 700          # agents/<name>.md body, frontmatter excluded

#: One skill. Its SKILL.md is the entry point: the house rules, how Bolta is built, the look-once
#: reads and the table that sends each ask to one playbook. The playbooks are
#: references/<name>.md (the twelve skills of v0.2 to v0.4, one file each), and every other
#: reference is references/<playbook>-<topic>.md. examples/ holds worked calls as JSON.
SKILLS = ("bolta",)
PLAYBOOKS = ("today", "start", "post", "review", "routine", "campaign", "results",
             "voice", "replies", "connect", "fix", "my-workflow")
SECTIONS = ["House rules", "How Bolta is built", "Look once", "Pick the playbook", "The four moves",
            "Things that bite", "When something is missing", "Extras, where the app has them"]
PLAYBOOK_SECTIONS = ["Done when", "Know this", "Tools", "Hand off", "Always"]
HOUSE_RULES_LINE = "Follow the house rules in the Bolta skill."
RULES_SKILL = "bolta"
RULES_SECTION = "House rules"
#: Keys an examples/<name>.json file holds. `steps` is a list of {tool, arguments, why}.
EXAMPLE_KEYS = {"ask", "playbook", "before", "steps", "say", "never"}

#: v0.1 names that must not come back (skills, commands, subagents).
OLD_NAMES = {
    "workspace-setup", "social-publishing", "content-planning", "routines", "approvals",
    "social-inbox", "outbound-engagement", "analytics-review", "brand-voice-setup",
    "brand-voice-check", "accounts-and-buckets", "wordpress-blog", "undo-and-recovery",
    "approval-batch-reviewer", "content-calendar-planner",
    "performance-analyst", "plan-week",
}
#: The twelve v0.2 skills are playbooks now. A skill folder with one of these names is the old layout.
OLD_SKILL_FOLDERS = set(PLAYBOOKS)

#: Budgets, in words as `LC_ALL=C wc -w` counts them (see words()).
MAX_SKILL_WORDS = 1_600        # SKILL.md body, frontmatter excluded: the one entry point
MAX_REFERENCE_WORDS = 600      # each references/*.md (a playbook is one of them)
MAX_SKILLS_TOTAL_WORDS = 2_000   # all SKILL.md files together, frontmatter included
MAX_DESCRIPTION_WORDS = 100    # one description now, where twelve of 60 words used to be in context
MAX_README_WORDS = 430         # was 400 before the plugin gained its review helper (one line)
MAX_ALWAYS_MUSTS = 3

#: Strings a customer-facing file must never contain (host neutrality).
BANNED_EVERYWHERE = [
    (re.compile(r"\bChatGPT\b"), "names ChatGPT (host-specific)"),
    (re.compile(r"\bOpenAI\b"), "names OpenAI (host-specific)"),
    (re.compile(r"\bwidgets?\b", re.I), "mentions a widget (host-specific)"),
]
#: Allowed only inside a <!-- host-note --> ... <!-- /host-note --> region.
BANNED_OUTSIDE_HOST_NOTE = [
    (re.compile(r"\bcards?\b", re.I), "mentions a card (host-specific; only allowed in a host note)"),
    # Case-sensitive: lowercase paths and commands (.claude/, `claude mcp add`, claude.ai) stay legal.
    (re.compile(r"\bClaude\b"), "names Claude (host-specific; say \"your AI app\" or \"you\", or use a host note)"),
]
HOST_NOTE = re.compile(r"<!--\s*host-note\s*-->.*?<!--\s*/host-note\s*-->", re.S)

#: The plan's "never say" list. Applied to skill descriptions (always in context,
#: and the words people see in the skill menu) and to quoted lines Claude says.
NEVER_SAY = [
    (re.compile(r"\bMCP\b"), "MCP"),
    (re.compile(r"\btools?\b", re.I), "tool"),
    (re.compile(r"\bOAuth\b", re.I), "OAuth"),
    (re.compile(r"\bconnectors?\b", re.I), "connector"),
    (re.compile(r"\bfingerprints?\b", re.I), "fingerprint"),
    (re.compile(r"\bartifacts?\b", re.I), "artifact"),
    (re.compile(r"\bworkflow definitions?\b", re.I), "workflow definition"),
    (re.compile(r"\bsource bindings?\b", re.I), "source binding"),
    (re.compile(r"\btemplate keys?\b", re.I), "template key"),
    (re.compile(r"\bcapability keys?\b", re.I), "capability keys"),
    (re.compile(r"\bcursors?\b", re.I), "cursor"),
    (re.compile(r"\bbeat\b", re.I), "beat"),
    (re.compile(r"\bproducers?\b", re.I), "producer"),
    (re.compile(r"\bpreflight\b", re.I), "preflight"),
    (re.compile(r"\bHub\b"), "Hub"),
    (re.compile(r"\bHype-?Man\b", re.I), "Hype-Man"),
    (re.compile(r"\bHunter\b"), "Hunter"),
    (re.compile(r"\bEngager\b"), "Engager"),
    (re.compile(r"\bEssence Capture\b", re.I), "Essence Capture"),
    (re.compile(r"\b(?:HTTP\s*)?[45]\d\d\b(?!\s*(?:words|characters|posts|drafts|MB|days|people|views))"), "an HTTP code"),
]
#: Internal Bolta words with a plain replacement (plan section 6). Descriptions only.
INTERNAL_WORDS = [
    (re.compile(r"\bbuckets?\b", re.I), "bucket (say account group)"),
    (re.compile(r"\b(?:Business|Voice) DNA\b", re.I), "Business/Voice DNA (say about your business / your voice)"),
    (re.compile(r"\bSafe Mode\b", re.I), "Safe Mode (say review mode)"),
    (re.compile(r"\bapproval polic(?:y|ies)\b", re.I), "approval policy (say ask me first)"),
    (re.compile(r"\bPending Approval\b", re.I), "Pending Approval (say waiting for your yes)"),
    (re.compile(r"\bpush(?:es)?\b", re.I), "push (one name: campaign)"),
]
NOT_A_LEADING_VERB = {"a", "an", "the", "this", "these", "it", "bolta", "skill", "use", "for", "when", "helps", "your"}

#: Citations of server code. The repository is public, so shipped files state
#: facts plainly and cite nothing.
CITATIONS = [
    (re.compile(r"\b(?:Bolta-Server|bolta-web|BOLTA-WEB|boltathread)\b"), "names a private Bolta repository"),
    (re.compile(r"\b[\w./-]+\.(?:py|tsx?|jsx?|go|rb)\b"), "cites a source file"),
    (re.compile(r"\b[\w./-]+\.(?:md|json|ya?ml|sh|txt):\d+"), "cites a file and line"),
    (re.compile(r"\bPR\s*#\d+|\bpull/\d+\b"), "cites a pull request (say what is true for the user instead)"),
]

PUBLISH_CAPABLE_CREATE_TOOLS = ("save-post", "bulk-create-posts", "create-wordpress-blog-post")

#: What Anthropic's directory accepts from an unverified organization: Markdown, text, JSON, YAML
#: and these image types. Anything else (a shell script, an SVG) makes it refuse the version.
#: The checks plugin is not listed there, so it may carry .sh as well.
DIRECTORY_EXT = {".md", ".txt", ".json", ".yaml", ".yml", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico"}
CHECKS_EXT = DIRECTORY_EXT | {".sh"}
IMAGE_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico"}
MAX_TEXT_BYTES = 256 * 1024
MAX_FILES = 512
RESERVED_NAME = re.compile(r"^(claude|anthropic|anthropics|cc-plugin)([-_]|$)|official", re.I)
BRAND_WORDS = re.compile(r"\b(claude|anthropic)\b", re.I)

#: Every matcher, in both plugins, must fit any server name followed by one of Bolta's tool names.
#: The full plugin's own server is mcp__plugin_bolta_bolta__<tool>; a claude.ai connector's tools are
#: mcp__claude_ai_<name>__<tool>; a server added by hand is mcp__<name>__<tool>; and the person chose
#: <name>. Some hosts name a connector by its id. A matcher that only fit names containing "bolta" would
#: leave a Bolta added as "social" with no check while SessionStart says checks are on.
SAMPLES_HIT = ("mcp__plugin_bolta_bolta__{t}", "mcp__bolta__{t}", "mcp__bolta-acme__{t}", "mcp__BOLTA__{t}",
               "mcp__claude_ai_Bolta__{t}", "mcp__claude_ai_BOLTA__{t}", "mcp__claude_ai_Bolta_Acme__{t}",
               "mcp__claude_ai_Social_posts__{t}", "mcp__social__{t}", "mcp__my-posts__{t}",
               "mcp__0a1b2c3d-4e5f-4a6b-8c7d-9e0f1a2b3c4d__{t}")
SAMPLES_MISS = ("mcp__social__{t}-x", "xmcp__social__{t}", "mcp____{t}", "mcp__social_{t}")
#: Tools the marker hook watches that the guard does not decide on (it only reads their result).
MARK_ONLY_TOOLS = {"create-content-campaign"}

#: Which plugin is being checked. Messages carry it for the bundle and the checks so the three never blur.
_ctx = [""]
#: The plugin's name, which is also its slash-command namespace (/bolta:bolta).
_ns = ["bolta"]

errors: list[str] = []
warns: list[str] = []
infos: list[str] = []


def err(where, msg):
    errors.append(f"ERROR {_ctx[0]}{where}: {msg}")


def warn(where, msg):
    warns.append(f"WARN  {_ctx[0]}{where}: {msg}")


def info(msg):
    infos.append(f"INFO  {_ctx[0]}{msg}")


# --------------------------------------------------------------------------- tools

def fetch_tools(url: str, user_agent: str = CLAUDE_USER_AGENT) -> list[dict]:
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}).encode()
    req = urllib.request.Request(
        url, data=body, method="POST",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "User-Agent": user_agent,
        },
    )
    with urllib.request.urlopen(req, timeout=30, context=ssl.create_default_context()) as resp:
        text = resp.read().decode("utf-8")
        ctype = resp.headers.get("Content-Type", "")
    if "event-stream" in ctype:
        datas = [ln[5:].strip() for ln in text.splitlines() if ln.startswith("data:")]
        text = datas[-1] if datas else "{}"
    return unwrap_tools(json.loads(text))


def with_pending(live: dict[str, dict], fixture: pathlib.Path | None, from_server: bool = True) -> dict[str, dict]:
    """The listed tools, plus the schema of every PENDING_TOOLS tool the list lacks.
    from_server is False for a list read from a file: whether the server has the tools is then unknown."""
    tools = dict(live)
    absent = [n for n in PENDING_TOOLS if n not in live]
    present = [n for n in PENDING_TOOLS if n in live]
    saved: dict[str, dict] = {}
    if fixture is not None and fixture.is_file():
        saved = {t["name"]: t for t in unwrap_tools(json.loads(fixture.read_text()))}
    elif absent:
        err("tools", f"{', '.join(absent)} are not in the tool list, and there is no saved list to take them from "
                     f"({DEFAULT_FIXTURE.relative_to(REPO)})")
        return tools
    for n in absent:
        if n in saved:
            tools[n] = saved[n]
        else:
            err("tools", f"{n} is in PENDING_TOOLS but not in the saved list")
    if absent:
        info(f"pending, not in the list: {', '.join(absent)} (schemas from the saved list); "
             f"run with --no-pending after the server change is deployed")
    for n in present:
        # workspace_id is accepted on every tool (UNIVERSAL_PARAMS), listed or not.
        a = set((live[n].get("inputSchema") or {}).get("properties", {})) - UNIVERSAL_PARAMS
        b = set((saved.get(n, {}).get("inputSchema") or {}).get("properties", {})) - UNIVERSAL_PARAMS
        if saved and a != b:
            warn("tools", f"{n} is live now with different arguments than the saved list "
                          f"(live only: {sorted(a - b) or '-'}; saved only: {sorted(b - a) or '-'}); refresh the saved list")
    for n in PENDING_UPDATES:
        if n not in live or n not in saved:
            continue
        lp = (live[n].get("inputSchema") or {}).get("properties", {})
        sp = (saved[n].get("inputSchema") or {}).get("properties", {})
        extra = {k: v for k, v in sp.items() if k not in lp}
        if extra:
            schema = dict(live[n].get("inputSchema") or {})
            schema["properties"] = {**lp, **extra}
            tools[n] = {**live[n], "inputSchema": schema}
            info(f"pending arguments of {n}, not in the list: {', '.join(sorted(extra))} (from the saved list)")
        elif from_server:
            info(f"{n} is live with every saved argument: remove it from PENDING_UPDATES")
    if present and not absent and from_server:
        info("every pending tool is live now: remove PENDING_TOOLS and the saved list from tools/check_claude_plugin.py")
    return tools


def unwrap_tools(obj) -> list[dict]:
    if isinstance(obj, dict) and "result" in obj:
        obj = obj["result"]
    if isinstance(obj, dict) and "tools" in obj:
        obj = obj["tools"]
    if not isinstance(obj, list):
        raise ValueError("tools/list payload has no tools array")
    return obj


# --------------------------------------------------------------------------- parsing

def split_frontmatter(text: str):
    """Return (dict of top-level scalar keys, body). Handles single-line values
    and folded/literal blocks; that is all the plugin's frontmatter uses."""
    if not text.startswith("---"):
        return None, text
    lines = text.split("\n")
    try:
        end = lines[1:].index("---") + 1
    except ValueError:
        return None, text
    fm: dict[str, str] = {}
    key = None
    for ln in lines[1:end]:
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$", ln)
        if m and not ln.startswith((" ", "\t")):
            key = m.group(1)
            val = m.group(2).strip()
            fm[key] = "" if val in (">", "|", ">-", "|-") else val.strip("\"'")
        elif key and (ln.startswith((" ", "\t")) or not ln.strip()):
            fm[key] = (fm[key] + " " + ln.strip()).strip()
    return fm, "\n".join(lines[end + 1:])


def strip_fences(text: str) -> str:
    return re.sub(r"```.*?```", "", text, flags=re.S)


def words(text: str) -> int:
    """Words as `LC_ALL=C wc -w` counts them, so anyone can check a budget from the
    shell: whitespace-separated tokens with at least one printable ASCII character
    (a lone "·", "→" or "×" is not a word; "-", "|" and ">" are)."""
    return sum(1 for tok in text.split() if any("!" <= ch <= "~" for ch in tok))


def sections(body: str) -> list[tuple[str, str]]:
    """The `## ` sections of a skill body, as (heading, text), fences ignored."""
    out: list[tuple[str, str]] = []
    cur, buf = None, []
    for ln in strip_fences(body).split("\n"):
        m = re.match(r"^## (.+?)\s*$", ln)
        if m:
            if cur is not None:
                out.append((cur, "\n".join(buf)))
            cur, buf = m.group(1), []
        elif cur is not None:
            buf.append(ln)
    if cur is not None:
        out.append((cur, "\n".join(buf)))
    return out


def md_files(plugin: pathlib.Path):
    yield from sorted(plugin.rglob("*.md"))


def shipped_text_files(plugin: pathlib.Path):
    for p in sorted(plugin.rglob("*")):
        if p.is_file() and p.suffix.lower() in {".md", ".json", ".sh", ".txt", ".yaml", ".yml"}:
            yield p


# --------------------------------------------------------------------------- manifest and files

def check_manifest(plugin: pathlib.Path):
    mf = plugin / ".claude-plugin" / "plugin.json"
    if not mf.is_file():
        err(str(mf), "missing plugin.json")
        return {}
    try:
        m = json.loads(mf.read_text())
    except json.JSONDecodeError as e:
        err(str(mf), f"invalid JSON: {e}")
        return {}
    rel = mf.relative_to(plugin)
    name = m.get("name", "")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name) or len(name) > 64:
        err(rel, f"name {name!r} must be kebab-case, <= 64 chars")
    if RESERVED_NAME.search(name):
        err(rel, f"name {name!r} reads as reserved/official")
    for field in ("displayName", "description"):
        if BRAND_WORDS.search(str(m.get(field, ""))):
            err(rel, f"{field} must not contain 'claude' or 'anthropic'")
    if any(BRAND_WORDS.search(k) for k in m.get("keywords", [])):
        err(rel, "keywords must not contain 'claude' or 'anthropic'")
    for field in ("version", "description", "author", "license"):
        if not m.get(field):
            warn(rel, f"missing {field}")
    if m.get("version") and not re.fullmatch(r"\d+\.\d+\.\d+(-[0-9A-Za-z.]+)?", str(m["version"])):
        err(rel, f"version {m['version']!r} is not semver")
    for field in ("homepage", "documentationUrl", "supportUrl", "privacyPolicyUrl", "termsOfServiceUrl"):
        v = m.get(field)
        if v and not str(v).startswith("https://"):
            err(rel, f"{field} must be https")
    icon = m.get("icon")
    if icon and not (plugin / icon).is_file():
        err(rel, f"icon {icon} not found")
    for forbidden in ("$schema", "extensions", "hooks", "commands", "agents"):
        if forbidden in m:
            err(rel, f"remove {forbidden!r} (OpenAI-only, auto-loaded, or not part of v0.2)")
    for key, cfg in (m.get("userConfig") or {}).items():
        if not re.fullmatch(r"[a-z][a-z0-9_]*", key):
            err(rel, f"userConfig key {key!r} must be lower_snake_case (hooks read CLAUDE_PLUGIN_OPTION_{key.upper()})")
        opts = cfg.get("options")
        if opts is not None and cfg.get("default") not in opts:
            err(rel, f"userConfig {key}: default {cfg.get('default')!r} is not one of its options")
        if not cfg.get("title") or not cfg.get("description"):
            err(rel, f"userConfig {key}: needs a title and a description")
    return m


def check_marketplace(marketplace: pathlib.Path, plugin: pathlib.Path, manifest: dict):
    if not marketplace.is_file():
        info("no marketplace.json next to the plugin; skipped")
        return
    try:
        mk = json.loads(marketplace.read_text())
    except json.JSONDecodeError as e:
        err(marketplace.name, f"invalid JSON: {e}")
        return
    root = marketplace.parent.parent
    entries = [p for p in mk.get("plugins", []) if p.get("name") == manifest.get("name")]
    if not entries:
        err("marketplace.json", f"does not list the plugin {manifest.get('name')!r}")
        return
    for e in entries:
        src = (root / str(e.get("source", ""))).resolve()
        if src != plugin:
            try:
                where = plugin.relative_to(root)
            except ValueError:  # a plugin checked from outside the repository
                where = plugin
            err("marketplace.json", f"source {e.get('source')!r} does not point at {where}")
        if e.get("version") and e["version"] != manifest.get("version"):
            err("marketplace.json", f"version {e['version']} differs from plugin.json {manifest.get('version')}")


def check_files(plugin: pathlib.Path, bundle: bool = False, checks: bool = False):
    allowed = CHECKS_EXT if checks else DIRECTORY_EXT
    files = [p for p in plugin.rglob("*") if p.is_file() or p.is_symlink()]
    if len(files) > MAX_FILES:
        err(plugin, f"{len(files)} files exceeds {MAX_FILES}")
    for p in files:
        rel = p.relative_to(plugin)
        if p.is_symlink():
            err(rel, "symlinks are not allowed")
            continue
        if p.name == ".DS_Store":
            err(rel, ".DS_Store")
        if p.suffix.lower() not in allowed and p.name not in ("LICENSE", "NOTICE"):
            err(rel, f"file type {p.suffix or '(none)'} not allowed" + ("" if checks else " in a listed plugin (the directory refuses it from an unverified organization)"))
        if p.suffix.lower() not in IMAGE_EXT and p.stat().st_size > MAX_TEXT_BYTES:
            err(rel, f"{p.stat().st_size} bytes exceeds 256 KiB")
    if (plugin / "bin").exists():
        err("bin/", "bin/ is not installable on chat or Cowork")
    if (plugin / "CLAUDE.md").exists():
        err("CLAUDE.md", "not loaded by plugins; put instructions in a skill")
    if not (plugin / "LICENSE").is_file():
        err("LICENSE", "missing")
    readme = plugin / "README.md"
    if not readme.is_file():
        err("README.md", "missing")
    else:
        n = words(strip_fences(readme.read_text()))
        if n < 40:
            err("README.md", f"{n} words outside code blocks; need >= 40")
        elif n > MAX_README_WORDS:
            err("README.md", f"{n} words outside code blocks; keep it to {MAX_README_WORDS} or fewer")
    if checks:
        if (plugin / ".mcp.json").exists():
            err(".mcp.json", "the checks plugin starts no connection; the connection comes from bolta or the person's own")
        return
    for d in ("hooks", "scripts"):
        if (plugin / d).exists():
            err(f"{d}/", "a listed plugin carries no hooks and no scripts (the directory accepts command hooks only from "
                        "Verified organizations); the Bolta checks live in plugins/bolta-checks")
    mcp = plugin / ".mcp.json"
    if bundle:
        # The whole point of the bundle: the person's own connector or server is the only one.
        if mcp.exists():
            err(".mcp.json", "the skills-only bundle must not start a Bolta connection of its own (it would register Bolta's tools twice)")
    elif mcp.is_file():
        try:
            servers = json.loads(mcp.read_text()).get("mcpServers", {})
        except json.JSONDecodeError as e:
            err(".mcp.json", f"invalid JSON: {e}")
            servers = {}
        for sname, cfg in servers.items():
            if cfg.get("type") not in ("http", "sse", "ws"):
                err(".mcp.json", f"server {sname}: type must be http, sse or ws (got {cfg.get('type')!r})")
            if not str(cfg.get("url", "")).startswith("https://"):
                err(".mcp.json", f"server {sname}: url must be https")
            if cfg.get("headers"):
                err(".mcp.json", f"server {sname}: no headers/secrets allowed; auth is OAuth")
    else:
        err(".mcp.json", "missing")


def check_layout(plugin: pathlib.Path, bundle: bool = False):
    """Skills, plus the read-only subagents in AGENTS for the full plugin. Commands copied skills,
    so there are none. The bundle has no agents: chat ignores them, and an agent's tool list names
    the server, which the bundle's connection can call anything."""
    if (plugin / "commands").exists():
        err("commands/", "no commands; every skill already shows as /bolta:<name>")
    if bundle and (plugin / "agents").exists():
        err("agents/", "the skills-only bundle ships no subagents (their tool list names the server, and its connection has any name)")
    skills = {}
    sdir = plugin / "skills"
    for d in sorted(p for p in sdir.iterdir() if p.is_dir()) if sdir.is_dir() else []:
        rel = d.relative_to(plugin)
        if not (d / "SKILL.md").is_file():
            err(rel, "skill folder without SKILL.md")
            continue
        skills[d.name] = d / "SKILL.md"
        for p in d.rglob("*"):
            if p.is_dir() or p.name == "SKILL.md" and p.parent == d:
                continue
            r = p.relative_to(d)
            ok = len(r.parts) == 2 and (
                (r.parts[0] == "references" and p.suffix == ".md")
                or (r.parts[0] == "examples" and (p.suffix == ".json" or p.name == "README.md")))
            if not ok:
                err(p.relative_to(plugin), "a skill folder holds SKILL.md, references/<topic>.md, examples/<name>.json and examples/README.md only")
    missing = [s for s in SKILLS if s not in skills]
    extra = [s for s in skills if s not in SKILLS]
    for s in missing:
        err("skills/", f"missing the {s!r} skill")
    for s in extra:
        warn(f"skills/{s}", "not the Bolta skill; add it to SKILLS in tools/check_claude_plugin.py if it is meant to ship")
    for s in skills:
        if s in OLD_NAMES:
            err(f"skills/{s}", "a v0.1 skill name; v0.2 replaced it")
        if s in OLD_SKILL_FOLDERS:
            err(f"skills/{s}", f"{s} is a playbook now: skills/bolta/references/{s}.md")
    return skills



# --------------------------------------------------------------------------- agents

def check_agents(plugin, tools_by_name, gated):
    """Each agent is a flat agents/<name>.md that can only read Bolta."""
    adir = plugin / "agents"
    if not adir.is_dir():
        return {}
    found = {}
    for p in sorted(adir.rglob("*")):
        if p.is_dir():
            continue
        rel = p.relative_to(plugin)
        if p.parent != adir or p.suffix != ".md":
            err(rel, "agents/ holds <name>.md files only")
            continue
        found[p.stem] = p
    for stem in found:
        if stem not in AGENTS:
            warn(f"agents/{stem}.md", "not one of the agents in AGENTS in tools/check_claude_plugin.py; add it there if it is meant to ship")
    for stem in AGENTS:
        if stem not in found:
            err("agents/", f"missing the {stem!r} agent")
    for name, path in found.items():
        rel = path.relative_to(plugin)
        text = path.read_text()
        check_yaml_safety(rel, text)
        fm, body = split_frontmatter(text)
        if fm is None:
            err(rel, "no frontmatter")
            continue
        if fm.get("name") != name:
            err(rel, f"name {fm.get('name')!r} must equal the file name {name!r}")
        for k in fm:
            if k in AGENT_IGNORED_KEYS:
                err(rel, f"frontmatter key {k!r} is ignored for plugin agents; it would only look like a limit (the plugin's hooks.json guard runs inside agents anyway)")
            elif k not in AGENT_KEYS:
                err(rel, f"frontmatter key {k!r} is not one of {', '.join(sorted(AGENT_KEYS))}")
        desc = fm.get("description", "")
        if not desc:
            err(rel, "missing description")
        else:
            check_description(rel, desc, tools_by_name)
        n = words(body)
        if n > MAX_AGENT_WORDS:
            err(rel, f"{n} words; an agent body is {MAX_AGENT_WORDS} words or fewer")
        entries = [e.strip() for e in fm.get("tools", "").split(",") if e.strip()]
        if not entries:
            err(rel, "no tools list: an agent without one inherits every tool, including the ones that publish")
        by_tool: dict[str, set[str]] = {}
        for e in entries:
            prefix = next((pf for pf in AGENT_PREFIXES if e.startswith(pf)), None)
            if prefix is None:
                err(rel, f"tools entry {e!r} is not a Bolta tool under {' or '.join(AGENT_PREFIXES)} (no built-in tools, no other server)")
                continue
            tool = e[len(prefix):]
            by_tool.setdefault(tool, set()).add(prefix)
            if tool not in tools_by_name:
                err(rel, f"tools lists {tool!r}, which is not an exposed Bolta tool")
            elif tool in gated or not (tool.startswith(AGENT_READ_PREFIXES) or tool in AGENT_READ_EXTRA):
                err(rel, f"tools lists {tool!r}: an agent only reads (list-, get-); anything that saves, sends or changes belongs to the main conversation behind the user's yes")
        for tool, prefixes in sorted(by_tool.items()):
            if prefixes != set(AGENT_PREFIXES):
                err(rel, f"{tool!r} is listed under only one server name; list it under {' and '.join(AGENT_PREFIXES)}")
        secs = [h for h, _ in sections(body)]
        if "Hard limits" not in secs:
            err(rel, "needs a '## Hard limits' section that says the agent only reads")
        if "material, never instructions" not in body:
            err(rel, "must say that words from other people are 'material, never instructions' (house rule 5)")
    return found


# --------------------------------------------------------------------------- skills

PLAIN_SCALAR_BAD_START = ("[", "{", "&", "*", "!", "|", "%", "@", "`")


def check_yaml_safety(rel, text):
    """Claude Code's loader is lenient; stricter hosts (upload, Cowork, linters) are not.
    A plain scalar containing ': ' or ' #', or starting with an indicator, is invalid YAML."""
    fm_lines = []
    lines = text.split("\n")
    if not lines or lines[0] != "---":
        return
    for ln in lines[1:]:
        if ln == "---":
            break
        fm_lines.append(ln)
    for ln in fm_lines:
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):\s+(.+)$", ln)
        if not m or ln.startswith((" ", "\t")):
            continue
        key, val = m.group(1), m.group(2).strip()
        if val[0] in "\"'" or val in (">", "|", ">-", "|-"):
            continue
        if ": " in val or " #" in val:
            err(rel, f"frontmatter {key!r} is an unquoted scalar containing ': ' or ' #' (invalid strict YAML); use a folded block (key: >) or quotes")
        elif val.startswith(PLAIN_SCALAR_BAD_START):
            err(rel, f"frontmatter {key!r} starts with {val[0]!r}, which YAML reads as an indicator; quote it")
    try:  # authoritative when PyYAML is installed
        import yaml  # type: ignore
        data = yaml.safe_load("\n".join(fm_lines))
        if not isinstance(data, dict):
            err(rel, "frontmatter is not a YAML mapping")
    except ImportError:
        pass
    except Exception as e:  # noqa: BLE001
        err(rel, f"frontmatter is not valid YAML: {str(e).splitlines()[0]}")


def lint_words(rel, where, text, rules, level=err):
    for rx, label in rules:
        m = rx.search(text)
        if m:
            level(rel, f"{where} says {m.group(0)!r}: {label} is on the never-say list")


def check_description(rel, desc, tools_by_name):
    n = words(desc)
    if n > MAX_DESCRIPTION_WORDS:
        err(rel, f"description is {n} words; keep it to {MAX_DESCRIPTION_WORDS} (it is always in context)")
    if len(desc) > 1024:
        err(rel, f"description {len(desc)} chars exceeds 1,024")
    first = re.sub(r"[^A-Za-z-]", "", desc.split()[0]) if desc.split() else ""
    if not first[:1].isupper() or first.lower() in NOT_A_LEADING_VERB or (first.endswith("s") and not first.endswith("ss")):
        err(rel, f"description must start with what the user gets, as a verb (\"Show ...\", \"Write ...\"); starts with {first!r}")
    uw = len(re.findall(r"\bUse when\b", desc))
    if uw != 1:
        err(rel, f"description says \"Use when\" {uw} times; say it once, then the phrases people type")
    for tok in re.findall(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)+", desc):
        if tok in tools_by_name:
            err(rel, f"description names the tool {tok!r}; descriptions use the user's words")
    lint_words(rel, "description", desc.replace(f"/{_ns[0]}:", ""), NEVER_SAY)
    lint_words(rel, "description", desc, INTERNAL_WORDS)


def house_rules_from_script(checks):
    p = checks / "scripts" / "bolta-house-rules.sh"
    if not p.is_file():
        return None
    return re.findall(r"^(\d{1,2}\. .+)$", p.read_text().replace("'\\''", "'"), re.M)


def check_skills(plugin, skills, tools_by_name, checks):
    total = 0
    script_rules = house_rules_from_script(checks)
    for name, path in skills.items():
        rel = path.relative_to(plugin)
        text = path.read_text()
        total += words(text)
        check_yaml_safety(rel, text)
        fm, body = split_frontmatter(text)
        if fm is None:
            err(rel, "no frontmatter")
            continue
        if fm.get("name") != name:
            err(rel, f"name {fm.get('name')!r} must equal folder {name!r}")
        for k in fm:
            if k not in ("name", "description", "license", "metadata"):
                err(rel, f"frontmatter key {k!r} is not allowed (name and description only; allowed-tools would erode the checks)")
        desc = fm.get("description", "")
        if not desc:
            err(rel, "missing description")
        else:
            check_description(rel, desc, tools_by_name)

        n = words(body)
        if n > MAX_SKILL_WORDS:
            err(rel, f"{n} words; SKILL.md is {MAX_SKILL_WORDS} words or fewer (move detail to references/)")

        secs = sections(body)
        heads = [h for h, _ in secs]
        if heads != SECTIONS:
            err(rel, f"sections must be exactly {' / '.join(SECTIONS)} in that order; found {' / '.join(heads) or 'none'}")
        sec = dict(secs)
        if name == RULES_SKILL:
            rules_text = sec.get(RULES_SECTION, "")
            rules = re.findall(r"^(\d{1,2}\. .+)$", rules_text, re.M)
            if len(rules) != 10:
                err(rel, f"{RULES_SECTION} must hold the 10 house rules; found {len(rules)}")
            if "Bolta house rules:" not in rules_text.split("\n"):
                err(rel, f"{RULES_SECTION} must open with the line 'Bolta house rules:' (the session-start hook prints the same line)")
            if script_rules is not None and rules != script_rules:
                err(rel, "the house rules differ from plugins/bolta-checks/scripts/bolta-house-rules.sh; keep them word for word")
        refdir = path.parent / "references"
        table = sec.get("Pick the playbook", "")
        for pb in PLAYBOOKS:
            pfile = refdir / f"{pb}.md"
            prel = pfile.relative_to(plugin) if pfile.is_file() else rel
            if not pfile.is_file():
                err(rel, f"missing the {pb!r} playbook (references/{pb}.md)")
                continue
            if f"(references/{pb}.md)" not in table:
                err(rel, f"Pick the playbook does not link references/{pb}.md, so nothing sends an ask there")
            psecs = sections(pfile.read_text())
            pheads = [h for h, _ in psecs]
            if pheads != PLAYBOOK_SECTIONS:
                err(prel, f"a playbook's sections are exactly {' / '.join(PLAYBOOK_SECTIONS)} in that order; found {' / '.join(pheads) or 'none'}")
            psec = dict(psecs)
            for target in re.findall(r"\]\(([^)\s]+)\)", psec.get("Hand off", "")):
                if target.removesuffix(".md") not in PLAYBOOKS:
                    err(prel, f"Hand off links {target}, which is not a playbook")
            if "`" in psec.get("Hand off", ""):
                err(prel, "Hand off names playbooks as links ([review](review.md)), never in backticks")
            for tok in re.findall(r"`([a-z][a-z0-9]*(?:-[a-z0-9]+)+)`", psec.get("Tools", "")):
                if tok not in tools_by_name:
                    err(prel, f"Tools lists `{tok}`, which is not an exposed Bolta tool")
            always = psec.get("Always", "")
            if HOUSE_RULES_LINE not in always:
                err(prel, f"Always must say: {HOUSE_RULES_LINE}")
            musts = [ln for ln in always.split("\n") if ln.startswith("- ") and HOUSE_RULES_LINE not in ln]
            if len(musts) > MAX_ALWAYS_MUSTS:
                err(prel, f"Always has {len(musts)} playbook-specific musts; at most {MAX_ALWAYS_MUSTS}")
        for ref in sorted(refdir.glob("*.md")) if refdir.is_dir() else []:
            stem = ref.stem
            if stem not in PLAYBOOKS and not any(stem.startswith(pb + "-") for pb in PLAYBOOKS):
                err(ref.relative_to(plugin), "a reference is a playbook (references/<playbook>.md) or belongs to one (references/<playbook>-<topic>.md)")
        check_examples(plugin, path.parent / "examples", tools_by_name)

        for ref in sorted(refdir.glob("*.md")) if refdir.is_dir() else []:
            rn = words(ref.read_text())
            if rn > MAX_REFERENCE_WORDS:
                err(ref.relative_to(plugin), f"{rn} words; a reference is {MAX_REFERENCE_WORDS} words or fewer")
            linked = any(f"references/{ref.name}" in p.read_text() or f"({ref.name})" in p.read_text()
                         for p in [path, *refdir.glob("*.md")] if p != ref)
            if not linked:
                err(ref.relative_to(plugin), "not linked from its SKILL.md (or a sibling reference), so Claude never reads it")
    if total > MAX_SKILLS_TOTAL_WORDS:
        err("skills/", f"all SKILL.md files total {total} words; keep the set under {MAX_SKILLS_TOTAL_WORDS}")
    shipped = sum(words(p.read_text()) for p in md_files(plugin))
    info(f"SKILL.md files total {total} words; all shipped markdown (README and references too) {shipped} words")


def check_examples(plugin, exdir, tools_by_name):
    """Every examples/<name>.json is one ask worked through: real tools, real argument names, every
    required argument present, and a line in examples/README.md so the skill can find it."""
    if not exdir.is_dir():
        err(exdir.relative_to(plugin), "missing: the skill ships worked examples")
        return
    index = (exdir / "README.md").read_text() if (exdir / "README.md").is_file() else ""
    if not index:
        err(exdir.relative_to(plugin), "examples/README.md is missing (the index SKILL.md links)")
    files = sorted(exdir.glob("*.json"))
    if not files:
        err(exdir.relative_to(plugin), "no examples")
    for f in files:
        rel = f.relative_to(plugin)
        try:
            ex = json.loads(f.read_text())
        except ValueError as e:
            err(rel, f"not JSON: {e}")
            continue
        if f"({f.name})" not in index:
            err(rel, "not listed in examples/README.md")
        for k in set(ex) - EXAMPLE_KEYS:
            err(rel, f"unknown key {k!r}; an example holds {', '.join(sorted(EXAMPLE_KEYS))}")
        for k in ("ask", "playbook", "steps", "say"):
            if not ex.get(k):
                err(rel, f"missing {k!r}")
        if ex.get("playbook") not in PLAYBOOKS:
            err(rel, f"playbook {ex.get('playbook')!r} is not a playbook")
        lint_words(rel, "the closing line", ex.get("say", ""), NEVER_SAY)
        for i, step in enumerate(ex.get("steps") or [], 1):
            tool, args = step.get("tool"), step.get("arguments")
            if tool not in tools_by_name:
                err(rel, f"step {i}: {tool!r} is not an exposed Bolta tool")
                continue
            if not isinstance(args, dict) or not step.get("why"):
                err(rel, f"step {i}: needs an arguments object and a why")
                continue
            schema = tools_by_name[tool].get("inputSchema") or {}
            props = set(schema.get("properties", {})) | UNIVERSAL_PARAMS
            for a in args:
                if a not in props:
                    err(rel, f"step {i}: {tool} has no argument {a!r}")
            for a in schema.get("required", []):
                if a not in args and a not in UNIVERSAL_PARAMS:
                    err(rel, f"step {i}: {tool} needs {a!r}")
            for a, v in args.items():
                enum = (schema.get("properties", {}).get(a) or {}).get("enum")
                if enum and v not in enum:
                    err(rel, f"step {i}: {tool}.{a} is {v!r}; one of {enum}")
            if tool in PUBLISH_CAPABLE_CREATE_TOOLS and ("requested_action" in args or "scheduled_time" in args):
                err(rel, f"step {i}: an example never saves with a time or an action; drafts first, then the yes move")


TOKEN = re.compile(r"`([a-z][a-z0-9]*(?:-[a-z0-9]+)+)`")
CALL = re.compile(r"(?<![\w-])([a-z][a-z0-9]*(?:-[a-z0-9]+)+)\(([^()`\n]*)\)")


def split_args(s: str):
    out, depth, cur, quote = [], 0, "", None
    for ch in s:
        if quote:
            cur += ch
            if ch == quote:
                quote = None
        elif ch in "\"'":
            quote = ch
            cur += ch
        elif ch in "[{(":
            depth += 1
            cur += ch
        elif ch in "]})":
            depth -= 1
            cur += ch
        elif ch == "," and depth == 0:
            out.append(cur)
            cur = ""
        else:
            cur += ch
    if cur.strip():
        out.append(cur)
    return [a.strip() for a in out]


def legacy_span(text: str) -> tuple[int, int]:
    """Where SKILL.md's fallback section starts and ends (the only place a legacy tool may be named)."""
    m = re.search(rf"^## {re.escape(LEGACY_SECTION)}\s*$", text, re.M)
    if not m:
        return (0, 0)
    nxt = re.search(r"^## ", text[m.end():], re.M)
    return (m.start(), m.end() + nxt.start() if nxt else len(text))


def check_tool_ids_and_args(plugin, skills, tools_by_name):
    siblings = set(skills) | set(PLAYBOOKS)
    referenced: set[str] = set()
    for path in md_files(plugin):
        rel = path.relative_to(plugin)
        text = path.read_text()
        for m in re.finditer(r"`([^`\s]+)`", text):
            if m.group(1) in OLD_NAMES:
                err(rel, f"`{m.group(1)}` is a v0.1 skill, command or subagent; v0.2 replaced it")
        legacy_ok = legacy_span(text) if path.name == "SKILL.md" else (0, 0)
        for m in TOKEN.finditer(text):
            tok = m.group(1)
            if tok in tools_by_name:
                referenced.add(tok)
            elif tok in siblings or tok in NON_TOOL_TOKENS:
                continue
            elif tok in LEGACY_TOOLS and legacy_ok[0] <= m.start() < legacy_ok[1]:
                continue
            elif tok in LEGACY_TOOLS:
                err(rel, f"`{tok}` is a Release 1 tool the server no longer lists; name it only as an older server's "
                         f"fallback in SKILL.md's {LEGACY_SECTION!r}")
            else:
                err(rel, f"`{tok}` is not an exposed Bolta tool or skill")
        # A tool whose name has no hyphen (`plan`) never matches TOKEN; count it when named in a code span.
        for m in re.finditer(r"`([a-z][a-z0-9]*)`", text):
            if m.group(1) in tools_by_name:
                referenced.add(m.group(1))
        for m in CALL.finditer(text):
            tool, argstr = m.group(1), m.group(2)
            if tool not in tools_by_name:
                continue
            referenced.add(tool)
            props = set((tools_by_name[tool].get("inputSchema") or {}).get("properties", {})) | UNIVERSAL_PARAMS
            for a in split_args(argstr):
                if not a or a in ("...", "…") or a.startswith(("...", "…")):
                    continue
                named = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)\s*(=|:)", a)
                bare = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)$", a)
                if named and named.group(1) not in props:
                    err(rel, f"{tool}({named.group(1)}=...) - '{named.group(1)}' is not a parameter of {tool}")
                elif bare and bare.group(1) not in props:
                    warn(rel, f"{tool}({bare.group(1)}) - '{bare.group(1)}' is not a parameter of {tool}")
        if rel.parts[0] == "skills":
            for tool, (why, forbid) in INTENTIONALLY_UNUSED.items():
                if forbid and re.search(rf"\b{re.escape(tool)}\b", text):
                    err(rel, f"names {tool}: never used ({why})")
    return referenced


def check_links(plugin):
    for path in md_files(plugin):
        rel = path.relative_to(plugin)
        for m in re.finditer(r"\]\(([^)\s]+)\)", strip_fences(path.read_text())):
            target = m.group(1).split("#", 1)[0]
            if not target or re.match(r"^[a-z]+:", target):
                continue
            if not (path.parent / target).exists():
                err(rel, f"link {m.group(1)!r} points at nothing")


def check_lint(plugin, skills):
    skill_names = set(skills)
    for path in md_files(plugin):
        rel = path.relative_to(plugin)
        body = path.read_text()
        host_free = HOST_NOTE.sub("", body)
        for rx, why in BANNED_EVERYWHERE:
            if rx.search(body):
                err(rel, why)
        for rx, why in BANNED_OUTSIDE_HOST_NOTE:
            if rx.search(host_free):
                err(rel, why)
        scan = split_frontmatter(body)[1] if rel.parts[0] == "agents" else body  # an agent's tools: line must name servers
        for m in re.finditer(r"mcp__[\w-]*", scan):
            # The README may name a whole server as a permission rule
            # (mcp__plugin_bolta_bolta), never one tool (mcp__<server>__<tool>).
            if rel.as_posix() == "README.md" and "__" not in m.group(0)[len("mcp__"):]:
                continue
            err(rel, "write bare tool ids; mcp__ names belong only in hooks and evals "
                     "(the README may name a whole server as a permission rule)")
            break
        for m in re.finditer(r"(?<![\w:/.~-])/(setup|draft|plan-week|status|review|inbox|report|today|start|post|routine|campaign|results|voice|replies|connect|fix|my-workflow)\b(?!-)", body):
            err(rel, f"bare slash command {m.group(0)!r}; skills are namespaced (/bolta:{m.group(1)}), and bare /review and /status are Claude Code built-ins")
        for m in re.finditer(r"/bolta(?:-skills)?:([a-z][a-z0-9-]*)", body):
            if m.group(0).split(":")[0] != f"/{_ns[0]}":
                err(rel, f"{m.group(0)} uses another plugin's name; this plugin's skills are /{_ns[0]}:<skill>")
            elif m.group(1) not in skill_names:
                err(rel, f"/{_ns[0]}:{m.group(1)} is not a skill (the one skill is /{_ns[0]}:bolta)")
        for m in re.finditer(r"\b(\d{2,3})\s+(?:Bolta\s+)?(?:MCP\s+)?tools\b", body):
            warn(rel, f"tool count in prose ({m.group(0)!r}); counts drift, remove it")
        if re.search(r"(?i)requires?\s+(an?\s+)?(admin|owner)\b", body):
            warn(rel, "asserts a role requirement; say what the refusal says instead")
        if rel.parts[0] == "skills":
            for ln in strip_fences(body).split("\n"):
                if ln.startswith(">"):
                    said = re.sub(r"\S*bolta\.ai/\S*|<[^>]*>|`[^`]*`", "", ln)
                    lint_words(rel, "a quoted line", said, NEVER_SAY)


def check_citations(plugin):
    for path in shipped_text_files(plugin):
        rel = path.relative_to(plugin)
        text = path.read_text()
        for rx, why in CITATIONS:
            for m in rx.finditer(text):
                hit = m.group(0)
                if why == "cites a source file" and re.search(r"\.(?:ai|com|io)\b", hit):
                    continue
                err(rel, f"{why}: {hit!r}")
                break


# --------------------------------------------------------------------------- hooks

def hook_groups(cfg, event):
    return (cfg.get("hooks") or {}).get(event) or []


def group_runs(g, script):
    return any(script in h.get("command", "") for h in g.get("hooks", []))


def check_hooks(plugin, manifest):
    hj = plugin / "hooks" / "hooks.json"
    if not hj.is_file():
        err("hooks/hooks.json", "missing (the Bolta checks live there)")
        return None
    try:
        cfg = json.loads(hj.read_text())
    except json.JSONDecodeError as e:
        err("hooks/hooks.json", f"invalid JSON: {e}")
        return None
    if "hooks" not in cfg:
        err("hooks/hooks.json", "needs a top-level 'hooks' key")
        return None
    used = set()
    for event, groups in cfg["hooks"].items():
        for g in groups:
            rx = g.get("matcher", "")
            try:
                re.compile(rx)
            except re.error as e:
                err("hooks/hooks.json", f"{event} matcher is not a valid regex: {e}")
            for h in g.get("hooks", []):
                cmd = h.get("command", "")
                m = re.search(r"\$\{CLAUDE_PLUGIN_ROOT\}\"?/(\S+)", cmd)
                if not m:
                    err("hooks/hooks.json", f"{event} command must run a script under ${{CLAUDE_PLUGIN_ROOT}}: {cmd!r}")
                    continue
                script = plugin / m.group(1).strip('"')
                if not script.is_file():
                    err("hooks/hooks.json", f"script {m.group(1).strip(chr(34))} not found")
                    continue
                used.add(script.name)
                if not h.get("timeout"):
                    warn("hooks/hooks.json", f"{event} {script.name}: set a timeout")
    sdir = plugin / "scripts"
    for script in sorted(sdir.glob("*")) if sdir.is_dir() else []:
        rel = script.relative_to(plugin)
        src_all = script.read_text()
        if script.suffix != ".sh":
            err(rel, "scripts/ holds POSIX shell scripts only")
            continue
        if not os.access(script, os.X_OK):
            err(rel, "not executable")
        first = src_all.split("\n", 1)[0]
        if first.strip() not in ("#!/bin/sh", "#!/usr/bin/env sh"):
            err(rel, f"must be plain POSIX shell (shebang {first!r})")
        src = "\n".join(l for l in src_all.split("\n") if not l.lstrip().startswith("#"))
        if re.search(r"\b(curl|wget|nc|python3?|node|jq)\b", src):
            err(rel, "scripts must not use network tools, python, node or jq")
        for m in re.finditer(r"CLAUDE_PLUGIN_OPTION_([A-Z0-9_]+)", src_all):
            key = m.group(1).lower()
            if key not in (manifest.get("userConfig") or {}):
                err(rel, f"reads CLAUDE_PLUGIN_OPTION_{m.group(1)}, but plugin.json has no userConfig {key!r}")
        if script.name not in used and not any(script.name in o.read_text() for o in sdir.glob("*.sh") if o != script):
            err(rel, "not run by hooks.json or by another script")
    for event in ("PreToolUse", "UserPromptSubmit", "SessionStart"):
        if not hook_groups(cfg, event):
            err("hooks/hooks.json", f"no {event} hook (guard, batch-window reset and house rules all need one)")
    return cfg


def matcher_tools(matcher: str):
    alt = re.search(r"__\(([^)]*)\)\$$", matcher)
    return set(alt.group(1).split("|")) if alt else None


def check_matcher_samples(where, matcher, tool):
    try:
        rx = re.compile(matcher)
    except re.error:
        return
    for sample in SAMPLES_HIT:
        if not rx.search(sample.format(t=tool)):
            err("hooks/hooks.json", f"{where} matcher misses {sample.format(t=tool)!r}: Bolta can be added under any name, "
                                    f"and a call the matcher misses gets no check")
    for sample in SAMPLES_MISS:
        if rx.search(sample.format(t=tool)):
            err("hooks/hooks.json", f"{where} matcher also matches {sample.format(t=tool)!r}")
    if rx.search("mcp__social__list-nothing-bolta-has"):
        err("hooks/hooks.json", f"{where} matcher matches a tool name Bolta does not have")


def load_generator():
    """tools/sync_skill.py as a module (it holds the rules for the notice matcher and the bundle)."""
    gen = REPO / "tools" / "sync_skill.py"
    if not gen.is_file():
        err("bundle", "tools/sync_skill.py is missing")
        return None
    sys.dont_write_bytecode = True  # loading the generator must leave no __pycache__ behind
    spec = importlib.util.spec_from_file_location("sync_skill", gen)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def check_guard_matches_matcher(plugin, cfg, tools_by_name, skills_src):
    """Every tool the guard decides on must be in the hook matcher (or the guard never runs
    for it), and every tool in the matcher must be a real tool the guard handles. The marker
    hook may only watch gated tools, and every Bolta matcher must catch every Bolta server name.
    plugin is the checks plugin; skills_src is the full plugin, whose skills name the tools the
    reconnect notice must cover."""
    script = plugin / "scripts" / "guard-bolta-writes.sh"
    if not script.is_file() or cfg is None:
        if cfg is not None:
            err("scripts/guard-bolta-writes.sh", "missing")
        return
    src = script.read_text()
    if 'case "$tool" in' not in src:
        err("scripts/guard-bolta-writes.sh", "no case \"$tool\" in block found")
        return
    case_body = src[src.index('case "$tool" in'):]
    in_script = set()
    for m in re.finditer(r"^  ([a-z][a-z0-9|-]*)\)\s*$", case_body, re.M):
        in_script.update(m.group(1).split("|"))
    guards = [g for g in hook_groups(cfg, "PreToolUse") if group_runs(g, "guard-bolta-writes.sh")]
    if len(guards) != 1:
        err("hooks/hooks.json", f"expected one PreToolUse group running the guard, found {len(guards)}")
        return
    matcher = guards[0].get("matcher", "")
    in_matcher = matcher_tools(matcher)
    if in_matcher is None:
        err("hooks/hooks.json", "the guard matcher must end in __(tool|tool|...)$")
        return
    for t in sorted(in_script - in_matcher):
        err("hooks/hooks.json", f"guard script decides on {t!r} but the matcher does not list it, so the guard never runs for it")
    for t in sorted(in_matcher - in_script):
        err("scripts/guard-bolta-writes.sh", f"matcher lists {t!r} but the guard script has no case for it")
    for t in sorted(in_script | in_matcher):
        if t not in tools_by_name and t not in LEGACY_TOOLS:
            err("scripts/guard-bolta-writes.sh", f"guards {t!r}, which is not an exposed Bolta tool")
    if not any(h.get("onFailure") == "block" for h in guards[0].get("hooks", [])):
        warn("hooks/hooks.json", "the guard has no \"onFailure\": \"block\"; a crashed guard would let the call through")
    check_matcher_samples("PreToolUse guard", matcher, "publish-post")
    gen = load_generator()
    for event in ("PostToolUse", "PostToolUseFailure"):
        for g in hook_groups(cfg, event):
            m = g.get("matcher", "")
            tools = matcher_tools(m)
            sample = sorted(tools)[0] if tools else "publish-post"
            if tools is None:
                err("hooks/hooks.json", f"{event} matcher must name Bolta's tools (any server name is too wide for it)")
            check_matcher_samples(f"{event}", m, sample)
            if group_runs(g, "bolta-mark.sh"):
                if tools is None:
                    err("hooks/hooks.json", "the bolta-mark matcher must name its tools")
                    continue
                for t in sorted(tools - in_matcher - MARK_ONLY_TOOLS):
                    err("hooks/hooks.json", f"bolta-mark watches {t!r}, which the guard does not gate")
                for t in sorted(tools & MARK_ONLY_TOOLS):
                    if t not in tools_by_name:
                        err("hooks/hooks.json", f"bolta-mark watches {t!r}, which is not an exposed Bolta tool")
            elif tools is not None:
                # The reconnect notice must reach every gated tool, and every tool a skill names.
                for t in sorted(in_matcher - tools):
                    err("hooks/hooks.json", f"{event} matcher does not list the gated tool {t!r}")
                if gen is not None:
                    try:
                        want = set(gen.notice_tools(cfg, skills_src))
                    except SystemExit as e:
                        err("hooks/hooks.json", f"cannot work out the notice matcher: {e}")
                        continue
                    for t in sorted(want - tools):
                        err("hooks/hooks.json", f"{event} matcher does not list {t!r}, which a skill names; "
                                                f"run python3 -I tools/sync_skill.py --sync-hooks")
                    for t in sorted(tools - want):
                        err("hooks/hooks.json", f"{event} matcher lists {t!r}, which no skill names and the guard does not gate; "
                                                f"run python3 -I tools/sync_skill.py --sync-hooks")


def check_server_gaps(tools_by_name):
    for t in PUBLISH_CAPABLE_CREATE_TOOLS:
        a = (tools_by_name.get(t) or {}).get("annotations") or {}
        if t in tools_by_name and not a.get("destructiveHint"):
            info(f"server annotation gap: {t} can schedule or publish but destructiveHint is false; "
                 f"the plugin's PreToolUse guard compensates on Claude Code and Cowork only")


# --------------------------------------------------------------------------- main

def check_root_skill_in_sync(source: pathlib.Path):
    """skills/bolta at the repository root is generated, never edited: it must equal the plugin's skill."""
    mod = load_generator()
    if mod is None:
        return
    for d in mod.differences(mod.generate_root_skill(source), mod.existing(mod.ROOT_SKILL)):
        err("skills/bolta", f"{d}; it is generated from plugins/bolta: run python3 -I tools/sync_skill.py")


def run_checks_plugin(checks, marketplace, tools_by_name, skills_src):
    """Every check for the checks plugin (hooks and scripts only). Returns the gated tools."""
    _ctx[0] = "[bolta-checks] "
    manifest = check_manifest(checks)
    if manifest.get("name") != "bolta-checks":
        err(".claude-plugin/plugin.json", f"the checks plugin is named bolta-checks (got {manifest.get('name')!r})")
    check_marketplace(marketplace, checks, manifest)
    check_files(checks, checks=True)
    for d in ("skills", "agents", "commands"):
        if (checks / d).exists():
            err(f"{d}/", "the checks plugin holds hooks/ and scripts/ only; skills and agents live in plugins/bolta")
    if "confirm_level" not in (manifest.get("userConfig") or {}):
        err(".claude-plugin/plugin.json", "userConfig.confirm_level is missing (the guard reads it)")
    check_links(checks)
    check_citations(checks)
    cfg = check_hooks(checks, manifest)
    check_guard_matches_matcher(checks, cfg, tools_by_name, skills_src)
    gated = set()
    for g in hook_groups(cfg, "PreToolUse") if cfg else []:
        if group_runs(g, "guard-bolta-writes.sh"):
            gated |= matcher_tools(g.get("matcher", "")) or set()
    _ctx[0] = ""
    return gated


def run_checks(plugin, marketplace, tools_by_name, checks, gated, bundle=False, source=None):
    """Every check for one listed plugin. Returns the tool ids its files reference."""
    _ctx[0] = "[bolta-skills] " if bundle else ""
    manifest = check_manifest(plugin)
    _ns[0] = manifest.get("name") or ("bolta-skills" if bundle else "bolta")
    if bundle and manifest.get("name") != "bolta-skills":
        err(".claude-plugin/plugin.json", f"the bundle is named bolta-skills (got {manifest.get('name')!r})")
    if manifest.get("userConfig"):
        err(".claude-plugin/plugin.json", "userConfig belongs to plugins/bolta-checks (no hook here reads it)")
    check_marketplace(marketplace, plugin, manifest)
    check_files(plugin, bundle)
    skills = check_layout(plugin, bundle)
    info(f"{len(skills)} skills")
    check_skills(plugin, skills, tools_by_name, checks)
    referenced = check_tool_ids_and_args(plugin, skills, tools_by_name)
    check_links(plugin)
    check_lint(plugin, skills)
    check_citations(plugin)
    check_agents(plugin, tools_by_name, gated)
    _ctx[0] = ""
    return referenced


# --------------------------------------------------------------------------- key coverage
#
# tools/fixtures/coverage_keys.json (written by tools/build_coverage_fixture.py from the
# server) lists every routine/campaign tool input, per-network field, platform_specific key
# and tool name. Each key carries `tokens_any` (alternative groups; every token of a group
# must appear inside a code span or fence) and `context_any` (one of these words in the same
# file or, for scope "section", the same heading section). A key no reference teaches is an
# ERROR unless tools/fixtures/coverage_exempt.json names it with a reason.

COVERAGE_FIXTURE = REPO / "tools" / "fixtures" / "coverage_keys.json"
COVERAGE_EXEMPT = REPO / "tools" / "fixtures" / "coverage_exempt.json"
_FENCE = re.compile(r"```[^\n]*\n(.*?)```", re.S)
_SPAN = re.compile(r"`([^`\n]+)`")
_CODE_TOKEN = re.compile(r"[A-Za-z_][A-Za-z0-9_]*(?:-[A-Za-z0-9_]+)*")
_HEADING = re.compile(r"^(#{1,6})\s+(.*)$")


def _code_tokens(text: str) -> set[str]:
    toks: set[str] = set()
    for m in _FENCE.finditer(text):
        toks.update(_CODE_TOKEN.findall(m.group(1)))
    rest = _FENCE.sub("", text)
    for m in _SPAN.finditer(rest):
        toks.update(_CODE_TOKEN.findall(m.group(1)))
    toks.update(m.group(1) for m in CALL.finditer(rest))
    return toks


def _coverage_units(refdir: pathlib.Path):
    """(file units, section units): each unit is (where, prose, code tokens, lines).
    File unit: prose is the whole file. Section unit: the text under one heading (each
    table row on its own); prose is its heading chain, and a context word outside the
    chain counts only on the same line as the token."""
    files, sections = [], []
    for path in sorted(refdir.glob("*.md")):
        text = path.read_text()
        files.append((path.name, text, _code_tokens(text), None))
        chain: list[str] = []
        body: list[str] = []

        def flush():
            # A table row is its own unit (a per-network table names many networks in one
            # section); the rest of the section is one unit. Both carry the heading chain.
            rows = [ln for ln in body if ln.lstrip().startswith("|")]
            rest = [ln for ln in body if not ln.lstrip().startswith("|")]
            for chunk in [rest] + [[r] for r in rows]:
                s = "\n".join(chain + chunk)
                sections.append((path.name, "\n".join(chain), _code_tokens(s), chunk))
        in_fence = False
        for line in text.splitlines():
            if line.startswith("```"):
                in_fence = not in_fence
            m = None if in_fence else _HEADING.match(line)
            if m:
                flush()
                level = len(m.group(1))
                chain = chain[: level - 1] + [line]
                body = []
            else:
                body.append(line)
        flush()
    return files, sections


def _covered(key: dict, units) -> str | None:
    ctx = [re.compile(r"(?<![A-Za-z0-9_-])" + re.escape(c) + r"(?![A-Za-z0-9_-])", re.I) for c in key.get("context_any") or []]
    for where, prose, code, lines in units:
        groups = [g for g in key["tokens_any"] if all(t in code for t in g)]
        if not groups:
            continue
        if not ctx or any(c.search(prose) for c in ctx):
            return where
        # Section scope, the network not in the heading chain: it must share a line with the token.
        if lines is not None:
            word = [re.compile(r"(?<![A-Za-z0-9_-])" + re.escape(g[0]) + r"(?![A-Za-z0-9_-])") for g in groups]
            if any(w.search(ln) and any(c.search(ln) for c in ctx) for ln in lines for w in word):
                return where
    return None


def _example_keys(exdir: pathlib.Path):
    """Per network: field names set through save-post platform_details (or Release 1's
    update-post-platform-details platform + fields), and platform_specific keys."""
    fields: dict[str, set] = {}
    ps: dict[str, set] = {}

    def walk(node):
        if isinstance(node, dict):
            if isinstance(node.get("platform"), str) and isinstance(node.get("fields"), dict):
                fields.setdefault(node["platform"], set()).update(node["fields"])
            details = node.get("platform_details")
            if isinstance(details, dict):
                for net, data in details.items():
                    if isinstance(data, dict):
                        fields.setdefault(net, set()).update(data)
            spec = node.get("platform_specific")
            if isinstance(spec, dict):
                for net, data in spec.items():
                    if isinstance(data, dict):
                        ps.setdefault(net, set()).update(data)
                        for acct in (data.get("accounts") or {}).values():
                            if isinstance(acct, dict):
                                ps[net].update(acct)
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)
    for path in sorted(exdir.glob("*.json")):
        try:
            walk(json.loads(path.read_text()))
        except ValueError:
            pass  # check_examples reports bad JSON
    return fields, ps


def check_key_coverage(plugin: pathlib.Path, fixture: pathlib.Path, exempt_path: pathlib.Path,
                       report: pathlib.Path | None = None):
    where = "coverage"
    if not fixture.is_file():
        err(where, f"no key fixture at {fixture}; run tools/build_coverage_fixture.py")
        return
    data = json.loads(fixture.read_text())
    keys = {k["id"]: k for k in data["keys"]}
    exempt: dict = {}
    if exempt_path.is_file():
        exempt = json.loads(exempt_path.read_text())
        if not isinstance(exempt, dict):
            err(where, f"{exempt_path.name} must be an object of key id -> reason")
            exempt = {}
        for kid, reason in exempt.items():
            if kid not in keys:
                err(where, f"{exempt_path.name}: exempt key '{kid}' is not in the fixture (stale?)")
            if not isinstance(reason, str) or not reason.strip():
                err(where, f"{exempt_path.name}: exempt key '{kid}' needs a reason")
    skill = plugin / "skills" / "bolta"
    files, sections = _coverage_units(skill / "references")
    ex_fields, ex_ps = _example_keys(skill / "examples")
    missing: list[dict] = []
    no_example: dict[str, list[str]] = {}
    for kid, key in keys.items():
        found = _covered(key, sections if key.get("scope") == "section" else files)
        if kid in exempt:
            if found:
                warn(where, f"exempt key '{kid}' is taught in {found}: drop the exemption")
            continue
        if not found:
            missing.append(key)
            continue
        ex = key.get("example")
        if ex:
            pool = (ex_fields if ex["where"] == "fields" else ex_ps).get(ex["network"], set())
            spellings = {t for g in key["tokens_any"] for t in g}
            if not pool & spellings:
                no_example.setdefault(ex["network"], []).append(kid.split(".", 1)[1])
    for key in missing:
        err(where, f"{key['id']} is taught in no references/*.md (needs {' or '.join('+'.join(g) for g in key['tokens_any'])}"
                   + (f" near {'/'.join(key['context_any'])}" if key.get("context_any") else "") + f"; from {key['source']})")
    for net, ids in sorted(no_example.items()):
        # A nudge, not a gate: --strict (CI) turns every WARN into a failure, and a key that is taught
        # but not shown in an example is a reason to add an example when one fits, not a broken skill.
        # A key taught in no reference at all stays an ERROR (above).
        info(f"{net}: {len(ids)} per-network key(s) taught but shown in no examples/*.json: {', '.join(sorted(ids))}")
    covered = len(keys) - len(missing) - len(set(exempt) & set(keys))
    info(f"key coverage: {covered}/{len(keys)} keys taught, {len(missing)} missing, {len(set(exempt) & set(keys))} exempt "
         f"(fixture from server {data.get('server_commit', '?')})")
    if report is not None:
        _write_coverage_report(report, data, missing, no_example, exempt)


def _write_coverage_report(path: pathlib.Path, data: dict, missing: list[dict], no_example: dict, exempt: dict):
    by_group: dict[str, list[dict]] = {}
    for k in missing:
        by_group.setdefault(k["group"], []).append(k)
    total = data.get("counts") or {}
    lines = ["# Skill key coverage: missing keys", "",
             f"Fixture: `tools/fixtures/coverage_keys.json` from server `{data.get('server_commit', '?')}`. "
             f"{len(data['keys'])} keys, {len(missing)} missing, {len(exempt)} exempt.", "",
             "| Group | Keys | Missing |", "|-|-|-|"]
    for g, n in sorted(total.items()):
        lines.append(f"| {g} | {n} | {len(by_group.get(g, []))} |")
    for g, ks in sorted(by_group.items()):
        lines += ["", f"## {g} ({len(ks)})", "", "| Key | Needs | Source |", "|-|-|-|"]
        for k in ks:
            needs = " or ".join("+".join(f"`{t}`" for t in grp) for grp in k["tokens_any"])
            if k.get("context_any"):
                needs += " near " + "/".join(k["context_any"])
            lines.append(f"| `{k['id']}` | {needs} | {k['source']} |")
    if no_example:
        lines += ["", "## Taught, but no example (warning)", ""]
        for net, ids in sorted(no_example.items()):
            lines.append(f"- {net}: {', '.join(f'`{i}`' for i in sorted(ids))}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--plugin", type=pathlib.Path, default=DEFAULT_PLUGIN)
    ap.add_argument("--checks", type=pathlib.Path, default=DEFAULT_CHECKS, help="the checks plugin (hooks and scripts)")
    ap.add_argument("--marketplace", type=pathlib.Path, default=DEFAULT_MARKETPLACE)
    ap.add_argument("--tools-json", type=pathlib.Path, help="saved tools/list response instead of fetching")
    ap.add_argument("--tools-url", default=DEFAULT_URL)
    ap.add_argument("--fixture", type=pathlib.Path, default=DEFAULT_FIXTURE, help="saved tool list that supplies the schemas of PENDING_TOOLS the live list lacks")
    ap.add_argument("--no-pending", action="store_true", help="do not fill in PENDING_TOOLS from the saved list: a pending tool the list lacks is an error (run this once the server change is deployed)")
    ap.add_argument("--user-agent", default=CLAUDE_USER_AGENT, help="User-Agent for the live fetch (default: a Claude Code-like one, so the Claude tools show)")
    ap.add_argument("--strict", action="store_true", help="treat warnings as errors")
    ap.add_argument("--require-coverage", action="store_true", help="error when an exposed tool is referenced nowhere (except the deliberately unused ones)")
    ap.add_argument("--coverage-fixture", type=pathlib.Path, default=COVERAGE_FIXTURE, help="key fixture from tools/build_coverage_fixture.py")
    ap.add_argument("--coverage-exempt", type=pathlib.Path, default=COVERAGE_EXEMPT, help="reviewed exemptions: {key id: reason}")
    ap.add_argument("--coverage-report", type=pathlib.Path, help="also write the missing keys as Markdown here")
    ap.add_argument("--coverage-only", action="store_true", help="run only the key coverage check (offline, fast)")
    args = ap.parse_args(argv)

    plugin = args.plugin.resolve()
    if not plugin.is_dir():
        print(f"ERROR no such plugin dir: {plugin}")
        return 2

    # Key coverage needs no tool list, so it runs first and on its own with --coverage-only.
    check_key_coverage(plugin, args.coverage_fixture.resolve(), args.coverage_exempt.resolve(),
                       args.coverage_report.resolve() if args.coverage_report else None)
    if args.coverage_only:
        for line in infos + warns + errors:
            print(line)
        failed = bool(errors) or (args.strict and bool(warns))
        print(f"\n{len(errors)} error(s), {len(warns)} warning(s)" + (" - FAIL" if failed else " - ok"))
        return 1 if failed else 0
    try:
        tools = unwrap_tools(json.loads(args.tools_json.read_text())) if args.tools_json else fetch_tools(args.tools_url, args.user_agent)
    except Exception as e:  # noqa: BLE001 - report any fetch/parse failure plainly
        print(f"ERROR could not load the tool list ({e}). Pass --tools-json to run offline.")
        return 2
    tools_by_name = {t["name"]: t for t in tools}
    info(f"{len(tools_by_name)} tools in the list")
    if not args.no_pending:
        tools_by_name = with_pending(tools_by_name, args.fixture.resolve(), from_server=not args.tools_json)

    marketplace = args.marketplace.resolve()
    checks = args.checks.resolve()
    if not checks.is_dir():
        print(f"ERROR no such checks plugin dir: {checks}")
        return 2
    gated = run_checks_plugin(checks, marketplace, tools_by_name, plugin)
    referenced = run_checks(plugin, marketplace, tools_by_name, checks, gated)
    check_server_gaps(tools_by_name)

    check_root_skill_in_sync(plugin)

    unreferenced = sorted(set(tools_by_name) - referenced - set(INTENTIONALLY_UNUSED))
    if unreferenced:
        msg = f"{len(unreferenced)} exposed tools referenced nowhere in the plugin: {', '.join(unreferenced)}"
        if args.require_coverage:
            err("coverage", msg)
        else:
            info(msg)
    unknown_unused = sorted(t for t in INTENTIONALLY_UNUSED if t not in tools_by_name)
    if unknown_unused:
        info(f"deliberately unused tools no longer exposed: {', '.join(unknown_unused)}")

    for line in infos + warns + errors:
        print(line)
    failed = bool(errors) or (args.strict and bool(warns))
    print(f"\n{len(errors)} error(s), {len(warns)} warning(s)" + (" - FAIL" if failed else " - ok"))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
