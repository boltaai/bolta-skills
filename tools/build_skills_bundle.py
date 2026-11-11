#!/usr/bin/env python3
"""Build the skills-only bundle (plugins/bolta-skills) from the full plugin (plugins/bolta).

Some people already connected Bolta themselves: as a connector in claude.ai,
the desktop app or Cowork, or as an MCP server added by hand (`claude mcp add`).
Installing the full plugin on top registers Bolta's tools a second time. The
bundle has the same skills and no `.mcp.json`, so it never starts a connection
of its own.

Nothing in the bundle is written by hand except the README text in this file.
Everything else is derived from plugins/bolta, so the two cannot drift:

  copied as is      assets/, LICENSE, every skill file (SKILL.md, references/, examples/)
  text rewritten    "/bolta:<skill>" becomes "/bolta-skills:<skill>" (a plugin's
                    name is its slash-command namespace)
  rewritten         .claude-plugin/plugin.json (name, display name, description)
                    README.md (this file's BUNDLE_README)
  left out          .mcp.json, agents/

Neither plugin carries hooks. The Bolta checks (hooks/hooks.json and the
scripts) live in plugins/bolta-checks, a plugin of their own: Anthropic's
directory accepts command hooks and shell scripts only from Verified
organizations, so the listed plugins ship without them and the checks install
from GitHub next to either. Their matchers match any server name followed by
one of Bolta's own tool names: a claude.ai connector's tools are
mcp__claude_ai_<name>__<tool>, a server added with `claude mcp add <name>` is
mcp__<name>__<tool>, and the full plugin's own server is
mcp__plugin_bolta_bolta__<tool>. The guard never asks about a tool it has no
case for, and it asks (never allows) for every tool it does, so matching every
server name can only add a check. Nothing there has to be told which server it
runs for.

The reconnect-notice matcher lists tools by name (any server name is too wide
for a hook that runs after every call). Keep it in step with the skills:

    python3 -I tools/build_skills_bundle.py --sync-hooks   # rewrite it in plugins/bolta-checks/hooks/hooks.json

Usage:
    python3 -I tools/build_skills_bundle.py            # write plugins/bolta-skills
    python3 -I tools/build_skills_bundle.py --check    # exit 1 if it is out of date
    python3 -I tools/build_skills_bundle.py --sync-hooks   # refresh the notice matcher in plugins/bolta-checks
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
SRC = REPO / "plugins" / "bolta"
DST = REPO / "plugins" / "bolta-skills"
#: The checks plugin: the one place hooks/hooks.json and the scripts live.
CHECKS = REPO / "plugins" / "bolta-checks"

#: The skill on its own at the repository root (skills/bolta), byte for byte the plugin's. It is
#: what every other client reads: the open `skills` installer, a Cursor plugin, a Gemini CLI
#: extension and anything else that looks for skills/<name>/SKILL.md. Generated, never edited.
ROOT_SKILL = REPO / "skills" / "bolta"
SKILL_SRC = "skills/bolta"

BUNDLE_NAME = "bolta-skills"
FULL_NAME = "bolta"

#: How every matcher begins: any server name, then a tool name.
PREFIX = "^mcp__[A-Za-z0-9_-]+__"

#: Files of the full plugin that the bundle does not copy: its own connection, and the subagents
#: (an agent's tool list names the server, and this bundle's connection can have any name; chat
#: ignores agents too, so the skills do that work themselves). hooks/ and scripts/ belong to
#: plugins/bolta-checks and must not be in either listed plugin.
LEFT_OUT = {".mcp.json"}
LEFT_OUT_DIRS = ("agents/", "hooks/", "scripts/")
#: Files the bundle writes itself.
REWRITTEN = {".claude-plugin/plugin.json", "README.md"}

BUNDLE_DESCRIPTION = (
    "Bolta's skills for people who already connected Bolta themselves, "
    "as a connector or an MCP server they added. No second connection. "
    "Nothing goes out until you say yes."
)

BUNDLE_README = """# BOLTA skills

The same Bolta skill as the `bolta` plugin, with no connection of its own. Tell Claude what you want to post about. Bolta writes it in your voice every week, and nothing goes out until you say yes.

## Which one to install

- **bolta** brings its own Bolta connection. Pick it if Bolta is not connected yet.
- **bolta-skills** (this one) brings none. Pick it if you already added Bolta in claude.ai (Customize > Connectors), in Cowork, or with `claude mcp add`.
- Never both: the skill would load twice.
- **bolta-checks** adds the Bolta checks in Claude Code (see below). Install it next to either.

Claude Code connects an address once, and your own `claude mcp add` server wins over the plugin's.

## Install

```
/plugin marketplace add boltaai/bolta-skills
/plugin install bolta-skills@bolta-marketplace
```

Then `/mcp`: Bolta should show as connected. Start with `/bolta-skills:bolta` or "set me up".

## What Bolta checks, and where

Nothing is approved, scheduled, published or switched on until you say yes: Claude asks in words first, and posts stay on your review list until then. In the connector's settings, keep approve, schedule, publish and reject on "Needs approval".

In Claude Code, `bolta-checks` turns that into a Bolta check you answer before anything public, approving or turning down posts (once per batch per message), running a Bolta routine now, starting or finishing a campaign, changing a running campaign, and changing your voice or business details. Drafts need none. The checks go by each tool's name, so any connection name works. Chat and Cowork run no plugin hooks.

## Limits

- One connection is one organization and reaches the brands you ticked. A new brand needs a reconnect.
- No media upload: Instagram, TikTok, YouTube and Pinterest need a public link.

## Sent and stored

Bolta (mcp.bolta.ai) gets your requests and decisions. Claude handles sign-in; the plugin never sees a password. The plugin makes no network calls of its own.

v{version} (beta). [Privacy](https://bolta.ai/privacy-policy) · [Terms](https://bolta.ai/tos) · [Support](https://bolta.ai/support) · MIT licence
"""


def _read(path: pathlib.Path) -> bytes:
    return path.read_bytes()


def gated_tools(full_hooks: dict) -> list[str]:
    """The tools the full plugin's guard matcher lists."""
    for group in full_hooks["hooks"].get("PreToolUse", []):
        if any("guard-bolta-writes.sh" in h.get("command", "") for h in group.get("hooks", [])):
            m = re.search(r"__\(([^)]*)\)\$$", group["matcher"])
            if m:
                return m.group(1).split("|")
    raise SystemExit("build_skills_bundle: cannot find the guard matcher in plugins/bolta-checks/hooks/hooks.json")


def skill_tools(src: pathlib.Path) -> set[str]:
    """Every tool id named in a Tools section: the playbooks (references/<name>.md) hold them."""
    out: set[str] = set()
    for skill in sorted([*(src / "skills").glob("*/SKILL.md"), *(src / "skills").glob("*/references/*.md")]):
        text = skill.read_text()
        m = re.search(r"^## Tools\s*\n(.*?)(?=^## )", text, re.S | re.M)
        if m:
            out.update(re.findall(r"`([a-z][a-z0-9]*(?:-[a-z0-9]+)+)`", m.group(1)))
    return out


def notice_tools(full_hooks: dict, src: pathlib.Path) -> list[str]:
    """The tools the reconnect-notice matcher must list: the guard's, and every one a skill names.
    (Any server name is too wide for a hook that runs after every call, so it names the tools.)"""
    return sorted(set(gated_tools(full_hooks)) | skill_tools(src))


def notice_matcher(names: list[str]) -> str:
    return PREFIX + "(" + "|".join(names) + ")$"


def notice_groups(hooks: dict):
    """The PostToolUse and PostToolUseFailure groups that run the reconnect notice."""
    for event in ("PostToolUse", "PostToolUseFailure"):
        for group in hooks["hooks"].get(event, []):
            if any("bolta-auth-notice.sh" in h.get("command", "") for h in group.get("hooks", [])):
                yield event, group


def synced_hooks(full_hooks: dict, src: pathlib.Path) -> dict:
    """The full plugin's hooks with the reconnect-notice matchers rewritten from the skills."""
    out = json.loads(json.dumps(full_hooks))  # deep copy
    matcher = notice_matcher(notice_tools(full_hooks, src))
    for _event, group in notice_groups(out):
        group["matcher"] = matcher
    return out


def bundle_manifest(full_manifest: dict) -> dict:
    m = json.loads(json.dumps(full_manifest))
    m["name"] = BUNDLE_NAME
    m["displayName"] = "BOLTA skills"
    m["description"] = BUNDLE_DESCRIPTION
    m["keywords"] = list(full_manifest.get("keywords", [])) + ["skills-only"]
    m.pop("userConfig", None)  # the guard's setting lives with the guard, in bolta-checks
    return m


def dumps(obj: dict) -> bytes:
    return (json.dumps(obj, indent=2, ensure_ascii=False) + "\n").encode()


def generate(src: pathlib.Path = SRC) -> dict[str, tuple[bytes, bool]]:
    """The bundle as {relative path: (contents, executable)}."""
    files: dict[str, tuple[bytes, bool]] = {}
    for path in sorted(src.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(src).as_posix()
        if rel in LEFT_OUT or rel in REWRITTEN or rel.startswith(LEFT_OUT_DIRS):
            continue
        data = _read(path)
        if path.suffix == ".md":
            data = data.replace(b"/" + FULL_NAME.encode() + b":", b"/" + BUNDLE_NAME.encode() + b":")
        files[rel] = (data, bool(path.stat().st_mode & 0o111))
    full_manifest = json.loads((src / ".claude-plugin" / "plugin.json").read_text())
    files[".claude-plugin/plugin.json"] = (dumps(bundle_manifest(full_manifest)), False)
    files["README.md"] = (BUNDLE_README.replace("{version}", str(full_manifest["version"])).encode(), False)
    return files


def generate_root_skill(src: pathlib.Path = SRC) -> dict[str, tuple[bytes, bool]]:
    """skills/bolta at the repository root: the plugin's skill folder, unchanged."""
    base = src / SKILL_SRC
    return {p.relative_to(base).as_posix(): (_read(p), False)
            for p in sorted(base.rglob("*")) if p.is_file() and p.name != ".DS_Store"}


def existing(dst: pathlib.Path) -> dict[str, tuple[bytes, bool]]:
    out: dict[str, tuple[bytes, bool]] = {}
    if dst.is_dir():
        for path in sorted(dst.rglob("*")):
            if path.is_file() or path.is_symlink():
                out[path.relative_to(dst).as_posix()] = (path.read_bytes() if path.is_file() else b"", bool(path.stat().st_mode & 0o111))
    return out


def differences(expected: dict[str, tuple[bytes, bool]], actual: dict[str, tuple[bytes, bool]]) -> list[str]:
    diffs = []
    for rel in sorted(set(expected) | set(actual)):
        if rel not in actual:
            diffs.append(f"missing: {rel}")
        elif rel not in expected:
            diffs.append(f"not generated: {rel}")
        elif expected[rel][0] != actual[rel][0]:
            diffs.append(f"differs: {rel}")
        elif expected[rel][1] != actual[rel][1]:
            diffs.append(f"executable bit differs: {rel}")
    return diffs


def write(files: dict[str, tuple[bytes, bool]], dst: pathlib.Path = DST) -> None:
    for rel in sorted(existing(dst)):
        if rel not in files:
            (dst / rel).unlink()
    for rel, (data, executable) in files.items():
        path = dst / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        path.chmod(0o755 if executable else 0o644)
    for d in sorted((p for p in dst.rglob("*") if p.is_dir()), reverse=True):
        if not any(d.iterdir()):
            d.rmdir()


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="do not write; exit 1 if the bundle differs from what would be generated")
    ap.add_argument("--sync-hooks", action="store_true", help="rewrite the reconnect-notice matchers in the checks plugin's hooks.json from the skills, then stop")
    ap.add_argument("--src", type=pathlib.Path, default=SRC)
    ap.add_argument("--dst", type=pathlib.Path, default=DST)
    ap.add_argument("--root-skill", type=pathlib.Path, default=ROOT_SKILL, help="where the skill on its own is written (skills/bolta)")
    ap.add_argument("--checks", type=pathlib.Path, default=CHECKS, help="the checks plugin (hooks/hooks.json and scripts/)")
    args = ap.parse_args(argv)
    if args.sync_hooks:
        hooks_path = args.checks.resolve() / "hooks" / "hooks.json"
        current = json.loads(hooks_path.read_text())
        want = dumps(synced_hooks(current, args.src.resolve()))
        if hooks_path.read_bytes() == want:
            print(f"{hooks_path.relative_to(REPO) if hooks_path.is_relative_to(REPO) else hooks_path} is up to date")
        else:
            hooks_path.write_bytes(want)
            print(f"rewrote the reconnect-notice matchers in {hooks_path.relative_to(REPO) if hooks_path.is_relative_to(REPO) else hooks_path}; now run this script again without --sync-hooks")
        return 0
    files = generate(args.src.resolve())
    root_files = generate_root_skill(args.src.resolve())
    if args.check:
        diffs = differences(files, existing(args.dst.resolve()))
        diffs += [f"skills/bolta: {d}" for d in differences(root_files, existing(args.root_skill.resolve()))]
        for d in diffs:
            print(d)
        print("bundle and skills/bolta are up to date" if not diffs else "out of date: run python3 -I tools/build_skills_bundle.py")
        return 1 if diffs else 0
    write(files, args.dst.resolve())
    write(root_files, args.root_skill.resolve())
    print(f"wrote {len(files)} files to {args.dst.resolve().relative_to(REPO) if args.dst.resolve().is_relative_to(REPO) else args.dst}")
    print(f"wrote {len(root_files)} files to {args.root_skill.resolve().relative_to(REPO) if args.root_skill.resolve().is_relative_to(REPO) else args.root_skill}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
