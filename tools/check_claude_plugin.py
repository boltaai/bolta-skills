#!/usr/bin/env python3
"""Check the Bolta Claude plugin against the live Bolta tool surface and the
static rules Anthropic's directory applies.

The skills pack has drifted from the server before: a skill that names a tool
the host cannot call is worse than a missing skill, because the model tries it,
gets "unknown tool", and improvises. This gate makes that a CI failure.

Source of truth for tool names and arguments is the server's public
`tools/list`. It varies by User-Agent (OpenAI user agents lose 11 routine tools),
so this script sends a non-OpenAI one.

Usage:
    python3 -I tools/check_claude_plugin.py                       # fetch live
    python3 -I tools/check_claude_plugin.py --tools-json tools.json
    python3 -I tools/check_claude_plugin.py --strict              # warnings fail

Checks, in order: manifest and file hygiene, frontmatter, tool ids, call-site
arguments, host-neutrality lint, agent tool allow-lists, hook scripts.
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

REPO = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_PLUGIN = REPO / "plugins" / "bolta"
DEFAULT_URL = "https://mcp.bolta.ai/mcp"

#: Accepted on every Bolta tool regardless of its declared schema: the MCP layer
#: prepends an optional workspace_id and defaults it to the connection's workspace.
UNIVERSAL_PARAMS = {"workspace_id"}

#: Hyphenated words that legitimately appear in backticks and are not tool ids.
NON_TOOL_TOKENS = {
    "all-external-effects", "publish-only", "read-only", "draft-only",
    "mcp-app", "claude-code",
}

#: Strings a customer-facing skill must never contain (host neutrality).
BANNED_EVERYWHERE = [
    (re.compile(r"\bChatGPT\b"), "names ChatGPT (host-specific)"),
    (re.compile(r"\bOpenAI\b"), "names OpenAI (host-specific)"),
    (re.compile(r"\bwidgets?\b", re.I), "mentions a widget (host-specific)"),
]
#: Allowed only inside a <!-- host-note --> ... <!-- /host-note --> region.
BANNED_OUTSIDE_HOST_NOTE = [
    (re.compile(r"\bcards?\b", re.I), "mentions a card (host-specific; only allowed in the host note)"),
]
HOST_NOTE = re.compile(r"<!--\s*host-note\s*-->.*?<!--\s*/host-note\s*-->", re.S)

#: Tools an agent may call even though they are not annotated read-only.
#: Anything else not readOnlyHint=true in an agent's tools line is an error.
AGENT_WRITE_ALLOWLIST: dict[str, set[str]] = {
    "content-calendar-planner": {"create-post", "bulk-create-posts"},
    "community-triage": set(),
    "approval-batch-reviewer": set(),
    "performance-analyst": set(),
}

#: Known server annotation gaps the plugin hook compensates for.
PUBLISH_CAPABLE_CREATE_TOOLS = ("create-post", "bulk-create-posts", "create-wordpress-blog-post")

ALLOWED_EXT = {".md", ".json", ".sh", ".svg", ".png", ".yaml", ".yml", ".txt"}
IMAGE_EXT = {".png", ".svg", ".jpg", ".jpeg", ".gif", ".webp"}
MAX_TEXT_BYTES = 256 * 1024
MAX_FILES = 512
RESERVED_NAME = re.compile(r"^(claude|anthropic|anthropics|cc-plugin)([-_]|$)|official", re.I)
BRAND_WORDS = re.compile(r"\b(claude|anthropic)\b", re.I)

errors: list[str] = []
warns: list[str] = []
infos: list[str] = []


def err(where, msg):
    errors.append(f"ERROR {where}: {msg}")


def warn(where, msg):
    warns.append(f"WARN  {where}: {msg}")


def info(msg):
    infos.append(f"INFO  {msg}")


# --------------------------------------------------------------------------- tools

def fetch_tools(url: str) -> list[dict]:
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}).encode()
    req = urllib.request.Request(
        url, data=body, method="POST",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "User-Agent": "bolta-plugin-check/1.0",
        },
    )
    with urllib.request.urlopen(req, timeout=30, context=ssl.create_default_context()) as resp:
        text = resp.read().decode("utf-8")
        ctype = resp.headers.get("Content-Type", "")
    if "event-stream" in ctype:
        datas = [ln[5:].strip() for ln in text.splitlines() if ln.startswith("data:")]
        text = datas[-1] if datas else "{}"
    return unwrap_tools(json.loads(text))


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


def md_files(plugin: pathlib.Path):
    for p in sorted(plugin.rglob("*.md")):
        if "evals" in p.relative_to(plugin).parts:
            continue
        yield p


# --------------------------------------------------------------------------- checks

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
    name = m.get("name", "")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name) or len(name) > 64:
        err(mf, f"name {name!r} must be kebab-case, <= 64 chars")
    if RESERVED_NAME.search(name):
        err(mf, f"name {name!r} reads as reserved/official")
    for field in ("displayName", "description"):
        if BRAND_WORDS.search(str(m.get(field, ""))):
            err(mf, f"{field} must not contain 'claude' or 'anthropic'")
    if any(BRAND_WORDS.search(k) for k in m.get("keywords", [])):
        err(mf, "keywords must not contain 'claude' or 'anthropic'")
    for field in ("version", "description", "author", "license"):
        if not m.get(field):
            warn(mf, f"missing {field}")
    for field in ("homepage", "documentationUrl", "supportUrl", "privacyPolicyUrl", "termsOfServiceUrl"):
        v = m.get(field)
        if v and not str(v).startswith("https://"):
            err(mf, f"{field} must be https")
    icon = m.get("icon")
    if icon and not (plugin / icon).is_file():
        err(mf, f"icon {icon} not found")
    for forbidden in ("$schema", "extensions", "hooks"):
        if forbidden in m:
            err(mf, f"remove {forbidden!r} (OpenAI-only or auto-loaded)")
    return m


def check_files(plugin: pathlib.Path):
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
        words = len(re.findall(r"\w+", strip_fences(readme.read_text())))
        if words < 40:
            err("README.md", f"{words} words outside code blocks; need >= 40")
    mcp = plugin / ".mcp.json"
    if mcp.is_file():
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


def collect_components(plugin: pathlib.Path):
    skills = {p.parent.name: p for p in (plugin / "skills").glob("*/SKILL.md")}
    commands = {p.stem: p for p in (plugin / "commands").glob("*.md")}
    agents = {p.stem: p for p in (plugin / "agents").glob("*.md")}
    return skills, commands, agents


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
        elif val.startswith(PLAIN_SCALAR_BAD_START) and key != "tools":
            err(rel, f"frontmatter {key!r} starts with {val[0]!r}, which YAML reads as an indicator; quote it")
    try:  # authoritative when PyYAML is installed
        import yaml  # type: ignore
        yaml.safe_load("\n".join(fm_lines))
    except ImportError:
        pass
    except Exception as e:  # noqa: BLE001
        err(rel, f"frontmatter is not valid YAML: {str(e).splitlines()[0]}")


def check_frontmatter(plugin, skills, commands, agents, tools_by_name):
    for group in (skills, commands, agents):
        for _name, path in group.items():
            check_yaml_safety(path.relative_to(plugin), path.read_text())
    for name, path in skills.items():
        fm, body = split_frontmatter(path.read_text())
        rel = path.relative_to(plugin)
        if fm is None:
            err(rel, "no frontmatter")
            continue
        if fm.get("name") != name:
            err(rel, f"name {fm.get('name')!r} must equal folder {name!r}")
        desc = fm.get("description", "")
        if not desc:
            err(rel, "missing description")
        elif len(desc) > 1536:
            err(rel, f"description {len(desc)} chars exceeds the 1,536 listing cap")
        elif len(desc) > 900:
            warn(rel, f"description {len(desc)} chars; keep under ~900 (it is always in context)")
        for bad in ("allowed-tools", "allowed_tools", "tools_required"):
            if bad in fm:
                err(rel, f"frontmatter key {bad!r} is not allowed (erodes the confirmation gate)")
        n = len(body.split("\n"))
        if n > 500:
            err(rel, f"{n} lines; max 500")
        elif n > 250:
            warn(rel, f"{n} lines; move detail to references/")
    for name, path in commands.items():
        fm, _ = split_frontmatter(path.read_text())
        rel = path.relative_to(plugin)
        if not fm or not fm.get("description"):
            err(rel, "command needs a description in frontmatter")
        if fm and "allowed-tools" in fm:
            err(rel, "allowed-tools is not allowed")
    for name, path in agents.items():
        fm, _ = split_frontmatter(path.read_text())
        rel = path.relative_to(plugin)
        if not fm:
            err(rel, "no frontmatter")
            continue
        if fm.get("name") != name:
            err(rel, f"name {fm.get('name')!r} must equal file stem {name!r}")
        if not fm.get("description"):
            err(rel, "missing description")
        if not fm.get("model"):
            err(rel, "agent needs an explicit model")
        listed = [t.strip() for t in fm.get("tools", "").split(",") if t.strip()]
        if not listed:
            err(rel, "agent needs an explicit tools allow-list")
        allowed_writes = AGENT_WRITE_ALLOWLIST.get(name)
        if allowed_writes is None:
            warn(rel, "agent not in AGENT_WRITE_ALLOWLIST; add it to tools/check_claude_plugin.py")
            allowed_writes = set()
        for t in listed:
            if not t.startswith("mcp__"):
                if t not in ("Read", "Glob", "Grep"):
                    err(rel, f"built-in tool {t!r} not expected in a Bolta agent")
                continue
            base = t.rsplit("__", 1)[-1]
            tool = tools_by_name.get(base)
            if tool is None:
                err(rel, f"agent lists unknown Bolta tool {base!r}")
                continue
            if not (tool.get("annotations") or {}).get("readOnlyHint") and base not in allowed_writes:
                err(rel, f"agent {name} lists non-read-only tool {base!r}")
        # both naming forms must be present for every Bolta tool, or one install mode loses it
        bases = {t.rsplit("__", 1)[-1] for t in listed if t.startswith("mcp__")}
        for b in sorted(bases):
            for prefix in ("mcp__plugin_bolta_bolta__", "mcp__bolta__"):
                if prefix + b not in listed:
                    err(rel, f"missing {prefix}{b} (list both install-mode names)")


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


def check_tool_ids_and_args(plugin, skills, commands, agents, tools_by_name):
    siblings = set(skills) | set(commands) | set(agents)
    referenced: set[str] = set()
    for path in md_files(plugin):
        rel = path.relative_to(plugin)
        text = path.read_text()
        fm, _ = split_frontmatter(text)
        scan = text
        if rel.parts[0] == "agents" and fm:  # tools line holds mcp__ names, not prose
            scan = text.split("---", 2)[-1]
        for m in TOKEN.finditer(scan):
            tok = m.group(1)
            if tok in tools_by_name:
                referenced.add(tok)
            elif tok in siblings or tok in NON_TOOL_TOKENS:
                continue
            elif "_" in tok:
                continue
            else:
                err(rel, f"`{tok}` is not an exposed Bolta tool, skill, command or agent")
        for m in CALL.finditer(scan):
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
    return referenced


def check_lint(plugin):
    for path in md_files(plugin):
        rel = path.relative_to(plugin)
        text = path.read_text()
        body = text
        is_agent = rel.parts[0] == "agents"
        if is_agent:
            body = re.sub(r"^---.*?---", "", text, count=1, flags=re.S)  # tools line is allowed to carry mcp__
        host_free = HOST_NOTE.sub("", body)
        for rx, why in BANNED_EVERYWHERE:
            if rx.search(body):
                err(rel, why)
        for rx, why in BANNED_OUTSIDE_HOST_NOTE:
            if rx.search(host_free):
                err(rel, why)
        if "mcp__" in body:
            err(rel, "write bare tool ids; mcp__ names belong only in hooks, agent tools lines and evals")
        for m in re.finditer(r"(?<![\w:/.-])/(setup|draft|plan-week|status|review|inbox|report)\b(?!-)", body):
            err(rel, f"bare slash command {m.group(0)!r}; commands are namespaced (/bolta:{m.group(1)}) and bare /review and /status are Claude Code built-ins")
        for m in re.finditer(r"\b(\d{2,3})\s+(?:Bolta\s+)?(?:MCP\s+)?tools\b", body):
            warn(rel, f"tool count in prose ({m.group(0)!r}); counts drift, remove it")
        if re.search(r"(?i)requires?\s+(an?\s+)?(admin|owner)\b", body):
            warn(rel, "asserts a role requirement; say 'call get-my-capabilities' instead")
        if re.search(r"\bvoice-generate\b", body) and rel.parts[0] in ("skills", "commands", "agents"):
            warn(rel, "mentions voice-generate (async, no readback over MCP); only as a do-not-use note")


def check_hooks(plugin):
    hj = plugin / "hooks" / "hooks.json"
    if not hj.is_file():
        warn("hooks/hooks.json", "missing")
        return
    try:
        cfg = json.loads(hj.read_text())
    except json.JSONDecodeError as e:
        err("hooks/hooks.json", f"invalid JSON: {e}")
        return
    if "hooks" not in cfg:
        err("hooks/hooks.json", "needs a top-level 'hooks' key")
        return
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
                    err("hooks/hooks.json", f"script {script.relative_to(plugin)} not found")
                    continue
                if not os.access(script, os.X_OK):
                    err(script.relative_to(plugin), "not executable")
                first = script.read_text().split("\n", 1)[0]
                if first.strip() not in ("#!/bin/sh", "#!/usr/bin/env sh"):
                    err(script.relative_to(plugin), f"must be plain POSIX shell (shebang {first!r})")
                src = "\n".join(l for l in script.read_text().split("\n") if not l.lstrip().startswith("#"))
                if re.search(r"\b(curl|wget|nc|python3?|node|jq)\b", src):
                    err(script.relative_to(plugin), "scripts must not use network tools, python, node or jq")


def check_guard_matches_matcher(plugin, tools_by_name):
    """Every tool the guard script decides on must be in the hook matcher (or the guard never runs
    for it), and every tool in the matcher must be a real tool the guard handles."""
    script = plugin / "scripts" / "guard-bolta-writes.sh"
    hj = plugin / "hooks" / "hooks.json"
    if not script.is_file() or not hj.is_file():
        return
    src = script.read_text()
    case_body = src[src.index('case "$tool" in'):]
    in_script = set()
    for m in re.finditer(r"^  ([a-z][a-z0-9|-]*)\)\s*$", case_body, re.M):
        in_script.update(m.group(1).split("|"))
    try:
        matcher = json.loads(hj.read_text())["hooks"]["PreToolUse"][0]["matcher"]
    except (KeyError, IndexError, json.JSONDecodeError):
        err("hooks/hooks.json", "no PreToolUse matcher found")
        return
    alt = re.search(r"__\(([^)]*)\)\$", matcher)
    in_matcher = set(alt.group(1).split("|")) if alt else set()
    for t in sorted(in_script - in_matcher):
        err("hooks/hooks.json", f"guard script decides on {t!r} but the matcher does not list it, so the guard never runs for it")
    for t in sorted(in_matcher - in_script):
        err("scripts/guard-bolta-writes.sh", f"matcher lists {t!r} but the guard script has no case for it")
    for t in sorted(in_script | in_matcher):
        if t not in tools_by_name:
            err("scripts/guard-bolta-writes.sh", f"guards {t!r}, which is not an exposed Bolta tool")


def check_server_gaps(tools_by_name):
    for t in PUBLISH_CAPABLE_CREATE_TOOLS:
        a = (tools_by_name.get(t) or {}).get("annotations") or {}
        if t in tools_by_name and not a.get("destructiveHint"):
            info(f"server annotation gap: {t} can schedule or publish but destructiveHint is false; "
                 f"the plugin's PreToolUse guard compensates on Claude Code and Cowork only")


# --------------------------------------------------------------------------- main

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--plugin", type=pathlib.Path, default=DEFAULT_PLUGIN)
    ap.add_argument("--tools-json", type=pathlib.Path, help="saved tools/list response instead of fetching")
    ap.add_argument("--tools-url", default=DEFAULT_URL)
    ap.add_argument("--strict", action="store_true", help="treat warnings as errors")
    ap.add_argument("--require-coverage", action="store_true", help="error when an exposed tool is referenced nowhere")
    args = ap.parse_args(argv)

    plugin = args.plugin.resolve()
    if not plugin.is_dir():
        print(f"ERROR no such plugin dir: {plugin}")
        return 2
    try:
        tools = unwrap_tools(json.loads(args.tools_json.read_text())) if args.tools_json else fetch_tools(args.tools_url)
    except Exception as e:  # noqa: BLE001 - report any fetch/parse failure plainly
        print(f"ERROR could not load the tool list ({e}). Pass --tools-json to run offline.")
        return 2
    tools_by_name = {t["name"]: t for t in tools}
    info(f"{len(tools_by_name)} tools exposed by the server")

    check_manifest(plugin)
    check_files(plugin)
    skills, commands, agents = collect_components(plugin)
    info(f"{len(skills)} skills, {len(commands)} commands, {len(agents)} agents")
    check_frontmatter(plugin, skills, commands, agents, tools_by_name)
    referenced = check_tool_ids_and_args(plugin, skills, commands, agents, tools_by_name)
    check_lint(plugin)
    check_hooks(plugin)
    check_guard_matches_matcher(plugin, tools_by_name)
    check_server_gaps(tools_by_name)

    unreferenced = sorted(set(tools_by_name) - referenced)
    if unreferenced:
        msg = f"{len(unreferenced)} exposed tools referenced nowhere in the plugin: {', '.join(unreferenced)}"
        if args.require_coverage:
            err("coverage", msg)
        else:
            info(msg)

    for line in infos + warns + errors:
        print(line)
    failed = bool(errors) or (args.strict and bool(warns))
    print(f"\n{len(errors)} error(s), {len(warns)} warning(s)" + (" - FAIL" if failed else " - ok"))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
