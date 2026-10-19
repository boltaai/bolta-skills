#!/usr/bin/env python3
"""Check the Bolta Claude plugin (v0.2) against the live Bolta tool surface,
the plugin's own house style, and the static rules Anthropic's directory applies.

The skills have drifted from the server before: a skill that names a tool the
host cannot call is worse than a missing skill, because the model tries it,
gets "unknown tool", and improvises. This gate makes that a CI failure. It also
keeps v0.2 short and plain: twelve skills, each a few hundred words, no
commands, no subagents, and no internal words in what the user reads.

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

It checks two plugins: plugins/bolta (the full plugin, with its own Bolta
connection) and plugins/bolta-skills (the skills-only bundle for people who
already connected Bolta themselves, generated from the full plugin by
tools/build_skills_bundle.py). The bundle must have no .mcp.json and must match
what the generator would write byte for byte. In both plugins the hook matchers
must fit Bolta under any server name (the plugin's own, a connector, or a server
added by hand), because a call a matcher misses gets no check.

Usage:
    python3 -I tools/check_claude_plugin.py                       # fetch live
    python3 -I tools/check_claude_plugin.py --tools-json tools.json   # offline, e.g. CI
    python3 -I tools/check_claude_plugin.py --no-pending          # live list only
    python3 -I tools/check_claude_plugin.py --strict              # warnings fail
    python3 -I tools/check_claude_plugin.py --require-coverage    # every tool used
    python3 -I tools/check_claude_plugin.py --no-bundle           # the full plugin only

Checks, in order: manifest and marketplace, file hygiene, layout (skills only,
no commands/ or agents/), skill frontmatter (strict YAML, name, description),
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
DEFAULT_BUNDLE = REPO / "plugins" / "bolta-skills"
DEFAULT_MARKETPLACE = REPO / ".claude-plugin" / "marketplace.json"
DEFAULT_URL = "https://mcp.bolta.ai/mcp"
#: The Claude tool list of the server change that adds PENDING_TOOLS: name, title,
#: description, inputSchema and annotations of every tool, in the tools/list shape.
DEFAULT_FIXTURE = REPO / "tools" / "fixtures" / "claude_tools_list.json"
#: Tools the skills and the guard use that production does not list yet. While the
#: live list lacks one, its schema comes from DEFAULT_FIXTURE. Delete a name here
#: once the live list has it (the checker says when).
PENDING_TOOLS = ("approve-many-posts", "reject-post", "set-content-campaign-targets",
                 "analyze-content-campaign-source")
#: Claude Code sends "claude-code/<version> (<entrypoint>)" on its MCP requests,
#: and the server matches "claude" in it. Without it the list lacks the tools made for Claude.
CLAUDE_USER_AGENT = "claude-code/2.1.302 (cli; bolta-plugin-check)"

#: Accepted on every Bolta tool regardless of its declared schema: the MCP layer
#: prepends an optional workspace_id and defaults it to the connection's workspace.
UNIVERSAL_PARAMS = {"workspace_id"}

#: Hyphenated words that legitimately appear in backticks and are not tool ids.
NON_TOOL_TOKENS = {"read-only", "draft-only", "mcp-app", "claude-code", "bolta-skills"}

#: Exposed tools the skills deliberately never use. Naming one in a skill is an
#: error only where the reason says so (`forbid`).
INTENTIONALLY_UNUSED = {
    "voice-generate": ("spends credits on every call and nothing here can read what it makes", True),
    "list-reviews": ("the review list is read with list-inbox-items", False),
}

#: The v0.2 skill set and the order of sections inside every SKILL.md.
SKILLS = ("today", "start", "post", "review", "routine", "campaign", "results",
          "voice", "replies", "connect", "fix", "my-workflow")
SECTIONS = ["Done when", "Know this", "Tools", "Hand off", "Always"]
HOUSE_RULES_LINE = "Follow the house rules in the `today` skill."
RULES_SKILL = "today"

#: v0.1 names that must not come back (skills, commands, subagents).
OLD_NAMES = {
    "workspace-setup", "social-publishing", "content-planning", "routines", "approvals",
    "social-inbox", "outbound-engagement", "analytics-review", "brand-voice-setup",
    "brand-voice-check", "accounts-and-buckets", "wordpress-blog", "undo-and-recovery",
    "approval-batch-reviewer", "community-triage", "content-calendar-planner",
    "performance-analyst", "plan-week",
}

#: Budgets, in words as `LC_ALL=C wc -w` counts them (see words()).
MAX_SKILL_WORDS = 500          # SKILL.md body, frontmatter excluded
MAX_REFERENCE_WORDS = 600      # each references/*.md
MAX_SKILLS_TOTAL_WORDS = 10_000  # all SKILL.md files together, frontmatter included
MAX_DESCRIPTION_WORDS = 60
MAX_README_WORDS = 400
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

PUBLISH_CAPABLE_CREATE_TOOLS = ("create-post", "bulk-create-posts", "create-wordpress-blog-post")

ALLOWED_EXT = {".md", ".json", ".sh", ".svg", ".png", ".yaml", ".yml", ".txt"}
IMAGE_EXT = {".png", ".svg", ".jpg", ".jpeg", ".gif", ".webp"}
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

#: Which plugin is being checked. Messages carry it for the bundle so the two never blur.
_ctx = [""]
#: The plugin's name, which is also its slash-command namespace (/bolta:today, /bolta-skills:today).
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
        a = set((live[n].get("inputSchema") or {}).get("properties", {}))
        b = set((saved.get(n, {}).get("inputSchema") or {}).get("properties", {}))
        if saved and a != b:
            warn("tools", f"{n} is live now with different arguments than the saved list "
                          f"(live only: {sorted(a - b) or '-'}; saved only: {sorted(b - a) or '-'}); refresh the saved list")
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


def check_files(plugin: pathlib.Path, bundle: bool = False):
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
        if p.suffix.lower() not in ALLOWED_EXT and p.name not in ("LICENSE", "NOTICE"):
            err(rel, f"file type {p.suffix or '(none)'} not allowed")
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


def check_layout(plugin: pathlib.Path):
    """v0.2 is skills only. Commands copied skills; subagents are ignored by chat and
    their hard-coded tool names break for a connection named after a client."""
    for d in ("commands", "agents"):
        if (plugin / d).exists():
            err(f"{d}/", "v0.2 ships no commands or subagents; every skill already shows as /bolta:<name>")
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
            if r.parts[0] != "references" or p.suffix != ".md" or len(r.parts) != 2:
                err(p.relative_to(plugin), "a skill folder holds SKILL.md and references/<topic>.md only")
    missing = [s for s in SKILLS if s not in skills]
    extra = [s for s in skills if s not in SKILLS]
    for s in missing:
        err("skills/", f"missing the {s!r} skill")
    for s in extra:
        warn(f"skills/{s}", "not one of the v0.2 skills; add it to SKILLS in tools/check_claude_plugin.py if it is meant to ship")
    for s in skills:
        if s in OLD_NAMES:
            err(f"skills/{s}", "a v0.1 skill name; v0.2 replaced it")
    return skills


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


def house_rules_from_script(plugin):
    p = plugin / "scripts" / "bolta-house-rules.sh"
    if not p.is_file():
        return None
    return re.findall(r"^(\d{1,2}\. .+)$", p.read_text(), re.M)


def check_skills(plugin, skills, tools_by_name):
    total = 0
    script_rules = house_rules_from_script(plugin)
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
        for tok in re.findall(r"`([^`]+)`", sec.get("Hand off", "")):
            if tok.startswith("/bolta:"):
                tok = tok[len("/bolta:"):]
            if tok not in skills:
                err(rel, f"Hand off names `{tok}`, which is not a skill")
        for tok in re.findall(r"`([a-z][a-z0-9]*(?:-[a-z0-9]+)+)`", sec.get("Tools", "")):
            if tok not in tools_by_name:
                err(rel, f"Tools lists `{tok}`, which is not an exposed Bolta tool")
        always = sec.get("Always", "")
        if name == RULES_SKILL:
            rules = re.findall(r"^(\d{1,2}\. .+)$", always, re.M)
            if len(rules) != 10:
                err(rel, f"Always must hold the 10 house rules; found {len(rules)}")
            if script_rules is not None and rules != script_rules:
                err(rel, "the house rules differ from scripts/bolta-house-rules.sh; keep them word for word")
        else:
            if HOUSE_RULES_LINE not in always:
                err(rel, f"Always must say: {HOUSE_RULES_LINE}")
            musts = [ln for ln in always.split("\n") if ln.startswith("- ") and HOUSE_RULES_LINE not in ln]
            if len(musts) > MAX_ALWAYS_MUSTS:
                err(rel, f"Always has {len(musts)} skill-specific musts; at most {MAX_ALWAYS_MUSTS}")

        refdir = path.parent / "references"
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


def check_tool_ids_and_args(plugin, skills, tools_by_name):
    siblings = set(skills)
    referenced: set[str] = set()
    for path in md_files(plugin):
        rel = path.relative_to(plugin)
        text = path.read_text()
        for m in re.finditer(r"`([^`\s]+)`", text):
            if m.group(1) in OLD_NAMES:
                err(rel, f"`{m.group(1)}` is a v0.1 skill, command or subagent; v0.2 replaced it")
        for m in TOKEN.finditer(text):
            tok = m.group(1)
            if tok in tools_by_name:
                referenced.add(tok)
            elif tok in siblings or tok in NON_TOOL_TOKENS:
                continue
            else:
                err(rel, f"`{tok}` is not an exposed Bolta tool or skill")
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
        for m in re.finditer(r"mcp__[\w-]*", body):
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
                err(rel, f"/{_ns[0]}:{m.group(1)} is not a skill (v0.2 has no commands)")
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
    """tools/build_skills_bundle.py as a module (it holds the rules for the notice matcher and the bundle)."""
    gen = REPO / "tools" / "build_skills_bundle.py"
    if not gen.is_file():
        err("bundle", "tools/build_skills_bundle.py is missing")
        return None
    sys.dont_write_bytecode = True  # loading the generator must leave no __pycache__ behind
    spec = importlib.util.spec_from_file_location("build_skills_bundle", gen)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def check_guard_matches_matcher(plugin, cfg, tools_by_name):
    """Every tool the guard decides on must be in the hook matcher (or the guard never runs
    for it), and every tool in the matcher must be a real tool the guard handles. The marker
    hook may only watch gated tools, and every Bolta matcher must catch every Bolta server name."""
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
        if t not in tools_by_name:
            err("scripts/guard-bolta-writes.sh", f"guards {t!r}, which is not an exposed Bolta tool")
    if not any(h.get("onFailure") == "block" for h in guards[0].get("hooks", [])):
        warn("hooks/hooks.json", "the guard has no \"onFailure\": \"block\"; a crashed guard would let the call through")
    check_matcher_samples("PreToolUse guard", matcher, "approve-post")
    gen = load_generator()
    for event in ("PostToolUse", "PostToolUseFailure"):
        for g in hook_groups(cfg, event):
            m = g.get("matcher", "")
            tools = matcher_tools(m)
            sample = sorted(tools)[0] if tools else "approve-post"
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
                        want = set(gen.notice_tools(cfg, plugin))
                    except SystemExit as e:
                        err("hooks/hooks.json", f"cannot work out the notice matcher: {e}")
                        continue
                    for t in sorted(want - tools):
                        err("hooks/hooks.json", f"{event} matcher does not list {t!r}, which a skill names; "
                                                f"run python3 -I tools/build_skills_bundle.py --sync-hooks")
                    for t in sorted(tools - want):
                        err("hooks/hooks.json", f"{event} matcher lists {t!r}, which no skill names and the guard does not gate; "
                                                f"run python3 -I tools/build_skills_bundle.py --sync-hooks")


def check_server_gaps(tools_by_name):
    for t in PUBLISH_CAPABLE_CREATE_TOOLS:
        a = (tools_by_name.get(t) or {}).get("annotations") or {}
        if t in tools_by_name and not a.get("destructiveHint"):
            info(f"server annotation gap: {t} can schedule or publish but destructiveHint is false; "
                 f"the plugin's PreToolUse guard compensates on Claude Code and Cowork only")


# --------------------------------------------------------------------------- main

def check_bundle_in_sync(bundle: pathlib.Path, source: pathlib.Path):
    """The bundle is generated, never edited: it must equal what the generator writes now."""
    mod = load_generator()
    if mod is None:
        return
    try:
        expected = mod.generate(source)
    except SystemExit as e:
        err("bundle", f"the generator refused: {e}")
        return
    for d in mod.differences(expected, mod.existing(bundle)):
        err("bundle", f"{d}; it is generated from plugins/bolta: run python3 -I tools/build_skills_bundle.py")


def run_checks(plugin, marketplace, tools_by_name, bundle=False, source=None):
    """Every check for one plugin. Returns the tool ids its files reference."""
    _ctx[0] = "[bolta-skills] " if bundle else ""
    manifest = check_manifest(plugin)
    _ns[0] = manifest.get("name") or ("bolta-skills" if bundle else "bolta")
    if bundle and manifest.get("name") != "bolta-skills":
        err(".claude-plugin/plugin.json", f"the bundle is named bolta-skills (got {manifest.get('name')!r})")
    check_marketplace(marketplace, plugin, manifest)
    check_files(plugin, bundle)
    skills = check_layout(plugin)
    info(f"{len(skills)} skills")
    check_skills(plugin, skills, tools_by_name)
    referenced = check_tool_ids_and_args(plugin, skills, tools_by_name)
    check_links(plugin)
    check_lint(plugin, skills)
    check_citations(plugin)
    cfg = check_hooks(plugin, manifest)
    check_guard_matches_matcher(plugin, cfg, tools_by_name)
    if bundle:
        check_bundle_in_sync(plugin, source)
    _ctx[0] = ""
    return referenced


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--plugin", type=pathlib.Path, default=DEFAULT_PLUGIN)
    ap.add_argument("--bundle", type=pathlib.Path, default=DEFAULT_BUNDLE, help="the skills-only bundle (generated by tools/build_skills_bundle.py)")
    ap.add_argument("--no-bundle", action="store_true", help="check the full plugin only")
    ap.add_argument("--marketplace", type=pathlib.Path, default=DEFAULT_MARKETPLACE)
    ap.add_argument("--tools-json", type=pathlib.Path, help="saved tools/list response instead of fetching")
    ap.add_argument("--tools-url", default=DEFAULT_URL)
    ap.add_argument("--fixture", type=pathlib.Path, default=DEFAULT_FIXTURE, help="saved tool list that supplies the schemas of PENDING_TOOLS the live list lacks")
    ap.add_argument("--no-pending", action="store_true", help="do not fill in PENDING_TOOLS from the saved list: a pending tool the list lacks is an error (run this once the server change is deployed)")
    ap.add_argument("--user-agent", default=CLAUDE_USER_AGENT, help="User-Agent for the live fetch (default: a Claude Code-like one, so the Claude tools show)")
    ap.add_argument("--strict", action="store_true", help="treat warnings as errors")
    ap.add_argument("--require-coverage", action="store_true", help="error when an exposed tool is referenced nowhere (except the deliberately unused ones)")
    args = ap.parse_args(argv)

    plugin = args.plugin.resolve()
    if not plugin.is_dir():
        print(f"ERROR no such plugin dir: {plugin}")
        return 2
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
    referenced = run_checks(plugin, marketplace, tools_by_name)
    check_server_gaps(tools_by_name)

    if not args.no_bundle:
        bundle = args.bundle.resolve()
        if not bundle.is_dir():
            err("bundle", f"{args.bundle} does not exist; generate it with python3 -I tools/build_skills_bundle.py")
        else:
            run_checks(bundle, marketplace, tools_by_name, bundle=True, source=plugin)

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
